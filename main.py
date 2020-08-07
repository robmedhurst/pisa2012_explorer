"""
PISA2012_EXPLORER.

This project aims to develop tools to assist with the wrangling and
exploration of the PISA 2012 dataset. Specifically, groups of similar
variables are explored concurrently.
"""

import zipfile
import pickle

import pandas as pd

from wrangle import wrangle as wrangler
import post_wrangling
import category_definitions
import test_groupings
import univariate_graphics_pool
import user_interaction as ui


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
    def confirm_pisa_df(df_through):
        """
        Placehold function.

        Will implement hash check on the csv and/or zip files.
        """
        if integrity_check:
            print("Checking file integrity(this may take a few minutes)...\n")
            # TODO: implement integrity check
            #
            # do the check here
            #
            #
            #
            #
            #
            passed = True    # result of check
            # return if test passed, raise error if failed
            if passed:
                print("Dataframe passed integrity check.\n")
                return df_through
            raise FileExistsError("Datafrane failed integrity check!")
        return df_through

    if 'PISA2012' not in globals():
        print("PISA2012 original not in locals, attempting to load",
              "(this may take a few minutes)...\n")
    elif reload:
        print("PISA2012 original exists, attempting to reload",
              "(this may take a few minutes)...\n")
    else:
        print("Variable with name PISA2012 already in memory.\n")
        return confirm_pisa_df(PISA2012)

    # load, check, raise error if needed
    if ('PISA2012' not in globals()) or (reload):
        # global PISA2012
        try:    # loading directly from csv
            pisa_df = pd.read_csv(
                'pisa2012.csv', sep=',', encoding='latin-1',
                error_bad_lines=False, dtype='unicode', index_col=False)
            print("Loaded from csv.\n")
            return confirm_pisa_df(pisa_df)
        except FileNotFoundError:
            try:    # loading directly from zip
                pisa_df = pd.read_csv(
                    zipfile.ZipFile(
                        'pisa2012.csv.zip', 'r').open('pisa2012.csv'),
                    sep=',', encoding='latin-1', error_bad_lines=False,
                    dtype='unicode', index_col=False)
                print("Loaded from zip.\n")
                return confirm_pisa_df(pisa_df)
            except FileNotFoundError:    # loading failed
                raise FileNotFoundError("pisa2012 not in local directory.")


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


def post_wrangle(pisa_df, inputs, group_category_matches):
    """Apply category specific post wrangle functions."""
    # group_category_matches holds indep and dependent groups seperately
    for subset in group_category_matches:
        # iterate group category matches
        for group_name in group_category_matches[subset]:
            category = group_category_matches[subset][group_name]

            # check if associated post wrangling group actions are available
            if category + "_group_post_wrangle" in dir(post_wrangling):
                # function call using getattr
                getattr(
                    post_wrangling,
                    (category + "_group_post_wrangle"))(
                        group_name, pisa_df, inputs)
    return pisa_df, inputs, group_category_matches


# def univariate_graphics(pisa_df, inputs, group_category_matches):
#     """
#     Call category specific graphics functions.

#     undesired_graphics, is a list of strings to ignore when searching for
#     graphics functions.
#     """
#     (independent_groups, dependent_groups) = inputs[2:]

#     def get_vars(group_name):
#         """Get list of variable names for group of vars, group_name."""
#         v_list = []
#         if group_name in independent_groups:
#             v_list = independent_groups[group_name]
#         elif group_name in dependent_groups:
#             v_list = dependent_groups[group_name]
#         return v_list

#     def get_univariate_graphic():
#         print("calling:  ", function_name)
#         return getattr(
#             univariate_graphics_pool,
#             (function_name))(
#                 group_specific_parameters, pisa_df, inputs)

#     graphic_objects = []
#     # iterate group category matches
#     for subset in group_category_matches:
#         print("\n\n", list(group_category_matches[subset]))
#         for group_name in group_category_matches[subset]:

#             # group specific parameters:
#             category = group_category_matches[subset][group_name]
#             group_specific_parameters = (
#                 group_name, get_vars(group_name), category)
#             print("\n", group_name, " -  ", category)
#             # univariate_graphics_pool contains univariate graphics functions
#             for function_name in dir(univariate_graphics_pool)[8:]:

#                 if category in function_name:
#                     graphic_objects.append(get_univariate_graphic())

#                 if category in inputs[0] and "categorical" in function_name:
#                     graphic_objects.append(get_univariate_graphic())

#             if category in inputs[0] and len(inputs[0][category]) == 2:
#                 function_name = "binary_counts_singleplot"
#                 group_specific_parameters = (
#                     group_name, get_vars(group_name), category)
#                 graphic_objects.append(get_univariate_graphic())

