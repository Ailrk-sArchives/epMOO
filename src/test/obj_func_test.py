import sys
sys.path.append("../")
sys.path.append("../temp")
from objective_functions import f1_energy_consumption as f1
from objective_functions import f2_aPMV as f2
from objective_functions import f3_economy as f3

arg = (1, 4, 1, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 2.5)

print(f1(*arg))
print(f2(*arg))
print(f3(*arg))

