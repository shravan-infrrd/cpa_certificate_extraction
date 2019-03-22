#text_file = "./textfiles/21.txt"
import re
from lib.common_methods import remove_extra_spaces, validate_line, find_pattern, check_for_valid_string


preceding_keywords = ['has successfully completed', 'CERTIFICATE OF ATTENDANCE', 'has successfully completed the online course', 'Online Certification training:', 'Certificate of Attendance', 'Certificate of Completion', 'for participation in', 'for participation in', 'successfully completed', 'completion ot the course', 'entitled', 'for successfully completing', 'completed', 'For Successfully Completing', 'has successfully completed:', 'Has Successfully Completed the Course:', 'Has Successfully Completed the Course:', 'For successful completion of', 'for the successful completion of', 'has completed', 'has completed the group Internet-based course', 'nas success*u ly comoleted:', 'Forattending', 'For attending', 'FOR THE PROGRAM ENTITLED', 'Congratulations on the successful completion of', 'for successful completion of the course', 'Has Successtully Completed the Course:', 'COMPLETION OF THE FOLLOWING ', 'for successful completion of', 'For successfully completing:', 'FOR THE COURSE ENTITLED', 'For completion of', 'FOR SUCCESSFUL COMPLETION OF', 'HAS COMPLETED THE TRAINING COURSETITLED', 'HAS COMPLETED THE TRAINING COURSE TITLED', 'For successfully completing']

"""
Is hereby awardedto (the institute of internal)
"""
following_keywords = ['Course Name'] #, 'Is hereby awardedto', 'Is hereby awarded to']
line_keywords = ['Course Title:', 'for successfully completing:', 'for successfully completing', 'Program Title:', 'PROGRAM TITLE:', 'For successful completion of', 'Title.', 'Title:', 'for success‘ully comp et ng', 'Course:', 'Event Title:', 'tor successfully completing', 'Course Title', 'Subject:', 'Event:', 'NAME OF COURSE:', 'Course', 'Title of Training:', 'For Attending', 'For successfully completing the' ]


invalid_keywords = ['presented to', 'Awarded to', 'Date', 'Freserted to', 'successful', 'granted', 'Association of Cortificd', 'Association of Certified', 'Field of Study', 'Please', 'Program Location', 'CPE', 'Credits', 'CTEC', 'Participant', 'Sent', 'This is to ceruty that', 'This is to certify that', 'This is to', 'awardedthis', 'awarded this', 'preserted to', 'success‘ully', '@', 'certify that', 'Instructional Delivery Method', 'Attendee', 'Exam', 'Attendee Name:', 'SPONSOR', 'sponsor', 'PROGRAM TITLE:', 'program title', 'Successfully', 'successfully', 'ACKNOWLEDGES', 'THIS CERTIFIES THAT', 'this certifies that', 'for participation in', 'This certificate is presentedto', 'This certificate is presented to', 'Author', 'Congratulations', 'Self-Study Programs', 'CourseTitle', 'Course Title', 'DELIVERY METHOD', 'awardedto', 'awarded to', 'Location', 'CPEcredits', 'CPE credits', 'Event Dates', 'OBJECTIVE', 'Units', 'Has Successtully Completed the', 'Course Freld of Study', 'Course Field of Study', 'Course Number', 'Delivery Method Used', 'Type of InstructionalDelivery', 'Type of Instructional Delivery']

possible_keywords = ['Conference', 'Event', 'Webcast', 'Seminar', 'Review Course', 'Ethics:']

priority_keywords = ['(Part |)', 'Part |', 'PART 1', 'Module 1', 'Module |']

class ParseProgramName():

		def __init__(self, contents, name):
				self.contents = contents
				self.name = name
				self.program_name = ""

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
										self.program_name = ""
										return False

				print("ValidateProgramName**2", len(self.program_name.strip()))
				if len(self.program_name.strip()) <= 4:
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

		def validate_each_value(self, values, check_for_line_keywords=False):
				print("VALIDATION====PROGRAM_NAME===>", values)
				if not values:
						return [], True
				status = True
				if check_for_line_keywords:
								#print("VALIDATION====PROGRAM_NAME===>2", values[0])
								for kw in line_keywords:
										#print("VALIDATION====PROGRAM_NAME===>3", kw)
										if kw in values[0]:
												#print("VALIDATION====FOUND_LINE_KEYWORDS===>3", kw)
												status = False
				#print("=======STATUS===>", status)
				#try:
				if values[0] != "":
						print("***VALiDATE***1", self.check_invalid_keywords(values[0]))
						if not self.check_invalid_keywords(values[0]):
								return [], status
						print("***VALiDATE***2")
						if self.name != "":
								if find_pattern(self.name.lower(), values[0]):
										return [], status
						print("***VALiDATE***3")
						if ':' in values[0]:
								for k in ['ethics']:
										if find_pattern('ethics', values[0]):
												return [], status
						print("***VALiDATE***4", check_for_valid_string(values[0]))
						if not check_for_valid_string(values[0]):
								return [], status
						print("***VALiDATE***5")
						return values, status
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
										try:
												print("***START***PROGRAM_NAME*****", content, "***KW***", kw)
												values_1, status = self.validate_each_value(remove_extra_spaces( self.contents[index + 1].strip() ), True )
												if status:
														values_2, status = self.validate_each_value(remove_extra_spaces(self.contents[index + 2].strip() ), True )
												else:
														values_1 = []
														values_2 = []
												if status:
														values_3, status = self.validate_each_value(remove_extra_spaces(self.contents[index + 3].strip() ), True )
												else:
														values_1 = []
														values_2 = []
														values_3 = []
												#print(f"values_1-->{values_1}, values_2-->{values_2}, values_3-->{values_3}")
												#print("TRUE/FALSE-------->", self.is_valid_program_name(values_1, values_2, values_3))
												#values_1, values_2, values_3 = self.is_valid_program_name(values_1, values_2, values_3)
												print(f"values_1-->{values_1}, values_2-->{values_2}, values_3-->{values_3}")
												self.program_name = self.get_progrma_name(values_1, values_2, values_3)
												if self.program_name is not None:			 
														if self.validate_program_name():
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
														#print(f"************HERE--7--HERE==*{self.program_name}*")
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
								valid_words = validate_line(content, kw)

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
								return

		
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
				if self.program_name != "":
						self.refine_program_name()
						return True
				return True

