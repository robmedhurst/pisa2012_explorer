"""."""

import main.category_definitions as definitions

from main.interface.helpers import (
    single_response_from_list, multi_responses_from_list, pool_string_to_loc)


def build_group_selection_key(target, response, delimeter='_vs_'):
    """."""
    if target == 'singlevariable':
        return response['independent_groups'][0]['name']
    group_selection_key = response['dependent_groups']['name']
    for indep_group in response['independent_groups']:
        group_selection_key += delimeter
        group_selection_key += indep_group['name']
    return group_selection_key


def get_functions_by_group(independent_input_groups, target):
    """."""
    # independent_input_groups are in order of plot primacy
    # two entries implies a bivariate plot, where the second is
    # the more specific visualization
    known_categories = definitions.KNOWN_CATEGORIES

    def get_function_by_key(name_key, target):
        """Return functions from local_py_file.py that contain name_key."""
        matching_functions = []
        for function_name in dir(pool_string_to_loc(target))[8:]:
            if name_key in function_name:
                matching_functions.append(function_name)
        return matching_functions

    def gather_accepted_functions():
        def list_common(a, b):
            c = [value for value in a if value in b]
            return c
        for index in range(len(independent_input_groups)):
            if index > 0:
                potential_functions['accepted'].extend(list_common(
                    potential_functions[index],
                    potential_functions[index - 1]))
        if len(independent_input_groups) == 1:
            potential_functions['accepted'].extend(potential_functions[0])
        return potential_functions['accepted']

    def gather_potential_known_category_functions():
        for index, group in enumerate(independent_input_groups):
            search_key = str(index + 1) + group['category']
            potential_functions[index].extend(
                get_function_by_key(search_key, target))

    def gather_potential_binary_functions():
        for index, group in enumerate(independent_input_groups):
            if group['category'] in known_categories and len(
                    known_categories[group['category']]) == 2:
                search_key = str(index + 1) + 'binary'
                potential_functions[index].extend(
                    get_function_by_key(search_key, target))

    def gather_potential_categorical_functions():
        for index, group in enumerate(independent_input_groups):
            search_key = str(index + 1) + 'cat'
            if group['category'] in known_categories:
                potential_functions[index].extend(
                    get_function_by_key(search_key, target))

    potential_functions = {'accepted': []}
    for index in range(len(independent_input_groups)):
        potential_functions[index] = []

    gather_potential_known_category_functions()
    gather_potential_binary_functions()
    gather_potential_categorical_functions()
    return gather_accepted_functions()


