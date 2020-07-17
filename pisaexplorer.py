# This tool aims to aid in the exploration of the PISA 2012 dataset,
# allowing users to concurrently examine a group of similar variables.


#%% Import Libraries

import zipfile

import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


#%% FUNCTIONS


def initialize(pisa_df):
    """
    general wrapper
    """
    wrangle(pisa_df)

    # df is edited in place, return is for pipeline
    return pisa_df


#%%% Wrangling Functions

def wrangle(pisa_df):
    """
    wrangling wrapper
    """
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

    ### CAUTION:    large sets of variables will reduce the sample size
    ### Reason:     each variable has its own set of nulls
    ### Solution:   reduce variable sets after finding interactions
    select_columns_and_drop_nulls()

    ### match variable type and update each
    for pisa_group in (
            list(independent_groups.values()) +
            list(dependent_groups.values())):
        strings_to_known_categories(pisa_group, pisa_df)

    return pisa_df


def strings_to_known_categories(pisa_group, pisa_df):
    """
    Get variable type from of known_categories.
    Apply formatting if value types of group memebers is not mismatched.
    """
    def apply_preferred_values(category_key):
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

    def get_category():
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

    ### assume numeric and try to force conversion
    numeric = True
    try:
        pisa_df[pisa_group] = pisa_df[pisa_group].astype(int)
    except:
        try:
            pisa_df[pisa_group] = pisa_df[pisa_group].astype(float)
        except:
            # if conversion not possible, assume non numeric
            numeric = False
    if not numeric:
        pisa_df[pisa_group] = pisa_df[pisa_group].astype(str)
        # attempt to match and update values to known PISA category
        apply_preferred_values(get_category(pisa_group, pisa_df))

    return pisa_df



#%% MAIN


#%%% Load CSVs

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


#%%% Load Terms

### Known Categories
#
# Dictionary containing lists. Each list contains the values of known
# PISA variables. The key is a short string description of the category.
#
known_categories = {
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
preferred_naming = {
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
independent_groups = {
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
dependent_groups = {
    'math_result': ['PV1MATH', 'PV2MATH', 'PV3MATH', 'PV4MATH', 'PV5MATH'],
    'read_result': ['PV1READ', 'PV2READ', 'PV3READ', 'PV4READ', 'PV5READ']
    }


sample_size = 500

pisa_sample = PISA2012.sample(sample_size)

initialize(pisa_sample)
