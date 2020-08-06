"""
### Groups of Indepenent Variables
#
# Dictionary containing lists. Each list is a group of variable names.
# The variables in a group must be of same type (float, yn, category X).
#
### Groups of Depenent Variables
#
# Dictionary containing list. Lists are groups of variable names.
# The variables must be numeric.
#
"""


# test_grouping01
# intial test set, no real meaning oustide of the study it emerged from
INDEP_TEST_GROUPING01 = {
    'family_home': ['ST11Q01', 'ST11Q02', 'ST11Q03', 'ST11Q04', 'ST11Q05'],
    'parent_work': ['ST15Q01', 'ST19Q01'],
    'parent_isei': ['BFMJ2', 'BMMJ1', 'HISEI'],
    'HOMEPOS': ['HOMEPOS'],
    'person_item': ['ST26Q02', 'ST26Q03', 'ST26Q08',
                    'ST26Q09', 'ST26Q10', 'ST26Q11']}
DEPEN_TEST_GROUPING01 = {
    'math_result': ['PV1MATH', 'PV2MATH', 'PV3MATH', 'PV4MATH', 'PV5MATH'],
    'read_result': ['PV1READ', 'PV2READ', 'PV3READ', 'PV4READ', 'PV5READ']}


# test_grouping02
# intended to cover a few unresolved response types
INDEP_TEST_GROUPING02 = {
    'grpname1': ['ST05Q01'],
    'grpname2': ['ST44Q07'],
    'grpname3': ['ST28Q01'],
    'grpname4': ['ST37Q02']}
DEPEN_TEST_GROUPING02 = {
    'grpname1': [],
    'grpname2': []}


# test_grouping99
# empty test set
INDEP_TEST_GROUPING99 = {
    'grpname1': [],
    'grpname2': [],
    'grpname3': [],
    'grpname4': [],
    'grpname5': []}
DEPEN_TEST_GROUPING99 = {
    'grpname1': [],
    'grpname2': []}


PLACEHOLDER_QUESTIONS = {
    'question1': {
        'question_type': "single",
        'not_selectable': [1],
        'selection_options': [
            'blue',
            'red',
            'green']
        },
    'question2': {
        'preface': 'What are your favorite colors? ',
        'question_type': "multi",
        'not_selectable': [],
        'max_selectable': 2,
        'selection_options': [
            'blue',
            'red',
            'green']
        }
    }

# =============================================================================
# Unused helper functions, will delete later
# =============================================================================
# # --------------------------------------------------------------------------
# # TEMPORARY (build know_categories)
# # A helper function to view a list of categories extracted from PISA2012
# # Can be used to create new category_definitons.
# def get_all_unique_short_categories(pisadf, max_length=5,
#                                     column_start=None, column_end=None):
#     """
#     Pull sets of unique values from PISA2012 dataset for building
#     collection of known categories.
#     """
#     found_unique_sets = []
#     for var in pisadf.columns[column_start:column_end]:

#         # get unique_values, without nulls
#         unique_values = set({})
#         for unique_val in set(pisadf[var].unique()):
#             if not pd.isnull(unique_val):
#                 unique_values.add(unique_val.strip())

#         # check if already found, check length
#         if (unique_values not in found_unique_sets
#             ) and (1 < len(unique_values) < max_length):
#             # check for subsets
#             for past_match in found_unique_sets:
#                 # skip if subset of existing set
#                 if set(unique_values).issubset(past_match):
#                     unique_values = False
#                     break
#                 # remove existing set if superset of existing set
#                 if set(past_match).issubset(unique_values):
#                     found_unique_sets.remove(past_match)
#             if unique_values:
#                 found_unique_sets.append(unique_values)
#     return found_unique_sets

# # A helper function to check each column against known categories
# def completeness_check(df, specific_vars: list):
#     """
#     A helper function to check each column against known categories
#     """
#     pisadf = df.copy()
#     dataframe_returned = pd.DataFrame()

#     for i, var in enumerate(specific_vars):
#         del pisadf
#         pisadf = df.copy()

#         print("var numer: ", str(i))
#         print(pisadf.shape)

#         indep_categories = initialize(
#             pisadf,
#             [category_definitions.KNOWN_CATEGORIES,
#               category_definitions.PREFERRED_NAMING,
#               {var: [var]},
#               {}])[2]['indep_categories']

