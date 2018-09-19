"""
This file contains a library of graphing functions to be used in the Drive
Inspector tool.

Note that these functions make use of the external matplotlib, pyplot, numpy
and mpld3 libraries.
"""
from matplotlib import pyplot
import numpy
import mpld3

def totalContributionChart(dictInput):
    """
    Displays a pie chart showing percentages of each person's contribution.

    @:param dictInput: A dictionary with key-value pair of team member:
                       contribution.
    @:return: A figure object containing the pie chart.
    @:pre-condition: Input must be a dictionary with numbers as values.
    @:post-condition: None.
    @:complexity: Best and worst case: O(N), where N is the length of input.
    """
    if type(dictInput) != dict:
        raise TypeError
    
    names = list(dictInput)
    contribution = [dictInput[name] for name in names] # Creating a list of the
                                                       # 'value' items from the
                                                       # input.

    fig, ax = pyplot.subplots()
    ax.pie(contribution, labels=names, autopct="%1.1f%%")
    ax.axis("equal")
    ax.set_title("Percentage contribution per person")
    pyplot.show()

    return fig

def timelineChart(dictInput):
    """
    Displays a bar chart depicting the contributions based on time.

    @:param dictInput: A dictionary with key-value pair of team member:
                       contribution, where contribution is also a dictionary
                       with key-value pair of week:contribution.
    @:return: A figure object containing the stacked bar chart.
    @:pre-condition: Input must be a dictionary with values of dictionaries with
                     numbers as values.
    @:post-condition: None.
    @:complexity: Best and worst case: O(MN^2), where M is the number of weeks
                  and N is the number of people in the team.
    """
    if type(dictInput) != dict:
        raise TypeError

    for key in dictInput:
        if type(dictInput[key]) != dict:
            raise TypeError

    names = list(dictInput)
    weeks = list(dictInput[names[0]])   # Assume that every person has the same
                                        # weeks.
    # Creating and filling up a contribution matrix.
    contributions = [[dictInput[name][week] for week in weeks]
                     for name in names]
    
    ind = numpy.arange(len(weeks))
    fig, ax = pyplot.subplots()
    plots = [None for i in range(len(names))]

    for person in range(len(contributions)):
        thisBottom = [0 for i in range(len(weeks))]
        for before in range(0, person):
            thisBottom = [thisBottom[week] + contributions[before][week]
                          for week in range(len(thisBottom))]
        plots[person] = ax.bar(ind, contributions[person], bottom = thisBottom)
    pyplot.ylabel("contributions")
    pyplot.title("Contributions per person on a weekly basis")
    pyplot.xticks(ind, weeks)
    pyplot.legend([plots[i][0] for i in range(len(plots))], names)
    pyplot.show()

    return fig
    
# Test code.
if __name__ == "__main__":
    myDict = {"Test 1": 10, "Test 2": 20, "Test 3": 30}

    myFig1 = totalContributionChart(myDict)

    dict2 = {"Peak Khor":{"2018week36":2,"2018week37":5},"Clare":{"2018week36":5,"2018week37":0}}

    myFig2 = timelineChart(dict2)
