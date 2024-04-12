#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/21
# @Author  : yanxiaodong
# @File    : eval_metric.py
"""
import math
import os
from typing import List, Dict
import copy
import numpy as np
from collections import defaultdict
import logging
import cv2

from gaea_operator.utils import write_file
from gaea_operator.metric.operator import MeanAveragePrecision, \
    BboxConfusionMatrix, \
    Accuracy, \
    PrecisionRecallF1score, \
    ConfusionMatrix, \
    MeanIoU
from gaea_operator.metric.types.metric import BOUNDING_BOX_MEAN_AVERAGE_RECALL_METRIC_NAME, \
    CONFUSION_MATRIX_METRIC_NAME, \
    BOUNDING_BOX_LABEL_AVERAGE_PRECISION_METRIC_NAME, \
    BOUNDING_BOX_MEAN_AVERAGE_PRECISION_METRIC_NAME, \
    BOUNDING_BOX_LABEL_METRIC_NAME, \
    ConfusionMatrixMetric, \
    ConfusionMatrixMetricResult, \
    ConfusionMatrixAnnotationSpec, \
    ConfusionMatrixRow, \
    CLASSIFICATION_LABEL_PRECISION_METRIC_NAME, \
    CLASSIFICATION_ACCURACY_METRIC_NAME, \
    SEMANTIC_SEGMENTATION_MIOU_METRIC_NAME, \
    SEMANTIC_SEGMENTATION_LABEL_IOU_METRIC_NAME
from gaea_operator.metric.types.object_detection_metric import ObjectDetectionMetric, \
    BoundingBoxMeanAveragePrecision, \
    BoundingBoxMeanAverageRecall, \
    BoundingBoxLabelAveragePrecision, \
    BoundingBoxLabelAveragePrecisionResult, \
    BoundingBoxLabelMetric, \
    BoundingBoxLabelMetricResult, \
    BoundingBoxLabelConfidenceMetric
from gaea_operator.metric.types.image_classification_metric import ImageClassificationMetric, \
    LabelPrecisionMetric, \
    LabelPrecisionMetricResult, \
    AccuracyMetric
from gaea_operator.metric.types.semantic_segmentation_metric import SemanticSegmentationMetric, \
    LabelIntersectionOverUnionMetric, \
    LabelIntersectionOverUnionMetricResult, \
    MeanIntersectionOverUnionMetric


class EvalMetricAnalysis(object):
    """
    Evaluation metric analysis.
    """

    def __init__(self,
                 category: str,
                 labels: List = None,
                 images: List[Dict] = None,
                 conf_threshold: float = 0,
                 iou_threshold: float = 0.5):
        self.labels = labels
        self.images = images
        self.category = category
        self.data_format_valid = True
        self.conf_threshold = float(conf_threshold)
        self.iou_threshold = float(iou_threshold)

        self.image_dict = {}
        self.img_id_str2int = {}
        self.labels = []
        self.label_id2index = {}
        self.label_index2id = {}
        self.label_id2name = {}
        self.label_index2name = {}
        self.metric = []
        self.format_input = None
        self.format_result = None

        self.set_images(images)
        self.set_labels(labels)

    def reset(self):
        """
        Reset metric.
        """
        for metric in self.metric:
            metric.reset()
        self.data_format_valid = True

    def set_images(self, images: List[Dict]):
        """
        Set images.
        """
        if images is None:
            return
        self.image_dict = {item["image_id"]: item for item in images}
        self.img_id_str2int = {key: idx + 1 for idx, key in enumerate(self.image_dict)}

    def set_labels(self, labels: List):
        """
        Set labels.
        """
        if labels is None:
            return
        self.labels = [{"id": int(label["id"]), "name": label["name"]} for label in labels]
        self.label_id2index = {label["id"]: idx for idx, label in enumerate(self.labels)}
        self.label_index2id = {idx: label["id"] for idx, label in enumerate(self.labels)}
        self.label_id2name = {label["id"]: label["name"] for label in self.labels}
        self.label_index2name = {idx: label["name"] for idx, label in enumerate(self.labels)}
        self.set_metric()

    def set_metric(self):
        """
        Set metric.
        """
        if self.category == "Image/ObjectDetection":
            self.metric = [MeanAveragePrecision(labels=self.labels,
                                                num_classes=len(self.labels),
                                                classwise=True),
                           BboxConfusionMatrix(labels=self.labels,
                                               conf_threshold=self.conf_threshold,
                                               iou_threshold=self.iou_threshold,
                                               num_classes=len(self.labels))]
            self.format_input = self._format_to_object_detection
            self.format_result = self._format_object_detection_result
        elif self.category == "Image/ImageClassification/MultiClass":
            self.metric = [Accuracy(num_classes=len(self.labels)),
                           PrecisionRecallF1score(num_classes=len(self.labels), average="none"),
                           ConfusionMatrix(num_classes=len(self.labels))]
            self.format_input = self._format_to_classification
            self.format_result = self._format_classification_result
        elif self.category == "Image/SemanticSegmentation":
            self.metric = [MeanIoU(num_classes=len(self.labels))]
            self.format_input = self._format_to_semantic_segmentation
            self.format_result = self._format_semantic_segmentation_result
        else:
            raise ValueError(f"Unknown category: {self.category}")

    def update(self, predictions: List[Dict], references: List[Dict], **kwargs):
        """
        Update metric.
        """
        if predictions is None or references is None:
            logging.warning(f"Predictions {type(predictions)} or references {type(references)} is None.")
            self.data_format_valid = False
            return

        predictions, references = self.format_input(predictions, references)

        for metric in self.metric:
            metric.update(predictions=predictions, references=references)

    def _format_to_object_detection(self, predictions: List[Dict], references: List[Dict]):
        """
        Format to object detection metric.
        """
        ann_id = 1
        references_dict = defaultdict(list)
        for item in references:
            im_id = item["image_id"]
            img = self.image_dict[im_id]
            im_id_int = self.img_id_str2int[im_id]
            if item.get("annotations") is None:
                anno = {"id": ann_id, "image_id": im_id_int, "width": img["width"], "height": img["height"]}
                references_dict[im_id_int].append(anno)
                continue
            for anno in item["annotations"]:
                anno["id"] = ann_id
                anno["image_id"] = im_id_int
                anno["width"] = img["width"]
                anno["height"] = img["height"]
                anno['ignore'] = anno['ignore'] if 'ignore' in anno else 0
                anno['iscrowd'] = "iscrowd" in anno and anno["iscrowd"]
                for idx in range(len(anno["labels"])):
                    anno_copy = copy.deepcopy(anno)
                    if isinstance(anno_copy["labels"][idx]["id"], str):
                        anno_copy["labels"][idx]["id"] = int(anno_copy["labels"][idx]["id"])
                    if math.isnan(anno_copy["labels"][idx]["id"]):
                        continue
                    # 如果标注标签id不在label,则跳过（修改了标签但是标注没有同步修改）
                    if anno_copy["labels"][idx]["id"] not in self.label_id2index:
                        continue
                    anno_copy['category_id'] = anno_copy["labels"][idx]["id"]
                    references_dict[im_id_int].append(anno_copy)
                ann_id += 1

        predictions_list = []
        ann_id = 1
        for item in predictions:
            im_id = item["image_id"]
            im_id_int = self.img_id_str2int[im_id]
            # 如果预测结果不在 gt里面，是一张未标注的图片，不参与指标计算
            if item["annotations"] is None or im_id_int not in references_dict:
                continue
            for anno in item["annotations"]:
                anno["image_id"] = im_id_int
                for idx in range(len(anno["labels"])):
                    anno_copy = copy.deepcopy(anno)
                    anno_copy["id"] = ann_id
                    if isinstance(anno_copy["labels"][idx]["id"], str):
                        anno_copy["labels"][idx]["id"] = int(anno_copy["labels"][idx]["id"])
                    if math.isnan(anno_copy["labels"][idx]["id"]):
                        continue
                    # 如果预测结果标签id不在label,则跳过（修改了标签但是预测结果没有同步修改）
                    if anno_copy["labels"][idx]["id"] not in self.label_id2index:
                        continue
                    anno_copy['category_id'] = anno["labels"][idx]["id"]
                    anno_copy['score'] = anno["labels"][idx]["confidence"]
                    predictions_list.append(anno_copy)
                    ann_id += 1

        references_list = []
        for _, anno in references_dict.items():
            references_list.extend(anno)

        return {"bbox": predictions_list}, {"bbox": references_list}

    def _format_object_detection_result(self, metric_result: Dict):
        metric = ObjectDetectionMetric(labels=self.labels, metrics=[])
        bbox_metric_result = metric_result[MeanAveragePrecision.global_name()]
        bounding_box_mean_average_precision = BoundingBoxMeanAveragePrecision(
            name=BOUNDING_BOX_MEAN_AVERAGE_PRECISION_METRIC_NAME,
            displayName="AP50指标",
            result=bbox_metric_result["bbox"][1])
        bounding_box_mean_average_recall = BoundingBoxMeanAverageRecall(
            name=BOUNDING_BOX_MEAN_AVERAGE_RECALL_METRIC_NAME,
            displayName="AR50指标",
            result=bbox_metric_result["bbox"][8])
        bounding_box_label_average_precision = BoundingBoxLabelAveragePrecision(
            name=BOUNDING_BOX_LABEL_AVERAGE_PRECISION_METRIC_NAME,
            displayName="类别AP结果",
            result=[])
        confusion_matrix = ConfusionMatrixMetric(
            name=CONFUSION_MATRIX_METRIC_NAME,
            displayName="混淆矩阵",
            result=ConfusionMatrixMetricResult(annotationSpecs=[], rows=[]))
        bounding_box_label_metric = BoundingBoxLabelMetric(name=BOUNDING_BOX_LABEL_METRIC_NAME,
                                                           displayName="PR曲线",
                                                           result=[])
        for item in bbox_metric_result["bbox_results_per_label"]:
            bounding_box_label_average_precision.result.append(
                BoundingBoxLabelAveragePrecisionResult(labelName=item["labelName"],
                                                       averagePrecision=item["averagePrecision"]))
        for item in bbox_metric_result["pr_curve"]:
            bounding_box_label_metric_result = BoundingBoxLabelMetricResult(labelName=item[0],
                                                                            iouThreshold=0.5,
                                                                            averagePrecision=item[1],
                                                                            confidenceMetrics=[])
            for idx, p in enumerate(item[2]):
                bounding_box_label_metric_result.confidenceMetrics.append(
                    BoundingBoxLabelConfidenceMetric(
                        precision=p,
                        recall=item[3][idx]))
            bounding_box_label_metric.result.append(bounding_box_label_metric_result)
        lower_bound, upper_bound = 0, 0
        for idx, item in enumerate(metric_result[BboxConfusionMatrix.global_name()]):
            lower_bound = min(lower_bound, min(item))
            upper_bound = max(upper_bound, max(item))
            if idx not in self.label_index2id:
                label_id = max(self.label_index2id.values()) + 1
                label_name = "背景图"
            else:
                label_id = self.label_index2id[idx]
                label_name = self.label_index2name[idx]
            annotation_spec = ConfusionMatrixAnnotationSpec(id=label_id, labelName=label_name)
            row = ConfusionMatrixRow(row=item)
            confusion_matrix.result.annotationSpecs.append(annotation_spec)
            confusion_matrix.result.rows.append(row)
            confusion_matrix.result.lowerBound = lower_bound
            confusion_matrix.result.upperBound = upper_bound

        metric.metrics.extend([bounding_box_mean_average_precision,
                               bounding_box_mean_average_recall,
                               bounding_box_label_average_precision,
                               bounding_box_label_metric,
                               confusion_matrix])
        return metric.dict()

    def _format_to_classification(self, predictions: List[Dict], references: List[Dict]):
        """
        Format to classification metric.
        """
        predictions_list = []
        for item in predictions:
            if item.get("annotations") is None:
                continue
            anno = item["annotations"][0]
            if isinstance(anno["labels"][0]["id"], str):
                anno["labels"][0]["id"] = int(anno["labels"][0]["id"])
            if math.isnan(anno["labels"][0]["id"]):
                continue
            # 如果标注标签id不在label,则跳过（修改了标签但是标注没有同步修改）
            if anno["labels"][0]["id"] not in self.label_id2index:
                continue
            index = self.label_id2index[anno["labels"][0]["id"]]
            predictions_list.append(index)

        references_list = []
        for item in references:
            if item.get("annotations") is None:
                continue
            anno = item["annotations"][0]
            if isinstance(anno["labels"][0]["id"], str):
                anno["labels"][0]["id"] = int(anno["labels"][0]["id"])
            if math.isnan(anno["labels"][0]["id"]):
                continue
            # 如果预测结果标签id不在label,则跳过（修改了标签但是预测结果没有同步修改）
            if anno["labels"][0]["id"] not in self.label_id2index:
                continue
            index = self.label_id2index[anno["labels"][0]["id"]]
            references_list.append(index)

        return predictions_list, references_list

    def _format_classification_result(self, metric_result: Dict):
        metric = ImageClassificationMetric(labels=self.labels, metrics=[])
        accuracy_metric = AccuracyMetric(name=CLASSIFICATION_ACCURACY_METRIC_NAME,
                                         displayName="准确率",
                                         result=metric_result[Accuracy.global_name()])
        label_precision_metric = LabelPrecisionMetric(name=CLASSIFICATION_LABEL_PRECISION_METRIC_NAME,
                                                      displayName="类别AP结果",
                                                      result=[])
        confusion_matrix = ConfusionMatrixMetric(name=CONFUSION_MATRIX_METRIC_NAME,
                                                 displayName="混淆矩阵",
                                                 result=ConfusionMatrixMetricResult(annotationSpecs=[], rows=[]))
        precisions = metric_result[PrecisionRecallF1score.global_name()][0]
        recalls = metric_result[PrecisionRecallF1score.global_name()][1]
        for idx, precision in enumerate(precisions):
            label_precision_metric.result.append(LabelPrecisionMetricResult(labelName=self.label_index2name[idx],
                                                                            precision=precision,
                                                                            recall=recalls[idx]))

        for idx, item in enumerate(metric_result[ConfusionMatrix.global_name()]):
            annotation_spec = ConfusionMatrixAnnotationSpec(id=self.label_index2id[idx],
                                                            labelName=self.label_index2name[idx])
            row = ConfusionMatrixRow(row=item)
            confusion_matrix.result.annotationSpecs.append(annotation_spec)
            confusion_matrix.result.rows.append(row)

        metric.metrics.extend([accuracy_metric, label_precision_metric, confusion_matrix])

        return metric.dict()

    def _format_to_semantic_segmentation(self, predictions: List[Dict], references: List[Dict]):
        references_dict = {}
        for item in references:
            im_id = item["image_id"]
            img = self.image_dict[im_id]
            im_id_int = self.img_id_str2int[im_id]
            if "width" not in img:
                width = item["width"]
                img["width"] = width
            else:
                width = img["width"]
            if "height" not in img:
                height = item["height"]
                img["height"] = height
            else:
                height = img["height"]

            label_raw = np.zeros((height, width), dtype=np.uint8)
            if item.get("annotations") is None:
                references_dict[im_id_int] = label_raw
                continue
            for anno in item["annotations"]:
                rle = anno["rle"]
                rle_count = rle['counts']
                if isinstance(anno["labels"][0]["id"], str):
                    anno["labels"][0]["id"] = int(anno["labels"][0]["id"])
                if math.isnan(anno["labels"][0]["id"]):
                    continue
                # 如果标注标签id不在label,则跳过（修改了标签但是标注没有同步修改）
                if anno["labels"][0]["id"] not in self.label_id2index:
                    continue

                start = 0
                pixel = 0
                mask = np.zeros(height * width, dtype=np.uint8)
                for num in rle_count:
                    stop = start + num
                    mask[start:stop] = pixel
                    pixel = self.label_id2index[anno["labels"][0]["id"]] - pixel
                    start = stop
                mask = mask.reshape((height, width))
                index = mask == self.label_id2index[anno["labels"][0]["id"]]
                label_raw[index] = mask[index]

            references_dict[im_id_int] = {"mask": label_raw, "width": width, "height": height}

        predictions_dict = {}
        for item in predictions:
            im_id = item["image_id"]
            im_id_int = self.img_id_str2int[im_id]
            # 如果预测结果不在 gt里面，是一张未标注的图片，不参与指标计算
            if item.get("annotations") is None or im_id_int not in references_dict:
                continue
            img = self.image_dict[im_id]
            width = img["width"]
            height = img["height"]
            label_raw = np.zeros((height, width), dtype=np.uint8)
            for anno in item["annotations"]:
                polygon = np.array(anno["segmentation"])
                size = polygon.size
                assert size % 2 == 0, "polygon size error: {}".format(size)
                if isinstance(anno["labels"][0]["id"], str):
                    anno["labels"][0]["id"] = int(anno["labels"][0]["id"])
                if math.isnan(anno["labels"][0]["id"]):
                    continue
                # 如果预测结果标签id不在label,则跳过（修改了标签但是预测结果没有同步修改）
                if anno["labels"][0]["id"] not in self.label_id2index:
                    continue
                polygon = np.array([[polygon[i], polygon[i + 1]] for i in range(size) if i % 2 == 0], dtype=np.int32)
                cv2.fillPoly(label_raw, [polygon], self.label_id2index[anno["labels"][0]["id"]])
            predictions_dict[im_id_int] = label_raw

        references_list = []
        predictions_list = []
        for img_id, raw in references_dict.items():
            references_list.append(raw["mask"])
            width = raw["width"]
            height = raw["height"]
            # 如果没有预测结果，则用0填充
            predictions_list.append(predictions_dict[img_id] if img_id in predictions_dict else
                                    np.zeros((height, width), dtype=np.uint8))

        return predictions_list, references_list

    def _format_semantic_segmentation_result(self, metric_result: Dict):
        metric = SemanticSegmentationMetric(labels=self.labels, metrics=[])
        iou_result = metric_result[MeanIoU.global_name()]
        mean_iou = MeanIntersectionOverUnionMetric(
            name=SEMANTIC_SEGMENTATION_MIOU_METRIC_NAME,
            displayName="均交并比",
            result=iou_result[0])
        label_iou = LabelIntersectionOverUnionMetric(
            name=SEMANTIC_SEGMENTATION_LABEL_IOU_METRIC_NAME,
            displayName="标签交并比",
            result=[])
        for idx, iou in enumerate(iou_result[1]):
            label_iou.result.append(LabelIntersectionOverUnionMetricResult(labelName=self.label_index2name[idx],
                                                                           iou=iou))

        metric.metrics.extend([mean_iou, label_iou])

        return metric.dict()

    def compute(self):
        """
        Compute metric.
        """
        results = {}

        if not self.data_format_valid:
            return results

        for metric in self.metric:
            results[metric.name] = metric.compute()

        metric_result = self.format_result(metric_result=results)

        return metric_result

    def save(self, metric_result: Dict, output_uri: str):
        """
        Save metric.
        """
        if os.path.splitext(output_uri)[1] == "":
            output_dir = output_uri
            file_name = "metric.json"
        else:
            output_dir = os.path.dirname(output_uri)
            file_name = os.path.basename(output_uri)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        write_file(obj=metric_result, output_dir=output_dir, file_name=file_name)

    def __call__(self, predictions: List[Dict], references: List[Dict], output_uri: str):
        self.update(predictions=predictions, references=references)
        metric_result = self.compute()

        self.save(metric_result=metric_result, output_uri=output_uri)
