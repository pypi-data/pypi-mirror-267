#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ File Name      :  logger.py
@ Time           :  2024/04/14 17:09:01
@ Author         :  Keyork
@ Version        :  0.1
@ Contact        :  chengky18@icloud.com
@ Description    :  None
@ History        :  0.1(2024/04/14) - None(Keyork)
"""
import sys
from loguru import logger


def init_logger(level: str):
    logger.remove()
    logger.add(
        sys.stdout,
        level=level,
        format="{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}",
    )
    return logger
