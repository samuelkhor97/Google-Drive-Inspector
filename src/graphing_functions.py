"""
This file contains a library of graphing functions to be used in the Drive
Inspector tool.

Note that these functions make use of the external matplotlib, pyplot, numpy
and mpld3 libraries.
"""
#import matplotlib
from matplotlib import pyplot
import numpy
import mpld3


def totalContributionChart(dictInput):
    """
    Displays a pie chart showing percentages of each person's contribution.

    @:param dictInput: A dictionary with key-value pair of team member:
                       contribution.
    @:return: The figure.
    @:pre-condition:
    @:post-condition: None.
    @:complexity: Best and worst case: O(N), where N is the length of input.
    """
    if type(dictInput) != dict:
        raise TypeError

    keys = list(dictInput)
    contribution = [dictInput[key] for key in keys]  # Creating a list of the
    # 'value' items from the
    # input.

    fig1, ax1 = pyplot.subplots()
    ax1.pie(contribution, labels=keys, autopct="%1.1f%%")
    ax1.axis("equal")
    ax1.set_title("The following is the percentage contribution per person")
    pyplot.show()

    return fig1


def timelineChart(dictInput):
    """
    Displays a bar chart depicting the contributions based on time.

    @:param dictInput: A dictionary with key-value pair of team member:
                       contribution, where contribution is also a dictionary
                       with key-value pair of week:contribution.
    @:return: None.
    @:pre-condition:
    @:post-condition: None.
    @:complexity: Best and worst case: O(MN^2), where M is the number of weeks
                  and N is the number of people in the team.
    """
    if type(dictInput) != dict:
        raise TypeError

    names = list(dictInput)
    weeks = list(dictInput[names[0]])   # Assume that every person has the same
    # weeks.
    # Creating and filling up a contribution matrix.
    contributions = [[dictInput[name][week] for week in weeks]
                     for name in names]

    ind = numpy.arange(len(weeks))
    plots = [None for i in range(len(names))]

    for person in range(len(contributions)):
        thisBottom = [0 for i in range(len(weeks))]
        for before in range(0, person):
            thisBottom = [thisBottom[week] + contributions[before][week]
                          for week in range(len(thisBottom))]
        plots[person] = pyplot.bar(ind, contributions[person],
                                   bottom=thisBottom)
    pyplot.ylabel("contributions")
    pyplot.title("Contributions per person on a weekly basis")
    pyplot.xticks(ind, weeks)
    pyplot.legend([plots[i][0] for i in range(len(plots))], names)
    pyplot.show()

    return

# Test code.
if __name__ == "__main__":
    myDict = {"Test 1": 10, "Test 2": 20, "Test 3": 30}

    # myPlot = totalContributionChart(myDict)

    dict2 = {"Peak Khor": {"2018week36": 2, "2018week37": 5},
             "Clare": {"2018week36": 5, "2018week37": 0}}

    timelineChart(dict2)
