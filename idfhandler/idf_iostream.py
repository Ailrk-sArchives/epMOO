from idfhandler.ep_input_model import IdfModel, JdfModel
from typing import Union

Model = Union[IdfModel, JdfModel, None]


class IdfIOStream:
    """
    A RAII manager for idf file.
    """
    def __init__(self, input_path: str, output_path: str, mode: str = 'idf'):
        self._input_path = input_path
        self._output_path = output_path
        self.model: Model = None
        self.mode = mode

    def __enter__(self):
        if self.mode == 'idf':
            self.model = IdfModel(self._input_path, self._output_path)

        elif self.mode == 'jdf':
            self.model = JdfModel(self._input_path, self._output_path)

        return self.model

    def __exit__(self, *args):
        self.model.close()
