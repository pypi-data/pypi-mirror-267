#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ File Name      :  run.py
@ Time           :  2024/04/14 15:49:19
@ Author         :  Keyork
@ Version        :  0.1
@ Contact        :  chengky18@icloud.com
@ Description    :  None
@ History        :  0.1(2024/04/14) - None(Keyork)
"""

import argparse
import os

from core.core import Core
from model.state import CoreState
from utils.checkdir import is_bottom_dir
from utils.logger import init_logger


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ipgogogo")
    parser.add_argument(
        "-i", "--input", type=str, default="./data/in/", help="input path"
    )
    parser.add_argument(
        "-o", "--output", type=str, default="./data/out/", help="output path"
    )
    parser.add_argument("-l", "--loglevel", type=str, default="INFO", help="log level")
    return parser.parse_args()


def run_single(core_state: CoreState) -> None:
    core = Core(core_state)
    core.run()


def run_multi(core_state: CoreState) -> None:
    if is_bottom_dir(core_state.get_input_path()):
        core_state.check_out_path()
        core_state.add_end_pdf()
        run_single(core_state)
        return
    else:
        for bottom in os.listdir(core_state.get_input_path()):
            core_state.add_input_path(bottom)
            core_state.add_output_path(bottom)
            run_multi(core_state)
            core_state.remove_end_input_path()
            core_state.remove_end_output_path()


if __name__ == "__main__":

    core_state = CoreState()
    args = get_args()
    logger = init_logger(args.loglevel)
    core_state.init_input_path(args.input)
    core_state.init_output_path(args.output)
    core_state.init_logger(logger)
    run_multi(core_state)
