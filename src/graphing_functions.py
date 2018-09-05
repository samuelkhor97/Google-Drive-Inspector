"""
This file contains a library of graphing functions to be used in the Drive
Inspector tool.

Note that these functions make use of the external matplotlib and pyplot
libraries extenxively.
"""
import matplotlib
from matplotlib import pyplot

def totalContributionChart(dictInput):
    """
    Displays a pie chart showing percentages of each person's contribution.

    @:param dictInput: A dictionary with key-value pair of team mamber:
                       contribution.
    @:return: None.
    @:pre-condition:
    @:post-condition: None.
    @:complexity: Best and worst case: O(N), where N is the length of input.
    """
    keys = list(dictInput)
    contribution = [dictInput[key] for key in keys] # Creating a list of the
                                                    # 'value' items from the
                                                    # input.

    fig1, ax1 = pyplot.subplots()
    ax1.pie(contribution, labels=keys, autopct="%1.1f%%")
    ax1.axis("equal")
    ax1.set_title("The following is the percentage contribution per person")
    pyplot.show()

    return

# Test code.
if __name__ == "__main__":
    myDict = {"Test 1": 10, "Test 2": 20, "Test 3": 30}

    totalContributionChart(myDict)
