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



"""
### NEXT ADDITIONS:

	ST05Q01
189327	Yes, for more than one year

	ST29Q06
189327	Agree

	ST28Q01
189327	0-10 books 

	ST37Q02
189327	Confident

	ST44Q07
189327	Likely
"""