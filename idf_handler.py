"""
An idf file handler. 2019-05-18
Ep take two type of input files: .idf and .epJson.

Input Object Groups for Energy Plus:
    Simulation Parameters,
    Location and Climate,
    Schedule,
    Surface Construction Element,
    ThermalZones and Surface,
    Shading Related,
    Input Object Varanation,
    Internal Gains,
    DayLighting,
    Exterior Equipment
    Zone AirFlow

HVAC template (is expanded by preprocessor called ExpandObject):
Note if HVAC template is used, no regular idf file should be used.

"""
from typing import TextIO, IO
from typing import Optional, Dict, Any, Union, List, Tuple, Callable
import os.path
import csv
import json
import re

# two types of models for idf and jdf respectively.
Pattern = str
JsonDict = Dict[str, Any]
IdfRecords = List[int]
Operator = Callable[..., Optional[List]]
ApplyList = List[Tuple[str, Pattern, Pattern, Optional[Operator]]]


class EPOutputReader:
    def __init__(self, path: str):
        self.path = path
        self.file: IO = open(path, 'r')

    def read_column(self, column_name) -> List[str]:
        reader = csv.DictReader(self.file)
        column: List[str] = []
        for row in reader:
            column.append(row[column_name])

        return column

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.file.close()


class EPInputModel:
    """Base class for both idf and jdf input format"""
    def __init__(self, path: str):
        self.path = os.path.abspath(path)
        self.updated = False  # indicate if the model is modified.
        self.file: Optional[TextIO] = None

    def close(self) -> None:
        if self.file is not None and not self.file.closed:
            self.file.close()


class IdfModel(EPInputModel):
    """
    idf file object
    A simple class for text file search and replacement
    """

    def __init__(self, path: str):
        super().__init__(path=os.path.abspath(path))
        self.temp_path = os.path.abspath("./temp.idf")

        self.rlines: List[str] = []
        with open(path, "r") as f:
            self.rlines = f.readlines()

    def apply(self, op: Callable):
        # def op(list, i): apply(...), sub(...), search(...)
        # op is the collection of all operations.

        for idx, _ in enumerate(self.rlines):
            op(self.rlines, idx)

    def append(self, data: List[str]):
        self.rlines.extend(data)

    def search(self, capture_list: List, patterns: List[Pattern], rlines: List,
               idx=0, depth=20, matched=False):
        # recursively search, put result into capture_list.
        if depth == 0:
            return

        line = rlines[idx]
        p = patterns.pop(0)
        match = re.match(p, line)

        if match:
            matched = True

            if len(patterns) == 0:    # hit target.
                if len(match.groups()) == 1:
                    capture_list.append(match.group(1))
                else:
                    capture_list.append(match.groups())
                return

            else:                     # in process.
                self.search(capture_list, patterns, rlines, idx + 1, depth - 1, matched)
            return

        elif matched:                 # hit anchor already.
            patterns.append(p)
            self.search(capture_list, patterns, rlines, idx + 1, depth - 1, matched)

        return

    def grap(self, capture_list, patterns: List[Pattern], rlines: List,
             idx=0, depth=20, matched=False):
        # grap all anchors after found a

        line = rlines[idx]
        p = patterns[0]
        sub_patterns = [patterns[:i+1] for i in range(len(patterns))]

        if self.__search_one(p, line):
            sub_capture_list: List = []

            for i, sub_pattern in enumerate(sub_patterns):  # grouping.
                self.search(sub_capture_list, sub_pattern, rlines, idx)
            capture_list.append(sub_capture_list)

    def sub(self, patterns: List[Pattern], replacement: Pattern, rlines, idx, depth=20, matched=False):
        # recursively search till find the target, then do text substitution.
        if depth == 0:
            return

        p = patterns.pop(0)
        line = rlines[idx]
        hit_anchor = self.__search_one(p, line)

        if len(patterns) == 0:      # Case: either hit target or in between.
            if hit_anchor:
                rlines[idx] = re.sub(p, replacement, line)  # bingo case
                return
            elif matched:
                patterns.append(p)
                self.sub(patterns, replacement, rlines, idx + 1, depth - 1, matched)
            return

        if hit_anchor:              # still has patterns remains.
            matched = True
            self.sub(patterns, replacement, rlines, idx + 1, depth - 1, matched)
            return

        elif matched:
            patterns.append(p)
            self.sub(patterns, replacement, rlines, idx + 1, depth - 1, matched)

        return

    def __write_back(self):
        # the last step after all operations.
        data = ""

        for line in self.rlines:
            data += line
        with open(self.temp_path, "w") as f:
            f.write(data)

    def __search_one(self, pattern: Pattern, line: str) -> bool:
        match = re.match(pattern, line)
        if match:
            return True
        else:
            return False

    def close(self):
        # currently it will create the new idf file in temp.idf.
        # changing the file name is not the duty of this library.
        self.__write_back()


class JdfModel(EPInputModel):
    """
    epJson file object
    The class support handling epJson format input file.
    """
    def __init__(self, path: str):
        super().__init__(path=path)
        self.ep_model: Optional[JsonDict] = None

        # create the json model, then open the file to write.
        try:
            with open(path, 'r') as f:
                self.ep_model = json.loads(f.read())
        except IOError:
            print(f"Failed to read jdf file {path}")

    def update(self, struct: JsonDict) -> None:
        # update struct into epJson model
        if self.ep_model is not None:
            self.ep_model.update(struct)
            self.updated = True

        else:
            raise RuntimeError("ep model doesn't exist")

    def write_back(self) -> None:
        # Write the ep_model back to file.
        # Invoke it after everything updated to improve performance.
        if self.file is None:
            if self.updated:
                try:
                    with open(self.path, "w") as f:
                        json_ep_model = json.dumps(self.ep_model, indent=4)
                        f.write(json_ep_model)
                except IOError:
                    print("Failed to open file {}".format(self.path))

        else:
            RuntimeError("File {} already openned".format(self.path))

    def get(self, key_lists: List[str]) -> Any:
        # TODO wrong! 2019-05-20
        if self.ep_model is not None:
            return None

        else:
            return None


# TODO Split into another file from here.
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
