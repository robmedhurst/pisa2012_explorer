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
    def activate_user_data(param_input):
        def build_sample(param_input):
            try:
                sample_in = param_input['pisa_sample']
            except KeyError:
                sample_in = param_input['sample_size']
            if isinstance(sample_in, int):
                param_input['sample_size'] = sample_in
                param_input['pisa_sample'] = pisa2012.sample(sample_in)
            return param_input

        # TODO: generate universal group traits that will be used often
        def build_meta(user_data):

            for target in ['dependent_groups', 'independent_groups']:
                for group_key, group in user_data[target].items():
                    if 'name' not in group:
                        group['name'] = group_key
                    if 'size' not in group:
                        group['size'] = len(group['variable_names'])
            return user_data

        def build_tracker(user_data):
            try:
                user_data['response_trackers']
            except KeyError:
                user_data['response_trackers'] = {}
            return user_data

        return build_tracker(build_meta(build_sample(param_input)))

    def gather_user_data():

        def user_data_via_user_input():
            def user_select_dependent_groups(variable_list):
                # User input dependent group
                print("\nDependent Variable Input")
                print("Input a group of dependent variables (numeric).")
                current_input = user_input_group(variable_list, known_names)
                known_names.append(current_input['name'])
                return {current_input['name']: current_input}

            def user_select_independent_groups(variable_list):
                """."""
                # User input independent groups
                independent_groups = {}
                print("\nIndependent Variable Input")
                print("Input groups of independent variables.")
                print("\n")
                while True:
                    if len(independent_groups) != 0:
                        print("Enter another independent group?")
                    else:
                        print("Enter an independent group?")
                    if single_response_from_list(['yes', 'no']) == 'no':
                        return independent_groups
                    current_input = user_input_group(
                        variable_list, known_names)
                    known_names.append(current_input['name'])
                    independent_groups[current_input['name']] = current_input
                    print("Group entered.")

            known_names = [None]
            built_data = {}
            built_data['dependent_groups'] = (
                user_select_dependent_groups(list(pisa2012.columns)))
            built_data['independent_groups'] = (
                user_select_independent_groups(list(pisa2012.columns)))
            built_data['sample_size'] = user_set_sample_size()
            return built_data

        def user_data_via_preset():
            print("Loaded variable selection from parameter.\n")
            return parameter_input

        if parameter_input is None:
            return user_data_via_user_input()
        return user_data_via_preset()

    # TODO: Include option to reload and/or verify local files
    if original_pisa2012 is None:
        print("pisa2012 not loaded.\n\n")
        pisa2012 = original_from_file()
    else:
        pisa2012 = original_pisa2012
        print("pisa2012 loaded.\n\n")

    print("Initiailize by selecting groups of variables to explore.\n")
    return activate_user_data(gather_user_data())
