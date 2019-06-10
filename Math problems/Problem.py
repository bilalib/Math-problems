import random
import names
from fractions import Fraction
import re
import json
from datetime import datetime

HISTORY_FILE_NAME = "history_json.txt"
ERROR_MARGIN = 0.1
VALUE_ERROR = -1

class Problem(object):

    problems = {
        0: "{0:s} makes ${1:d} per hour. {2:s} makes {3:d}/{4:d} times that much every half hour. {5:s} loses ${6:d}/{7:d} per hour. How much money will they have in {8:d} hours?",
        1: "{:s} is {:d}/{:d} ft tall and grows {:d}/{:d} inches a week. How many days until he/she is {:d} ft tall?",
        2: "{0:s} mows {1:d} lawns an hour. {2:s} mowes {3:d} lawns every {4:d}/{5:d} hours. How long until they mow {6:d} lawns?",
        3: "-{:d}+{:d}-{:d}+{:d}", 
        4: "{:d}-{:d}-{:d}+{:d}", 
        5: "{:d}/{:d}"
        }
    
    normal_solutions = (0, 1, 2)
    provide_negatives = (3, 4, 5)
    num_problems = len(problems)
    filler_templates = list()

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
        self.idx = random.randint(0, Problem.num_problems - 1)
        self.filler = tuple()
        self.soln = int()
        self.statement = str()
        self.attempt = 0
        self.correct = False

    def solve(self):
        f = self.filler
        solutions = {
            0: lambda: (f[1] + f[3] / f[4] - f[6] / f[7]) * f[8], 
            1: lambda: f[6] / (f[1] + f[3] * f[4] / f[5]), 
            2: lambda: (f[-1] - f[1] / f[2]) / (f[3] / f[4]), 
            3: lambda: -f[0] + f[1] - f[2] + f[3], 
            4: lambda: f[0] - f[1] - f[2] + f[3],
            5: lambda: f[0] / f[1]
            }
        self.soln = solutions[self.idx]()

    def generate_filler(self):
        number_range = tuple(i for i in range(-20, 11) if i <= -3 or 3 <= i) \
                       if self.idx in Problem.provide_negatives else range(3, 21)
        filler = list()
        for elt in Problem.filler_templates[self.idx]:
            if elt[1] == "s":
                fill_value = names.get_first_name()
                event = random.randint(0, 10)
                if event == 0:
                    fill_value = "Lil' " + fill_value
                elif event == 1:
                    fill_value = "Swaglord " + fill_value
            else:
                fill_value = random.choice(number_range)
            filler.append(fill_value)
        self.filler = filler

    def pose(self):
        self.generate_filler()
        self.solve()
        while (self.idx in Problem.normal_solutions and self.float_soln < 1) \
               or len(str(Fraction(self.soln).limit_denominator())) > 4 \
               or abs(self.soln) > 30:
            self.generate_filler()
            self.solve()
        self.statement = Problem.problems[self.idx].format(*self.filler)

    def check(self, input):
        try:
            if " " in input:
                input = input.partition(" ")
                input = int(input[0]) + Fraction(input[2]).limit_denominator()
            else:
                input = Fraction(input).limit_denominator()
        except ValueError:
            self.correct = VALUE_ERROR

        if abs(float(input) - self.soln) < ERROR_MARGIN:
            self.correct = True
        else:
            self.attempt += 1

    def save_result(self, input):
        now = datetime.now()
        result = {"date": now.strftime("%m/%d/%Y"),
                  "time": now.strftime("%I:%M %p"), "idx": self.idx,
                  "attempt": self.attempt, "soln": self.float_soln,
                  "input": input, "correct": self.correct}
        try:
            with open(HISTORY_FILE_NAME) as history_file:
                history = json.load(history_file)
        except (EOFError, ValueError, FileNotFoundError) as _:
            history = list()
        with open(HISTORY_FILE_NAME, "w") as history_file:
            history.append(result)
            json.dump(history, history_file, indent=1)