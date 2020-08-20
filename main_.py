"""
PISA2012_EXPLORER.

This project aims to develop tools to assist with the wrangling and
exploration of the PISA 2012 dataset. Specifically, groups of similar
variables are explored concurrently.
"""

import zipfile
import pickle

import pandas as pd

import main_category_actions

from main_wrangle import wrangle
from main_ui import (
    user_select_dependent_group, user_select_independent_groups,
    single_response_from_list, multi_responses_from_list, get_function_by_key,
    get_single_graphic, get_next_unused_name, initialize_tracker,
    graphics_from_responses, user_set_sample_size)

from main_definitions import PRESET1, KNOWN_CATEGORIES
# import graphics_pool_singlevar as singlevar_graphics_pool
# import graphics_pool_univariate as univariate_graphics_pool
# import graphics_pool_bivariate as bivariate_graphics_pool
# import graphics_pool_multivariate as multivariate_graphics_pool


def load_original_from_file():
    """."""
    def load_pisa_csv():
        return pd.read_csv(
            'pisa2012.csv',
            sep=',', encoding='latin-1', error_bad_lines=False,
            dtype='unicode', index_col=False)

    def pisa_csv_from_zip():
        return zipfile.ZipFile('pisa2012.csv.zip', 'r').open('pisa2012.csv')

    def load_pisa_zip():
        return pd.read_csv(
            pisa_csv_from_zip(),
            sep=',', encoding='latin-1', error_bad_lines=False,
            dtype='unicode', index_col=False)

    print("Attempting to load original PISA 2012 data from file",
          "(this may take a few minutes)...\n")
    for loader_name in ['load_pisa_csv', 'load_pisa_zip']:
        try:
            print("Attempting", loader_name, "...")
            pisa = locals()[loader_name]()
            print("Finished loading from", loader_name[-3:], "file.")
            return pisa
        except FileNotFoundError:
            print("Failed loading from", loader_name[-3:], "file.")
    print("Could not load from local csv or zip file.")


def initialize(user_data=None):
    """Wrap function calls."""
    # returns pisa_df, inputs, categories_found, and graphics_objects
    return (
        user_request_bivariate_graphics(
            user_request_univariate_graphics(
                user_single_variable_graphics(
                    post_wrangle(
                        wrangle(
                            user_initialize(user_data)))))))


def post_wrangle(user_data):
    """Apply category specific post wrangle functions."""
    group_category_matches = user_data['group_category_matches']
    pisa_df = user_data['custom_dataframe']

    # group_category_matches holds indep and dependent groups seperately
    for subset in group_category_matches:
        # iterate group category matches
        for group_name in group_category_matches[subset]:
            category = group_category_matches[subset][group_name]

            # check if associated post wrangling group actions are available
            if category + "_group_post_wrangle" in dir(main_category_actions):
                # function call using getattr
                getattr(
                    main_category_actions,
                    (category + "_group_post_wrangle"))(
                        group_name, user_data)
    # update and return user_data
    user_data['custom_dataframe'] = pisa_df
    return user_data


# %%% user_initialize

def user_initialize(parameter_input=None):
    """
    User inputs to initialize.

    Question user to build sample data and groups of interest.

    Returns pisa_sample, inputs
    """
    def apply_preset(preset):
        try:
            sample_in = preset['pisa_sample']
            if isinstance(sample_in, int):
                preset['sample_size'] = sample_in
                preset['pisa_sample'] = pisa2012.sample(sample_in)
        except KeyError:
            return "KeyError on user_initialize 'preset'"
        return preset

    def build_new_user_data():
        built_data = {}
        built_data['dependent_groups'] = (
            user_select_dependent_group(list(pisa2012.columns)))
        built_data['independent_groups'] = (
            user_select_independent_groups(list(pisa2012.columns)))
        built_data['sample_size'] = user_set_sample_size()
        built_data['pisa_sample'] = pisa2012.sample(built_data['sample_size'])
        return built_data

    def do_build_user_data():
        # check for paramater input and existing gloabl OUTPUT
        if parameter_input is not None:
            print("Skipping initialize, loaded selection from parameter.\n")
            return apply_preset(parameter_input)
        if 'OUTPUT' in globals():
            print("Would you like to reuse existing OUTPUT?")
            if single_response_from_list(['yes', 'no']) == 'yes':
                return apply_preset(OUTPUT.copy())
        # user initiated preset
        print("\n")
        print("Use preset? ('no' to input sample size and groups)")
        if single_response_from_list(['yes', 'no']) == 'yes':
            print("Using preset...")
            return apply_preset(PRESET1.copy())
        # user create new user_data
        return build_new_user_data()

    # load original data
    try:
        pisa2012 = PISA2012.copy()
    # fall back to reload from csv, then zip
    except NameError:
        pisa2012 = load_original_from_file()

    user_data = do_build_user_data()
    print(user_data)
    return user_data


