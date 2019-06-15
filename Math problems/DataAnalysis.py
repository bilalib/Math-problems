from pylab import *
import json
from Problem import Problem


HISTORY_FILE_NAME = "history_json.txt"
GRAPH_ROWS = 2
GRAPH_COLS = 2


def analyze():
    
    # Opens json file that class Problems saves to
    with open(HISTORY_FILE_NAME) as history_file:
        history = json.load(history_file)

    # Store per-day measurements
    dates = [history[0]["date"]]
    day_correct = [0]
    day_incorrect = [0]
    day_total = [0]
    
    # Store per-question measurements
    pblm_total = np.zeros(Problem.num_problems, dtype=np.int)
    pblm_correct = np.zeros(Problem.num_problems, dtype=np.int)

    # Store per-attempt measurements
    attempt_times = np.zeros(3, dtype=np.float)
    attempt_counts = np.zeros(3, dtype=np.int)

    # Gets all required vaules for all charts
    for problem in history:

        # Gets per-day values
        curr_date = problem["date"]
        if curr_date != dates[-1]:
            dates.append(curr_date)
            day_correct.append(0)
            day_incorrect.append(0)
            day_total.append(0)
        
        idx = problem["index"]
        
        # Iterates through each attempt, getting all values for all charts
        for i, attempt in enumerate(problem["attempts"]):

            # Gets per-day result totals
            if attempt["result"] == "correct":
                day_correct[-1] += 1
            else:
                day_incorrect[-1] += 1
            day_total[-1] += 1

            # Gets per-question result totals
            if attempt["result"] == "correct":
                pblm_correct[idx] += 1
            pblm_total[idx] += 1

            # Gets per-attempt-number time totals
            attempt_times[i] += attempt["seconds"]
            attempt_counts[i] += 1


    # Plotting the data
    fig, axes = plt.subplots(GRAPH_ROWS, GRAPH_COLS, figsize=(4,3))
    fig.subplots_adjust(right=3, top=3)

    # Per-day plot
    # Reformats the dates
    for i, date in enumerate(dates):
        if date[0] == "0":
            date = date.replace("0", "", 1)
        dates[i] = date.rpartition("/")[0]

    axes[0][0].plot(dates, day_correct, color = "green", marker="o")
    axes[0][0].plot(dates, day_incorrect, color = "red", marker="o")
    axes[0][0].plot(dates, day_total, color = "blue", marker="o")
    axes[0][0].legend(["correct", "incorrect", "total"])

    axes[0][0].set_xlabel("Dates")
    axes[0][0].set_ylabel("Total")
    axes[0][0].set_title("Per-day totals")


    # Per-question bar graph
    problem_indexes = range(Problem.num_problems)
    avg_correct = pblm_correct / pblm_total
    axes[0][1].bar(problem_indexes, avg_correct, align="center")
    axes[0][1].set_xticks(problem_indexes)

    axes[0][1].set_xlabel("Problem index")
    axes[0][1].set_ylabel("Correct / incorrect ratio")
    axes[0][1].set_title("Per-problem scores")

    # Provides the total problem attempts at top
    for i, height in enumerate(avg_correct):
        axes[0][1].text(i - 0.13, height + .01, str(pblm_total[i]))


    # Per-attempt-number bar graph
    attempt_numbers = np.arange(1, 4, dtype=np.int)
    avg_attempt_times = attempt_times / attempt_counts / 60
    axes[1][0].bar(attempt_numbers, avg_attempt_times, align="center")
    axes[1][0].set_xticks(attempt_numbers)

    axes[1][0].set_xlabel("Attempt number")
    axes[1][0].set_ylabel("Average time taken (min)")
    axes[1][0].set_title("Average time taken on each attempt")

    for i, height in enumerate(avg_attempt_times):
        # Provides number of times student got to attempt number at top
        axes[1][0].text(attempt_numbers[i] - .02, height + .05, str(attempt_counts[i]))


    return fig