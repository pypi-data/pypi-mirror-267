#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ File Name      :  rcore.py
@ Time           :  2024/04/14 15:53:18
@ Author         :  Keyork
@ Version        :  0.1
@ Contact        :  chengky18@icloud.com
@ Description    :  None
@ History        :  0.1(2024/04/14) - None(Keyork)
"""
import os
from typing import List

from PIL import Image


class RCore:
    """read img path file
    input_path: str, input file path, dir
    """

    def __init__(self, input_path: str) -> None:
        self.input_path: str = input_path
        self.img_list: List = []
        self.img_num = 0

    def read_img_list(self) -> None:
        """read img list from input_path"""
        path_list = os.listdir(self.input_path)
        path_list.sort()
        for img in path_list:
            self.img_list.append(
                self.read_single_img(os.path.join(self.input_path, img))
            )
            self.img_num += 1

    def read_single_img(self, img_path: str) -> Image:
        """read single img"""
        return Image.open(img_path)
