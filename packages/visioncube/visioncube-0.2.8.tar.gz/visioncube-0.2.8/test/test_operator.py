#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
author：yannan1
since：2024-03-22
"""
import cv2
import numpy as np
from visioncube.measure import ColorMeasurement

from visioncube import TransformPipeline
from visioncube.recognition import CnOCR

img_path = 'data/test-150.jpg'
img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

"""算子如何用"""
# ocr
# 方式1
output = CnOCR(use_gpu=False)({"image": img})['ocr']

# 方式2
# 和图像处理的调用方式一致
# pipeline = TransformPipeline('test/config.yml', training=True, device='cpu')  # 这里的device只写成cpu
# # pipeline = TransformPipeline([
# #     {'name': 'CnOCR', 'tag': 'None', 'kwargs': {'use_gpu': True}}
# # ], training=True, device='cpu')
# output = pipeline({"image": img})['ocr']

# color measure
output = ColorMeasurement()({"image": img})['color_measure']
print(output)

"""获得算子和算子参数"""
from visioncube import format_operator_param
from visioncube import measure, recognition

results = []
results.extend(format_operator_param(measure))  # 得到测量的算子和参数
results.extend(format_operator_param(recognition))  # 得到识别的算子和参数
