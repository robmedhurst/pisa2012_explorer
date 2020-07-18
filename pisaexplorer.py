# This tool aims to aid in the exploration of the PISA 2012 dataset,
# allowing users to concurrently examine a group of similar variables.


#%% Import Libraries

import zipfile

import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


#%% FUNCTIONS


def initialize(pisa_df, inputs):
    """
    general wrapper
    """
    wrangle(pisa_df, inputs)
    return pisa_df, inputs


#%%% Wrangling Functions

def wrangle(pisa_df, inputs):
    """
    wrangling wrapper
    """
    (known_categories, preferred_naming,
     independent_groups, dependent_groups) = inputs

    def select_columns_and_drop_nulls():
        """
        Remove columns from that are not in any given groups.
        Remove observations containing nulls.
        """
        # drop unused columns
        pisa_df.drop(pisa_df.columns.difference(
            [var_name for sublist in list(independent_groups.values())
             for var_name in sublist] +
            [var_name for sublist in list(dependent_groups.values())
             for var_name in sublist]),
            axis='columns', inplace = True)
        # drop nulls
        pisa_df.dropna(inplace=True)

    def get_category(pisa_group):
        """
        Determine if variables in pisa_group match a known categoy.
        Determine if variables in pisa_group each have same category.
        If consistent category found, return associated category_key.
        Otherwise returns "text_response", indicating group is 
        treated as plain text responses rather than categoricals.
        """
        # check each variable in group: all must be same category
        for index, variable_name in enumerate(pisa_group):
            # gather unique values for this variable
            unique_values = set({})
            for unique_val in set(pisa_df[variable_name].unique()):
                # trailing white spaces do occur in the dataset
                unique_values.add(unique_val.strip())

            # first variable for potential group category will suffice
            if index == 0:
                for known_cat in known_categories:
                    if unique_values.issubset(known_categories[known_cat]):
                        category_key = known_cat

            # if variable isnt in suspected category, group fails check
            if not unique_values.issubset(known_categories[category_key]):
                category_key = "text_response"
                break
        return category_key

    def apply_preferred_values(pisa_group, category_key):
        """
        update strings to preferred values (ex: "Yes" == True)
        raise ValueError if incomplete preferred values found
        """
        # ignore numerical and text_response types
        if category_key in known_categories:
            # update to corresponding preferred values
            for var in pisa_group:

                # strip white space to match know_categories
                pisa_df[var] = pisa_df[var].map(lambda x: x.strip())

                # replace each known value
                for known, preferred  in zip(
                        known_categories[category_key],
                        preferred_naming[category_key]):
                    pisa_df.loc[pisa_df[var] == known, var] = preferred

                # confirm values are from preferred_naming, none overlooked
                if not set(pisa_df[var].unique()).issubset(
                        preferred_naming[category_key]):
                    raise ValueError(var + ': incomplete preferred values.')

    def process_pisa_set_of_groups(pisa_set_of_groups):
        """
        Get category for each group,
        set corresponding values for each group,
        return dictionary containting found group/category key pairs.
        """
        group_category_matches = {}
        for group_key in pisa_set_of_groups:
            pisa_group = pisa_set_of_groups[group_key]

            # attempt to convert group to numeric
            try:
                pisa_df[pisa_group] = pisa_df[pisa_group].astype(int)
                category = "integer"
            except:
                try:
                    pisa_df[pisa_group] = pisa_df[pisa_group].astype(float)
                    category = "float"
                except:
                    category = None
            if not category:
                pisa_df[pisa_group] = pisa_df[pisa_group].astype(str)
                
                # attempt to match and update values to known PISA category
                category = get_category(pisa_group)
                apply_preferred_values(pisa_group, category)
            group_category_matches[group_key]=category
        return group_category_matches

    ### CAUTION:    large sets of variables will reduce the sample size
    ### Reason:     each variable has its own set of nulls
    ### Solution:   reduce variable sets after finding interactions
    select_columns_and_drop_nulls()
    # independent_groups_keys = process_pisa_set_of_groups(independent_groups)
    group_category_matches = process_pisa_set_of_groups(
        {**independent_groups, **dependent_groups})

    return group_category_matches



#%% MAIN

### raw csv data
PISA2012 = pd.read_csv(
    zipfile.ZipFile('pisa2012.csv.zip', 'r').open('pisa2012.csv'),
    sep=',', encoding='latin-1', error_bad_lines=False,
    dtype='unicode', index_col=False)

### variable descriptions
PISADICT2012 = pd.read_csv(
    'pisadict2012.csv',
    sep=',', encoding='latin-1', error_bad_lines=False,
    dtype='unicode', index_col=False).rename(
        columns={'Unnamed: 0':'varname', 'x': 'description'})

### Known Categories
#
# Dictionary containing lists. Each list contains the values of known
# PISA variables. The key is a short string description of the category.
#
KNOWN_CATEGORIES = {
    'work_status':[
        'Working full-time <for pay>',
        'Working part-time <for pay>',
        'Not working, but looking for a job',
        'Other (e.g. home duties, retired)'],
    'binary_yn':['Yes', 'No']
}

### Preferred Category Values
#
# Dictionary containing lists. Each list contains preferred values for
# known category associated with key.
#
PREFERRED_NAMING = {
    'work_status':[
        'Full-time',
        'Part-time',
        'Not working',
        'Other'],
    'binary_yn':[True, False]
    }

### Groups of Indepenent Variables
#
# Dictionary containing lists. Each list is a group of variable names.
# The variables in a group must be of same type (float, y/, category X).
#
INDEPENDENT_GROUPS = {
    'family_home': ['ST11Q01', 'ST11Q02', 'ST11Q03', 'ST11Q04', 'ST11Q05'],
    'parent_work': ['ST15Q01', 'ST19Q01'],
    'parent_isei': ['BFMJ2', 'BMMJ1', 'HISEI'],
    'HOMEPOS'    : ['HOMEPOS'],
    'person_item': ['ST26Q02', 'ST26Q03', 'ST26Q08',
                    'ST26Q09', 'ST26Q10', 'ST26Q11']}

### Groups of Depenent Variables
#
# Dictionary containing list. Lists are groups of variable names.
# The variables must be numeric.
#
DEPENDENT_GROUPS = {
    'math_result': ['PV1MATH', 'PV2MATH', 'PV3MATH', 'PV4MATH', 'PV5MATH'],
    'read_result': ['PV1READ', 'PV2READ', 'PV3READ', 'PV4READ', 'PV5READ']
    }


temp_df = initialize(
    PISA2012.sample(500),
    [KNOWN_CATEGORIES, PREFERRED_NAMING,
     INDEPENDENT_GROUPS, DEPENDENT_GROUPS])
