"""User interactions."""

import pandas as pd


def user_batch_questioning(question_set=None):
    """
    Return user selections from set of selections options.

    Each key identifies a question.
    Values are dictionaries containting at least "type" and "selections"

    question_set is a dictionary, entries are questions to ask the user.
    Each entry is a dictionary whose keys represent the elements of a
    question.
    """
    # dumbie question set, delete once function is wrapped
    if question_set is None:
        # this is never called so keeping import local
        import test_groupings
        question_set = test_groupings.PLACEHOLDER_QUESTIONS

    # parse each question
    for question in question_set:
        print("\n\n")
        try:
            print(question_set[question]['preface'])
        except KeyError:
            pass

        # default to single response if none specified
        try:
            question_type = question_set[question]['question_type']
        except KeyError:
            question_type = 'single'

        # default to y/n if no selection
        try:
            selection_options = question_set[question]['selection_options']
        except KeyError:
            selection_options = ['yes', 'no']

        # default to no maximum numer of selections
        try:
            max_selectable = question_set[question]['max_selectable']
        except KeyError:
            max_selectable = None

        # default to no excluded selections
        try:
            not_selectable = question_set[question]['not_selectable']
        except KeyError:
            not_selectable = None

        # default to no max or min
        try:
            max_min_vals = question_set[question]['max_min_vals']
        except KeyError:
            max_min_vals = (None, None)

        # user to select one or multiple
        if question_type in ['single']:
            question_set[question]['response'] = single_response_from_list(
                selection_options, not_selectable
                )

        elif question_type in ['multi']:
            question_set[question]['response'] = multi_responses_from_list(
                selection_options, not_selectable, max_selectable
                )

        elif question_type in ['integer']:
            question_set[question]['response'] = input_integer(*max_min_vals)

        elif question_type in ['string']:
            question_set[question]['response'] = input_simple_string(
                *max_min_vals)

    return question_set


def single_response_from_list(list_input, not_selectable_indices=None):
    """
    Return a single selection by user from given list of strings.

    Indices represented by 'not_selectable_indices' are excluded
    from selection options but still printed.


    Parameters
    ----------
    list_input : list of strings to be selection options.

    not_selectable_indices : list of integers representing indices to bypass.

    Returns
    -------
    The selected string from list_input.
    """
    if not_selectable_indices is None:
        not_selectable_indices = []
    # accepted responses are the indices of list_input as strings
    accepted_responses = set(list(range(len(list_input))))
    # remove not_selectable_indices
    accepted_responses.difference_update(set(not_selectable_indices))
    accepted_responses = pd.array(list(accepted_responses)).astype(str)

    prompt_string = "Select an option by index:\n"
    for index, phrase in enumerate(list_input):
        # not selectable items are marked with a dash instead of index number
        if index in not_selectable_indices:
            prompt_string += ("[-]   " + phrase + "\n")
        else:
            prompt_string += ("[" + str(index) + "]   " + phrase + "\n")
    prompt_string += "\nYour input: "
    # user repsonse must be in accepted_responses before returning
    response = ''
    while response.lower() not in accepted_responses:
        response = input(prompt_string)
    return list_input[int(response)]


def multi_responses_from_list(list_input, not_selectable_indices=None,
                              max_selected=None):
    """Return selections made by user from given list of strings."""
    potential_selections = list_input.copy()

    # human readable exit string, insert ahead of other selection options
    exit_selection_message = '-FINISH SELECTION-'
    # insert exit key
    potential_selections.insert(0, exit_selection_message)

    # human readable reset string, insert behind other selection options
    reset_selection_message = '-RESTART SELECTION-'
    potential_selections.insert(
        len(potential_selections), reset_selection_message)

    # if no maximum number of selections specified, user retains control
    if max_selected is None:
        max_selected = len(list_input) + 1

    # loop in case user wants to start over
    while True:
        returning_strings = []
        if not_selectable_indices is None:
            current_not_selectable_indices = []
        else:
            current_not_selectable_indices = not_selectable_indices.copy()

        # repeat single_response_from_list until exit conditions met
        while True:

            # return on max number of selections reached
            if len(returning_strings) == max_selected:
                return returning_strings

            # user selection made
            current_selection = single_response_from_list(
                potential_selections, current_not_selectable_indices)

            # return on user command
            if current_selection == exit_selection_message:
                return returning_strings

            # restart selection on user command
            if current_selection == reset_selection_message:
                break

            # update current_not_selectable_indices
            current_not_selectable_indices.append(
                potential_selections.index(current_selection))
            # update returning_strings
            returning_strings.append(current_selection)


def input_integer(min_int=None, max_int=None):
    """Return an integer within given range, specified by user."""
    prompt_string = "Please enter an integer: "
    while True:
        response = input(prompt_string)

        try:
            response = int(response)
            if max_int is None and min_int is None:
                return response

            elif max_int is not None and min_int is not None:
                if min_int <= response <= max_int:
                    return response
                else:
                    print("integer expected between ",
                          min_int, " and ", max_int)

            elif max_int is not None:
                if max_int >= response:
                    return response
                else:
                    print("integer expected less than ", max_int+1)

            else:
                if min_int <= response:
                    return response
                else:
                    print("integer expected greater than ", min_int-1)

        except ValueError:
            print("not an integer")


def input_simple_string(min_length=None, max_length=None):
    """Return a simple string specified by user."""
    prompt_string = "Please enter a simple string: "
    while True:
        response = input(prompt_string)

        response.strip()

        if min_length is None and max_length is None:
            break

        elif min_length is not None and max_length is not None:
            if min_length <= len(response) <= max_length:
                break
            else:
                print("string length expected between ",
                      min_length, " and ", max_length)

        elif max_length is not None:
            if max_length >= len(response):
                break
            else:
                print("string length expected less than ", max_length+1)

        else:
            if min_length <= len(response):
                break
            else:
                print("string length expected greater than ", min_length-1)

    return response


def input_pisa_var_name(valid_names):
    """Return valid PISA variable name input by user."""
    prompt_string = "Please enter a valid PISA variable (column name): "

    while True:
        response = input(prompt_string)
        if response in valid_names:
            return response
