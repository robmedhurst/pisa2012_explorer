"""
PISA2012_EXPLORER.

This project aims to develop tools to assist with the wrangling and
exploration of the PISA 2012 dataset. Specifically, groups of similar
variables are explored concurrently.
"""

import zipfile
import pickle

import pandas as pd

import main.category_actions as category_actions
import main.wrangle as wrangle
import ui.ui as ui


# test_grouping01
# intial test set, no real meaning oustide of the study it emerged from
PRESET1 = {
    'dependent_groups': {
        'math_result': [
            'PV1MATH', 'PV2MATH', 'PV3MATH', 'PV4MATH', 'PV5MATH'],
        'read_result': [
            'PV1READ', 'PV2READ', 'PV3READ', 'PV4READ', 'PV5READ']},
    'independent_groups': {
        'family_home': [
            'ST11Q01', 'ST11Q02', 'ST11Q03', 'ST11Q04', 'ST11Q05'],
        'parent_work': [
            'ST15Q01', 'ST19Q01'],
        'parent_isei': [
            'BFMJ2', 'BMMJ1', 'HISEI'],
        'HOMEPOS': [
            'HOMEPOS'],
        'person_item': [
            'ST26Q02', 'ST26Q03', 'ST26Q08', 'ST26Q09', 'ST26Q10', 'ST26Q11']},
    'pisa_sample': 1000}


# %% Support
def load_original_from_file():
    """."""
    def load_pisa_csv():
        return pd.read_csv(
            'pisa2012.csv',
            sep=',', encoding='latin-1', error_bad_lines=False,
            dtype='unicode', index_col=False)

    def load_pisa_zip():
        return pd.read_csv(
            zipfile.ZipFile(
                'pisa2012.csv.zip', 'r').open('pisa2012.csv'),
            sep=',', encoding='latin-1', error_bad_lines=False,
            dtype='unicode', index_col=False)

    for file_type, function_name in {
            'csv': 'load_pisa_csv', 'zip': 'load_pisa_zip'}.items():
        try:
            print("Reading pisa2012 from", file_type, "file.\n",
                  "This may take a few minutes...")

            pisa = locals()[function_name]()

            print("Finished loading from", file_type, "file.\n\n")
            return pisa
        except FileNotFoundError:
            print("Did not find", file_type, "file.")
    raise Exception('Could not load from local csv or zip file.')


def pickled_objects_from_file(filename):
    """."""
    extracted_objects = []
    with (open(filename, "rb")) as open_file:
        while True:
            try:
                extracted_objects .append(pickle.load(open_file))
            except EOFError:
                break
    return extracted_objects


# %% Process
def initialize(user_data=None, pisa2012=None):
    """Wrap function calls."""
    # returns pisa_df, inputs, categories_found, and graphics_objects
    return user_request_delivery(
        user_request_multivariate_graphics(
            user_request_bivariate_graphics(
                user_request_univariate_graphics(
                    user_single_variable_graphics(
                        post_wrangle(
                            wrangle.wrangle(
                                user_initialize(user_data, pisa2012))))))))


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
            if category + "_post_wrangle" in dir(category_actions):
                # function call using getattr
                getattr(
                    category_actions,
                    (category + "_post_wrangle"))(
                        group_name, user_data)
    # update and return user_data
    user_data['custom_dataframe'] = pisa_df
    return user_data


# %% User Interaction
# %%% user_initialize

def user_initialize(parameter_input, original_pisa2012):
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

    def do_build_user_data():

        def initialize_using_parameter():
            if parameter_input is not None:
                print("Loaded user selection from parameter.\n")
                return activate_preset(parameter_input)
            return initialize_using_preset()

        def initialize_using_preset():
            # TODO: Add preset selection:
            #         - few meaningful selections with descriptions
            #         - load presets from user specified file
            #
            print("Use preset? ('no' to manually enter groups)")
            if ui.single_response_from_list(['yes', 'no']) == 'yes':
                return activate_preset(PRESET1.copy())
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
        print("Original pisa2012 not preloaded.\n\n")
        pisa2012 = load_original_from_file()
    else:
        pisa2012 = original_pisa2012
        print("Origial pisa2012 loaded.\n\n")

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


# %%% user_request_multivariate_graphics
def user_request_multivariate_graphics(user_data):
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


# %%% user_request_delivery
def user_request_delivery(user_data):
    """."""
    # Helper functions
    #
    def rip_lanes(application):
        for key in user_data.keys():
            if 'graphic_objects' in key:
                for group in user_data[key].values():
                    for graphic in group.values():
                        if graphic is not None:
                            application(graphic)

    def save_pickle_next_location(selection, base_name):
        import os.path

        def get_next_save_location():
            save_num = 0
            while os.path.isfile(base_name + "_" + str(save_num).zfill(3)):
                save_num += 1
            return base_name + "_" + str(save_num).zfill(3)

        with open(get_next_save_location(), "wb") as open_file:
            pickle.dump(selection, open_file)

    # Delivery functions
    #
    def do_display_figures():
        def do_display_figure(graphic):
            graphic.seek(0)
            pickle.load(graphic)
            # graphic.show()
        rip_lanes(do_display_figure)

    # def do_store_pickles():
    #     def do_store_pickle(graphic):
    #         file_name = str(graphic)[-9:-1]
    #         with open(file_name, "wb") as open_file:
    #             open_file.write(graphic.getbuffer())
    #     rip_lanes(do_store_pickle)

    # def do_store_images():
    #     def do_store_image(graphic):
    #         graphic.seek(0)
    #         pickle.load(graphic).savefig(str(graphic)[-9:-1] + ".png")
    #     rip_lanes(do_store_image)

    # def do_display_images():
    #     # TODO: OS display
    #     from PIL import Image

    #     def do_display_image(graphic):
    #         file_name = str(graphic)[-9:-1] + ".png"
    #         graphic.seek(0)
    #         pickle.load(graphic).savefig(file_name)
    #         image = Image.open(file_name)
    #         image.show()
    #     rip_lanes(do_display_image)

    def do_big_pickle():
        selection = user_data
        save_pickle_next_location(selection, "saved_user_data")

    def do_little_pickle():
        desired_keys = [
            'dependent_groups',
            'group_category_matches',
            'independent_groups',
            'response_trackers']
        selection = {
            k: user_data[k] for k in user_data.keys() if k in desired_keys}
        save_pickle_next_location(selection, "saved_user_selections")

    # User selection options and corresponding functions
    #
    delivery_options = [
        'Display figures through backend',
        # 'Save all figures to file as BytesIO Objects',
        # 'Save all figures to file as images',
        # 'Display figures as images through OS.',
        'Pickle and save all user_data to a single file',
        'Pickle and save user selections to a single file'
        ]
    delivery_functions = [
        do_display_figures,
        # do_store_pickles,
        # do_store_images,
        # do_display_images,
        do_big_pickle,
        do_little_pickle
        ]

    # Action
    #
    print("\n-Delivery Options-")
    for user_request in ui.multi_responses_from_list(delivery_options):
        delivery_functions[delivery_options.index(user_request)]()

    return user_data


# %% Main

if __name__ == '__main__':
    # load a global copy to avoid reloading
    if 'PISA2012' not in globals():
        PISA2012 = load_original_from_file()
    if 'OUTPUT' not in globals():
        OUTPUT = initialize(pisa2012=PISA2012)
    else:
        OUTPUT = initialize(OUTPUT, PISA2012)