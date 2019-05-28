"""
This module make creating and managing multiprocessing preamble functions
easier.
"""
import os
import time
from typing import Dict, Callable, List


class Preamble:
    """
    A functor.
    Encapsulate all preamble creating methods.
    """

    def __init__(self, constants: Dict, paths: Dict):
        self._constants = constants
        self._paths = paths
        self._args: List = []

        for k, v in self._paths.items():
            self._paths[k] = os.path.abspath(v)

    def __call__(self, *args):
        # override by subclass
        self._pid = str(os.getpid())
        self._args = args
        self._start_log()

    def _operator(self, lines: List[str], idx: int):
        # override by subclass
        pass

    def _start_log(self):
        print("===============start in pid {} at {}===============>".format( self._pid, time.ctime()))



