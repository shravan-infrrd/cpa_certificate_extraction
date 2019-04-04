import re
from lib.common_methods import remove_extra_spaces, validate_line, hasNumbers
from dateutil.parser import *
from word2number import w2n


#line_keywords = ['ofContinuing ProfessionalEducation Credits:', 'CPE credit1', 'CPE Hours', 'Credit', 'hours of CPE', 'hours of Continuing', 'CPE credits']
pre_line_keywords = ['ofContinuing ProfessionalEducation Credits:', 'CPE credit1', 'CPE Hours', 'Credit', 'hours of CPE', 'hours of Continuing', 'CPE credits', 'CPE is awarded', 'CPE Hour', 'CPE credit hours', 'Hour Continuing Education Credit']

post_line_keywords = ['Recommended CPE Credits:', 'Interactive Credit in CPE Hours:', 'For a total of', 'Total CPF. Hours:', 'Total CPE Hours:', 'Total CPF. Hours:', 'Has Successfully Completed', 'Hours of Recommended CPE Credit:', 'CPE Credit Hours:', 'CPE Hours:', 'Number of CPE Credits', 'Total Credit Earned:', 'Duration:', 'CPE Credits:', 'Credit Hours:', 'CPE credit:', 'Credits:', 'CPE Credit Hours.', 'CPE Credits earned:', 'Recommendedfor', 'Recommended for', 'CPE credits:', 'Course Credit:', 'TSCPA Sponsor ID #', 'CPE:', 'Total Credits Earned:', 'Number of CPE credits', 'CPE Credit:', 'CPE Hours ', 'Approved CPE credit(s):', 'CPE Credits', 'Number of CPE credits', 'Recommended CPE credits for this course:', 'CPE Credits Received:', 'Recommended CPE credit', 'Total Hours:']

keywords = ['Numberof CPE Credits', 'Earned CPE credit(s)', 'Awarded CPE Credit Hours', 'Earned CPE Credit(s)', 'Number of CPE Credits', 'Earned CPE credit(s)', 'CPE Credit Hours', 'CPE Credit']

post_keywords = ['Recommended for:', 'CPE CREDIT EARNED', 'CPECredits', 'Credas', 'Recommendedfor:', 'CPE Credit', 'CPE Credits:'] 

invalid_keywords = ['Completion Date:']


