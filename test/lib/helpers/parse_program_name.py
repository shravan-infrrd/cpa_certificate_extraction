#text_file = "./textfiles/21.txt"
import re
from lib.common_methods import remove_extra_spaces, validate_line, find_pattern, check_for_valid_string



preceding_keywords = ['has successfully completed', 'CERTIFICATE OF ATTENDANCE', 'has successfully completed the online course', 'Online Certification training:', 'Certificate of Attendance', 'Certificate of Completion', 'for participation in', 'for participation in', 'successfully completed', 'completion ot the course', 'entitled', 'for successfully completing', 'completed', 'For Successfully Completing', 'has successfully completed:', 'Has Successfully Completed the Course:', 'Has Successfully Completed the Course:', 'For successful completion of:', 'for the successful completion of', 'has completed', 'has completed the group Internet-based course', 'nas success*u ly comoleted:', 'Forattending', 'For attending', 'FOR THE PROGRAM ENTITLED', 'Congratulations on the successful completion of', 'for successful completion of the course', 'Has Successtully Completed the Course:', 'COMPLETION OF THE FOLLOWING ', 'for successful completion of', 'For successfully completing:', 'FOR THE COURSE ENTITLED', 'For completion of', 'FOR SUCCESSFUL COMPLETION OF', 'HAS COMPLETED THE TRAINING COURSETITLED', 'HAS COMPLETED THE TRAINING COURSE TITLED', 'For successfully completing', 'On Demand Video', 'FOR SUCCESSFUL COMPLETION', 'For successful completionof:', 'For successful completion of', 'attended the course', 'Successful campletion of', 'HAS SUCCESSFULLY COMPLETED', 'For the successful completion of', 'This certifies that', 'Has Successfully Completed:', 'Has successfully completed', 'has successfully completed the course', 'Has successfully completed the Introduction to', 'course.', 'for successfully completing the event', 'has completed the training session', '(Please record only those hours you haveactually attended.)', 'has completed the group live course', 'Has successfully completed the QuickBooks', 'Has successfully completed the following training:', 'HAS SUCCESSFULLY COMPLETED THE COURSE', 'Successful campletion of:', 'Successfully completed the', 'who haspursued studies and completed all the', 'who has pursued studies and completed all the', 'successfully completed the webinar', 'Has successfully completed course:', 'has successfully completed the program:']

"""
Is hereby awardedto (the institute of internal)
"""
following_keywords = ['Course Name', 'a seminar presented by'] #, 'Is hereby awardedto', 'Is hereby awarded to']
line_keywords = ['Program Name:', 'Course Tithe:', 'Course Title:', 'for successfully completing:', 'for successfully completing', 'Program Title:', 'PROGRAM TITLE:', 'For successful completion of', 'Title.', 'Title:', 'for success‘ully comp et ng', 'Course:', 'Event Title:', 'tor successfully completing', 'Course Title', 'Subject:', 'Event:', 'NAME OF COURSE:', 'Course', 'Title of Training:', 'For Attending', 'For successfully completing the', 'EVENT NAME:', 'has successfully completed:', 'TOPIC:', 'CourseTitle:', 'On Demand Video:', 'For successfully completing:', 'Attended Quarterly', 'For attending the Career Development Series:', 'ProgramTitle: ' ]