# %%% user_request_singlevar_graphics

def user_single_variable_graphics(user_data):
    """User select plots."""
    # ========================================================================
    #
    group_category_matches = user_data['group_category_matches']

    # private=================================================================
    #
    def user_select_groups(list_of_groups):
        """User choose any number from list of groups."""
        if len(list_of_groups) > 1:
            print("\n")
            print("Which groups to use...")
            print("Use all groups?")
            if single_response_from_list(['yes', 'no']) == 'yes':
                return list_of_groups
            print("Which groups to use...")
            return multi_responses_from_list(list_of_groups)
        return list_of_groups

    def get_singlevar_group_functions(group_info):
        # get functions matching category key from univatiate pool
        list_of_functions = get_function_by_key(
            group_info['category'], 'singlevariable')
        # Detect BINARY
        if group_info['category'] in KNOWN_CATEGORIES and len(
                KNOWN_CATEGORIES[group_info['category']]) == 2:
            # get binary functions
            list_of_functions.extend(
                get_function_by_key('binary', 'singlevariable'))
        # Detect CATEGORICAL
        if group_info['category'] in KNOWN_CATEGORIES:
            # get binary functions
            list_of_functions.extend(
                get_function_by_key('cat', 'singlevariable'))
        return list_of_functions

    def user_select_functions(group_info):
        list_of_functions = get_singlevar_group_functions(group_info)
        # bypass user input
        if response_tracker['bypass'] == 'none':
            return []
        elif response_tracker['bypass'] == 'all':
            return list_of_functions
        # different user prompts for different number of available functions
        elif len(list_of_functions) == 1:
            print("\n")
            print("Do you want to use function",
                  list_of_functions[0], "for group", group_info['name'], "?")
            if single_response_from_list(['yes', 'no']) == 'no':
                return []
        elif len(list_of_functions) > 1:
            print("\n")
            print("Use all functions for group", group_info['name'], "?")
            if single_response_from_list(['yes', 'no']) == 'no':
                print("\n")
                print("Which functions to use for group",
                      group_info['name'], "?")
                return multi_responses_from_list(list_of_functions)
        return list_of_functions

    def get_singlevar_graphic(function_name, group_info):
        return get_single_graphic(
            'singlevariable', function_name, (group_info, user_data))

    def iterate_group_function_selection(location):
        groups_to_check = response_tracker[location]
        graphics_by_group = {}
        for group_name in groups_to_check:
            # define group
            graphics_by_group[group_name] = {}
            group_info = {
                'name': group_name,
                'variables': user_data[location][group_name],
                'category': group_category_matches[location][group_name]}
            # interact with user
            response_tracker['functions'][group_name] = (
                user_select_functions(group_info))
            # call selected functions
            for function_name in response_tracker['functions'][group_name]:
                graphics_by_group[group_name][function_name] = (
                    get_singlevar_graphic(function_name, group_info))
        return graphics_by_group

    def init_response_tracker(bypass_type):
        if bypass_type == "Yes, with all plots.":
            return {
                # populate with responses indicating ALL options selected
                'bypass': 'all',
                'dependent_groups':
                    list(group_category_matches['dependent_groups'].keys()),
                'independent_groups':
                    list(group_category_matches['independent_groups'].keys()),
                'functions': {}}
        elif bypass_type == "Yes, with no plots.":
            return {
                # populate with responses indicating NO options selected
                'bypass': 'none',
                'independent_groups': [],
                'dependent_groups': []}
        else:
            return {'bypass': False}

    def user_select_bypass():
        # User Select Bypass
        print("Bypass selection?")
        return single_response_from_list([
            "Yes, with all plots.",
            "Yes, with no plots.",
            "No, manually select groups to explore."
            ])

    print("\n\n")
    print("Choose Single Variable Graphics")
    try:
        response_tracker = user_data['response_trackers']['singlevariable']
    except KeyError:
        response_tracker = False
    #
    # response_tracker old
    if response_tracker is not False:
        print("Existing responses found, reuse them?")
        if single_response_from_list(["yes", "no"]) == 'no':
            # move the old tracker
            user_data['response_trackers'][
                get_next_unused_name(
                    user_data,
                    ['response_trackers'], 'singlevariable'
                    )] = response_tracker
            response_tracker = False
    # response_tracker new
    if response_tracker is False:
        response_tracker = init_response_tracker(user_select_bypass())
    # storage
    singlevar_graphic_objects = {
        'dependent_groups': {},
        'independent_groups': {}
        }
    #
    # Dependent Groups
    print("\n")
    print("Dependent Variables")
    # group selection
    if not response_tracker['bypass']:  # user select groups if no bypass
        response_tracker['dependent_groups'] = user_select_groups(list(
            group_category_matches['dependent_groups'].keys()))
    # function selection
    singlevar_graphic_objects['dependent_groups'] = (
        iterate_group_function_selection('dependent_groups'))
    #
    # Independent Groups
    print("\n")
    print("Independent Variables")
    # group selection
    if not response_tracker['bypass']:  # user select groups if no bypass
        response_tracker['independent_groups'] = user_select_groups(list(
            group_category_matches['independent_groups'].keys()))
    # function selection
    singlevar_graphic_objects['independent_groups'] = (
        iterate_group_function_selection('independent_groups'))
    #
    # interaction end ========================================================
    # ========================================================================
    #
    # Update and Return user_data
    if 'response_trackers' not in user_data.keys():
        user_data['response_trackers'] = {}
    user_data['response_trackers']['singlevariable'] = response_tracker
    user_data['singlevariable_graphic_objects'] = singlevar_graphic_objects
    return user_data


