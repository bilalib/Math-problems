from pylab import *
import json
from Problem import Problem


HISTORY_FILE_NAME = "history_json.txt"
GRAPH_ROWS = 1
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

    # Gets all required vaules for all charts
    for problem in history:

        # Gets per-day values
        curr_date = problem["date"]
        if curr_date != dates[-1]:
            dates.append(curr_date)
            day_correct.append(0)
            day_incorrect.append(0)
            day_total.append(0)

        for attempt in problem["attempts"]:
            if attempt["result"] == "correct":
                day_correct[-1] += 1
            else:
                day_incorrect[-1] += 1
            day_total[-1] += 1

        # Gets per-question values
        idx = problem["index"]
        for attempt in problem["attempts"]:
            if attempt["result"] == "correct":
                pblm_correct[idx] += 1
            pblm_total[idx] += 1


    # Plotting the data
    fig, axes = plt.subplots(GRAPH_ROWS, GRAPH_COLS)
    fig.subplots_adjust(right=2)

    # Per-day plot
    # Reformat the dates
    for i, date in enumerate(dates):
        if date[0] == "0":
            date = date.replace("0", "", 1)
        dates[i] = date.rpartition("/")[0]

    axes[0].plot(dates, day_correct, color = "green")
    axes[0].plot(dates, day_incorrect, color = "red")
    axes[0].plot(dates, day_total, color = "blue")
    axes[0].legend(["correct", "incorrect", "total"])

    axes[0].set_xlabel("Dates")
    axes[0].set_ylabel("Total")
    axes[0].set_title("Per-day totals")


    # Per-question bar graph
    problem_indexes = range(Problem.num_problems)
    ratios = pblm_correct / pblm_total
    axes[1].bar(problem_indexes, ratios, color="blue", align="center")

    axes[1].set_xticks(problem_indexes)
    axes[1].set_xlabel("Problem index")
    axes[1].set_ylabel("Correct / incorrect ratio")
    axes[1].set_title("Per-problem scores")

    # Provides the total problem attempts at top
    for i, height in enumerate(ratios):
        axes[1].text(i - 0.2, height + 0.01, str(pblm_total[i]))


    return fig