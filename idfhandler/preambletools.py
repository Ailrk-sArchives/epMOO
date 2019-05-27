"""
This module make creating and managing multiprocessing preamble functions
easier.
"""
import os
from typing import Dict, Callable

# TODO


class Preamble:
    """
    A functor.
    Encapsulate all preamble creating methods.
    """

    def __init__(self, constants: Dict, paths: Dict, operator: Callable):
        self._pid = os.getpid()
        self._constants = constants
        self._paths = paths
        self._op = operator
        for

    def __call__(self, *args):
        pass

    def customize_operator(self):
        pass

    def log(self):
        pass
