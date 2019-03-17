import re

import dateparser
from dateutil.parser import parse
import datefinder


def format_date_with_input(date):
    date = str(date)
    print("===DATE_FORMATING===", date)
    #Expected date is: 2017-10-18 00:00:00
    #Modified format is: 10-18-2017 (mm/dd/yyyy)

    date = date.split(' ')[0].split('-')
    require_date = date[1] + '-' + date[2] + '-' + date[0]
    return require_date

def format_date(date):
    print(f"FORMAT_DATE----->", date)
    date = date.replace('.', ',')
    print(f"FORMAT_DATE----->", date)
    try:
        if date != '':
            dates = datefinder.find_dates(date)
            print("date---FORMAT---->", dates)
            for date in dates:
                print("DateFinder--->", date)  
                valid_date = date
  
            formated_date = format_date_with_input(valid_date)  
            date = str(dateparser.parse(formated_date , settings={'DATE_ORDER': 'MDY'}))
            date = format_date_with_input(date)
            date = date.replace('-', '/')
            return date
    except:
        return date


def find_pattern(kw, content):
    try:
        match = re.compile(r'\b({0})\b'.format(kw), flags=re.IGNORECASE).search(content)
        if match is None:
            return False
        else:
            return True
    except:
        print("FindPattern Error--->")
        return False
    #return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def remove_extra_spaces( line ):
    words = line.split('  ')
    valid_words = list( filter( None, words ) )
    #print("RemoveExtraSpaces---->", valid_words)
    return valid_words

def validate_line(content, keyword):
    words = content.split(keyword)
    #print(f"CommonMEthod2---->{words}--->{keyword}")
    if len(words) == 1:
        return None
    valid_words = remove_extra_spaces( words[1].strip() )
    if len(valid_words) == 0:
        return None
    return valid_words
