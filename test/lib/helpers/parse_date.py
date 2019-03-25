#from dateparser.search import search_dates
#import dateparser
from lib.common_methods import remove_extra_spaces, validate_line, hasNumbers, format_date, find_pattern
#from dateutil.parser import parse
import datefinder
import datetime
import re
line_keywords = ['Date of Completion:', 'Date Issued:', 'End Date', 'End Date:', 'Date Completed:', 'Presentation Date:', 'Date Attended:', 'Completion Date:', 'Event Date:', 'Session End Date', 'Oate Attended:', 'Completion Date', 'Session End Date', 'awarded this certificate on', 'Date(s) Completed:', 'PROGRAM DATES:', 'Program Date:', 'Date Issued:', 'Class End Date', 'DATE ATTENDED:', 'Date:', 'Dated', 'Date.', 'Date', 'Awarded:', 'Completion date:', 'Seal of the Association this']
post_keywords = [ 'Completion Date:', 'Date Attended', 'Date of Completion', 'event on', 'awardedthis certificate on', 'awarded this certificate on']
pre_keywords	= ['Date Certified', 'Date', 'Date of Course', 'Dace of Course', 'Program Date(s)', 'Course Date', 'pate', 'Date of Completion']

invalid_keywords = ['cpe', 'CPE', 'Location', 'of course', 'tatas8']

class ParseDate():

		def __init__(self, contents, name, program_name):
				self.contents = contents
				self.date			= ""
				self.name			= name		
				try:
						self.program_name = program_name.lower().strip()
				except:
						self.program_name = "" #program_name

		def validate_date(self):
				print("DATE_VALIDATION________", self.date, "***")
				if self.date == "":
						return False
				for kw in invalid_keywords:
						if kw.lower() in self.date.lower():
								self.date = ""
								return False
				return True

		def make_corrections(self, date):
				print("DATE---make_corrections--->1", date)
				date = date.lower().split(' to ')[-1]
				date = date.lower().split(' at ')[0]
				date = date.replace('virtue of the', '')
				print("DATE---make_corrections--->2", date)
				if 'Part'.lower() in date:
						print("DATE---make_corrections--->3", date)
						dates = re.findall(r"part \d+ on (.*)$", date.lower())
						print("DATE---make_corrections--->4", dates)
						if dates:
								print("DATE---make_corrections--->5", date)
								date = dates[0]
				"""
				date = date.lower().replace('october', 'octaber')
				date = date.lower().replace('to', 'to a')
				date = date.lower().replace('octaber', 'october')
				"""
				return date


		def parse_within_lines(self):
				for content in self.contents:
						for kw in line_keywords:
								if kw in content:
										print("WithINLINE----->", content, "---KEYWORD---", kw)
										valid_words = validate_line(content, kw)
										if valid_words is None:
												continue
										for val in valid_words:
												print("VALID_WORD----->", valid_words)
												if hasNumbers(val):
														val = val.replace('.', ',')
														self.date = val #valid_words[0]
														if self.validate_date():
																return


		def parse_between_lines(self): 
				for index, content in enumerate(self.contents):
						for kw in post_keywords:
								if kw in content:
										print("2DATE---->", kw, "content--->", content)
										values = remove_extra_spaces( self.contents[index+1].strip() )
										print("POST--->", values)

										for val in values:
												print("val--->1", val)
												if hasNumbers(val) and len(val)>4:
														self.date = val
														print("val--->2", self.date)
														print("val--->3", self.validate_date())
														if self.validate_date():
																return

				
				if self.date == "":
						for index, content in enumerate(self.contents):
								for kw in pre_keywords:
										if kw in content:
												print("1DATE---->", kw, "content--->", content)
												values = remove_extra_spaces( self.contents[index-1].strip())
												print(f"1.1Date--->{values}")
												if len(values) == 0 :
														values = remove_extra_spaces( self.contents[index-2].strip())
												print(f"1.2Date--->{values}")
												
												for val in values:
														if hasNumbers(val) and len(val) > 4:
																self.date = val.strip()
																if self.validate_date():
																		return


		def extract_without_keywords(self):
				print("****WITHOUT_KEYWORD_EXTRACTION***")
				parse = False
				for content in self.contents:
						#print(f"Date:------>{self.program_name.lower().strip()}") #===Content:-->{content.lower().strip()}")
						#print(f"Content:--->{content.lower().strip()}")
						#print(f"TRUE/FALSE---DATE--->{find_pattern(self.program_name.lower().strip(), content.lower().strip())}")
						#print(f"TRUE/FALSE->{find_pattern(content.lower().strip(), self.program_name.lower().strip())}")
						#if find_pattern(self.program_name.lower().strip(), content.lower().strip()):
						#print("1***PARSE***", str(parse))
						if self.program_name == "":
								parse = True
						#print("2***PARSE_Pattern***", str(parse))
						#print("content.lower().strip()======>", content.lower().strip())
						#print("self.program_name.lower().strip()===>", self.program_name.lower().strip())
						if find_pattern(content.lower().strip(), self.program_name.lower().strip()):
						#if self.name.lower() in content.lower().strip():
								parse = True
						#print("3***PARSE***", str(parse))
						if parse:
								#if hasNumbers(content):
								#print("FINDING-DATE----->1", content)
								content = self.make_corrections(content)

								content = content.replace('.', ',')
								#print("FINDING-DATE----->2", content)
								dates = list(datefinder.find_dates(content))
								#print("Dates------------>3", dates)
								if len(dates) > 0:
										if dates[-1].year > datetime.datetime.now().year or dates[-1].year < 2000:
												continue
										self.date = str(dates[-1])
										#print(f"CASE_ONE----->{dates[-1].year}")
										#print(f"CASE_ONE----->{datetime.datetime.now().year}---type-->{type(datetime.datetime.now().year)}")
										#print(f"CASE_ONE----->{dates[-1].year > datetime.datetime.now().year}")
										#print(f"CASE_ONE----->{dates[-1].year < 2000}")
										#print("DateExtracted---->4", self.date)
										if self.validate_date():
												return




		def extract(self):
				self.parse_within_lines()
				if self.date == "":
						self.parse_between_lines()
				
				if self.date == "":
						self.extract_without_keywords()
				print("Date Extraction Complete===>1", self.date) 

				if self.date != "":
						self.date = self.make_corrections(self.date)
						print("Date Extraction Complete===>2", self.date)
						self.date = format_date(self.date)
						print("Date Extraction Complete===>3", self.date)


