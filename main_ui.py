"""User interactions."""

import pandas as pd

import main_definitions as definitions
import graphics_pool_univariate as univariate_graphics_pool
import graphics_pool_bivariate as bivariate_graphics_pool
import graphics_pool_multivariate as multivariate_graphics_pool


# =============================================================================
# %% Direct Inputs
# =============================================================================
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
    print(list_input[int(response)])
    return list_input[int(response)]


def input_integer(min_int=None, max_int=None):
    """Return an integer within given range, specified by user."""
    prompt_string = "Please enter an integer: "
    while True:
        response = input(prompt_string)

        try:
            response = int(response)
            if max_int is None and min_int is None:
                return response

            if max_int is not None and min_int is not None:
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
# =============================================================================
# %% Input Extension
# =============================================================================
    def user_input_group(pisa_var_list, group_size=None, group_name=None):
        """Return user defined group of pisa variables."""
        group = []
        if not group_name:
            print("\n")
            print("Enter short name for this group...")
            # user input group name
            group_name = input_simple_string(1, 20)
        if not group_size:
            print("\n")
            print("How many variables will this group contain?")
            # user input group size
            group_size = input_integer(1, 5)
        while len(group) < group_size:
            # user input variable names
            print("\n")
            group.append(input_pisa_var_name(pisa_var_list))
        return group, group_name


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
        # this is never called
        question_set = definitions.PLACEHOLDER_QUESTIONS

    # parse each question
    for question in question_set:
        # print("\n\n")
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


# =============================================================================
# %% User Data Build Helper Functions
# =============================================================================

def select_group(user_data, expected_groups='independent_groups'):
    """
    Return group properties of user selected group.

    putting groups in order give the user the option to use dependent
    and independent groups interchangably for univariate plots, without
    conflating the two when presenting the user with selection.
    """
    # placing independent or dependent groups at top of selection_list
    unexpected_groups = 'dependent_groups'
    if expected_groups == 'dependent_groups':
        unexpected_groups = 'independent_groups'
    selection_list = []
    # indicate group types in selection_list
    selection_list.append(expected_groups + ":")  # index is 0
    selection_list.extend(user_data[expected_groups])
    # indicate group types in selection_list
    selection_list.append(  # index is len(user_data[expected_groups])
        "Not originally entered as " + expected_groups + ":")
    selection_list.extend(user_data[unexpected_groups])
    # not_selectable_indices
    group_name = single_response_from_list(
        selection_list, [0, len(user_data[expected_groups]) + 1])
    # selection location
    if selection_list.index(group_name) > len(user_data[expected_groups]):
        location = unexpected_groups
    else:
        location = expected_groups
    return {
        'name': group_name,
        'variables': user_data[location][group_name],
        'category':
            user_data['group_category_matches'][location][group_name]}


def get_function_by_key(name_key, local_py_file):
    """Return function names from local_py_file.py that contain name_key."""
    matching_functions = []
    for function_name in dir(local_py_file)[8:]:
        if name_key in function_name:
            matching_functions.append(function_name)
    return matching_functions


def get_functions_by_group(independent_input_groups, graphics_pool):
    """."""
    # independent_input_groups are in order of plot primacy
    # two entries implies a bivariate plot, where the second is
    # the more specific visualization
    known_categories = definitions.KNOWN_CATEGORIES
    list_of_functions = []
    for index, group in enumerate(independent_input_groups):
        # known category
        search_key = str(index + 1) + group['category']
        list_of_functions.extend(
            get_function_by_key(
                search_key, graphics_pool))
        # generic categorical
        search_key = str(index + 1) + 'cat'
        if group['category'] in known_categories:
            list_of_functions.extend(get_function_by_key(
                search_key, graphics_pool))
        # generic binary
        if group['category'] in known_categories and len(
                known_categories[group['category']]) == 2:
            search_key = str(index + 1) + 'binary'
            list_of_functions.extend(get_function_by_key(
                search_key, graphics_pool))
    return list_of_functions


def graphics_from_responses(response_tracker, user_data, graphics_pool):
    """Generate graphics according to given responses."""
    def graphics_by_function(response):
        graphics_by_function = {}
        for function_name in response['functions']:
            graphics_by_function[function_name] = getattr(
                graphics_pool, (function_name))(response, user_data)
        return graphics_by_function
    graphics_by_groupkey = {}
    for groupkey, response in response_tracker.items():
        graphics_by_groupkey[groupkey] = graphics_by_function(response)
    return graphics_by_groupkey


