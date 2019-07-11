import sys
sys.path.append("../")
from moo.utils import generate_new_construction

s = generate_new_construction(
        "2.1",
        [(6, 0, 3), (6, 0, 0), (6, 3, 0), (6, 3, 3)],
        0.15)

print(s)

