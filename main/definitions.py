"""
Global Static Definitions.

known_categories are the expected values for PISA 2012 categorical variables.
preferred_vales are the vales to replace expected_vales with.

"""

ORIGINAL_COLUMNS = [
    'Unnamed: 0', 'CNT', 'SUBNATIO', 'STRATUM', 'OECD', 'NC', 'SCHOOLID',
    'STIDSTD', 'ST01Q01', 'ST02Q01', 'ST03Q01', 'ST03Q02', 'ST04Q01',
    'ST05Q01', 'ST06Q01', 'ST07Q01', 'ST07Q02', 'ST07Q03', 'ST08Q01',
    'ST09Q01', 'ST115Q01', 'ST11Q01', 'ST11Q02', 'ST11Q03', 'ST11Q04',
    'ST11Q05', 'ST11Q06', 'ST13Q01', 'ST14Q01', 'ST14Q02', 'ST14Q03',
    'ST14Q04', 'ST15Q01', 'ST17Q01', 'ST18Q01', 'ST18Q02', 'ST18Q03',
    'ST18Q04', 'ST19Q01', 'ST20Q01', 'ST20Q02', 'ST20Q03', 'ST21Q01',
    'ST25Q01', 'ST26Q01', 'ST26Q02', 'ST26Q03', 'ST26Q04', 'ST26Q05',
    'ST26Q06', 'ST26Q07', 'ST26Q08', 'ST26Q09', 'ST26Q10', 'ST26Q11',
    'ST26Q12', 'ST26Q13', 'ST26Q14', 'ST26Q15', 'ST26Q16', 'ST26Q17',
    'ST27Q01', 'ST27Q02', 'ST27Q03', 'ST27Q04', 'ST27Q05', 'ST28Q01',
    'ST29Q01', 'ST29Q02', 'ST29Q03', 'ST29Q04', 'ST29Q05', 'ST29Q06',
    'ST29Q07', 'ST29Q08', 'ST35Q01', 'ST35Q02', 'ST35Q03', 'ST35Q04',
    'ST35Q05', 'ST35Q06', 'ST37Q01', 'ST37Q02', 'ST37Q03', 'ST37Q04',
    'ST37Q05', 'ST37Q06', 'ST37Q07', 'ST37Q08', 'ST42Q01', 'ST42Q02',
    'ST42Q03', 'ST42Q04', 'ST42Q05', 'ST42Q06', 'ST42Q07', 'ST42Q08',
    'ST42Q09', 'ST42Q10', 'ST43Q01', 'ST43Q02', 'ST43Q03', 'ST43Q04',
    'ST43Q05', 'ST43Q06', 'ST44Q01', 'ST44Q03', 'ST44Q04', 'ST44Q05',
    'ST44Q07', 'ST44Q08', 'ST46Q01', 'ST46Q02', 'ST46Q03', 'ST46Q04',
    'ST46Q05', 'ST46Q06', 'ST46Q07', 'ST46Q08', 'ST46Q09', 'ST48Q01',
    'ST48Q02', 'ST48Q03', 'ST48Q04', 'ST48Q05', 'ST49Q01', 'ST49Q02',
    'ST49Q03', 'ST49Q04', 'ST49Q05', 'ST49Q06', 'ST49Q07', 'ST49Q09',
    'ST53Q01', 'ST53Q02', 'ST53Q03', 'ST53Q04', 'ST55Q01', 'ST55Q02',
    'ST55Q03', 'ST55Q04', 'ST57Q01', 'ST57Q02', 'ST57Q03', 'ST57Q04',
    'ST57Q05', 'ST57Q06', 'ST61Q01', 'ST61Q02', 'ST61Q03', 'ST61Q04',
    'ST61Q05', 'ST61Q06', 'ST61Q07', 'ST61Q08', 'ST61Q09', 'ST62Q01',
    'ST62Q02', 'ST62Q03', 'ST62Q04', 'ST62Q06', 'ST62Q07', 'ST62Q08',
    'ST62Q09', 'ST62Q10', 'ST62Q11', 'ST62Q12', 'ST62Q13', 'ST62Q15',
    'ST62Q16', 'ST62Q17', 'ST62Q19', 'ST69Q01', 'ST69Q02', 'ST69Q03',
    'ST70Q01', 'ST70Q02', 'ST70Q03', 'ST71Q01', 'ST72Q01', 'ST73Q01',
    'ST73Q02', 'ST74Q01', 'ST74Q02', 'ST75Q01', 'ST75Q02', 'ST76Q01',
    'ST76Q02', 'ST77Q01', 'ST77Q02', 'ST77Q04', 'ST77Q05', 'ST77Q06',
    'ST79Q01', 'ST79Q02', 'ST79Q03', 'ST79Q04', 'ST79Q05', 'ST79Q06',
    'ST79Q07', 'ST79Q08', 'ST79Q10', 'ST79Q11', 'ST79Q12', 'ST79Q15',
    'ST79Q17', 'ST80Q01', 'ST80Q04', 'ST80Q05', 'ST80Q06', 'ST80Q07',
    'ST80Q08', 'ST80Q09', 'ST80Q10', 'ST80Q11', 'ST81Q01', 'ST81Q02',
    'ST81Q03', 'ST81Q04', 'ST81Q05', 'ST82Q01', 'ST82Q02', 'ST82Q03',
    'ST83Q01', 'ST83Q02', 'ST83Q03', 'ST83Q04', 'ST84Q01', 'ST84Q02',
    'ST84Q03', 'ST85Q01', 'ST85Q02', 'ST85Q03', 'ST85Q04', 'ST86Q01',
    'ST86Q02', 'ST86Q03', 'ST86Q04', 'ST86Q05', 'ST87Q01', 'ST87Q02',
    'ST87Q03', 'ST87Q04', 'ST87Q05', 'ST87Q06', 'ST87Q07', 'ST87Q08',
    'ST87Q09', 'ST88Q01', 'ST88Q02', 'ST88Q03', 'ST88Q04', 'ST89Q02',
    'ST89Q03', 'ST89Q04', 'ST89Q05', 'ST91Q01', 'ST91Q02', 'ST91Q03',
    'ST91Q04', 'ST91Q05', 'ST91Q06', 'ST93Q01', 'ST93Q03', 'ST93Q04',
    'ST93Q06', 'ST93Q07', 'ST94Q05', 'ST94Q06', 'ST94Q09', 'ST94Q10',
    'ST94Q14', 'ST96Q01', 'ST96Q02', 'ST96Q03', 'ST96Q05', 'ST101Q01',
    'ST101Q02', 'ST101Q03', 'ST101Q05', 'ST104Q01', 'ST104Q04', 'ST104Q05',
    'ST104Q06', 'IC01Q01', 'IC01Q02', 'IC01Q03', 'IC01Q04', 'IC01Q05',
    'IC01Q06', 'IC01Q07', 'IC01Q08', 'IC01Q09', 'IC01Q10', 'IC01Q11',
    'IC02Q01', 'IC02Q02', 'IC02Q03', 'IC02Q04', 'IC02Q05', 'IC02Q06',
    'IC02Q07', 'IC03Q01', 'IC04Q01', 'IC05Q01', 'IC06Q01', 'IC07Q01',
    'IC08Q01', 'IC08Q02', 'IC08Q03', 'IC08Q04', 'IC08Q05', 'IC08Q06',
    'IC08Q07', 'IC08Q08', 'IC08Q09', 'IC08Q11', 'IC09Q01', 'IC09Q02',
    'IC09Q03', 'IC09Q04', 'IC09Q05', 'IC09Q06', 'IC09Q07', 'IC10Q01',
    'IC10Q02', 'IC10Q03', 'IC10Q04', 'IC10Q05', 'IC10Q06', 'IC10Q07',
    'IC10Q08', 'IC10Q09', 'IC11Q01', 'IC11Q02', 'IC11Q03', 'IC11Q04',
    'IC11Q05', 'IC11Q06', 'IC11Q07', 'IC22Q01', 'IC22Q02', 'IC22Q04',
    'IC22Q06', 'IC22Q07', 'IC22Q08', 'EC01Q01', 'EC02Q01', 'EC03Q01',
    'EC03Q02', 'EC03Q03', 'EC03Q04', 'EC03Q05', 'EC03Q06', 'EC03Q07',
    'EC03Q08', 'EC03Q09', 'EC03Q10', 'EC04Q01A', 'EC04Q01B', 'EC04Q01C',
    'EC04Q02A', 'EC04Q02B', 'EC04Q02C', 'EC04Q03A', 'EC04Q03B', 'EC04Q03C',
    'EC04Q04A', 'EC04Q04B', 'EC04Q04C', 'EC04Q05A', 'EC04Q05B', 'EC04Q05C',
    'EC04Q06A', 'EC04Q06B', 'EC04Q06C', 'EC05Q01', 'EC06Q01', 'EC07Q01',
    'EC07Q02', 'EC07Q03', 'EC07Q04', 'EC07Q05', 'EC08Q01', 'EC08Q02',
    'EC08Q03', 'EC08Q04', 'EC09Q03', 'EC10Q01', 'EC11Q02', 'EC11Q03',
    'EC12Q01', 'ST22Q01', 'ST23Q01', 'ST23Q02', 'ST23Q03', 'ST23Q04',
    'ST23Q05', 'ST23Q06', 'ST23Q07', 'ST23Q08', 'ST24Q01', 'ST24Q02',
    'ST24Q03', 'CLCUSE1', 'CLCUSE301', 'CLCUSE302', 'DEFFORT', 'QUESTID',
    'BOOKID', 'EASY', 'AGE', 'GRADE', 'PROGN', 'ANXMAT', 'ATSCHL', 'ATTLNACT',
    'BELONG', 'BFMJ2', 'BMMJ1', 'CLSMAN', 'COBN_F', 'COBN_M', 'COBN_S',
    'COGACT', 'CULTDIST', 'CULTPOS', 'DISCLIMA', 'ENTUSE', 'ESCS', 'EXAPPLM',
    'EXPUREM', 'FAILMAT', 'FAMCON', 'FAMCONC', 'FAMSTRUC', 'FISCED', 'HEDRES',
    'HERITCUL', 'HISCED', 'HISEI', 'HOMEPOS', 'HOMSCH', 'HOSTCUL', 'ICTATTNEG',
    'ICTATTPOS', 'ICTHOME', 'ICTRES', 'ICTSCH', 'IMMIG', 'INFOCAR', 'INFOJOB1',
    'INFOJOB2', 'INSTMOT', 'INTMAT', 'ISCEDD', 'ISCEDL', 'ISCEDO', 'LANGCOMM',
    'LANGN', 'LANGRPPD', 'LMINS', 'MATBEH', 'MATHEFF', 'MATINTFC', 'MATWKETH',
    'MISCED', 'MMINS', 'MTSUP', 'OCOD1', 'OCOD2', 'OPENPS', 'OUTHOURS',
    'PARED', 'PERSEV', 'REPEAT', 'SCMAT', 'SMINS', 'STUDREL', 'SUBNORM',
    'TCHBEHFA', 'TCHBEHSO', 'TCHBEHTD', 'TEACHSUP', 'TESTLANG', 'TIMEINT',
    'USEMATH', 'USESCH', 'WEALTH', 'ANCATSCHL', 'ANCATTLNACT', 'ANCBELONG',
    'ANCCLSMAN', 'ANCCOGACT', 'ANCINSTMOT', 'ANCINTMAT', 'ANCMATWKETH',
    'ANCMTSUP', 'ANCSCMAT', 'ANCSTUDREL', 'ANCSUBNORM', 'PV1MATH', 'PV2MATH',
    'PV3MATH', 'PV4MATH', 'PV5MATH', 'PV1MACC', 'PV2MACC', 'PV3MACC',
    'PV4MACC', 'PV5MACC', 'PV1MACQ', 'PV2MACQ', 'PV3MACQ', 'PV4MACQ',
    'PV5MACQ', 'PV1MACS', 'PV2MACS', 'PV3MACS', 'PV4MACS', 'PV5MACS',
    'PV1MACU', 'PV2MACU', 'PV3MACU', 'PV4MACU', 'PV5MACU', 'PV1MAPE',
    'PV2MAPE', 'PV3MAPE', 'PV4MAPE', 'PV5MAPE', 'PV1MAPF', 'PV2MAPF',
    'PV3MAPF', 'PV4MAPF', 'PV5MAPF', 'PV1MAPI', 'PV2MAPI', 'PV3MAPI',
    'PV4MAPI', 'PV5MAPI', 'PV1READ', 'PV2READ', 'PV3READ', 'PV4READ',
    'PV5READ', 'PV1SCIE', 'PV2SCIE', 'PV3SCIE', 'PV4SCIE', 'PV5SCIE',
    'W_FSTUWT', 'W_FSTR1', 'W_FSTR2', 'W_FSTR3', 'W_FSTR4', 'W_FSTR5',
    'W_FSTR6', 'W_FSTR7', 'W_FSTR8', 'W_FSTR9', 'W_FSTR10', 'W_FSTR11',
    'W_FSTR12', 'W_FSTR13', 'W_FSTR14', 'W_FSTR15', 'W_FSTR16', 'W_FSTR17',
    'W_FSTR18', 'W_FSTR19', 'W_FSTR20', 'W_FSTR21', 'W_FSTR22', 'W_FSTR23',
    'W_FSTR24', 'W_FSTR25', 'W_FSTR26', 'W_FSTR27', 'W_FSTR28', 'W_FSTR29',
    'W_FSTR30', 'W_FSTR31', 'W_FSTR32', 'W_FSTR33', 'W_FSTR34', 'W_FSTR35',
    'W_FSTR36', 'W_FSTR37', 'W_FSTR38', 'W_FSTR39', 'W_FSTR40', 'W_FSTR41',
    'W_FSTR42', 'W_FSTR43', 'W_FSTR44', 'W_FSTR45', 'W_FSTR46', 'W_FSTR47',
    'W_FSTR48', 'W_FSTR49', 'W_FSTR50', 'W_FSTR51', 'W_FSTR52', 'W_FSTR53',
    'W_FSTR54', 'W_FSTR55', 'W_FSTR56', 'W_FSTR57', 'W_FSTR58', 'W_FSTR59',
    'W_FSTR60', 'W_FSTR61', 'W_FSTR62', 'W_FSTR63', 'W_FSTR64', 'W_FSTR65',
    'W_FSTR66', 'W_FSTR67', 'W_FSTR68', 'W_FSTR69', 'W_FSTR70', 'W_FSTR71',
    'W_FSTR72', 'W_FSTR73', 'W_FSTR74', 'W_FSTR75', 'W_FSTR76', 'W_FSTR77',
    'W_FSTR78', 'W_FSTR79', 'W_FSTR80', 'WVARSTRR', 'VAR_UNIT', 'SENWGT_STU',
    'VER_STU']


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
