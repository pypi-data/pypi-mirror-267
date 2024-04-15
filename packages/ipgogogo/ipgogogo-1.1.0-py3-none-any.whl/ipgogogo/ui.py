#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ File Name      :  ui.py
@ Time           :  2024/04/14 18:27:01
@ Author         :  Keyork
@ Version        :  0.1
@ Contact        :  chengky18@icloud.com
@ Description    :  None
@ History        :  0.1(2024/04/14) - None(Keyork)
"""


import os
from tkinter import Button, Label, Tk, filedialog, messagebox


from .core.core import Core
from .model.state import CoreState
from .utils.checkdir import is_bottom_dir
from .utils.logger import init_logger


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


def run():
    window = Tk()
    window.title("IPGoGoGo")
    window.geometry("500x300")

    input_dir = "Input"
    output_dir = "Output"
    label_input = Label(window, text=input_dir)
    label_input.grid(row=0, column=1)
    label_output = Label(window, text=output_dir)
    label_output.grid(row=1, column=1)

    def get_input_dir():
        global input_dir
        input_dir = filedialog.askdirectory()
        label_input.config(text=input_dir)

    def get_output_dir():
        global output_dir
        output_dir = filedialog.askdirectory()
        label_output.config(text=output_dir)

    btn_input = Button(window, text="Select Input Dir", command=get_input_dir)
    btn_input.grid(row=0, column=0)
    btn_output = Button(window, text="Select Output Dir", command=get_output_dir)
    btn_output.grid(row=1, column=0)

    def run():
        global input_dir
        global output_dir
        core_state = CoreState()
        logger = init_logger("INFO")
        core_state.init_input_path(input_dir)
        core_state.init_output_path(output_dir)
        core_state.init_logger(logger)
        run_multi(core_state)
        messagebox.showinfo("Done", "Convert Finished!")

    btn_run = Button(window, text="Run", command=run)
    btn_run.grid(row=2, column=0)

    window.mainloop()
