### Known Categories
#
# Dictionary containing lists. Each list contains the values of known
# PISA variables. The key is a short string description of the category.
#
KNOWN_CATEGORIES = {

    'binary_yn': ['Yes',
                  'No'],

    'work_status': [
        'Working full-time <for pay>',
        'Working part-time <for pay>',
        'Not working, but looking for a job',
        'Other (e.g. home duties, retired)'],

    'about_year': ['No',
                   'Yes, for more than one year',
                   'Yes, for one year or less'],

    'likelihood': ['Likely',
                   'Slightly likely',
                   'Very   Likely',
                   'Not at all likely']

    }




### Preferred Category Values
#
# Dictionary containing lists. Each list contains preferred values for
# known category associated with key.
#
PREFERRED_NAMING = {

    'binary_yn':[True, False],

    'work_status':[
        'Full-time',
        'Part-time',
        'Not working',
        'Other'],

    'about_year': ['No',
                   'Yes, more than',
                   'Yes, less than'],

    'likelihood': ['Likely',
               'Slightly likely',
               'Very Likely',
               'Not likely']

    }
