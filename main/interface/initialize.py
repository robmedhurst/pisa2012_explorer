"""."""

from main.interface.loaders import original_from_file
from main.interface.helpers import (
    user_input_group, single_response_from_list, user_set_sample_size)


def initialize(parameter_input, original_pisa2012):
    """
    User inputs to initialize.

    Question user to build sample data and groups of interest.

    Returns pisa_sample, inputs
    """
    def user_select_dependent_groups(variable_list):
        """."""
        # User input dependent group
        print("\nDependent Variable Input")
        print("Input a group of dependent variables (numeric).")
        current_input = user_input_group(variable_list)
        return {current_input[1]: current_input[0]}

    def user_select_independent_groups(variable_list):
        """."""
        # User input independent groups
        independent_groups = {}
        print("\nIndependent Variable Input")
        print("Input groups of independent variables.")
        print("\n")
        while True:
            print("Enter an independent group?")
            if single_response_from_list(['yes', 'no']) == 'no':
                break
            current_input = user_input_group(variable_list)
            independent_groups[current_input[1]] = current_input[0]
            print("Group entered.")
        return independent_groups

    def activate_preset(user_data):
        def do_pisa_sample(user_data):
            try:
                sample_in = user_data['pisa_sample']
            except KeyError:
                sample_in = user_data['sample_size']
            if isinstance(sample_in, int):
                user_data['sample_size'] = sample_in
                user_data['pisa_sample'] = pisa2012.sample(sample_in)
            return user_data

        def do_response_tracker_key(user_data):
            try:
                user_data['response_trackers']
            except KeyError:
                user_data['response_trackers'] = {}
            return user_data
        return do_response_tracker_key(do_pisa_sample(user_data))

    def do_build_user_data():

        def initialize_using_parameter():
            if parameter_input is not None:
                print("Loaded variable selection from parameter.\n")
                return activate_preset(parameter_input)
            return initialize_using_user_input()

        def initialize_using_user_input():
            built_data = {}
            built_data['dependent_groups'] = (
                user_select_dependent_groups(list(pisa2012.columns)))
            built_data['independent_groups'] = (
                user_select_independent_groups(list(pisa2012.columns)))
            built_data['sample_size'] = user_set_sample_size()
            return activate_preset(built_data)

        print("Initiailize by selecting groups of variables to explore.\n")
        return initialize_using_parameter()

    # TODO: Include option to reload and/or verify local files
    if original_pisa2012 is None:
        print("pisa2012 not loaded.\n\n")
        pisa2012 = original_from_file()
    else:
        pisa2012 = original_pisa2012
        print("pisa2012 loaded.\n\n")

    return do_build_user_data()