#             if category == "float" and len(get_vars(group_name)) > 1:
#                 function_name = "float_means_singleplot"
#                 group_specific_parameters = (
#                     group_name, [group_name + "_mean"], category)
#                 graphic_objects.append(get_univariate_graphic())

#     return pisa_df, inputs, group_category_matches, graphic_objects


def get_function_by_key(name_key, local_py_file):
    """Return function names from local_py_file.py that contain name_key."""
    matching_functions = []
    for function_name in dir(local_py_file)[8:]:
        if name_key in function_name:
            matching_functions.append(function_name)
    return matching_functions


def initialize(pisa_sample=None, preset=None):
    """Wrap function calls."""
    # returns pisa_df, inputs, categories_found, and graphics_objects
    return (
        user_request_univariate_graphics(
            *post_wrangle(
                *wrangler(
                    *user_initialize(pisa_sample, preset)))))


def user_initialize(pisa_sample=None, preset=None):
    """User inputs to initialize."""
    init_q1 = {'q': {'preface': "Perform integrity check on original csv?"}}
    init_q2 = {'q': {'preface': "Do you want to resample?"}}
    init_q3 = {'q': {
        'preface': "Which sample size should we start with?",
        'question_type': "single",
        'selection_options': [
            "500",
            "5000",
            "50000"]}}
    init_q4 = {'q': {'question_type': "integer", 'max_min_vals': (1, 5)}}
    init_q5 = {'q': {'question_type': "string", 'max_min_vals': (1, 20)}}
    inputs = [
        category_definitions.KNOWN_CATEGORIES,
        category_definitions.PREFERRED_NAMING]

    # ====================================================================
    # User bypass user_initialize interactions with 'preset'
    # ====================================================================
    # ====================================================================
    # ex:
    #     preset1 = {
    #         'initialize': {
    #             'indep_sets': test_groupings.INDEP_TEST_GROUPING01,
    #             'dep_sets': test_groupings.DEPEN_TEST_GROUPING01,
    #             'sample': 1000  # or subset of pisa}}
    # ====================================================================
    def do_preset():
        try:
            sample = preset['initialize']['sample']
            pisa2012 = load_original()
            inputs.append(preset['initialize']['indep_sets'])
            inputs.append(preset['initialize']['dep_sets'])
            if isinstance(sample, int):
                pisa_sample = pisa2012.sample(sample)
            elif isinstance(sample, pd.DataFrame):
                pisa_sample = sample
            return pisa_sample, inputs  # , preset    may want to pass along
        except KeyError:
            return "KeyError on user initialization 'preset'"
    if preset is not None:
        return do_preset()

    # ====================================================================
    #     User integrity check
    # ====================================================================
    if ui.user_batch_questioning(init_q1)['q']['response'] == 'yes':
        pisa2012 = load_original(integrity_check=True)
    else:
        pisa2012 = load_original()

    # ====================================================================
    #     User option to use quick preset var groups (demo)
    # ====================================================================
    # TODO: offer initialize preset

    # ====================================================================
    #     User sample/resample
    # ====================================================================
    if pisa_sample is None:
        pisa_sample = pisa2012.sample(
            int(ui.user_batch_questioning(init_q3)['q']['response']))
    elif ui.user_batch_questioning(init_q2)['q']['response'] == 'yes':
        pisa_sample = pisa2012.sample(
            int(ui.user_batch_questioning(init_q3)['q']['response']))

    # ====================================================================
    #     User manual input group information
    # ====================================================================
    def user_input_group(group_size=None, group_name=None):
        group = []
        if not group_name:
            print("What would you like to name this group?")
            # user input group_name
            group_name = ui.user_batch_questioning(init_q5)['q']['response']
        if not group_size:
            print("How many variables will this group contain?")
            # user input group_size
            group_size = ui.user_batch_questioning(init_q4)['q']['response']
        for new_entry in range(group_size):
            print("Enter a pisa variable (column name):")
            group.append(
                ui.input_pisa_var_name(list(PISA2012.columns)))
        return group, group_name

    print("\nInput a group of dependent variables (numeric).")
    current_input = user_input_group()
    inputs.append({current_input[1]: current_input[0]})
    print("Now input the groups of independent variables.")
    independent_groups = {}
    print("How many groups of independent variables?")
    num_groups = ui.user_batch_questioning(init_q4)['q']['response']
    print("Groups each need a name and list of variables.")
    for x in range(num_groups):
        current_input = user_input_group()
        independent_groups[current_input[1]] = current_input[0]
    inputs.insert(2, independent_groups)

    return pisa_sample, inputs


