#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ File Name      :  wcore.py
@ Time           :  2024/04/14 15:53:24
@ Author         :  Keyork
@ Version        :  0.1
@ Contact        :  chengky18@icloud.com
@ Description    :  None
@ History        :  0.1(2024/04/14) - None(Keyork)
"""

from typing import List


class WCore:

    def __init__(self, output_path: str) -> None:
        self.output_path: str = output_path
        self.img_list: List = []

    def load_img_list(self, img_list: List) -> None:
        self.img_list = img_list

    def check_rgb(self) -> None:
        for idx, img in enumerate(self.img_list):
            if img.mode != "RGB":
                self.img_list[idx] = img.convert("RGB")

    def write_pdf(self) -> None:
        self.img_list[0].save(
            self.output_path,
            save_all=True,
            append_images=self.img_list[1:],
        )
