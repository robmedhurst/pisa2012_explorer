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

import main_user_input as ui
import main_definitions as definitions
import graphics_pool_singlevar as singlevar_graphics_pool
import graphics_pool_univariate as univariate_graphics_pool


# Dataset can take a few minutes to load on some systems.
# Load once and only work on copy.
# Try to laod from csv then from zip.
def load_original(reload=False, integrity_check=False):
    """
    Load original pisa2012 dataset from file and return it as an DataFrame.

    Does not load if already in memory.
    Forces reload on parameter 'reload=True'.
    Checks datastructure if parameter 'integrety_check=True'.
    """
    if 'PISA2012' not in globals():
        print("PISA2012 original not in locals, attempting to load",
              "(this may take a few minutes)...\n")
    elif reload:
        print("PISA2012 original exists, attempting to reload",
              "(this may take a few minutes)...\n")
    else:
        print("Variable with name PISA2012 already in memory.\n")

    # load, check, raise error if needed
    if ('PISA2012' not in globals()) or (reload):
        # global PISA2012
        try:    # loading directly from csv
            pisa_df = pd.read_csv(
                'pisa2012.csv', sep=',', encoding='latin-1',
                error_bad_lines=False, dtype='unicode', index_col=False)
            print("Loaded from csv.\n")
            return confirm_pisa_df(pisa_df, integrity_check)
        except FileNotFoundError:
            try:    # loading directly from zip
                pisa_df = pd.read_csv(
                    zipfile.ZipFile(
                        'pisa2012.csv.zip', 'r').open('pisa2012.csv'),
                    sep=',', encoding='latin-1', error_bad_lines=False,
                    dtype='unicode', index_col=False)
                print("Loaded from zip.\n")
                return confirm_pisa_df(pisa_df, integrity_check)
            except FileNotFoundError:    # loading failed
                raise FileNotFoundError("pisa2012 not in local directory.")
    pisa_df = PISA2012.copy()
    return confirm_pisa_df(pisa_df, integrity_check)


def confirm_pisa_df(df_through, integrity_check):
    """Verify pisa csv and/or zip files."""
    if integrity_check:
        print("Checking file integrity(this may take a few minutes)...\n")
        # TODO: implement integrity check
        #
        # do the check here
        #
        #
        passed = True    # result of check
        # return if test passed, raise error if failed
        if passed:
            print("Dataframe passed integrity check.\n")
            return df_through
        raise FileExistsError("Datafrane failed integrity check!")
    return df_through


def get_longnames(names):
    """
    Return PISA 2012 long names given short names.

    Return list of PISA variable descriptions corresponding to variable
    shortnames given by list name.
    Resource is read from local copy of pisadict2012.csv
    """
    pisadict2012 = pd.read_csv(
        'pisadict2012.csv',
        sep=',', encoding='latin-1', error_bad_lines=False,
        dtype='unicode', index_col=False).rename(
            columns={'Unnamed: 0': 'varname', 'x': 'description'})
    names = list(names)
    return list(pisadict2012.query("varname in @names")['description'])


def get_function_by_key(name_key, local_py_file, key_location=None):
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
    def graphics_by_function(response):
        graphics_by_function = {}
        for function_name in response['functions']:
            graphics_by_function[function_name] = getattr(
                univariate_graphics_pool, (function_name))(
                    response, user_data)
        return graphics_by_function
    graphics_by_groupkey = {}
    for groupkey, response in response_tracker.items():
        graphics_by_groupkey[groupkey] = graphics_by_function(response)
    return graphics_by_groupkey


def get_next_unused_name(user_data, location, name, appendage="_old_"):
    """."""
    working_dictionary = user_data.copy()
    # navigate location specified
    for depth in range(len(location)):
        working_dictionary = working_dictionary[location[depth]]
    # find smallest integer such that new_name doesnt yet exist
    back_up_num = 0
    while name + appendage + str(back_up_num) in working_dictionary.keys():
        back_up_num += 1
    return name + appendage + str(back_up_num)


def initialize(user_data=None):
    """Wrap function calls."""
    # returns pisa_df, inputs, categories_found, and graphics_objects
    return (
        user_request_univariate_graphics(
            user_single_variable_graphics(
                post_wrangle(
                    wrangle(
                        user_initialize(user_data))))))


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


# =============================================================================
# %% user interaction
# =============================================================================

# %%% user_initialize

