import re

import dateparser
from dateutil.parser import parse
import datefinder


def populate_missing(r1, r2):
    for k, v in r1.items():
        if not v:
            if r2[k]:
                r1[k] = r2[k]


def check_for_valid_string(s):
	
		print("CHECK_FOR_VALID_STRING---->", s)
		if not re.match(r'^[_\W]+$', s):
				return True
		else:
				return False


def format_date_with_input(date):
		date = str(date)
		print("===DATE_FORMATING===", date)
		#Expected date is: 2017-10-18 00:00:00
		#Modified format is: 10-18-2017 (mm/dd/yyyy)

		date = date.split(' ')[0].split('-')
		require_date = date[1] + '-' + date[2] + '-' + date[0]
		return require_date

def format_date(date, validate=False):
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
				if validate:
						return ""
				else:
						return date


def find_pattern(kw, content):
		invalid_char = ['(', ')', ',', '.', '|']
		for inc in invalid_char:
				kw = kw.replace(inc, '')
				if not type(content) is list:
						content = content.replace(inc, '')
			
		try:
				match = re.compile(r'\b({0})\b'.format(kw), flags=re.IGNORECASE).search(content)
				if match is None:
						#print("FIND_PATTERN*****FALSE")
						return False
				else:
						#print("FIND_PATTERN*****TRUE")
						return True
		except:
				#print("FindPattern Error--->")
				return False
		#return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def hasNumbers(inputString):
		return any(char.isdigit() for char in inputString)

def remove_extra_spaces( line ):
		words = line.split('  ')
		valid_words = list( filter( None, words ) )
		return valid_words

def validate_line(content, keyword):
		#print(f"Content-->{content}, keyword-->{keyword}")
		words = content.split(keyword)
		if len(words) == 1:
				return None
		valid_words = remove_extra_spaces( words[1].strip() )
		if len(valid_words) == 0:
				return None
		return valid_words
