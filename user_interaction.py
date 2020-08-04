"""User interactions."""

import pandas as pd


def single_response_from_list(list_input):
    """Return a single selection by user from given list of strings."""
    print("\n\nSelect an option by index:")

    accepted_responses = set(pd.array(list(range(
        len(list_input)))).astype(str))

    prompt_string = ""
    for index, phrase in enumerate(list_input):
        # index = ("[" + str(index) + "]   ")
        prompt_string += ("[" + str(index) + "]   " + phrase + "\n")
    prompt_string += "\nYour input: "

    response = ''
    while response.lower() not in accepted_responses:
        response = input(prompt_string)

    return list_input[int(response)]


def multi_responses_from_list(list_input, max_selected=None):
    """Return selections made by user from given list of strings."""
    # when an index is selected, remove it from the accepted_responses list
    #                         , replace index in prompt_string with an 'X'
    #                         , add selection to list
    #                         , when len list == max_selected, return
    print("\n\nSelect an options by index:")

    accepted_responses = set(pd.array(list(range(
        len(list_input)))).astype(str))

    prompt_string = ""
    for index, phrase in enumerate(list_input):
        prompt_string += ("[" + str(index) + "]   " + phrase + "\n")
    prompt_string += "\nYour input: "

    response = ''
    while response.lower() not in accepted_responses:
        response = input(prompt_string)

    return list_input[int(response)]
