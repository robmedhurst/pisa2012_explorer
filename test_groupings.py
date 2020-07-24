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


### test_grouping01
# intial test set, no real meaning oustide of the study it emerged from
INDEP_test_grouping01 = {
    'family_home': ['ST11Q01', 'ST11Q02', 'ST11Q03', 'ST11Q04', 'ST11Q05'],
    'parent_work': ['ST15Q01', 'ST19Q01'],
    'parent_isei': ['BFMJ2', 'BMMJ1', 'HISEI'],
    'HOMEPOS'    : ['HOMEPOS'],
    'person_item': ['ST26Q02', 'ST26Q03', 'ST26Q08',
                    'ST26Q09', 'ST26Q10', 'ST26Q11']}
DEPEN_test_grouping01 = {
    'math_result': ['PV1MATH', 'PV2MATH', 'PV3MATH', 'PV4MATH', 'PV5MATH'],
    'read_result': ['PV1READ', 'PV2READ', 'PV3READ', 'PV4READ', 'PV5READ']}


### test_grouping02
# intended to cover a few unresolved response types
INDEP_test_grouping02 = {
    'grpname1': ['ST05Q01'],
    'grpname2': ['ST44Q07'],
    'grpname3': ['ST28Q01'],
    'grpname4': ['ST37Q02']}
DEPEN_test_grouping02 = {
    'grpname1': [],
    'grpname2': []}


### test_grouping99
# empty test set
INDEP_test_grouping99 = {
    'grpname1': [],
    'grpname2': [],
    'grpname3': [],
    'grpname4': [],
    'grpname5': []}
DEPEN_test_grouping99 = {
    'grpname1': [],
    'grpname2': []}



# A helper function to view a list of categories extracted from PISA2012
# Can be used to create new category_definitons.
def get_all_unique_short_categories(pisadf, max_length=5,
                                    column_start=None, column_end=None):
    """
    Pull sets of unique values from PISA2012 dataset for building 
    collection of known categories.
    """
    import pandas as pd
    found_unique_sets = []
    for var in pisadf.columns[column_start:column_end]:

        # get unique_values, without nulls
        unique_values = set({})
        for unique_val in set(pisadf[var].unique()):
            if not pd.isnull(unique_val):
                unique_values.add(unique_val.strip())

        # check if already found, check length
        if (unique_values not in found_unique_sets) and (1 < len(unique_values) < max_length):
            # check for subsets
            for past_match in found_unique_sets:
                # skip if subset of existing set
                if set(unique_values).issubset(past_match):
                    unique_values = False
                    break
                # remove existing set if superset of existing set
                elif set(past_match).issubset(unique_values):
                    found_unique_sets.remove(past_match)
            if unique_values:
                found_unique_sets.append(unique_values)

    return found_unique_sets




# A helper function to check each column against known categories
def completeness_check(pisadf, column_start, column_end, interest_in=None):
    """
    A helper function to check each column against known categories
    """
    check = {}
    for var in pisadf.columns[column_start:column_end]:
        check[str(var)] = [str(var)]

    completeness = initialize(
        pisadf.sample(500),
        [category_definitions.KNOWN_CATEGORIES,
          category_definitions.PREFERRED_NAMING,
          check,
          test_groupings.DEPEN_test_grouping01]
        )[2]['indep_categories']

    if interest_in:
        for key in completeness:
            if completeness!= interest_in:
                print(key)

    return completeness
