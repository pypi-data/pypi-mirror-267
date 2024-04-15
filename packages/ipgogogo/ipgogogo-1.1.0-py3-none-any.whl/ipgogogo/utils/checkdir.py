#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ File Name      :  checkdir.py
@ Time           :  2024/04/14 16:10:43
@ Author         :  Keyork
@ Version        :  0.1
@ Contact        :  chengky18@icloud.com
@ Description    :  判断是否为底层文件夹
@ History        :  0.1(2024/04/14) - None(Keyork)
"""

import os
from typing import List


def is_bottom_dir(path: str) -> bool:
    """判断是否为底层文件夹

    Args:
        path (str): 文件夹路径

    Returns:
        bool: True or False
    """
    data_list: List = os.listdir(path)
    for data in data_list:
        if os.path.isdir(os.path.join(path, data)):
            return False
    return True
