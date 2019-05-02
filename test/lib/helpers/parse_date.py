#from dateparser.search import search_dates
#import dateparser
from lib.common_methods import remove_extra_spaces, validate_line, hasNumbers, format_date, find_pattern
#from dateutil.parser import parse
import datefinder
import datetime
import re
from pygrok import Grok


#line_keywords = ['Date of Completion:', 'Date Issued:', 'End Date', 'End Date:', 'Date Completed:', 'Presentation Date:', 'Date Attended:', 'Completion Date:', 'Event Date:', 'Session End Date', 'Oate Attended:', 'Completion Date', 'Session End Date', 'awarded this certificate on', 'Date(s) Completed:', 'PROGRAM DATES:', 'Program Date:', 'Date Issued:', 'Class End Date', 'DATE ATTENDED:', 'Date:', 'Dated', 'Date.', 'Date', 'Awarded:', 'Completion date:', 'Seal of the Association this', 'Completed on', 'awardedthis certificate on', 'completed on']
line_keywords = ['Date of Completion:', 'Date Issued:', 'End Date', 'End Date:', 'Date Completed:', 'Presentation Date:', 'Date Attended:', 'Completion Date:', 'Event Date:', 'Session End Date', 'Oate Attended:', 'Completion Date', 'Session End Date', 'awarded this certificate on', 'Date(s) Completed:', 'PROGRAM DATES:', 'Program Date:', 'Date Issued:', 'Class End Date', 'DATE ATTENDED:', 'Dated', 'Awarded:', 'Completion date:', 'Seal of the Association this', 'Completed on', 'awardedthis certificate on', 'completed on']

post_keywords = [ 'Completion Date:', 'Date Attended', 'Date of Completion', 'event on', 'awardedthis certificate on', 'awarded this certificate on']
pre_keywords	= ['Date Certified', 'Date of Course', 'Dace of Course', 'Program Date(s)', 'Course Date', 'pate', 'Date of Completion', 'Date']

date_keywords = ["Date:", "Date.", "Date"]
invalid_keywords = ['cpe', 'CPE', 'Location', 'of course', 'tatas8', 'Title', 'Time']