def user_request_univariate_graphics(pisa_df, inputs, group_category_matches):
    """User select plots."""
    graphic_objects = []
    print("\n\nUnivariate Graphics\n\n")

    def get_univariate_graphic(function_name, group_info):
        return getattr(
            univariate_graphics_pool,
            (function_name))(group_info, pisa_df, inputs)

    # # ====================================================================
    # # Selected dependent group
    # # ====================================================================
    # for dep_gp_name in group_category_matches['depen_categories']:
    #     dep_gp_vars = inputs[3][dep_gp_name]
    #     dep_gp_kcat = (
    #         group_category_matches['depen_categories'][dep_gp_name])
    #     break
    # print("Using first dependent group, ", dep_gp_name)

    # ====================================================================
    # Selected independent group
    # ====================================================================
    selected_indep_groups = []
    # TODO: Plot all independent variable groups?
    #     if yes: use all
    selected_indep_groups = inputs[2].keys()  # all
    # TODO: else: user_select_mult from list of independent group

    # Iterate independent groups
    for ind_gp_name in selected_indep_groups:
        group_info = [
            ind_gp_name,
            inputs[2][ind_gp_name],
            group_category_matches['indep_categories'][ind_gp_name]
            ]
    # fetch functions by category
        avail_plots = get_function_by_key(
            group_info[2], univariate_graphics_pool)

    # TODO: Plot all possible univariate plots for this variable?
        plots_decided = []
    #   if yes, do all, if not:
        plots_decided = avail_plots
    # TODO: user_select_mult
        for function_name in plots_decided:
            new_graphic = get_univariate_graphic(function_name, group_info)
            graphic_objects.append(new_graphic)

# get_function_by_key(name_key, univariate_graphics_pool)
# get_univariate_graphic(function_name, group_info)

# roup_name, get_vars(group_name), category

#     for ind_gp_name in group_category_matches['indep_categories']:
#         ind_gp_vars = inputs[2][ind_gp_name]
#         ind_gp_kcat = (
#             group_category_matches['indep_categories'][ind_gp_name])

# Plot all independent variable groups?
#     if not: user_select_mult from list of independent groups:
# For independent group in selected groups:
#     determine which from graphics_pool apply to category(if any)
#     user_select_mult from list of appropriate_graphics

    return pisa_df, inputs, group_category_matches, graphic_objects


def show_all_output():
    """Display results."""
    for i in OUTPUT[3]:
        i.seek(0)
        pickle.load(i)

# %%


if __name__ == '__main__':
    PISA2012 = load_original()

    preset1 = {
        'initialize': {
            'indep_sets': test_groupings.INDEP_TEST_GROUPING01,
            'dep_sets': test_groupings.DEPEN_TEST_GROUPING01,
            'sample': 1000}}

    OUTPUT = initialize(preset=preset1)

    show_all_output()

# ===========================================================================
#     input = [
#         category_definitions.KNOWN_CATEGORIES,
#         category_definitions.PREFERRED_NAMING,
#         test_groupings.INDEP_TEST_GROUPING01,
#         test_groupings.DEPEN_TEST_GROUPING01]
# ===========================================================================

# ===========================================================================
#     preset1 = {
#         'initialize': {
#             'indep_sets': test_groupings.INDEP_TEST_GROUPING01,
#             'dep_sets': test_groupings.DEPEN_TEST_GROUPING01,
#             'sample': 1000  # or subset of pisa}}
# ===========================================================================

# ===========================================================================
#     preset1 = {
#         'initialize': {
#             'indep_sets': {
#                 'family_home': ['ST11Q01', 'ST11Q02', 'ST11Q03', 'ST11Q04',
#                                 'ST11Q05'],
#                 'parent_work': ['ST15Q01', 'ST19Q01'],
#                 'parent_isei': ['BFMJ2', 'BMMJ1', 'HISEI'],
#                 'HOMEPOS': ['HOMEPOS'],
#                 'person_item': ['ST26Q02', 'ST26Q03', 'ST26Q08', 'ST26Q09',
#                                 'ST26Q10', 'ST26Q11']},
#             'dep_sets': {
#                 'math_result': ['PV1MATH', 'PV2MATH', 'PV3MATH', 'PV4MATH',
#                                 'PV5MATH'],
#                 'read_result': ['PV1READ', 'PV2READ', 'PV3READ', 'PV4READ',
#                                 'PV5READ']},
#             'sample': 1000  # or subset of pisa
#             }
#         }
# ===========================================================================
