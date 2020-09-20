"""."""

import ui.ui as ui
from ui.save_load import load_original_from_file


def initialize(parameter_input, original_pisa2012):
    """
    User inputs to initialize.

    Question user to build sample data and groups of interest.

    Returns pisa_sample, inputs
    """
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
                print("Loaded user selection from parameter.\n")
                return activate_preset(parameter_input)
            return initialize_using_user_input()

        def initialize_using_user_input():
            built_data = {}
            built_data['dependent_groups'] = (
                ui.user_select_dependent_groups(list(pisa2012.columns)))
            built_data['independent_groups'] = (
                ui.user_select_independent_groups(list(pisa2012.columns)))
            built_data['sample_size'] = ui.user_set_sample_size()
            return activate_preset(built_data)

        print("Initiailize by selecting groups of variables to explore.\n")
        return initialize_using_parameter()

    # TODO: Include option to reload and/or verify local files
    if original_pisa2012 is None:
        print("pisa2012 not loaded.\n\n")
        pisa2012 = load_original_from_file()
    else:
        pisa2012 = original_pisa2012
        print("pisa2012 loaded.\n\n")

    return do_build_user_data()


def single_variable_graphics(user_data):
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


def request_univariate_graphics(user_data):
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


def request_bivariate_graphics(user_data):
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


def request_multivariate_graphics(user_data):
    """."""
    print("\n\n")
    print("Choose Multivariate Graphics")
    # INPUTS
    response_tracker = ui.initialize_tracker(
        user_data, 'multivariate')
    # GRAPHICS
    graphic_buffer_objects = ui.graphics_from_responses(
        response_tracker, user_data, 'multivariate')
    # UPDATES
    user_data['response_trackers']['multivariate'] = response_tracker
    user_data['multivariate_graphic_objects'] = graphic_buffer_objects
    return user_data