class ParseDate():

		def __init__(self, contents, name, program_name, input_format=""):
				self.contents = contents
				self.date			= ""
				self.name			= name
				self.input_format = format_date	
				try:
						self.program_name = program_name.lower().strip()
				except:
						self.program_name = "" #program_name

		def validate_date(self):
				print("DATE_VALIDATION________", self.date, "***")
				if self.date == "":
						return False
				if len(self.date) > 20:
						self.date = ""
						return False
				for kw in invalid_keywords:
						if kw.lower() in self.date.lower():
								self.date = ""
								return False
				return True

		def make_corrections(self, date):
				print("DATE---make_corrections--->1", date)
				date = date.replace('.', ',')
				date = date.lower().split(' to ')[-1]
				date = date.lower().split(' at ')[0]
				date = date.replace('virtue of the', '')
				date = date.replace('location:', '')
				date = date.replace('date:', '')
				date = date.replace('Date:', '')
				if 'Scptember'.lower() in date.lower():
						print("Date modification")
						date = date.replace('scptember', 'September')
				#print("DATE---make_corrections--->2", date)
				if 'Part'.lower() in date:
						#print("DATE---make_corrections--->3", date)
						dates = re.findall(r"part \d+ on (.*)$", date.lower())
						#print("DATE---make_corrections--->4", dates)
						if dates:
								#print("DATE---make_corrections--->5", date)
								date = dates[0]
				dates = re.findall(r"\d+/\d+/\d{2} \d{2}", date)
				if len(dates) > 0:
						date = dates[0].replace(' ', '')

				dates = re.findall(r"\d{2},\d{4}", date)
				if len(dates) > 0:
						date = date.replace(',', ', ')
			

				print("DATE---make_corrections--->2", date)

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
												numbers = sum(c.isdigit() for c in val.strip())
												if numbers <= 3:
														continue
												if hasNumbers(val):
														val = val.replace('.', ',')
														self.date = val #valid_words[0]
														if self.validate_date():
																return

		def parse_lines_for_date(self):
				for content in self.contents:
						for kw in date_keywords:
								if kw in content:
										print("WithINLINE----->", content, "---KEYWORD---", kw)
										valid_words = validate_line(content, kw)
										if valid_words is None:
												continue
										for val in valid_words:
												print("VALID_WORD----->", valid_words)
												numbers = sum(c.isdigit() for c in val.strip())
												if numbers <= 3:
														continue
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
														date_format = format_date(self.date, True)
														print("VALIDATE_FORMAT_DATE*****2", date_format)
														if date_format == "":
																self.date = ""
																continue
														if self.validate_date():
																return
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
																date_format = format_date(self.date, True)
																print("VALIDATE_FORMAT_DATE*****2", date_format)
																if date_format == "":
																		self.date = ""
																		continue
																if self.validate_date():
																		return

		def extract_without_keywords(self, name_keyword=""):
				print("****WITHOUT_KEYWORD_EXTRACTION***")
				parse = False
				for content in self.contents:
						if content.strip() == "":
								continue
			
						if parse:	
								max_dig_count = 0
								digits = re.findall(r"\d+", content.strip())
								for dig in digits:
										if len(str(dig)) >1:
												max_dig_count = len(str(dig))
												break
								if max_dig_count <= 1:
										continue

								if len(content.lower().strip()) > len(name_keyword.lower().strip()):
										first_arg = name_keyword.lower().strip()
										second_arg = content.lower().strip()
								else:
										first_arg = content.lower().strip()
										second_arg = name_keyword.lower().strip()
								print(f"first_arg**{first_arg}** second_arg-->**{second_arg}**--")
								print("FIND_PATTERN_RESULT--->1", find_pattern( first_arg, second_arg))
								if find_pattern(first_arg, second_arg):
										continue
						#print(f"Date:------>{self.program_name.lower().strip()}") #===Content:-->{content.lower().strip()}")
						else:
								print(f"Content:--->{content.lower().strip()}")
								if name_keyword == "":
										parse = True
								else:
										if len(content.lower().strip()) > len(name_keyword.lower().strip()):
												first_arg = name_keyword.lower().strip()
												second_arg = content.lower().strip()
										else:
												first_arg = content.lower().strip()
												second_arg = name_keyword.lower().strip()
										print("FIND_PATTERN_RESULT--->2", find_pattern( first_arg, second_arg))
										if find_pattern(first_arg, second_arg):
												#if self.name.lower() in content.lower().strip():
												parse = True
												continue
						print("2***PARSE_Pattern***", str(parse))
						numbers = sum(c.isdigit() for c in content.strip())
						if numbers <2:
								continue
						print("3***PARSE_DATE***", str(parse), "\n")
						if parse:
								#if hasNumbers(content):
								print("FINDING-DATE----->1", content)
								content = self.make_corrections(content)

								content = content.replace('.', ',')

								edate = re.findall(r"\d{1,2}-\d{1,2} \w+ \d{4}", content.strip().lower())
								print("FINDING-DATE----->2-->", edate)
								if edate:
										content = edate[0].split('-')[-1]
					
								print("FINDING-DATE----->2-->", content)
								dates = list(datefinder.find_dates(content))
								print("Dates------------>3", dates)
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
		"""
		def extract_without_keywords1(self, name_keyword=""):
				print("****WITHOUT_KEYWORD_EXTRACTION***")
				parse = False
				for content in self.contents:
						if content.strip() == "":
								continue
			
						if parse:	
								max_dig_count = 0
								digits = re.findall(r"\d+", content.strip())
								for dig in digits:
										if len(str(dig)) >1:
												max_dig_count = len(str(dig))
												break
								if max_dig_count <= 1:
										continue

								if len(content.lower().strip()) > len(self.program_name.lower().strip()):
										first_arg = self.program_name.lower().strip()
										second_arg = content.lower().strip()
								else:
										first_arg = content.lower().strip()
										second_arg = self.program_name.lower().strip()
								print(f"first_arg**{first_arg}** second_arg-->**{second_arg}**--")
								print("FIND_PATTERN_RESULT--->1", find_pattern( first_arg, second_arg))
								if find_pattern(first_arg, second_arg):
										continue
						#print(f"Date:------>{self.program_name.lower().strip()}") #===Content:-->{content.lower().strip()}")
						else:
								print(f"Content:--->{content.lower().strip()}")
								if self.program_name == "":
										parse = True
								else:
										if len(content.lower().strip()) > len(self.program_name.lower().strip()):
												first_arg = self.program_name.lower().strip()
												second_arg = content.lower().strip()
										else:
												first_arg = content.lower().strip()
												second_arg = self.program_name.lower().strip()
										print("FIND_PATTERN_RESULT--->2", find_pattern( first_arg, second_arg))
										if find_pattern(first_arg, second_arg):
												#if self.name.lower() in content.lower().strip():
												parse = True
												continue
						print("2***PARSE_Pattern***", str(parse))
						numbers = sum(c.isdigit() for c in content.strip())
						if numbers <2:
								continue
						print("3***PARSE_DATE***", str(parse), "\n")
						if parse:
								#if hasNumbers(content):
								print("FINDING-DATE----->1", content)
								content = self.make_corrections(content)

								content = content.replace('.', ',')
								edate = re.findall(r"\d{1,2}-\d{1,2} \w+ \d{4}", content.strip().lower())
								print("FINDING-DATE----->2-->", edate)
								if edate:
										content = edate[0].split('-')[-1]
					
								print("FINDING-DATE----->2-->", content)
								dates = list(datefinder.find_dates(content))
								print("Dates------------>3", dates)
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

		"""

		def get_date_from_program_name(self):
				print("get_date_from_program_name************>GROK", self.program_name)
				date_pattern = '%{MONTH:month} %{MONTHDAY:day}, %{YEAR:year}'
				grok = Grok(date_pattern)
				date_obj = grok.match(self.program_name)
				print("get_date_from_program_name************>GROK",date_obj)
				if date_obj is None:
						dates = list(datefinder.find_dates(self.program_name))
						print("DATE--->", dates)
						if len(dates) > 0:
								dates = dates[::-1]
								for date in dates:
										if date.year > datetime.datetime.now().year or date.year < 2000:
												continue
												#return
										self.date = str(date)
										if self.validate_date():
												return
				else:
						#{'month': 'January', 'day': '16', 'year': '2018'}
						self.date = date_obj['month'] + " " + date_obj['day'] + ", " + date_obj['year']
						if self.validate_date():
								return


		def expection_case(self):
				print("DATE_EXCEPTION----->", self.date)
				for content in self.contents:
						if 'Date' in content:
								print("DATE_EXCEPTION----->1", content)
								dates = re.findall(r"Date: (\d+.\d+.\d+)", content)
								print("DATE_EXCEPTION----->2", dates)
								try:
										self.date = dates[0].replace('.', '/')
										if self.validate_date():
												return
								except:
										continue
							

		def extract(self):
				self.parse_within_lines()
				print("Date Extraction Complete===>0", self.date) 

				#if self.date == "":
				#		self.parse_lines_for_date()

				print("Date Extraction Complete===>0.05", self.date) 

				if self.date == "":
						print("Date Extraction Complete===>0.1", self.date) 
						self.parse_between_lines()
				print("Date Extraction Complete===>0.2", self.date) 
				
				if self.date == "":
						self.extract_without_keywords(self.program_name)
				print("Date Extraction Complete===>1", self.date) 

				if self.date == "":
						self.extract_without_keywords(self.name)
				print("Date Extraction Complete===>1.1", self.date) 

				if self.date == "":
						self.parse_lines_for_date()

				if self.date == "":
						self.expection_case()

				if self.date != "":
						self.date = self.make_corrections(self.date)
						print("Date Extraction Complete===>2", self.date)
						self.date = format_date(self.date)
						print("Date Extraction Complete===>3", self.date)




