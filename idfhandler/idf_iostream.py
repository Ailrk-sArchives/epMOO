from idfhandler.ep_input_model import IdfModel, JdfModel
from typing import Union

Model = Union[IdfModel, JdfModel, None]


class IdfIOStream:
    """
    A RAII manager for idf file.
    """
    def __init__(self, path: str, mode: str = 'idf'):
        self.path = path
        self.model: Model = None
        self.mode = mode

    def __enter__(self):
        if self.mode == 'idf':
            self.model = IdfModel(self.path)

        elif self.mode == 'jdf':
            self.model = JdfModel(self.path)

        return self.model

    def __exit__(self, *args):
        self.model.close()