def initialize_tracker(user_data, target):
    """."""
    def user_select_group(user_data, expected_groups):
        """
        Return group properties of user selected group.

        putting groups in order give the user the option to use dependent
        and independent groups interchangably for univariate plots, without
        conflating the two when presenting the user with selection.
        """
        messages = [str("Entered as dependent_groups:"),
                    str("Entered as independent_groups:")]
        if expected_groups:
            messages = [str(expected_groups + ":"),
                        str("Not entered as " + expected_groups + ":")]
        else:
            expected_groups = 'dependent_groups'
        unexpected_groups = 'dependent_groups'
        if expected_groups == 'dependent_groups':
            unexpected_groups = 'independent_groups'
        # place expected groups at top of selection_list
        selection_list = []
        selection_list.append(messages[0])  # index is 0
        selection_list.extend(user_data[expected_groups])
        selection_list.append(messages[1])
        selection_list.extend(user_data[unexpected_groups])
        # user makes selection (messages can not be selected)
        group_name = single_response_from_list(
            selection_list, [0, len(user_data[expected_groups]) + 1])
        location = expected_groups  # location of selection
        if selection_list.index(group_name) > len(user_data[expected_groups]):
            location = unexpected_groups
        return {
            'name': group_name,
            'variables': user_data[location][group_name],
            'category':
                user_data['group_category_matches'][location][group_name]}

    def create_response(user_data, target):
        """."""
        def user_accept_selection(user_response):
            # TODO: Display current selection
            print()
            print("'dependent group':")
            print(user_response['dependent_groups']['name'])
            print("'independent groups':")
            for group in user_response['independent_groups']:
                print(group['name'])
            print("'functions':")
            for function_name in user_response['functions']:
                print(function_name + ":  " + getattr(
                    pool_string_to_loc(target), function_name).__doc__)
            print()
            print("Is this selection correct?")
            return single_response_from_list([
                    'Yes, continue.',
                    'No, lets try again.']) == 'Yes, continue.'

        def get_dependent_groups():
            # single variable dont need a dependent
            if target == 'singlevariable':
                return None
            else:
                print("Select a dependent group.")
                return user_select_group(user_data, 'dependent_groups')

        def get_independent_groups():

            def singlevarselection():
                return[
                    user_select_group(user_data, False)]

            def multivarselection():
                independent_groups_list = []

                def add_independent():
                    if len(independent_groups_list) < 1:
                        print("Select an independent group.")
                    else:
                        print("Select another independent group.")
                    independent_groups_list.append(
                        user_select_group(user_data, 'independent_groups'))

                add_independent()
                if target == 'bivariate':
                    add_independent()
                elif target == 'multivariate':
                    independent_var_count = 1
                    while True:
                        independent_var_count += 1
                        add_independent()
                        print(independent_var_count,
                              " independent groups selected.")
                        print("Select another?")
                        if single_response_from_list(['Yes', 'No']) == 'No':
                            break
                return independent_groups_list

            if target == 'singlevariable':
                return singlevarselection()
            else:
                return multivarselection()

        def build_response():
            def function_select(function_list):
                verbose_list = []
                for function_name in function_list:
                    verbose_list.append(function_name + ":  " + getattr(
                        pool_string_to_loc(target), function_name).__doc__)
                function_list = []
                for selection in multi_responses_from_list(verbose_list):
                    function_list.append(selection.split(":")[0])
                return function_list
            independent_groups = get_independent_groups()
            return {'independent_groups': independent_groups,
                    'dependent_groups': get_dependent_groups(),
                    'functions': function_select(get_functions_by_group(
                        independent_groups, target))}

        # loop for user correct input error
        while True:
            user_response = build_response()
            if user_accept_selection(user_response):
                return user_response

    def create_multiple_responses(user_data, target, response_tracker=None):

        def do_update_response_tracker(response):
            group_selection_key = build_group_selection_key(target, response)
            # merge list of functions if appending to an existing tracker
            if group_selection_key in list(response_tracker.keys()):
                response_tracker[group_selection_key]['functions'] += (
                    response['functions'])
            else:
                response_tracker[group_selection_key] = response
            # crude hack to remove duplicates
            response_tracker[group_selection_key]['functions'] = list(
                dict.fromkeys(
                    response_tracker[group_selection_key]['functions']))
        if response_tracker is None:
            response_tracker = {}
        # loop for multiple selections
        while True:
            # create new response and update response_trackers with it
            do_update_response_tracker(create_response(user_data, target))
            # user choose to exit univariate selection
            print()
            print("Enter another selection?")
            if single_response_from_list(
                    ['Yes, enter another.', 'No, done for now.']
                    ) == 'No, done for now.':
                return response_tracker

    def fresh_trackers(existing_trackers):
        new_trackers = create_multiple_responses(
            user_data, target)
        save_old_trackers(existing_trackers, new_trackers)
        return new_trackers

    def expand_trackers(existing_trackers):
        new_trackers = create_multiple_responses(
            user_data, target,
            existing_trackers.copy())
        save_old_trackers(existing_trackers, new_trackers)
        return new_trackers

    def all_trackers():
        return get_all_reponses(user_data, target)

    def save_old_trackers(existing_trackers, new_trackers):

        def get_next_unused_name(
                user_data, location, name, appendage="_old_"):
            """Get next free integer for a name in a dictionary."""
            working_dictionary = user_data.copy()
            # navigate location specified
            # for depth in range(len(location)):
            for depth, key in enumerate(location):
                working_dictionary = working_dictionary[key]
            # find smallest integer such that new_name doesnt yet exist
            back_up_num = 0
            while (name + appendage + str(back_up_num)
                   ) in working_dictionary.keys():
                back_up_num += 1
            return name + appendage + str(back_up_num)

        if existing_trackers != new_trackers:
            tracker_name = get_next_unused_name(
                user_data, ['response_trackers'], target)
            user_data['response_trackers'][tracker_name] = existing_trackers

    def do_no_existing_trackers():
        user_options = [
            str("Bypass " + target + " graphics?"),
            "Manually select " + target + " graphics by group",
            str("Generate all possible " + target + " graphics")]
        user_choice = single_response_from_list(user_options)
        if user_choice == user_options[0]:
            return {}
        elif user_choice == user_options[1]:
            return fresh_trackers(None)
        elif user_choice == user_options[2]:
            return all_trackers()

    def do_existing_trackers(existing_trackers):
        print("Previous selections found.")
        user_options = [
            "Reuse selections", "Create new selections", "Add to selections",
            str("Generate all possible " + target + " graphics"),
            str("Bypass " + target + "_graphics")]
        user_choice = single_response_from_list(user_options)

        if user_choice == user_options[0]:  # resuse
            return existing_trackers

        elif user_choice == user_options[1]:  # new
            return fresh_trackers(existing_trackers)

        elif user_choice == user_options[2]:  # append
            return expand_trackers(existing_trackers)

        elif user_choice == user_options[3]:  # all
            save_old_trackers(existing_trackers, {})
            return all_trackers()

        elif user_choice == user_options[4]:  # None
            save_old_trackers(existing_trackers, {})
            return {}

    # Try existing tracker
    try:
        return do_existing_trackers(user_data['response_trackers'][target])
    except KeyError:
        pass
    return do_no_existing_trackers()


