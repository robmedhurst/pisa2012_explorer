"""."""

from main.interface.response import initialize_tracker
from main.interface.helpers import pool_string_to_loc


def graphics_from_responses(response_tracker, user_data, target):
    """Generate graphics according to given responses."""
    graphics_pool = pool_string_to_loc(target)

    def get_single_graphic(graphics_pool, function_name, function_input):
        """."""
        if isinstance(graphics_pool, str):
            graphics_pool = pool_string_to_loc(graphics_pool)
        return getattr(graphics_pool, (function_name))(*function_input)

    def graphics_by_function(response):
        graphics_by_function = {}
        for function_name in response['functions']:
            graphics_by_function[function_name] = get_single_graphic(
                graphics_pool, function_name, (response, user_data))
        return graphics_by_function

    graphics_by_groupkey = {}
    for groupkey, response in response_tracker.items():
        graphics_by_groupkey[groupkey] = graphics_by_function(response)
    return graphics_by_groupkey


def single_variable(user_data):
    """."""
    print("\n\n")
    print("Choose Single Variable Graphics")
    # INPUTS
    response_tracker = initialize_tracker(user_data, 'singlevariable')
    # GRAPHICS
    graphic_buffer_objects = graphics_from_responses(
        response_tracker, user_data, 'singlevariable')
    # UPDATES
    user_data['response_trackers']['singlevariable'] = response_tracker
    user_data['singlevariable_graphic_objects'] = graphic_buffer_objects
    return user_data


def request_univariate(user_data):
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


def request_bivariate(user_data):
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


def request_multivariate(user_data):
    """."""
    print("\n\n")
    print("Choose Multivariate Graphics")
    # INPUTS
    response_tracker = initialize_tracker(
        user_data, 'multivariate')
    # GRAPHICS
    graphic_buffer_objects = graphics_from_responses(
        response_tracker, user_data, 'multivariate')
    # UPDATES
    user_data['response_trackers']['multivariate'] = response_tracker
    user_data['multivariate_graphic_objects'] = graphic_buffer_objects
    return user_data
