# TODO for building multiobjective optimizer
author: jimmy yao.

## matlab Legacy 
### 2019-05-12 02:03 [DONE]
1. [X] find the type or value of following variables:
    nsga2.m: empty_individual [X]
    nsga2.m: F                [X] 
    nsga2.m: pop              [X]
    nsga2.m: PFCosts          [X]
    nsga2.m: Cost             [X]
    nsga2.m: all parameters.  [X]
    myCost.m: B               [X]
    myCost.m: biaohao         [X]
    
2. confirm the source of initialInvestment (one objective)
    A:  An external table. Not in EP.

3. [X] energy plus output.

4. where did the program used objectives?


### 2019-05-14 06:52 
1. Read the %program\_path% in RunEnergyPlus.bat

## New Era
### 2019-05-16 Create a module for handling idf files. [DONE] 
1. Why create a module to handle idf file format exclusively.
    1. more extensible, the generic module can be reused next time.
    2. easier to use
    
2. How to organize?
    1. A RAII class to handle the file IO exclusively.
    2. A Idf Model class to support text file based modification.

3. Note about idf format.
    1. Although IDF format is a csv like file, as an external program without context of the format it is impossible to parse it like a read csv.
    2. The more practical method I think is to to text pattern mateching based on the format.
    3. The idf model class support mutile anchor -- the keyword that match a line in the text.
    4. By serilize multiple anchors, the class can provides a dictionary like feeling (not really).

4. Disadvantage:   
    1. Unrealiable right now, sensitive to the input idf file. (can be improved by add checking)
    2. Not very user fridenly. (Need to wrap the regex part into pure string)

5. What I cannot do:
    1. I tried to support energy plus builtin input objects, but it is a huge projects, and I don't plan to commit into this project too much... I guess there are already some other wrote similiar functionalities.

### 2019-05-22 Congras! 
1. Everyting runs in python! No more matlab. Btw it is my birthday.

### 2019-05-26 Multiprocessing [TODO]
Try to support multiprocessing for nsga2 algorithm while minimize the degree of coupling. (NO COUPLING!!!)

1. Start to make multiprocessing. Benefits:
    1. Speed up testing process (a lot).
    2. Speed up simulation process (even more).

2. How will it looks like:
    1. Spots for concurency optimizing are all around based on the function calculate\_objectives(.). 
    2. Spawn a pool with multiple processes, each process handle one input parameter list and one output objectives.
    3. The function will call energyplus, so energyplus will be parallelized (which is the goal).
    4. each function call will generate a idf file named by the pid of the process who created it.
    5. Energyplus output will be put into a directory named by the pid of the process who created it, too.
    6. Delete all output files and directories at the beginning of the function call. (preserve last output for validation)

3. How to design the code:
    1. Change the idfhandler class to support specific output name.
    2. Add an concurency parameter for class Evolution in nsga2.
    3. Create a module multiproc\_pool.py, which provides a decorator for multiprocessing.
    4. Modify the preamble to support multiprocessing (mainly about the idf name and directory name).

4. What will we achieve after implemented multiprocessing?
    Currently each run of energyplus takes around 40 seconds. Accroding to last time experience run 6 energyplus concurrently will take around 70 seconds, which means each turn only spend 11 seconds, so it can shorten 3/4 time of execution. A workstation with 16 cores will speed it up even further.


### 2019-05-26 A flexx based GUI [TODO]
Need a fancy gui for the program. Flexx is a python lib for creating web based gui.
1. Why need a gui?
    1. User of the program are not programmer.
    2. It is quite annoying to mannually tweak all those parameters

2. Why choose flexx?
    1. It is web based and has great crossplatform performance.
    2. It looks fancy.

3. How the gui will looks like?
    1. The gui should be a generic gui, means it should not be constrained by one perticular optimization problem.
    2. This means the panel for inputing parameter should be flexible. Maybe a pure text field or a list.
    3. There should be an output window which can show both program output and log for program work flow for multiprocessing.
    4. A panel for tweaking hyperparameters.
    5. A panel to design extra constants, those does not be used as input of the optimization problem.
    6. A control panel.

4. How to conncet the value in the gui to value in the model?
    MVC!

### 2019-05-26 Make the whole program a package [TODO]
1. Why?
    1. Easier to cross platform.
    2. Less hassle on setting environment up.

### 2019-05-26 Support remote multiprocessing [OPTINAL]
Support remote multiprocessing to improve the performance even further.
1. How?
    1. Maybe write a server client app, server dispatch randomly generated parameters for optimization problem into different clients, clients works out objectives and sent back to server.

2. How much could it be faster?:
    If your office has 8 machines, each machine with 8 cores, you are able to utilze 64 cores for the optimization problem. Because the function be parallelized is completely indepedent, there will be no data racing, no deadlock, nothing but faster speed. 

3. How to exactly?
    1. Server and client use python native socket.
    2. data will be lists of input parameters, so maybe transmitted inform of json.
    3. There might be some problem in scheduling when collecting results from different hosts, in that case just put everything in a que since the order doesn't matter.

### 2019-05-26 Betterl logging system. [TODO]
Now there are full of print in the program, change them into better logging module

1. Why?
    1. logging is more flexible, it can be controlled globally.
    2. it can output to files without handling manually.