# %%% user_request_univariate_graphics
def user_request_univariate_graphics(user_data):
    """."""
    print("\n\n")
    print("Choose Univariate Graphics")
    # INPUTS
    response_tracker = initialize_tracker(
        user_data, 'univariate')
    # GRAPHICS
    graphic_buffer_objects = graphics_from_responses(
        response_tracker, user_data, 'univariate')
    # UPDATES
    user_data['response_trackers']['univariate'] = response_tracker
    user_data['univariate_graphic_objects'] = graphic_buffer_objects
    return user_data


# %%% user_request_bivariate_graphics
def user_request_bivariate_graphics(user_data):
    """."""
    print("\n\n")
    print("Choose Bivariate Graphics")
    # INPUTS
    response_tracker = initialize_tracker(
        user_data, 'bivariate')
    # GRAPHICS
    graphic_buffer_objects = graphics_from_responses(
        response_tracker, user_data, 'bivariate')
    # UPDATES
    user_data['response_trackers']['bivariate'] = response_tracker
    user_data['bivariate_graphic_objects'] = graphic_buffer_objects
    return user_data


# %% Main


def show_all_output(result):
    """Display results."""
    def rip_lanes(lanes):
        target = result.copy()
        for lane_name in lanes:
            target = target[lane_name]
        for group in target.values():
            for graphic in group.values():
                if graphic is not None:
                    graphic.seek(0)
                    pickle.load(graphic)
    rip_lanes(['singlevariable_graphic_objects', 'dependent_groups'])
    rip_lanes(['singlevariable_graphic_objects', 'independent_groups'])
    rip_lanes(['univariate_graphic_objects'])


if __name__ == '__main__':
    # load a global copy to avoid reloading
    if 'PISA2012' not in globals():
        PISA2012 = load_original_from_file()
    OUTPUT = initialize()
    show_all_output(OUTPUT)
