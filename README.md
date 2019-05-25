### Multiple objectives optimizer for Building Design.

- 3 objectives. aPMV, energy consumption, economy.

- input: parameter vectors [old]

- output: csv for (vector - pareto optimal solution) pair and graph

- optimization algorithm: NSAG2

- multiprocessing boosting.

- (next goal) a better api 

### Prerequisite:
- energyplus in PATH

- python 3.7

- matplotlib


### file descriptions.
- main.py:
    The main program for defining and manage parameters.

- moo.py:
    Construct problems and call algorith.

- gui.py:
    The graphic interface.

- nsga2:
    A nsga2 algorithm implementation.

- objective\_functions.py:
    Defines objective funtions.       

- obj\_func\_preamble.py:
    Do some process before calculate objective funtions. It is useful when the objective functions requires to call external programs.

- utils.py
    Some helper functoins.

- sch.py:
    It is a modified version of sch, it can be used to verify the correctness of the nsga2 alogirthm.