def user_initialize(user_data=None):
    """
    User inputs to initialize.

    Question user to build sample data and groups of interest.

    Returns pisa_sample, inputs
    """
    def user_input_group(group_size=None, group_name=None):
        """Return user defined group of pisa variables."""
        group = []
        if not group_name:
            print("\n")
            print("Enter short name for this group...")
            # user input group name
            group_name = ui.input_simple_string(1, 20)
        if not group_size:
            print("\n")
            print("How many variables will this group contain?")
            # user input group size
            group_size = ui.input_integer(1, 5)
        while len(group) < group_size:
            # user input variable names
            print("\n")
            group.append(
                ui.input_pisa_var_name(list(PISA2012.columns)))
        return group, group_name

    def do_preset(user_data_in):
        try:
            sample_in = user_data_in['pisa_sample']
            if isinstance(sample_in, int):
                user_data_in['sample_size'] = sample_in
                user_data_in['pisa_sample'] = pisa2012.sample(sample_in)

        except KeyError:
            return "KeyError on user initialization 'preset'"
        print("Skipped input, loaded selection from parameter.\n")
        return user_data_in

    # ====================================================================
    # Bypass user initialize interactions via 'preset'
    # ====================================================================
    pisa2012 = load_original()
    if user_data is not None:
        return do_preset(user_data)

    # ====================================================================
    # User option to use quick preset var groups (demo)
    # ====================================================================
    print("\n")
    print("Use preset? ('no' to choose sample size and groups)")
    if ui.single_response_from_list(['yes', 'no']) == 'yes':
        print("Using preset...")
        return do_preset(definitions.PRESET1)

    # ====================================================================
    # User sample/resample
    # ====================================================================
    question = {'q': {
        'preface': "Select a sample size.",
        'selection_options': [
            "500",
            "5000",
            "50000",
            "Other value"
            ]}}
    if user_data is None:
        user_data = {}
        current_input = ui.user_batch_questioning(question)['q']['response']
        if current_input == "Other value":
            current_input = ui.input_integer(50, None)
        user_data['pisa_sample'] = pisa2012.sample(int(current_input))
        user_data['sample_size'] = int(current_input)
    # ====================================================================
    # User input group information
    # ====================================================================

    # dependend variables
    print("\n")
    print("Dependent Variable Input")
    print("Input a group of dependent variables (numeric).")
    current_input = user_input_group()
    dependent_groups = {current_input[1]: current_input[0]}
    user_data['dependent_groups'] = dependent_groups

    # independent variables
    print("\n")
    print("Independent Variable Input")
    print("Input groups of independent variables.")
    # print("\n")
    print("How many groups of independent variables?")
    num_groups = ui.input_integer(1, 5)
    print("\n")
    print("Groups each need a name and list of variables.")
    independent_groups = {}
    for index in range(num_groups):
        print("Describe group number", index+1, "of", num_groups)
        current_input = user_input_group()
        independent_groups[current_input[1]] = current_input[0]
        print("Group entered.")
    user_data['independent_groups'] = independent_groups

    return user_data


