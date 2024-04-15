#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ File Name      :  core.py
@ Time           :  2024/04/14 16:50:29
@ Author         :  Keyork
@ Version        :  0.1
@ Contact        :  chengky18@icloud.com
@ Description    :  None
@ History        :  0.1(2024/04/14) - None(Keyork)
"""

from ..model.state import CoreState

from .rcore import RCore
from .wcore import WCore


class Core:

    def __init__(self, core_state: CoreState) -> None:
        self.core_state = core_state
        self.read_core = RCore(core_state.get_input_path())
        self.write_core = WCore(core_state.get_output_path())

    def run(self) -> None:
        self.core_state.logger.info(
            f"{self.read_core.input_path} ---> {self.write_core.output_path}"
        )
        self.read_core.read_img_list()
        self.write_core.load_img_list(self.read_core.img_list)
        self.write_core.check_rgb()
        self.write_core.write_pdf()