invalid_keywords = ['presented to', 'Awarded to', 'Date', 'Freserted to', 'granted', 'Association of Cortificd', 'Association of Certified', 'Field of Study', 'Please', 'Program Location', 'Credits', 'CTEC', 'Participant', 'Sent', 'This is to ceruty that', 'This is to certify that', 'This is to', 'awardedthis', 'awarded this', 'preserted to', 'success‘ully', '@', 'certify that', 'Instructional Delivery Method', 'Attendee', 'Attendee Name:', 'SPONSOR', 'sponsor', 'PROGRAM TITLE:', 'program title', 'Successfully', 'successfully', 'ACKNOWLEDGES', 'THIS CERTIFIES THAT', 'this certifies that', 'for participation in', 'This certificate is presentedto', 'This certificate is presented to', 'Author', 'Congratulations', 'Self-Study Programs', 'CourseTitle', 'Course Title', 'DELIVERY METHOD', 'awardedto', 'awarded to', 'Location', 'CPEcredits', 'CPE credits', 'Event Dates', 'OBJECTIVE', 'Units', 'Has Successtully Completed the', 'Course Freld of Study', 'Course Field of Study', 'Course Number', 'Delivery Method Used', 'Type of InstructionalDelivery', 'Type of Instructional Delivery', 'Completion Certificate', 'Dates', 'Street', 'Pittsburgh', 'Sponsored by', 'Inc', 'Presenter', 'Fleld of Study', 'Field of Study', 'Fields of Study', 'http', 'Format', 'has completed', 'Auburn Folsom Rd', 'Student', 'SHRM', 'Certificate of Attendance', 'Instructor', 'Naine', 'Name', 'In accordance with the standards for']

possible_keywords = ['Conference', 'Event', 'Webcast', 'Seminar', 'Review Course', 'Ethics:', 'CPE DIRECT', 'A WORKSHIP ABOUT WEBINARS', "Accountant's Guide", 'Crosslin:']

priority_keywords = ['(Part |)', 'Part |', 'PART 1', 'Module 1', 'Module |', 'Module 2', 'Moduel 3', 'Module 4', 'Modeul 5', 'Module 6', 'MODULE 2']

