"""
Category Definitions

known_categories are the expected values for PISA 2012 categorical variables.
preferred_vales are the vales to replace expected_vales with.
"""


### Known Categories
#
# Dictionary containing lists. Each list contains the values of known
# PISA variables. The key is a short string description of the category.
#
KNOWN_CATEGORIES = {

    'binary_yn': [
        'Yes',
        'No'],

    'sex': [
        'Female',
        'Male'],

    'oecd': [
        'Non-OECD',
        'OECD'],

    'one_two_three': [
        'None',
        'One',
        'Two',
        'Three or more'],

    'confidence':[
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

    'exposure': [
        'No',
        'Yes, but only the teacher demonstrated this',
        'Yes, students did this'],

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
        'Not applicable']

}


### Preferred Category Values
#
# Dictionary containing lists. Each list contains preferred values for
# known category associated with key.
#
PREFERRED_NAMING = {

    'binary_yn': [
        True,
        False],

    'sex': [
        'Female',
        'Male'],

    'oecd': [
        'Non-OECD',
        'OECD'],

    'one_two_three': [
        'None',
        'One',
        'Two',
        'Three or more'],

    'confidence':[
        'Not at all confident',
        'Not very confident',
        'Confident',
        'Very confident'],

    'work_status':[
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

    'exposure': [
        'No',
        'Yes, but only teacher demonstrated',
        'Yes, students did this'],

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
        'Not applicable']

}
