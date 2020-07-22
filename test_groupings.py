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
