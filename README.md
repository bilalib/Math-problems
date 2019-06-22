# Math-problems
Math-problems is a program to ask a student math problems with randomized numbers and record their progress.
It has 3 main components, elaborated upon in later sections:
  1. The Problem class, which is one problem
  2. The ProgramWindow class, which is the GUI for user interaction
  3. The DataAnalysis module, which contains the analyze function to produce visuals of the student's progress.

# 3 Components
## 1. ProgramWindow
This is the GUI that the student will interact with. ```ProgramWindow.py``` should be compiled for the student to answer math problems. It depends on the next component, ```Problem.py``` Example pictures:
![image of GUI](https://github.com/bilalib/Math-problems/blob/master/Pictures/GUI.png)

## 2. Problem
### Adding problem types
A dictionary at the top of the Problem class, which contains the words of the problems to be used. In place of a name, there is ```{:s}``` or ```{i:s}```, where ```i``` is an index, as used by the ```str.format()``` function. In place of a number, there is ```{:d}``` or ```{i:d}```. Below the dictionary, there is a loop that will parse these, generating a template that will instruct ```generate_filler()``` on filling this. Any string in this format will work, as long as a solution is provided in ```solve()```. 

### ```solve()```
In solve(), ```f[i]``` stands for the i<sup>th</sup> thing to be filled in the problems dict. Ex. in ```"{:s} has {:d}/{:d}"```, the name is f[0], the numerator is ```f[1]```, and the denominator is ```f[2]```. The functions are in a dict, corresponding to the same key as that in ```problems```. Lambdas are used for lazy evaluation.

### ```pose()```
The problem index, ```idx```, is randomly decided upon creation of the instance. ```pose()``` will generate, solve, and fill the problem at the index. It will also make sure that the solution is not > 30 and that the the fraction answer contains at most 3 digits. ```normal_solutions``` is a tuple of problem indexes to which the solution will be >= 1. ```pose()``` will make sure of this.

### ```check()```
This is used in the gui only. When called and given a string, it will parse it it if the string is a fraction and set ```self.result``` to one of: "incorrect", "correct", or "ValueError". Answers must be within ```ERROR_MARGIN``` of answer to be correct. Unsimplified fractions are marked incorrect. ```check()``` will also use json to save detailed information about the problem and the attempts the student made, updating the persistent list in the file name given by ```HISTORY_FILE_NAME```.

## 3. DataAnalysis.py
This module contains a single function, ```analyze()```. Given the name of the file and the minimum or starting date, it will return a matplotlib figure of graphs about the student's progress. Saving the figure as a picture:
```DataAnalysis.analyze("history_json.txt", "06/16/2019").savefig("figure", bbox_inches='tight')```.
Example of the graphs it will make:

<img src="https://github.com/bilalib/Math-problems/blob/master/Pictures/figure.png" width="700">