def get_all_reponses(user_data, target):
    """Return all group combinations as response_tracker."""
    overgrown_response_tracker = {}

    def combination_generator(iterable, r):
        # combinations('ABCD', 2) --> AB AC AD BC BD CD
        # combinations(range(4), 3) --> 012 013 023 123
        pool = tuple(iterable)
        n = len(pool)
        if r > n:
            return
        indices = list(range(r))
        yield tuple(pool[i] for i in indices)
        while True:
            for i in reversed(range(r)):
                if indices[i] != i + n - r:
                    break
            else:
                return
            indices[i] += 1
            for j in range(i+1, r):
                indices[j] = indices[j-1] + 1
            yield tuple(pool[i] for i in indices)

    def all_responses(dependent_selection, num_independent_needed):
        """."""
        responses = {}
        for indep_selections in combination_generator(
                list(user_data['independent_groups'].keys()),
                num_independent_needed):
            independent_groups = []
            for group_name in indep_selections:
                independent_groups.append(
                    {'name': group_name,
                     'variables':
                         user_data['independent_groups'][group_name],
                     'category':
                         user_data['group_category_matches'
                                   ]['independent_groups'][group_name]})
            response = {
                'dependent_groups': dependent_selection,
                'independent_groups': independent_groups,
                'functions':
                    get_functions_by_group(independent_groups, target)}
            group_selection_key = build_group_selection_key(target, response)
            if len(response['functions']) > 0:
                responses[group_selection_key] = response
        return responses

    def single_independent_groups():
        response_tracker = {}
        for group_name, variables in user_data['independent_groups'].items():
            group_info = {
                'name': group_name,
                'variables': variables,
                'category': user_data['group_category_matches'
                                      ]['independent_groups'][group_name]}
            response = {
                'dependent_groups': None,
                'independent_groups': [group_info],
                'functions': get_functions_by_group([group_info], target)}
            if len(response['functions']) > 0:
                response_tracker[group_name] = response
        return response_tracker

    if target == 'singlevariable':
        overgrown_response_tracker.update(single_independent_groups())

    for group_name, variables in user_data['dependent_groups'].items():
        dependent_group = {
            'name': group_name,
            'variables': variables,
            'category': user_data[
                'group_category_matches']['dependent_groups'][group_name]}

        if target == 'singlevariable':  # depth = 0
            overgrown_response_tracker[group_name] = {
                'dependent_groups': None,
                'independent_groups': [dependent_group],
                'functions':
                    get_functions_by_group([dependent_group], target)}

        elif target == 'univariate':  # depth = 1
            overgrown_response_tracker.update(
                all_responses(dependent_group, 1))

        elif target == 'bivariate':  # depth = 2
            overgrown_response_tracker.update(
                all_responses(dependent_group, 2))

        elif target == 'multivariate':  # infinite depth
            max_num_indep = len(user_data['independent_groups'].keys())
            for num_indep in range(max_num_indep):
                overgrown_response_tracker.update(
                    all_responses(dependent_group, num_indep))

    return overgrown_response_tracker