#         print(PISA2012.shape)
#         print(pisadf.shape, "\n")

#         tempdf = pd.DataFrame(
#             data={'category_name': list(indep_categories.values()),
#                   'example1': PISA2012.iloc[250000],
#                   'example2': PISA2012.iloc[120000],
#                   'example3': PISA2012.iloc[80000],
#                   'example4': PISA2012.iloc[40],
#                   'example5': PISA2012.iloc[400],
#                   'example6': PISA2012.iloc[4000],
#                   'example7': PISA2012.iloc[40000],
#                   'example8': PISA2012.iloc[400000]},
#             index=list(indep_categories.keys()))
#         dataframe_returned = dataframe_returned.append(tempdf)

#     for col in dataframe_returned.columns[1:]:
#         for row, value in enumerate(dataframe_returned[col]):
#             if type(value) != float:
#                dataframe_returned[col][
#                    dataframe_returned.index[row]] = value.strip()

#     return dataframe_returned

# # # sets of unique vals pulled from original df
# if 'SHORT_UNIQUES' not in globals():
#     SHORT_UNIQUES = get_all_unique_short_categories(PISA2012, 80)
#     SHORT_UNIQUES_DF = pd.DataFrame(SHORT_UNIQUES)

# ## Dont rerun this, it takes forever
# # returned category for each var in original df
# COMPLETENESS_CHECK = completeness_check(PISA2012, PISA2012.columns)

# # Saving to csv
# COMPLETENESS_CHECK.to_csv('completeness_check.csv')

# # Loading from csv
# COMPLETENESS_CHECK = pd.read_csv(
#     "completeness_check.csv",header=0, index_col=0)

# # when complete, only variables associated with text_response should
# #     be those with too many unique values to justify a category
# TEXT_RESPONSES = COMPLETENESS_CHECK.query('category_name == "text_response"')

# # %%% LIST EXAMPLES

# # this can be used to get the sets from SHORT UNIQUES
# # corresponding to the examples of string reponses given
# def unique_sets_finder(df):
#     """
#     Print the sets from SHORT UNIQUES corresponding to the list of example
#     string reponses given.
#     """
#     repeat_tracker = {}
#     unmatched = {}
#     def match_uniques_sets(string_to_find, repeat_tracker):

#         string_name = (string_to_find[:15]) if len(
#             string_to_find) > 15 else string_to_find
#         string_name = string_name.strip(" ")
#         string_name = string_name.replace(" ", "_")

#         if len(list(
#                 SHORT_UNIQUES_DF[SHORT_UNIQUES_DF == string_to_find].dropna(
#                     thresh=1).index)) == 0:
#             unmatched[var] = string_to_find

#         for i in list(
#                 SHORT_UNIQUES_DF[SHORT_UNIQUES_DF == string_to_find].dropna(
#                     thresh=1).index):
#             new_set = set(SHORT_UNIQUES[i])
#             if new_set not in repeat_tracker.values():
#                 repeat_tracker[var] = new_set

#     for var in df.index:
#         examples = df.loc[var]
#         examples.dropna(inplace=True)
#         string_to_find = examples[1]
#         match_uniques_sets(string_to_find, repeat_tracker)

#     print("\n\nmatched text_responses:")
#     for a in repeat_tracker:
#         if len(list(repeat_tracker[a])) < 50:
#             print("\n")
#             line1 = ("'" + a + "':").strip(" ")
#             line1 = line1 + " ["
#             print(line1)
#             sorte = list(repeat_tracker[a])
#             sorte.sort()
#             for index, item in enumerate(sorte):
#                 if index < len(list(repeat_tracker[a]))-1:
#                     line2 = ("    '" + item + "',")
#                     print(line2)
#                 else:
#                     line2 = ("    '" + item + "'],")
#                     print(line2)
#         else:
#             print("Unique Longer than 20")
#     print(
#         pd.DataFrame(data={'ex': list(repeat_tracker.values())},
#                       index=(repeat_tracker.keys())))

#     print("\n\nunmatched text_responses:")
#     print(
#         pd.DataFrame(
#             data={'ex': list(unmatched.values()),
#                   'num_unique': PISA2012[list(unmatched.keys())].nunique()},
#             index=(unmatched.keys())))

# # # output will be used to populate category definitions
# unique_sets_finder(TEXT_RESPONSES)