class ParseCredits():

		def __init__(self, contents, fos):
				self.contents = contents
				self.credits = ""
				self.fos = fos
				self.max_credit_val = 40
				print("***CREDIT_INIT***", self.fos)
				self.field_of_study = []

		def validate_credits(self):
				if self.credits == "":
						return False
				if len(self.credits) > 4:
						self.credits = ""
						return False
				return True

		def get_credits(self):
				print("--GET_CREDITS-->", self.credits)
				creds = re.findall('\d*\.?\d+', self.credits)
				for cred in creds:
						if '.' not in cred:
								if len(str(cred.replace('.', ''))) >=4:
										self.credits = ""
										return ""
				print("--GET_CREDITS-->", creds)
				if creds:
						for cred in creds:
								print("--CRED-->", cred)
								try:
										if float(cred) < float(30):
												print("--CRED--2", float(cred))										
												return str(float(cred))
										else:
												self.credits = ""
												return ""
								except:
										print("get_credits---ERROR-->")
										self.credits = ""	
										return ""
				else:
						return self.credits

		def parse_with_fos_keyword(self, fos):
				for content in self.contents:
						content = content.lower().strip()
						if fos in content:
								cred = re.findall('\d*\.?\d+', content)
								if cred:
										self.credits = cred[0]
										self.credits = self.get_credits()
										return
						

		def parse_first_part_of_line(self):	
				print("***parse_first_part_of_line***")
				for content in self.contents:
						for kw in pre_line_keywords:
								if kw in content:
										#print("***CREDITS***====>", content, "***KW***", kw)
										#valid_words = validate_line(content.strip(), kw) #remove_extra_spaces( content.split(kw)[0].strip() )

										valid_words = remove_extra_spaces( content.split(kw)[0].strip() )
										for val in valid_words:
												if hasNumbers( val ):
														flag = False
														for ikw in invalid_keywords:
																if ikw in val.strip():
																		flag = True
																		break
														if flag:
																continue
														self.credits = val
														self.credits = self.get_credits()
														try:
																if float(self.credits) < float(self.max_credit_val):
																		return
														except:
																pass
												else:
														print("====WORD2NUMBER====1", val)
														try:
																number = w2n.word_to_num(val)
																print("====WORD2NUMBER====2", number)
																self.credits = str(number)
																self.credits = self.get_credits()
																return
														except:	
																print("====WORD2NUMBER====error")
																pass


		def parse_second_part_of_line(self):
				print("parse_second_part_of_line******START")
				for content in self.contents:
						for kw	in post_line_keywords:
								#print("CREDITS_KEYWORDS------------***********>", kw, "Content****", content.strip())
								if kw in content.strip():
										print("CREDIT--content-->", content)
										print("keyword-->", kw)
										valid_words = validate_line(content.strip(), kw)
										print("content-->", content)
										print("CREDIT-ParseSecondPartOfLine------>1", kw, valid_words)
										if valid_words is None:
												continue
										for val in valid_words:
												print("CREDIT-ParseSecondPartOfLine------>1.5",	val)
												if len(val) == 1:
														if val == 'l' or val == 'L' or val == 'I' or val == '|':
																val = '1'
												
												print("Credits--->", val)				
												if hasNumbers( val ):
														print("CREDIT-ParseSecondPartOfLine------>2", val)
														self.credits = val
														self.credits = self.get_credits()
														print("CREDIT-ParseSecondPartOfLine------>3", self.credits)
														try:
																if float(self.credits) < float(self.max_credit_val):
																		print("CREDIT-ParseSecondPartOfLine------>4", self.credits)
																		return
														except:
																pass
										"""
										print("ParseSecondPartOfLine------>2", content)
										self.credits = valid_words[0]
										self.credits = self.get_credits()
										print("ParseSecondPartOfLine------>3", self.credits)
										"""
				print("parse_second_part_of_line******END")
				if not hasNumbers(self.credits):
						self.credits = ""
				
		def parse_within_lines(self):
				print("1*************PARSING_CREDITS*****************")
				self.parse_first_part_of_line()
				print("2*************PARSING_CREDITS*****************")
				if self.credits != "":
						return
				print("3*************PARSING_CREDITS*****************")
				self.parse_second_part_of_line()
				print("4*************PARSING_CREDITS*****************")

		def parse_between_lines(self):
				
				print("5*************PARSING_CREDITS*****************")
				for index, content in enumerate(self.contents):
						for kw in keywords:
								if kw in content.strip():
										values = remove_extra_spaces( self.contents[ index - 1 ].strip() )
										if not values:
												values = remove_extra_spaces( self.contents[ index - 2 ].strip() )
									
										print("5.1*************PARSING_CREDITS*****************", values)
											
										for val in values:
												print("5.2*************PARSING_CREDITS*****************", val)
												if hasNumbers( val ):
														self.credits = val
														self.credits = self.get_credits()
														if self.validate_credits():
																return

				print("6*************PARSING_CREDITS*****************")
				for index, content in enumerate(self.contents):
						for kw in post_keywords:
								if kw in content:
										print("6.15*************PARSING_CREDITS*****************", kw)
										values = remove_extra_spaces( self.contents[ index + 1 ].strip() )
										print("6.16*************PARSING_CREDITS*****************", values)
										for val in values:

												if hasNumbers(val):
														print("6.1*************PARSING_CREDITS*****************", val)
														self.credits = val
														self.credits = self.get_credits()
														if self.validate_credits():
																return
										try: 
												print("6.15*************PARSING_CREDITS*****************", kw)
												values = remove_extra_spaces( self.contents[ index + 2 ].strip() )
												for val in values:
									 
														if hasNumbers(val):
																print("6.2*************PARSING_CREDITS*****************", val)
																self.credits = val
																self.credits = self.get_credits()
																print("6.3*************PARSING_CREDITS*****************", val)
																if self.validate_credits():
																		return
										except:
												continue


		def extract_credits(self, fos):
				print("extract_credits******", fos)
				self.credits = ""
				for content in self.contents:
						content = content.lower().strip()
						if fos.lower() in content.strip().lower():
								print(f"Content--->{content}, fos---->{fos}")
								print("Credits*******>", content.split(fos.lower()))

								credits = content.split(fos.lower())
								print("SPLIT_CREDITS--->", credits)
								for c in credits:
										extracted_credit = re.findall('\d*\.?\d+', c)
										print("EXTRACTED_CREDITS----->", extracted_credit)
										if extracted_credit:
												try:
														print("CREDIT_EXTRACTION---1--")
														self.credits = extracted_credit[0]

														if self.validate_credits():
																print("CREDIT_EXTRACTION---2--")
																if float(self.credits) < float(self.max_credit_val):
																		print("CREDIT_EXTRACTION---3--")
																		return self.credits
												except:
														print("CREDITS-ERROR-@@")
														continue
												#return extracted_credit[0]
										else:
												continue

				extracted_credit = ""
				if self.credits == "":
						extracted_credit = re.findall('\d*\.?\d+', fos)	
						if len(extracted_credit) > 0:
								self.credits = extracted_credit[0]
								if self.validate_credits():
										if float(self.credits) < float(self.max_credit_val):
												return self.credits
							
	
				return ""

		def exclude_if_date(self):
				patterns = ['%{YEAR:year}-%{MONTHNUM:month}-%{MONTHDAY:day}', '%{YEAR:year}/%{MONTHNUM:month}/%{MONTHDAY:day}']
				

		def find_credits(self, fos):
				print("*****FIND_CREDITS*****1", fos.lower())
				self.parse_within_lines()
				if self.credits != "":
						cred = re.findall('\d*\.?\d+', self.credits)
						print("****CREDITS*****EXTRACTION***", cred)
						try:
								if float(cred[0]) < float(self.max_credit_val):
										return cred[0]
						except:
								pass

				print("2*****FIND_CREDITS*****1", fos.lower())
				self.parse_between_lines()
				if self.credits != "":
						cred = re.findall('\d*\.?\d+', self.credits)
						print("2*****FIND_CREDITS*****2", cred)
						try:
								if float(cred[0]) < float(self.max_credit_val):
										return cred[0]
						except:
								pass

				print("3*****FIND_CREDITS*****1", fos.lower())
				for content in self.contents:
						content = content.lower().strip()
						if fos.lower() in content:
								print("CREDITS---CONTENT--->", content)
								credit = re.findall('\d*\.?\d+', content)
								print("CREDITS---CONTENT--->", credit)
								if len(credit) >= 3:
										continue
								print("Found Credits---->", credit)
								try:
										if credit:
												if float(credit[0]) < float(self.max_credit_val):
														return credit[0]
								except:
										continue

				print("5*****FIND_CREDITS*****", fos.lower())
				return ""

		def build_field_of_study(self):
				if len(self.fos) == 1:
						#self.find_credits(self.fos[0])
						print("====CREDITS===>1", self.fos)
						try:
								credit = float(self.find_credits(self.fos[0]))
								#self.field_of_study.append({"name": self.fos[0], "credits": str(credit), "score": ""})
								self.field_of_study.append({"name": self.fos[0], "credits": credit, "score": ""})
						except Exception as error:
								print("2***CREDIT_ERROR*****", error)
								#self.field_of_study.append({"name": self.fos[0], "credits": 0.0, "score": ""})
						#self.field_of_study.append({"name": self.fos[0], "credits": self.find_credits(self.fos[0]), "score": ""})
				else:
						for fos in self.fos:
								credits = self.extract_credits(fos)
								print("====Credits===>2", credits)
								if credits != "":
										try:
												credit = float(credits)
												print("1**CREDITS_INISIDE**", credit, "Assert---->", credit < float(self.max_credit_val))
												if credit < float(self.max_credit_val):
														#self.field_of_study.append({"name": fos, "credits": self.extract_credits(fos), "score":""})
														#self.field_of_study.append({"name": fos, "credits": str(credit), "score":""})
														self.field_of_study.append({"name": fos, "credits": credit, "score":""})
										except:
												print("1***CREDIT_ERROR*****")
												#self.field_of_study.append({"name": fos, "credits": self.extract_credits(fos), "score":""})
												pass

												
		def extract(self):
				self.build_field_of_study()
				"""
				if len(self.fos) == 1:
						self.parse_between_lines()
						if self.credits != "":
								return True
						self.parse_within_lines()
						fos = self.fos[0]
						fod['credits'] = self.credits
						self.fos = [fos]
						return True
				"""

