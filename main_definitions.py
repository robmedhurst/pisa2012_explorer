"""
Global Static Definitions.

known_categories are the expected values for PISA 2012 categorical variables.
preferred_vales are the vales to replace expected_vales with.

Some small dictionaries for testing also live here.
"""


# =============================================================================
# TEST VARIABLES
# =============================================================================

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
PRESET1 = {
    'dependent_groups': DEPEN_TEST_GROUPING01,
    'independent_groups': INDEP_TEST_GROUPING01,
    'pisa_sample': 1000}

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
# CATEGORY DEFINITIONS
# =============================================================================
# Known Categories
#
# Dictionary containing lists. Each list contains the values of known
# PISA variables. The key is a short string description of the category.
#
KNOWN_CATEGORIES = {

    'binary_yn1': [
        'Yes',
        'No'],

    'binary_yn2': [
        'Yes',
        'No, never'],

    'sex': [
        'Female',
        'Male'],

    'oecd': [
        'Non-OECD',
        'OECD'],


    'major_in': [
        'Major in college Science',
        'Major in college Math'],

    'study_harder': [
        'Study harder Math',
        'Study harder Test Language'],

    'maximum_classes': [
        'Maximum classes Math',
        'Maximum classes Science'],

    'pursuing_career': [
        'Pursuing a career Math',
        'Pursuing a career Science'],


    'one_two_three': [
        'None',
        'One',
        'Two',
        'Three or more'],

    'confidence': [
        'Not at all confident',
        'Not very confident',
        'Confident',
        'Very confident'],

    'work_status': [
        'Working full-time <for pay>',
        'Working part-time <for pay>',
        'Not working, but looking for a job',
        'Other (e.g. home duties, retired)'],

    'about_year': [
        'No',
        'Yes, for one year or less',
        'Yes, for more than one year'],

    'age_when': [
        'Never',
        '13 years old  or older',
        '10-12 years old',
        '7-9 years old',
        '6 years old or younger'],

    'how_long': [
        '0 to 3 years',
        '4 to 6 years',
        '7 to 9 years',
        '10 to 12 years',
        '13 years or older'],

    'likelihood': [
        'Not at all likely',
        'Slightly likely',
        'Likely',
        'Very   Likely'],

    'agreement': [
        'Strongly agree',
        'Agree',
        'Disagree',
        'Strongly disagree'],

    'heard_of_it': [
        'Never heard of it',
        'Heard of it a few times',
        'Heard of it often',
        'Heard of it once or twice',
        'Know it well,  understand the concept'],


    'frequency1': [
        'Never or rarely',
        'Sometimes',
        'Often',
        'Always or almost always'],

    'frequency2': [
        'No, never',
        'Yes, once',
        'Yes, twice or more'],

    'frequency3': [
        'None',
        'One or two times',
        'Three or four times',
        'Five or more times'],

    'frequency4': [
        'Never or hardly ever',
        'Once or twice a week',
        'Once or twice a month',
        'Almost every day',
        'Every day'],

    'frequency5': [
        'None',
        'Less than 2',
        '2 or more but less than 4',
        '4 or more but less than 6',
        '6 or more'],

    'frequency6': [
        'Never',
        'Rarely',
        'Sometimes',
        'Frequently'],


    'schooltype1': [
        'Pre-Vocational',
        'Vocational',
        'Modular',
        'General'],

    'isced_completed_m': [
        'He did not complete <ISCED level 1>',
        '<ISCED level 1>',
        '<ISCED level 2>',
        '<ISCED level 3B, 3C>',
        '<ISCED level 3A>'],

    'isced_completed_f': [
        'She did not complete <ISCED level 1>',
        '<ISCED level 1>',
        '<ISCED level 2>',
        '<ISCED level 3B, 3C>',
        '<ISCED level 3A>'],

    'isced': [
        'None',
        'ISCED 1',
        'ISCED 2',
        'ISCED 3B, C',
        'ISCED 3A, ISCED 4',
        'ISCED 5B',
        'ISCED 5A, 6'],

    'isced_level': [
        'ISCED level 1',
        'ISCED level 2',
        'ISCED level 3'],

    'StQ_form': [
        'StQ Form B',
        'StQ Form UH',
        'StQ Form C',
        'StQ Form A'],

    'M': [
        'C',
        'B',
        'M',
        'A'],


    'attendance': [
        'I do not attend <out-of-school time lessons> in this subject',
        'Less than 2 hours a week',
        '6 or more hours a week',
        '4 or more but less than 6 hours a week',
        '2 or more but less than 4 hours a week'],


    'num_books': [
        '0-10 books',
        '11-25 books',
        '26-100 books',
        '101-200 books',
        '201-500 books',
        'More than 500 books'],

    'about_lessons': [
        'Never or Hardly Ever',
        'Some Lessons',
        'Most Lessons',
        'Every Lesson'],

    'similarity': [
        'Not at all like me',
        'Not much like me',
        'Somewhat like me',
        'Mostly like me',
        'Very much like me'],

    'action': [
        'definitely not do this',
        'probably not do this',
        'probably do this',
        'definitely do this'],

    'usage': [
        'No',
        'Yes, but I don\x92t use it',
        'Yes, and I use it'],

    'memory': [
        'Most important',
        'by heart',
        'relating to known'],

    'understanding': [
        'Improve understanding',
        'new ways',
        'check memory'],

    'relating': [
        'Relating to other subjects',
        'learning goals',
        'in my sleep'],

    'learning1': [
        'everyday life',
        'Repeat examples',
        'more information'],

    'exposure': [
        'No',
        'Yes, but only the teacher demonstrated this',
        'Yes, students did this'],

    'calulator': [
        'No calculator',
        'A CAS calculator',
        'A Simple calculator',
        'A Graphics calculator',
        'A Scientific calculator'],

    'booklet_set': [
        'Easier set of booklets',
        'Standard set of booklets'],

    'after_school': [
        'Courses after school Math',
        'Courses after school Test Language'],

    'repeated': [
        'Did not repeat a <grade>',
        'Repeated a <grade>'],

    'location1': [
        'Country of test',
        'Other country'],

    'language1': [
        'Language of the test',
        'Other language'],

    'language2': [
        'other than <test language> or <other official national langu',
        '<test language> or <other official national language(s) or d'],

    'language3': [
        'Mostly <heritage language>',
        'About equally <heritage language> and <test language>',
        'Mostly <test language>',
        'Not applicable'],

    'native': [
        'Second-Generation',
        'Native',
        'First-Generation'],

    'booklet': [
        'UH booklet',
        'booklet 1',
        'booklet 3',
        'booklet 2',
        'booklet 4',
        'booklet 5',
        'booklet 6',
        'booklet 7',
        'booklet 8',
        'booklet 9',
        'booklet 10',
        'booklet 11',
        'booklet 12',
        'booklet 13',
        'booklet 21',
        'booklet 22',
        'booklet 23',
        'booklet 24',
        'booklet 25',
        'booklet 26',
        'booklet 27']


}


