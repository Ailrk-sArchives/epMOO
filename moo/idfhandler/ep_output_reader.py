import csv
from typing import List, IO


class EPOutputReader:
    def __init__(self, path: str):
        self.path = path
        self.file: IO = open(path, 'r')
        self.reader = csv.DictReader(self.file)

    def read_column(self, column_name) -> List[str]:
        column: List[str] = []
        for row in self.reader:
            column.append(row[column_name])

        return column

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.file.close()


