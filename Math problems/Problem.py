import random
import names
from fractions import Fraction
import re
import json
from datetime import datetime
from math import gcd

HISTORY_FILE_NAME = "history_json.txt"
ERROR_MARGIN = 0.1

class Problem(object):

    problems = {
        0: "{:s} makes ${:d} per hour. {:s} makes {:d}/{:d} times that much every half hour. How much money will they have in {:d} hours?",
        1: "{:s} is {:d}/{:d} ft tall and grows {:d}/{:d} inches a week. How many days until he/she is {:d} ft tall?",
        2: "{0:s} mows {1:d} lawns an hour. {2:s} mowes {3:d} lawns every {4:d}/{5:d} hours. How long until they mow {6:d} lawns?",
        3: "-{:d}+{:d}-{:d}+{:d}", 4: "{:d}-{:d}-{:d}+{:d}", 5: "{:d}/{:d}", 6: "{:d}*{:d}",
        7: "{0:s}'s cup has {1:d} mL of water and leaks {2:d}/{3:d} mL per second. How long until {0:s} has {4:d} mL of water left?",
        8: "{:d} squared",
        9: "{:d}x + {:d} = {:d}"
        }  


    normal_solutions = (0, 1, 2, 7)
    provide_negatives = (3, 4, 5, 6, 8)
    num_problems = len(problems)
    filler_templates = list()

    # Creates a template for each question for generat_filler() to use
    for elt in problems.values():
        elt = re.findall("\{.*?\}", elt)
        already_filled = set()
        for i, sub_elt in enumerate(elt):
            sub_elt = re.sub("{|}", "", sub_elt).split(":")
            format_idx = sub_elt[0]
            if format_idx.isdigit():
                sub_elt[0] = format_idx = int(format_idx)
                
            if format_idx == "" or format_idx not in already_filled:
                elt[i] = sub_elt
                already_filled.add(format_idx)
            else:
                del elt[i]
        filler_templates.append(elt)

    def __init__(self):
        self.idx = random.randint(0, len(self.problems))
        self.filler = tuple()
        self.statement = str()
        self.soln, self.soln_frac = int(), str()

        self.attempt = -1
        self.time_posed, self.sec_total = int(), int()

        self.pose()
        self.result = str()
        self.previous_answers = list()

    def solve(self):
        f = self.filler
        solutions = {
            0: lambda: (f[1] + f[3] / f[4]) * 5, 
            1: lambda: 7 * (f[-1] - f[1] / f[2]) / (f[3] / f[4]), 
            2: lambda: f[6] / (f[1] + f[3] * f[4] / f[5]), 
            3: lambda: -f[0] + f[1] - f[2] + f[3], 
            4: lambda: f[0] - f[1] - f[2] + f[3],
            5: lambda: f[0] / f[1],
            6: lambda: f[0] * f[1],
            7: lambda: (f[1] - f[4]) / (f[2] / f[3]),
            8: lambda: f[0] * f[0]
            }

        self.soln = solutions[self.idx]()
        self.soln_frac = Fraction(self.soln).limit_denominator()
    
    # Randomly generates numbers and names for the problem
    def generate_filler(self):
        number_range = tuple(i for i in range(-20, 11) if i <= -3 or 3 <= i) \
                       if self.idx in Problem.provide_negatives else range(3, 21)
        filler = list()

        for elt in Problem.filler_templates[self.idx]:
            if elt[1] == "s":
                fill_value = names.get_first_name()
                event = random.randint(0, 40)
                events = {0: "Lil' ", 1: "Swag Lord ", 
                          2: "Raccoon ", 3: "Supreme Leader ",
                          4: "Big boy "}
                fill_value = events.get(event, "") + fill_value
            else:
                fill_value = random.choice(number_range)
            filler.append(fill_value)

        self.filler = filler
    
    # Creates the problem statement
    def pose(self):
        self.attempt = -1
        self.sec_total = 0

        self.previous_answers = list()
        self.generate_filler()
        self.solve()

        # Makes sure that the solution isn't too complex
        while ((self.idx in Problem.normal_solutions and self.soln < 1) 
               or len(str(self.soln_frac)) > 4 or abs(self.soln) > 30):
            self.generate_filler()
            self.solve()

        self.statement = Problem.problems[self.idx].format(*self.filler)
        self.time_posed = datetime.now()

    # Checks the user input against the soulution and saves the result.
    def check(self, input):
        try:
            # Converts answer
            if " " in input:
                input_float = input.partition(" ")
                frac = tuple(int(x) for x in input_float[2].split("/"))
                input_float = float(int(input_float[0]) + Fraction(
                               input_float[2]).limit_denominator())
            else:
                frac = tuple(int(x) for x in input.split("/"))
                input_float = float(Fraction(input).limit_denominator())

        except ValueError:
            self.result = "ValueError"
            return

        # Checks answer if it parsed successfully
        if len(frac) >= 2 and gcd(frac[0], frac[1]) > 1:
            self.result = "incorrect"
        elif abs(input_float - self.soln) < ERROR_MARGIN:
            self.result = "correct"
        else:
            self.result = "incorrect"
            self.previous_answers.append(input)

        self.attempt += 1
        self.save_result(input_float)

    # Appends the result as a dictionary to a list in the json file
    def save_result(self, input_float):

        now = datetime.now()
        sec_taken = round((now - self.time_posed).total_seconds())
        self.sec_total += sec_taken
        data_attempt = {"input": input_float, "result": self.result,
                       "seconds": sec_taken}

        try:
            with open(HISTORY_FILE_NAME) as history_file:
                history = json.load(history_file)
        except (EOFError, ValueError, FileNotFoundError) as _:
            history = list()

        with open(HISTORY_FILE_NAME, "w") as history_file:
            
            # Adds general info about the problem if this is the first attempt
            if self.attempt == 0:
                data_problem = {
                     "date": now.strftime("%m/%d/%Y"), 
                     "time": now.strftime("%I:%M %p"), 
                     "index": self.idx, "solution": self.soln, 
                     "total seconds": self.sec_total, 
                     "num attempts": 0, "attempts": list()
                    }
                history.append(data_problem)

            history[-1]["total seconds"] = self.sec_total
            history[-1]["num attempts"] = self.attempt + 1
            history[-1]["attempts"].append(data_attempt)

            json.dump(history, history_file, indent=4)