# Preferred Category Values
#
# Dictionary containing lists. Each list contains preferred values for
# known category associated with key.
#
PREFERRED_NAMING = {

    'binary_yn1': [
        True,
        False],

    'binary_yn2': [
        'Yes',
        'No, never'],

    'sex': [
        'Female',
        'Male'],

    'oecd': [
        'Non-OECD',
        'OECD'],


    'major_in': [
        'Major in college Science',
        'Major in college Math'],

    'study_harder': [
        'Study harder Math',
        'Study harder Test Language'],

    'maximum_classes': [
        'Maximum classes Math',
        'Maximum classes Science'],

    'pursuing_career': [
        'Pursuing a career Math',
        'Pursuing a career Science'],


    'one_two_three': [
        'None',
        'One',
        'Two',
        'Three or more'],

    'confidence': [
        'Not at all confident',
        'Not very confident',
        'Confident',
        'Very confident'],

    'work_status': [
        'Full-time',
        'Part-time',
        'Not working',
        'Other'],

    'about_year': [
        'No',
        'Yes, less than',
        'Yes, more than'],

    'age_when': [
        'Never',
        '13 years old or older',
        '10-12 years old',
        '7-9 years old',
        '6 years old or younger'],

    'how_long': [
        '0 to 3 years',
        '4 to 6 years',
        '7 to 9 years',
        '10 to 12 years',
        '13 years or older'],

    'likelihood': [
        'Not at all likely',
        'Slightly likely',
        'Likely',
        'Very Likely'],

    'agreement': [
        'Strongly agree',
        'Agree',
        'Disagree',
        'Strongly disagree'],

    'heard_of_it': [
        'Never heard of it',
        'Heard of it a few times',
        'Heard of it often',
        'Heard of it once or twice',
        'Know it well,  understand the concept'],


    'frequency1': [
        'Never or rarely',
        'Sometimes',
        'Often',
        'Always or almost always'],

    'frequency2': [
        'No, never',
        'Yes, once',
        'Yes, twice or more'],

    'frequency3': [
        'None',
        'One or two times',
        'Three or four times',
        'Five or more times'],

    'frequency4': [
        'Never or hardly ever',
        'Once or twice a week',
        'Once or twice a month',
        'Almost every day',
        'Every day'],

    'frequency5': [
        'None',
        'Less than 2',
        '2 or more but less than 4',
        '4 or more but less than 6',
        '6 or more'],

    'frequency6': [
        'Never',
        'Rarely',
        'Sometimes',
        'Frequently'],


    'schooltype1': [
        'Pre-Vocational',
        'Vocational',
        'Modular',
        'General'],

    'isced_completed_m': [
        'Not ISCED level 1>',
        'ISCED level 1',
        'ISCED level 2',
        'ISCED level 3B, 3C',
        'ISCED level 3A'],

    'isced_completed_f': [
        'Not ISCED level 1>',
        'ISCED level 1',
        'ISCED level 2',
        'ISCED level 3B, 3C',
        'ISCED level 3A'],

    'isced': [
        'None',
        'ISCED 1',
        'ISCED 2',
        'ISCED 3B, C',
        'ISCED 3A, 4',
        'ISCED 5B',
        'ISCED 5A, 6'],

    'isced_level': [
        'ISCED level 1',
        'ISCED level 2',
        'ISCED level 3'],

    'StQ_form': [
        'StQ Form B',
        'StQ Form UH',
        'StQ Form C',
        'StQ Form A'],

    'M': [
        'C',
        'B',
        'M',
        'A'],

    'attendance': [
        'I do not attend extra lessons in this subject',
        'Less than 2 hours a week',
        '6 or more hours a week',
        '4 or more but less than 6 hours a week',
        '2 or more but less than 4 hours a week'],


    'num_books': [
        '0-10 books',
        '11-25 books',
        '26-100 books',
        '101-200 books',
        '201-500 books',
        'Over 500 books'],

    'about_lessons': [
        'Never or Hardly',
        'Some Lessons',
        'Most Lessons',
        'Every Lesson'],

    'similarity': [
        'Not at all like me',
        'Not much like me',
        'Somewhat like me',
        'Mostly like me',
        'Very much like me'],

    'action': [
        'definitely not do this',
        'probably not do this',
        'probably do this',
        'definitely do this'],

    'usage': [
        'No',
        'Yes, but I dont use it',
        'Yes, and I do use it'],

    'memory': [
        'Most important',
        'by heart',
        'relating to known'],

    'understanding': [
        'Improve understanding',
        'new ways',
        'check memory'],

    'relating': [
        'Relating to other subjects',
        'learning goals',
        'in my sleep'],

    'learning1': [
        'everyday life',
        'Repeat examples',
        'more information'],

    'exposure': [
        'No',
        'Yes, but only teacher demonstrated',
        'Yes, students did this'],

    'calulator': [
        'No calculator',
        'A CAS calculator',
        'A Simple calculator',
        'A Graphics calculator',
        'A Scientific calculator'],

    'booklet_set': [
        'Easier set of booklets',
        'Standard set of booklets'],

    'after_school': [
        'Courses after school Math',
        'Courses after school Test Language'],

    'repeated': [
        'Did not repeat a <grade>',
        'Repeated a <grade>'],

    'location1': [
        'Country of test',
        'Other country'],

    'language1': [
        'Language of the test',
        'Other language'],

    'language2': [
        'other than test language',
        'test language'],

    'language3': [
        'Mostly <heritage language>',
        'About equally <heritage language> and <test language>',
        'Mostly <test language>',
        'Not applicable'],

    'native': [
        'Second-Generation',
        'Native',
        'First-Generation'],


    'booklet': [
        'UH booklet',
        'booklet 01',
        'booklet 03',
        'booklet 02',
        'booklet 04',
        'booklet 05',
        'booklet 06',
        'booklet 07',
        'booklet 08',
        'booklet 09',
        'booklet 10',
        'booklet 11',
        'booklet 12',
        'booklet 13',
        'booklet 21',
        'booklet 22',
        'booklet 23',
        'booklet 24',
        'booklet 25',
        'booklet 26',
        'booklet 27']
}
