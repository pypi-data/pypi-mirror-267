import os

from .core.core import Core
from .model.state import CoreState
from .utils.checkdir import is_bottom_dir
from .utils.logger import init_logger
from .ui import run


class IPGoGoGo:

    def __init__(self, input_path: str, output_path: str, loglevel: str = "INFO"):
        self.input_path = input_path
        self.output_path = output_path
        self.loglevel = loglevel
        self.core_state = CoreState()
        self.logger = None

    def run_single(self) -> None:
        core = Core(self.core_state)
        core.run()

    def run_multi(self) -> None:
        if is_bottom_dir(self.core_state.get_input_path()):
            self.core_state.check_out_path()
            self.core_state.add_end_pdf()
            self.run_single()
            return
        else:
            for bottom in os.listdir(self.core_state.get_input_path()):
                self.core_state.add_input_path(bottom)
                self.core_state.add_output_path(bottom)
                self.run_multi()
                self.core_state.remove_end_input_path()
                self.core_state.remove_end_output_path()

    def run(self):
        self.core_state.init_input_path(self.input_path)
        self.core_state.init_output_path(self.output_path)
        self.logger = init_logger(self.loglevel)
        self.core_state.init_logger(self.logger)
        self.run_multi()


def run_ui():
    run()
