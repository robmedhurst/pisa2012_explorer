import zipfile

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pisaexplorer_wrangler import wrangle


# Dataset can take a few minutes to load on older sytems.
# Load once and only work on copy.
if 'PISA2012' not in locals():
    
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


def initialize(pisa_df, inputs):
    """
    general wrapper
    """
    wrangle(pisa_df, inputs)
    return pisa_df


temp_df = initialize(
    PISA2012.sample(500),
    [KNOWN_CATEGORIES, PREFERRED_NAMING,
     INDEPENDENT_GROUPS, DEPENDENT_GROUPS])