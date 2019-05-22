import sys
sys.path.append("../")
sys.path.append("../temp")
from objective_functions import f1_energy_consumption as f1
from objective_functions import f2_aPMV as f2
from objective_functions import f3_economy as f3

print(f1())
print(f2())
print(f3(1, 4, 1))