class ParseProgramName():

		def __init__(self, contents, name, sponsor):
				self.contents = contents
				self.name = name
				self.program_name = ""
				self.sponsor = sponsor

		def validate_program_name(self):
				print("ValidateProgramName**", self.program_name)
				if self.program_name.strip() == "":
						return False
				#print(f"InvalidKEYWORDS---->{invalid_keywords}--->program_name---->{self.program_name}")
				for kw in invalid_keywords:
						#print(f"===>INKW-->{kw}=====>pn==>{self.program_name}")
						if find_pattern(kw, self.program_name.lower()):
						#if kw.lower() in self.program_name.lower():
								print("Error--->1", kw, "pn", self.program_name)
								self.program_name = ""
								return False
				if self.name.lower() != "":
						if find_pattern(self.name.lower(), self.program_name.lower()):
								if not find_pattern('ethics', self.program_name.lower()):
										print("Error2--->")
										#self.program_name = ""
										#return False
				#Temporary Fix
				if len(self.program_name.split(' ')) == 1:
						if self.program_name == 'completed' or self.program_name == 'attended':
								self.program_name = ""
								return False
	
				"""	
				if self.sponsor.lower() != "":
						if find_pattern(self.sponsor.lower(), self.program_name.lower()):
								print("Error3--->")
								self.program_name = ""
								return False
				"""
				if '(' in self.program_name:
						if ')' not in self.program_name:
								self.program_name = ""
								return False
				elif ')' in self.program_name:
						self.program_name = ""
						return False
								


				print("ValidateProgramName**2", len(self.program_name.strip()))
				if len(self.program_name.strip()) <= 4:
						print("Error4--->")
						self.program_name = ""
						return False
				return True 

		def check_for_invalid_keywords(self, word):
				for kw in invalid_keywords:
						if find_pattern(kw.lower(), word.lower()):
								print("****CAUTION****")
								#print(f"Keyword-->{kw}, word-->{word}")
								return ""
				return word

		def check_invalid_keywords(self, word):
				for kw in invalid_keywords:
						#print(f"keyword--->{kw}----word---{word}---")
						if find_pattern(kw.lower(), word.lower()):
								print("VALIDATION----->", kw, "Content--->", word, "---end")
								return False
				return True

		def validate_each_value(self, values):
				#print("VALIDATION====PROGRAM_NAME===>", values)
				status = False
				if not values:
						return [], True
				#try:
				if values[0] != "":
						#print("***VALiDATE***1", self.check_invalid_keywords(values[0]))
						if not self.check_invalid_keywords(values[0]):
								return [], status
						#print("***VALiDATE***2")
						if self.name != "":
								if find_pattern(self.name.lower(), values[0]):
										return [], True
						#print("***VALiDATE***3")
						"""
						if ':' in values[0]:
								for k in ['ethics']:
										print("***VALiDATE***3", find_pattern('ethics', values[0]))
										if find_pattern('ethics', values[0]):
												pass
												#return [], status
						"""
						#print("***VALiDATE***4", check_for_valid_string(values[0]))
						if not check_for_valid_string(values[0]):
								return [], True
						#print("***VALiDATE***5")
						return values, True
				#except Exception as error:
						#print("ERROR IN VALIDATE_EACH_VALUE----->", values, "Error--->", error)
				#		return []

		def get_progrma_name(self, val_1, val_2, val_3):
				
				if val_1 and val_2 and val_3:
						print("PN***1***")
						return val_1[0] + " " + val_2[0] + " " + val_3[0]
				if val_1 and val_2:
						print("PN***2***")
						return val_1[0] + " " + val_2[0]
				if val_1 and val_3:
						print("PN***3***")
						return val_1[0] + " " + val_3[0]
				if val_2 and val_3:
						print("PN***4***")
						return val_2[0] + " " + val_3[0]
				if val_1:
						print("PN***5***")
						return val_1[0]
				if val_2:
						print("PN***6***")
						return val_2[0]
				if val_3:
						print("PN***7***")
						return val_3[0]
				
				print("PN***8***")
				return ""

		def parse_between_lines(self):
				for index, content in enumerate(self.contents):
						#Note: Parse Next Line
						for kw in preceding_keywords:
								#if kw == content.strip():
								if kw in content.strip():
										print(f"Content--->{content.strip()}, kw--->{kw}")
										check_valid_keyword_to_extract = [content.strip().split(kw)[1]]
										print("parse_between_lines****1", check_valid_keyword_to_extract)
										words = list( filter( None, check_valid_keyword_to_extract ) )
										print("parse_between_lines****2", words)
										if len(words) > 0:
												continue
										try:
												print("***START***PROGRAM_NAME*****", content, "***KW***", kw)

												"""
												values_1, status = self.validate_each_value(remove_extra_spaces( self.contents[index + 1].strip() ) )
												if status:
														values_2, status = self.validate_each_value(remove_extra_spaces( self.contents[index + 2].strip() ) )
												if not status_2:
														continue
												values_3, status = self.validate_each_value(remove_extra_spaces( self.contents[index + 3].strip() ) )
												if not status_3:
														continue
												"""
												values_1, status = self.validate_each_value(remove_extra_spaces( self.contents[index + 1].strip() ) )
												#values_1, status = self.validate_each_value( [self.contents[index + 1].strip() ])
												if status:
														values_2, status = self.validate_each_value(remove_extra_spaces(self.contents[index + 2].strip() ))
												else:
														#values_1 = []
														values_2 = []
												if status:
														values_3, status = self.validate_each_value(remove_extra_spaces(self.contents[index + 3].strip() ))
												else:
														#values_1 = []
														#values_2 = []
														values_3 = []
												print(f"values_1-->{values_1}, values_2-->{values_2}, values_3-->{values_3}")
												#print("TRUE/FALSE-------->", self.is_valid_program_name(values_1, values_2, values_3))
												#values_1, values_2, values_3 = self.is_valid_program_name(values_1, values_2, values_3)
												print(f"values_1-->{values_1}, values_2-->{values_2}, values_3-->{values_3}")
												self.program_name = self.get_progrma_name(values_1, values_2, values_3)
												if self.program_name is not None:
														print("***VALIDATING_PROGRAM_NAME***")
														if self.validate_program_name():
																print("***PROGRAM_NAME_FOUND***")
																return
										except Exception as error:
												print("Error===>", error)
												pass
										"""
										if self.is_valid_program_name(values_1, values_2, values_3):
												self.program_name = self.get_progrma_name(values_1, values_2, values_3)
												print(f"*****>{self.program_name}*****")	
												print(f"************HERE--4--HERE==*{self.program_name}*")
											 
												if self.validate_program_name():
														print(f"***************HERE--5--HERE==*{self.program_name}*")
														return
												print(f"************HERE--6--HERE==*{self.program_name}*")
										 """
								#print(f"************HERE--7--HERE==*{self.program_name}*")
								if self.program_name == "":
										#Note: Parse Previous Line
										#print(f"************HERE--6.5--HERE==*{self.program_name}*")
										for kw in following_keywords:
												if kw == content.strip():
														print(f"************HERE--7--HERE==*{self.program_name}*")
														values = remove_extra_spaces(self.contents[index - 1].strip())
														#print("Program_NAME--follow-->", values, kw)
														if len(values) == 0:
																continue
														self.program_name = values[0] # .split('	')[0]

														#print(f"following_keywords*****>{self.program_name}*****")
														if self.validate_program_name():
																return


		def parse_within_line(self):
				print("************PROGRAM***NAME**WITHIN_LINE**********")
				for index, content in enumerate(self.contents):
						for kw in line_keywords:
								if kw in content:
										print(f"PROGRAM_NAME===>Content->{content}, KW-->{kw}")
										valid_words = validate_line(content, kw)
										print(f"PROGRAM_NAME===>VALID_WORDS->{valid_words}")
                    
										if valid_words is None:
												continue
										print("Program_NAME--->", valid_words)
										pn_1, status = self.validate_each_value(remove_extra_spaces( self.contents[index + 1]) )
										pn_2, status = self.validate_each_value(remove_extra_spaces( self.contents[index + 2]) )
										print(f"pn_1--->{pn_1},--pn_2---->{pn_2}")
										self.program_name = valid_words[0] + " " + self.get_progrma_name(pn_1, pn_2, [])
										print("WITHIN_LINE========>", self.program_name)
										"""
										if pn:
												self.program_name = valid_words[0] + " " + pn_1[0] + " " + pn_2[0]
										else:
												self.program_name = valid_words[0]
										"""
										print("WITHIN_LINE---pn_1__")
										if self.program_name.strip() in ["Number:"]:
												print("WITHIN_LINE---pn_2__")
												self.program_name = ""
												continue
										if self.validate_program_name():
												print("WITHIN_LINE---pn_3__")
												return
										print("WITHIN_LINE---pn_4__")

		
		def find_key_words(self):
				ignore = ['date', 'number', 'location']
				for index, content in enumerate(self.contents):
						for kw in possible_keywords:
								if kw in content:
										self.program_name = content.strip() + " " + self.contents[index+1]
										print("ProgramName--PossibleKeywords--->", self.program_name)
										for kwi in ignore:
												if find_pattern(kwi.lower(), self.program_name.lower()):
														print("--Found Error--", kwi)
														self.program_name = ""
														break
										if self.program_name == "":
												continue
										else:
												print("***Found ProgramName***")
												return
										return
	 
			
		def find_from_priority_keywords(self):

				for content in self.contents:
						for kw in priority_keywords:
								if kw in content:
										self.program_name = content
										return

		def refine_program_name(self):
				for kw in line_keywords:
						if kw in self.program_name:
								print("REFINING--PROGRAM_NAME=================*********************", self.program_name, "KW--->", kw)
								self.program_name = self.program_name.replace(kw, '')


		def find_through_product_code(self):
				keywords = ['Product Code:']
				val = ""
				for content in self.contents:
						for kw in keywords:
								if kw in content.strip():
										val = content.split(kw)[1].strip()
				if len(val) > 0:	
						for content in self.contents:
								if val in content.strip():
										self.program_name = content
										if self.validate_program_name():
												return

		#def identify_program_name(self):
		def extract(self):
				self.find_from_priority_keywords()
				if self.program_name== "":
						self.parse_between_lines()
				print("--------ProgramName-------", self.program_name)
				if self.program_name == '':
						self.parse_within_line()
				if self.program_name == '':
						self.find_key_words()
				if self.program_name == "":
						self.find_through_product_code()
				if self.program_name != "":
						self.refine_program_name()
						return True

				return True