def create_response(user_data, graphics_pool):
    """."""
    independent_groups = []

    def add_independent():
        if len(independent_groups) < 1:
            print("Select an independent group.")
        else:
            print("Select another independent group.")
        independent_groups.append(select_group(
            user_data, 'independent_groups'))

    # loop for user correct input error
    while True:
        print("Select a dependent group.")
        dependent_group = select_group(
            user_data, 'dependent_groups')
        # at least one independent
        add_independent()
        # two for bivariate
        if graphics_pool == bivariate_graphics_pool:
            add_independent()
        # N for multivariate
        elif graphics_pool == multivariate_graphics_pool:
            independent_var_count = 2
            while True:
                independent_var_count += 1
                add_independent()
                print(independent_var_count, " independent groups selected.")
                print("Select another?")
                if single_response_from_list(['Yes', 'No']) == 'No':
                    break
        user_selected_functions = multi_responses_from_list(
            get_functions_by_group(
                independent_groups, graphics_pool))
        user_response = {
            'independent_groups': independent_groups,
            'dependent_group': dependent_group,
            'functions': user_selected_functions}
        # User Confirm Selection
        print(user_response)
        print("Is this selection correct?")
        if single_response_from_list([
                'Yes, continue.',
                'No, lets try again.']) == 'Yes, continue.':
            return user_response


def create_multiple_responses(user_data, graphics_pool, response_tracker=None):
    """."""
    if response_tracker is None:
        response_tracker = {}
    # loop for multiple selections
    while True:
        # create new tracker and key
        response = create_response(user_data, graphics_pool)
        # build group selection key
        group_selection_key = response['dependent_group']['name']
        for indep_group in response['independent_groups']:
            group_selection_key += "_vs_"
            group_selection_key += indep_group['name']
        # merge list of functions if appending to an existing tracker
        if group_selection_key in list(response_tracker.keys()):
            response_tracker[group_selection_key]['functions'] += (
                response['functions'])
        else:
            response_tracker[group_selection_key] = response
        # quick hack to remove duplicates
        response_tracker[group_selection_key]['functions'] = list(
            dict.fromkeys(
                response_tracker[group_selection_key]['functions']))
        # user choose to exit univariate selection
        print("Enter another selection?")
        if single_response_from_list(
                ['Yes, enter another.', 'No, done for now.']
                ) == 'No, done for now.':
            return response_tracker


def initialize_tracker(user_data, graphics_pool, target='univariate'):
    """."""
    def do_existing_tracker(existing_trackers, user_data, graphics_pool):
        """."""
        def save_old_trackers():
            tracker_name = get_next_unused_name(
                user_data, ['response_trackers'], 'univariate')
            user_data['response_trackers'][tracker_name] = existing_trackers
        # ask user what to do
        print("Previous selections found.")
        current_response = single_response_from_list([
            "Reuse selection", "Create new selection", "Add to selection"])
        if current_response == "Reuse selection":
            # No need to get more trackers or save the old ones
            return existing_trackers
        elif current_response == "Create new selection":
            new_trackers = create_multiple_responses(
                user_data, graphics_pool)
            if existing_trackers != new_trackers:
                save_old_trackers()
            return new_trackers
        elif current_response == "Add to selection":
            new_trackers = create_multiple_responses(
                user_data, graphics_pool, existing_trackers.copy())
            if existing_trackers != new_trackers:
                save_old_trackers()
            return new_trackers
    # check for existing tracker
    try:
        existing_tracker = user_data[
            'response_trackers'][target]
    except KeyError:
        existing_tracker = False
    # user interactions
    if existing_tracker is False:
        return create_multiple_responses(user_data, graphics_pool)
    # user choose how to use existing tracker
    return do_existing_tracker(
        existing_tracker, user_data, univariate_graphics_pool)


def get_next_unused_name(user_data, location, name, appendage="_old_"):
    """Get next free integer for a name in a dictionary."""
    working_dictionary = user_data.copy()
    # navigate location specified
    # for depth in range(len(location)):
    for depth, key in enumerate(location):
        working_dictionary = working_dictionary[location]
    # find smallest integer such that new_name doesnt yet exist
    back_up_num = 0
    while name + appendage + str(back_up_num) in working_dictionary.keys():
        back_up_num += 1
    return name + appendage + str(back_up_num)