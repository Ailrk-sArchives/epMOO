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
from typing import Optional, Dict, Any, List, Callable
import os
import json
import re

# two types of models for idf and jdf respectively.
Pattern = str
JsonDict = Dict[str, Any]
IdfRecords = List[int]
Operator = Callable[..., Optional[List]]


class EPInputModel:
    """
    Base class for both idf and jdf input format
    _input_path: path for base idf file.
    _output_path: path for generated idf file.
    """
    def __init__(self, input_path: str, output_path):
        self._input_path = os.path.abspath(input_path)
        self._output_path = os.path.abspath(output_path)
        self.updated = False  # indicate if the model is modified.

    def close(self) -> None:
        # override by subclass.
        pass


class IdfModel(EPInputModel):
    """
    idf file object
    A simple class for text file search and replacement
    """

    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path=input_path, output_path=output_path)

        self.idf_lines: List[str] = []
        with open(self._input_path, "r") as f:
            self.idf_lines = f.readlines()

    def apply(self, op: Callable):
        # def op(list, i): apply(...), sub(...), search(...)
        # op is the collection of all operations.

        for idx, _ in enumerate(self.idf_lines):
            op(self, self.idf_lines, idx)

    def append(self, data: List[str]):
        self.idf_lines.extend(data)

    def search(self, capture_list: List, patterns: List[Pattern], idf_lines: List,
               idx=0, depth=30, matched=False):
        # recursively search, put result into capture_list.
        if depth == 0:
            print("search out put depth")
            return

        line = idf_lines[idx]
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
                self.search(capture_list, patterns, idf_lines, idx + 1, depth - 1, matched)
            return

        elif matched:                 # hit anchor already.
            patterns.append(p)
            self.search(capture_list, patterns, idf_lines, idx + 1, depth - 1, matched)
        return

    def grap(self, capture_list, patterns: List[Pattern], idf_lines: List,
             idx=0, depth=30, matched=False, grouping=(1,)):
        # grap all anchors
        p = patterns[0]
        line = idf_lines[idx]
        sub_patterns = [patterns[:i + 1] for i in range(len(patterns))]

        if self.__search_one(p, line):  # matched.
            sub_capture_list: List = []

            for i, sub_pattern in enumerate(sub_patterns):
                self.search(sub_capture_list, sub_pattern, idf_lines, idx)

            assert len(grouping) <= len(sub_capture_list), "GRAB ERROR, group missmatch"
            capture_list.append(self.__grouping(sub_capture_list, grouping))

    def __grouping(self, capture_list, grouping=(1,)) -> List:
        # group is used to control the shape of the capture list.
        #
        # 1. (1,) is the base case, means capturing one by one.
        # 2. (1, 3, 3, 3, 3) means capture one elements, then
        #   groups 3 in a row for 4 times.

        if grouping == (1,):
            return capture_list

        else:
            temp_list: List = []
            for n in grouping:
                g: List = []
                if n == 1:
                    temp_list.append(capture_list.pop(0))
                else:
                    for i in range(n):
                        g.append(capture_list.pop(0))
                    temp_list.append(g)
        return temp_list

    def sub(self, patterns: List[Pattern], replacement: Pattern, idf_lines, idx, depth=30, matched=False):
        # recursively search till find the target, then do text substitution.
        if depth == 0:
            return

        p = patterns.pop(0)
        line = idf_lines[idx]
        hit_anchor = self.__search_one(p, line)

        if len(patterns) == 0:      # Case: either hit target or in between.
            if hit_anchor:
                idf_lines[idx] = re.sub(p, replacement, line)  # bingo case
                return
            elif matched:
                patterns.append(p)
                self.sub(patterns, replacement, idf_lines, idx + 1, depth - 1, matched)
            return

        if hit_anchor:              # still has patterns remains.
            matched = True
            self.sub(patterns, replacement, idf_lines, idx + 1, depth - 1, matched)
            return

        elif matched:
            patterns.append(p)
            self.sub(patterns, replacement, idf_lines, idx + 1, depth - 1, matched)

        return

    def __write_back(self):
        # the last step after all operations.
        data = ""

        for line in self.idf_lines:
            data += line
        with open(self._output_path, "w") as f:
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


class JdfModel(EPInputModel):  # NOTE unused.
    """
    epJson file object
    The class support handling epJson format input file.
    """
    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path=input_path, output_path=output_path)
        self.ep_model: Optional[JsonDict] = None
        self.file = None

        # create the json model, then open the file to write.
        try:
            with open(self._input_path, 'r') as f:
                self.ep_model = json.loads(f.read())
        except IOError:
            print(f"Failed to read jdf file {input_path}")

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
                    with open(self._output_path, "w") as f:
                        json_ep_model = json.dumps(self.ep_model, indent=4)
                        f.write(json_ep_model)
                except IOError:
                    print("Failed to open file {}".format(self._output_path))

        else:
            RuntimeError("File {} already openned".format(self.path))

    def get(self, key_lists: List[str]) -> Any:
        # TODO wrong! 2019-05-20
        if self.ep_model is not None:
            return None

        else:
            return None

