#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ File Name      :  state.py
@ Time           :  2024/04/14 16:36:50
@ Author         :  Keyork
@ Version        :  0.1
@ Contact        :  chengky18@icloud.com
@ Description    :  None
@ History        :  0.1(2024/04/14) - None(Keyork)
"""
import os


class CoreState:

    def __init__(self) -> None:
        self.input_path: str = None
        self.output_path: str = None
        self.logger = None

    def init_input_path(self, input_path: str) -> None:
        self.input_path = input_path

    def init_output_path(self, output_path: str) -> None:
        self.output_path = output_path

    def init_logger(self, logger) -> None:
        self.logger = logger

    def get_input_path(self) -> str:
        return self.input_path

    def get_output_path(self) -> str:
        return self.output_path

    def add_input_path(self, bottom: str) -> None:
        self.input_path = os.path.join(self.input_path, bottom)

    def add_output_path(self, bottom: str) -> None:
        self.output_path = os.path.join(self.output_path, bottom)

    def remove_end_input_path(self) -> None:
        self.input_path = os.path.dirname(self.input_path)

    def remove_end_output_path(self) -> None:
        self.output_path = os.path.dirname(self.output_path)

    def add_end_pdf(self) -> None:
        self.output_path = self.output_path + ".pdf"

    def check_out_path(self) -> None:
        if not os.path.exists(os.path.dirname(self.output_path)):
            os.makedirs(os.path.dirname(self.output_path))