# %%% user_request_singlevar_graphics
def user_single_variable_graphics(user_data):
    """User select plots."""
    # ========================================================================
    #
    known_categories = definitions.KNOWN_CATEGORIES
    group_category_matches = user_data['group_category_matches']

    # private=================================================================
    #
    def user_select_groups(list_of_groups):
        """User choose any number from list of groups."""
        if len(list_of_groups) > 1:
            print("\n")
            print("Which groups to use...")
            print("Use all groups?")
            if ui.single_response_from_list(['yes', 'no']) == 'yes':
                return list_of_groups
            print("Which groups to use...")
            return ui.multi_responses_from_list(list_of_groups)
        return list_of_groups

    def get_singlevar_group_functions(group_info):
        # get functions matching category key from univatiate pool
        list_of_functions = get_function_by_key(
                    group_info['category'], singlevar_graphics_pool)
        # Detect BINARY
        if group_info['category'] in known_categories and len(
                known_categories[group_info['category']]) == 2:
            # get binary functions
            list_of_functions.extend(
                get_function_by_key('binary', singlevar_graphics_pool))
        # Detect CATEGORICAL
        if group_info['category'] in known_categories:
            # get binary functions
            list_of_functions.extend(
                get_function_by_key('cat', singlevar_graphics_pool))
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
            if ui.single_response_from_list(['yes', 'no']) == 'no':
                return []
        elif len(list_of_functions) > 1:
            print("\n")
            print("Use all functions for group", group_info['name'], "?")
            if ui.single_response_from_list(['yes', 'no']) == 'no':
                print("\n")
                print("Which functions to use for group",
                      group_info['name'], "?")
                return ui.multi_responses_from_list(list_of_functions)
        return list_of_functions

    def get_singlevar_graphic(function_name, group_info):
        return getattr(
            singlevar_graphics_pool,
            (function_name))(group_info, user_data)

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

    def init_response_tracker(bypass_type='all'):
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
        return ui.single_response_from_list([
            "Yes, with all plots.",
            "Yes, with no plots.",
            "No, manually select groups to explore."
            ])

    print("\n\n")
    print("Choose Single Variable Graphics")
    try:
        response_tracker = user_data['response_trackers']['singlevar']
    except KeyError:
        response_tracker = False
    #
    # response_tracker old
    if response_tracker is not False:
        print("Existing responses found, reuse them?")
        if ui.single_response_from_list(["yes", "no"]) == 'no':
            # move the old tracker
            user_data['response_trackers'][
                get_next_unused_name(
                    user_data,
                    ['response_trackers'], 'singlevar'
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
    user_data['response_trackers']['singlevar'] = response_tracker
    user_data['singlevar_graphic_objects'] = singlevar_graphic_objects
    return user_data


# %%% user_request_univariate_graphics
def user_request_univariate_graphics(user_data):
    """."""
    known_categories = definitions.KNOWN_CATEGORIES

    def create_response():
        # loop for user correct input error
        while True:
            print("Select a dependent group.")
            dependent_group = ui.select_group(
                user_data, 'dependent_groups')
            print("Select an independent group.")
            independent_group = ui.select_group(
                user_data, 'independent_groups')
            user_selected_functions = ui.multi_responses_from_list(
                get_functions_by_group(
                    [independent_group], univariate_graphics_pool))
            user_responses = {
                'independent_group': independent_group,
                'dependent_group': dependent_group,
                'functions': user_selected_functions}
            # User Confirm Selection
            print(user_responses)
            print("Is this selection correct?")
            if ui.single_response_from_list([
                    'Yes, continue.',
                    'No, lets try again.']) == 'Yes, continue.':
                return user_responses

    def create_multiple_responses(response_tracker={}):
        # loop for multiple selections
        while True:
            # create new tracker and key
            response = create_response()
            group_selection_key = (
                response['dependent_group']['name'] + "_vs_" +
                response['independent_group']['name'])
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
            if ui.single_response_from_list([
                        'Yes, enter another.', 'No, done for now.']
                    ) == 'No, done for now.':
                return response_tracker

    def user_select_bypass(existing_trackers):
        def save_old_trackers():
            tracker_name = get_next_unused_name(
                user_data, ['response_trackers'], 'univariate')
            user_data['response_trackers'][tracker_name] = existing_trackers
        # ask user what to do
        print("Previous selections found.")
        current_response = ui.single_response_from_list([
            "Reuse selection", "Create new selection", "Add to selection"])
        if current_response == "Reuse selection":
            # No need to get more trackers or save the old ones
            return existing_trackers
        elif current_response == "Create new selection":
            new_trackers = create_multiple_responses()
            if existing_trackers != new_trackers:
                save_old_trackers()
            return new_trackers
        elif current_response == "Add to selection":
            new_trackers = create_multiple_responses(existing_trackers.copy())
            if existing_trackers != new_trackers:
                save_old_trackers()
            return new_trackers

    def initialize_tracker():
        # check for existing tracker
        try:
            existing_tracker = user_data[
                'response_trackers']['univariate']
        except KeyError:
            existing_tracker = False
        # user interactions
        if existing_tracker is False:
            return create_multiple_responses()
        else:
            # user choose how to use existing tracker
            return user_select_bypass(existing_tracker)

    print("\n\n")
    print("Choose Univariate Graphics")
    # INPUTS
    response_tracker = initialize_tracker()
    # GRAPHICS
    graphic_buffer_objects = graphics_from_responses(
        response_tracker, user_data, univariate_graphics_pool)
    # UPDATES
    user_data['response_trackers']['univariate'] = response_tracker
    user_data['univariate_graphic_objects'] = graphic_buffer_objects
    return user_data


# %%% user_request_bivariate_graphics
def user_request_bivariate_graphics(user_data):
    """."""
    known_categories = definitions.KNOWN_CATEGORIES

    pass



# %% Main


def show_all_output(result):
    """Display results."""
    def rip_lane_subland(lane, sub_lane):
        for group_name in result[lane][sub_lane]:
            for graphic in result[lane][sub_lane][group_name].values():
                graphic.seek(0)
                pickle.load(graphic)

    def rip_lane(lane):
        for group_name in result[lane]:
            for graphic in result[lane][group_name].values():
                graphic.seek(0)
                pickle.load(graphic)

    rip_lane_subland('singlevar_graphic_objects', 'dependent_groups')
    rip_lane_subland('singlevar_graphic_objects', 'independent_groups')
    rip_lane('univariate_graphic_objects')


if __name__ == '__main__':
    # load a global copy to avoid reloading
    PISA2012 = load_original()

    # OUTPUT = initialize(definitions.PRESET1)
    OUTPUT = initialize()

    show_all_output(OUTPUT)
