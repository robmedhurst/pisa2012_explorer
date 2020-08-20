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

import main_ui as ui

from main_definitions import PRESET1, KNOWN_CATEGORIES


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
    def activate_preset(user_data):
        def do_pisa_sample(user_data):
            sample_in = user_data['pisa_sample']
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

    def initialize_using_parameter():
        if parameter_input is not None:
            print("Skipping initialize, loaded selection from parameter.\n")
            return activate_preset(parameter_input)

    def initialize_using_output():
        if 'OUTPUT' in globals():
            print("Would you like to reuse existing OUTPUT?")
            if ui.single_response_from_list(['yes', 'no']) == 'yes':
                return activate_preset(OUTPUT.copy())

    def initialize_using_preset():
        print("Use preset? ('no' to input sample size and groups)")
        if ui.single_response_from_list(['yes', 'no']) == 'yes':
            return activate_preset(PRESET1.copy())

    def initialize_using_user_input():
        built_data = {}
        built_data['dependent_groups'] = (
            ui.user_select_dependent_group(list(pisa2012.columns)))
        built_data['independent_groups'] = (
            ui.user_select_independent_groups(list(pisa2012.columns)))
        built_data['sample_size'] = ui.user_set_sample_size()
        return activate_preset(built_data)

    def do_build_user_data():
        user_data = initialize_using_parameter()
        if not user_data:
            user_data = initialize_using_output()
        if not user_data:
            user_data = initialize_using_preset()
        if not user_data:
            user_data = initialize_using_user_input()
        return user_data

    try:
        pisa2012 = PISA2012.copy()
    except NameError:
        pisa2012 = load_original_from_file()
    return do_build_user_data()


# %%% user_request_singlevar_graphics
def user_single_variable_graphics(user_data):
    """."""
    print("\n\n")
    print("Choose Single Variable Graphics")
    # INPUTS
    response_tracker = ui.initialize_tracker(user_data, 'singlevariable')
    # GRAPHICS
    graphic_buffer_objects = ui.graphics_from_responses(
        response_tracker, user_data, 'singlevariable')
    # UPDATES
    user_data['response_trackers']['singlevariable'] = response_tracker
    user_data['singlevariable_graphic_objects'] = graphic_buffer_objects
    return user_data


# %%% user_request_univariate_graphics
def user_request_univariate_graphics(user_data):
    """."""
    print("\n\n")
    print("Choose Univariate Graphics")
    # INPUTS
    response_tracker = ui.initialize_tracker(
        user_data, 'univariate')
    # GRAPHICS
    graphic_buffer_objects = ui.graphics_from_responses(
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
    response_tracker = ui.initialize_tracker(
        user_data, 'bivariate')
    # GRAPHICS
    graphic_buffer_objects = ui.graphics_from_responses(
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
    rip_lanes(['singlevariable_graphic_objects'])
    rip_lanes(['singlevariable_graphic_objects'])
    rip_lanes(['univariate_graphic_objects'])


if __name__ == '__main__':
    # load a global copy to avoid reloading
    if 'PISA2012' not in globals():
        PISA2012 = load_original_from_file()
    OUTPUT = initialize()
    show_all_output(OUTPUT)
