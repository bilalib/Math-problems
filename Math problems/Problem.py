import random
import names
from fractions import Fraction
import re

class Problem(object):

    problems = tuple((
        "{0:s} makes ${1:d} per hour. {2:s} makes {3:d}/{4:d} times that much every half hour. {5:s} loses ${6:d}/{7:d} per hour. How much money will they have in {8:d} hours?",
        "A {:d} foot tall plant grows {:d}/{:d} inches a week. How many days until it is {:d} ft tall?",
        "{0:s} mows {1:d} lawns an hour. {2:s} mowes {3:d} lawns every {4:d}/{5:d} hours. How long until they mow {6:d} lawns?",
        "-{:d}+{:d}-{:d}+{:d}", "{:d}-{:d}-{:d}+{:d}"
        ))

    NUM_PROBLEMS = len(problems)
    filler_templates = list()

    for _, elt in enumerate(problems):
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

    normal_solutions = (0, 1, 2)
    provide_negatives = (3, 4)

    def __init__(self):
        self.idx = random.randint(0, Problem.NUM_PROBLEMS - 1)
        self.filler = tuple()
        self.float_soln = int()
        self.statement, self.frac_soln = str(), str()

    def solve(self):
        f = self.filler
        solutions = tuple((
            lambda: (f[1] + f[3] / f[4] - f[6] / f[7]) * f[8], 
            lambda: (f[3] - f[0])/(f[1]/f[2]), 
            lambda: f[6] / (f[1] + f[3] * f[4] / f[5]), 
            lambda: -f[0] + f[1] - f[2] + f[3], 
            lambda: f[0] - f[1] - f[2] + f[3]
            ))
        self.float_soln = solutions[self.idx]()
        self.frac_soln = str(Fraction(self.float_soln).limit_denominator())

    def generate_filler(self):
        number_range = tuple(i for i in range(-20, 21) if i <= -3 or 3 <= i) \
                       if self.idx in Problem.provide_negatives else range(3, 21)
        for elt in Problem.filler_templates[self.idx]:
            filler.append(names.get_first_name()) if elt[1] == "s" \
            else filler.append(random.choice(number_range))
        self.filler = filler

    def pose(self):
        self.generate_filler()
        self.solve()
        while (self.idx in Problem.normal_solutions and self.float_soln < 1) \
               or len(self.frac_soln) > 4 or abs(self.float_soln) > 30:
            self.generate_filler()
            self.solve()
        self.statement = Problem.problems[self.idx].format(*self.filler)