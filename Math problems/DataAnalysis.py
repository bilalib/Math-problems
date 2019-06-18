from pylab import *
import seaborn as sns
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import json
from Problem import Problem
from datetime import datetime


ERROR_MARGIN = 0.1

def analyze(history_file_name, min_date):
    
    # Opens json file that class Problems saves to
    with open(history_file_name) as history_file:
        history = json.load(history_file)

    # Store per-day measurements
    dates = [min_date]
    day_correct = [0]
    day_incorrect = [0]
    day_total = [0]
    
    # Store per-question measurements
    pblm_total = np.zeros(Problem.num_problems, dtype=np.int)
    pblm_correct = np.zeros(Problem.num_problems, dtype=np.int)

    # Store per-attempt measurements
    attempt_times = np.zeros(3, dtype=np.float)
    attempt_counts = np.zeros(3, dtype=np.int)
    attempt_date_counts = np.zeros(3, dtype=np.int)
    attempt_date_times = np.zeros((1, 3))

    # Stores per-answer distance measurements
    solutions = list()
    attempt_dists = list()
    result_colors = list()

    # Gets all required vaules for all charts
    for problem in (problem for problem 
                    in history if datetime.strptime(problem["date"], "%d/%M/%Y")
                   >=  datetime.strptime(min_date, "%d/%M/%Y")):

        curr_date = problem["date"]
        if curr_date != dates[-1]:
            # Adds new date for per-day data
            dates.append(curr_date)
            day_correct.append(0)
            day_incorrect.append(0)
            day_total.append(0)
            # Adds new date for per-attempt date count
            attempt_date_counts[attempt_date_counts == 0] = 1
            attempt_date_times[-1] /= attempt_date_counts * 60
            attempt_date_times = np.vstack([attempt_date_times, np.zeros(3)])
            attempt_date_counts = np.zeros(3, dtype=np.int)
        
        idx = problem["index"]
        solution = problem["solution"]
        
        # Iterates through each attempt, getting all values for all charts
        for i, attempt in enumerate(problem["attempts"]):

            result = attempt["result"]
            # Gets per-day result totals
            if result == "correct":
                day_correct[-1] += 1
            else:
                day_incorrect[-1] += 1
            day_total[-1] += 1

            # Gets per-question result totals
            if result == "correct":
                pblm_correct[idx] += 1
            pblm_total[idx] += 1

            # Gets per-attempt-number time totals
            sec = attempt["seconds"]
            attempt_times[i] += sec
            attempt_counts[i] += 1
            attempt_date_counts[i] += 1
            attempt_date_times[-1][i] += sec

            # Gets per-answer distance measurements
            solutions.append(solution)
            float_input = attempt["float input"]
            attempt_dists.append(abs(solution - float_input))
            if result == "correct":
                result_colors.append("none")
            elif abs(float_input - solution) < ERROR_MARGIN:
                result_colors.append("gold")
            else:
                result_colors.append("r")

    # Averages per-attempt daily measurements
    attempt_date_counts[attempt_date_counts == 0] = 1
    attempt_date_times[-1] /= attempt_date_counts * 60

    # Plotting the data
    fig, axes = plt.subplots(2, 2, figsize=(4,3))
    fig.subplots_adjust(right=3, top=3)

    # Per-day plot
    # Reformats the dates
    for i, date in enumerate(dates):
        if date[0] == "0":
            date = date.replace("0", "", 1)
        dates[i] = date.rpartition("/")[0]

    axes[0][0].plot(dates, day_correct, color = "green", marker="o")
    axes[0][0].plot(dates, day_incorrect, color = "red", marker="o")
    axes[0][0].plot(dates, day_total, marker="o")
    axes[0][0].legend(["correct", "incorrect", "total"])

    axes[0][0].set_xlabel("Dates")
    axes[0][0].set_ylabel("Total")
    axes[0][0].set_title("Per-day totals")


    # Per-question bar graph
    problem_indexes = range(Problem.num_problems)
    pblm_total[pblm_total == 0] = 1
    avg_correct = pblm_correct / pblm_total
    axes[0][1].bar(problem_indexes, avg_correct, align="center")
    axes[0][1].set_xticks(problem_indexes)

    axes[0][1].set_xlabel("Problem index")
    axes[0][1].set_ylabel("Correct / incorrect ratio")
    axes[0][1].set_title("Per-problem scores")

    # Provides the total problem attempts at top
    for i, height in enumerate(avg_correct):
        axes[0][1].text(i - 0.13, height + .01, str(pblm_total[i]))

    # Per-attempt-number bar graphs
    # Top graph compares attempts side by side
    attempt_numbers = np.arange(1, 4, dtype=np.int)
    attempt_counts[attempt_counts == 0] = 1
    avg_attempt_times = attempt_times / attempt_counts / 60

    axes[1][0].axis("off")
    top = inset_axes(axes[1][0], "100%", "60%", "upper right")
    bot = inset_axes(axes[1][0], "100%", "17%", "lower left")

    if np.all(attempt_date_times[0] == 0):
        attempt_date_times = np.delete(attempt_date_times, (0), 0)
    top.stackplot(dates, attempt_date_times.transpose(), colors=sns.color_palette("Greens", 3))
    top.legend(attempt_numbers, loc="upper left")
    top.set_title("Average time spent per attempt per day")
    top.set_xlabel("Dates")
    top.set_ylabel("Time spent (min)")
    
    bot.barh(attempt_numbers, avg_attempt_times, color=sns.color_palette("Greens", 3))
    bot.set_yticks(attempt_numbers)
    for i, height in enumerate(avg_attempt_times):
        # Provides at top of bar number of times student got to attempt
        bot.text(height + .02, attempt_numbers[i] - .15, str(attempt_counts[i]))
    bot.set_title("Average across all days of above graph")
    bot.set_xlabel("Time spent (min)")
    bot.set_ylabel("Attempt")
    bot.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Per-answer distance scatterplot
    axes[1][1].scatter(solutions, attempt_dists, c=result_colors, s=5)
    axes[1][1].set_ylim(0, 80)

    axes[1][1].set_xlabel("Solution")
    axes[1][1].set_title("Distance from answer vs solution")

    # Moves y-axis to center
    axes[1][1].spines['left'].set_position('zero')
    axes[1][1].spines['right'].set_color('none')


    return fig