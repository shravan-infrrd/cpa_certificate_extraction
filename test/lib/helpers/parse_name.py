#text_file = "./text_files/21.txt"
from lib.common_methods import remove_extra_spaces, validate_line, hasNumbers, find_pattern
import re

preceding_keywords = ['This certifies that', 'certifies that', 'Attendee', 'Certifies That', 'Attendee Name:', 'This certificate is presented to', 'Presents this Certificate of Completion to', 'Gg CalCPA																		 GS FOUNDATION', 'This certificate is presentedto:', 'Certificate of Completion', 'This certificate is presented to:', 'PRESENTED TO', "Participant's Name", "FOUNDATION", 'presented to', 'Freserted to', 'granted to', 'This is to ceruty that', 'Is hereby awardedto', 'Is hereby awarded to', 'awarded to', 'awardedto', 'Certificate of C completion', 'This certificate is awarded to', 'grantedto', 'Is hereby.grantedto', 'CERTIFICATE OF ATTENDANCE']

following_keywords = ['Has successfully completed the QuickBooks', "Participant's Name", 'for successfully completing', 'has successfully completed', 'Has Successfully Completed the Course:', 'Has successfully completed', 'UF,orattending', 'has completed the QASSelf-Study course', 'has completed the', 'FOR SUCCESSFUL COMPLETION OF', 'Participant Name', 'who haspursued studies and completed all the', 'who has pursued studies and completed all the']
#name_keywords = ['Attendee’s Name:', '\ Attendee’s Name:', 'V Attendee’s Name:', 'Awardedto:', 'Participant Name:', 'This certificate is presented to', 'Awarded to:']
line_keywords = ['Presents a Certification of Completion to:', 'Attendee’s Name:', '\ Attendee’s Name:', 'V Attendee’s Name:', 'Awardedto:', 'Participant Name:', 'This certificate is presented to', 'Awarded to:', 'This certifies that', 'Attendee:', 'NAME OF ATTENDEE.', 'Nameof Participant:', 'Name:', 'Attendee Name:', 'This certificate is presented to:', 'Name of Participant:', 'NAME OF PARTICIPANT:', 'Participant Name', 'Student', 'This certificate 1s presented to:', 'this certificate is presented to.', 'Name ofParticipant:', 'this certificate is presented to:', 'Congratulations,', 'Participant Name:', 'This to certify that', '[his certificate is presented to:', 'This certificate ts presented to', 'Th i s c e r t i f i e s t h a t', 'This c e r t i f i e s t h a t', 'c e r t i f i e s t h a t', 't h a t', 'to:', 'Thiscertificate ispresentedto', 'presentedto', 'To:', 'This      certifies that', 'certifies that']

invalid_words = ['Freserted to', 'Presented to', 'this', 'that', 'Awarded to', 'Program', 'CPE', 'Firm:', 'Participant', 'Sent', 'CERTIFICATION', '@', 'Issue', 'Attendee Name:', 'Instructional Delivery Method', 'Successful completion of:', 'ATTENDED', 'attended', 'SPONSOR', 'sponsor', 'for successfully completing', 'Individual', 'DATE', 'TIME', 'Certificate ofCompletion', 'Certificate of Completion', 'Congratulations', 'awardedto', 'awarded to', 'For successtully completing', 'TSCPA', 'Credits', 'SCalCPA', 'Street', 'Application', 'PRESENTED BY', 'Pittsburgh', 'ws DEN', 'Location', 'Tithe', 'Middle', 'Certificate Logo', 'IRS Course', 'Successful campletion of', 'stitute', 'institute', 'Number', 'AUDITING', 'PLANS', 'CPA Crossing', 'minute hour', 'Partici', 'Participant', 'http', 'Details', 'Affirmation', 'COMPLIANCE AUDITS', 'EDITION', 'Risk', 'Fundamentals', 'Review by', 'Instructor', 'Quality', 'Scheme', 'to:', 'Arizona', 'Internal Audit', 'PROVIDER', 'Astute CPA', 'Author']

invalid_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

class ParseName():

		def __init__(self, contents):
				self.contents = contents
				self.name = ""

		def cross_check_name(self):
				import probablepeople as pp
				name = pp.parse(self.name)
				print("Cross Check Name ---->", name)
				if len(self.name.strip().split(' ')) == 1 and len(name) >1:
						self.name = ""
						return False
				if len(name) == 1:
						if name[0][1] in ['GivenName', 'Surname']:
								return True
						else:
								self.name = ""
								return False
				elif len(name) >=3:
						count = 0
						for n in name:
								if n[1] in ['GivenName', 'Surname', 'MiddleInitial']:
										count = count + 1
						print("Count Val--->", count)
						if count < 1:
								self.name = ""
								return False
						return True
				elif len(name) == 2:
						count = 0
						for n in name:
								if n[1] in ['GivenName', 'Surname', 'CorporationName']:
										count = count + 1
						if count == 0:
								self.name = ""
								return False
						return True
				elif len(name) != 1:
						return True
				else:
						print("cross_check_name====>returning-->", self.name)
						self.name = ""
						return False
				
		

		def validate_name(self):
				print("***NAME***validation called", self.name)
				for kw in invalid_words:
						#print(f"keyword --> {kw.lower()} ===> {self.name.lower()}")
						if kw.lower() in self.name.lower():
								print("NAME-ERROR--0")
								print("True condition", kw, '**', self.name)
								self.name = ""
								return False
		
				for in_name in invalid_names:
						if find_pattern(in_name, invalid_names):
								self.name = ""
								return False
				print("****NAEM***FOUND***", self.name)
				if len(self.name.split(' ')) > 4:
						print("NAME-ERROR--1")
						self.name = ""
						return False
				if len(self.name.split(' ')[0]) <= 2:
						print("NAME-ERROR--1.5", self.name.split(' ')[0])
						if "." not in self.name:
								self.name = ""
								return False
				if hasNumbers(self.name):
						print("NAME-ERROR--2")
						if '(' in self.name or ')' in self.name or '-' in self.name:
						#if self.name in ['(', ')', '-']
								pass
						else:
								print("NAME--ERROR--2.1")
								self.name = ""
								return False
				print("NAMELENGTH---->", len(self.name))
				if len(self.name.strip()) <= 4:
						print("NAME-ERROR--3")
						self.name = ""
						return False
				print("NAME-FOUND-SUCCESS-----", self.name)
				return True

		def parse_between_lines(self):
				for index, content in enumerate(self.contents):
						#Note: Parse Next Line
						empty_content = True
						if content.strip() != "":
								flag = False
						for kw in preceding_keywords:
								#print(f"START***NAME**content=={content.strip()},***kw=={kw}")
								if kw.lower() in content.strip().lower():
										#print("1*****************NAME*****************", kw)
										values = remove_extra_spaces( self.contents[index + 1].strip() )
										if not values:
												values = remove_extra_spaces( self.contents[index + 2].strip() )
	
										#print("2*****************NAME*****************", values)
										for val in values:
												#print("NAME_VALIDATION=========>", val) 
												self.name = val
												word = 'successfully completed'
												if word.lower() in self.name.lower():
														if len(self.name.split(' ')) > 4:
																if word in self.name:
																		self.name = self.name.split(word)[0]
																		if len(self.name.split(' ')) > 4:
																				self.name = ""
																				continue
																		print("2.0*****************NAME*****************", self.name)
																		if self.validate_name():
																				print("2.01*****************NAME*****************", )
																				if self.cross_check_name():
																						print("2.02*****************NAME*****************", self.name)
																						return
																#print("2.1*****************NAME*****************", self.name)
																self.name = ""
																continue
												#print("3*****************NAME*****************", self.name)
												if self.validate_name():
														if self.cross_check_name():
																return
										try:
												if self.name == "":
														if empty_content:
																continue
														values = remove_extra_spaces( self.contents[index + 2].strip() )
														if len(values) == 0:
																values = remove_extra_spaces( self.contents[index + 3].strip() )
																
														#print("4*****************NAME*****************", values)
														for val in values:
																#print("4*****************NAME*****************", values)
																self.name = val
																word = 'successfully completed'
																if word.lower() in self.name.lower():
																		if len(self.name.split(' ')) > 4:
																				if word in self.name:
																						self.name = self.name.split(word)[0]
																						if len(self.name.split(' ')) > 4:
																								self.name = ""
																								continue
																						if self.validate_name():
																								#print("4.01*****************NAME*****************", self.name)
																								if self.cross_check_name():
																										#print("4.02*****************NAME*****************", self.name)
																										return
																				#print("4.1*****************NAME*****************", self.name)
																				self.name = ""
																				continue
																#print("5*****************NAME*****************", val)
																if self.validate_name():
																		#print("5.01*****************NAME*****************", self.cross_check_name())
																		if self.cross_check_name():
																				#print("5.02*****************NAME*****************", val)
																				return
																#print("5*****************NAME-FAILED*****************", val)
										except:
													continue

								#print("5*****************NAME*****************", content.strip())
								if self.name == "":

										#Note: Parse Previous Line
										for kw in following_keywords:
												#print("5*****************NAME*****************", kw)
												if kw in content.strip():
												#if kw == content.strip():
														print(f"***NAME****content=={content.strip()}===kw{kw}")
														values = remove_extra_spaces(self.contents[index - 1].strip())
														print("values---->1", values)
														for val in values:
																print("NAME---val-1", val)
																if ':' in val:
																		continue
																self.name = val
																print("NAME---val-2", self.name)
																word = 'successfully completed'
																if word.lower() in self.name.lower():
																		print("NAME---val-3", self.name)
																		self.name = self.name.split(word)[0]
																print("NAME---val-4", self.name)
																if self.validate_name():
																		print("NAME---val-5", self.name)
																		if self.cross_check_name():
																				print("4.021*****************NAME*****************", self.name)
																				return
																		#return
														values = remove_extra_spaces(self.contents[index - 2].strip())
														#print("values---->2", values)
														for val in values:
																#print("NAME---val", val)
																if ':' in val:
																		continue
																self.name = val
																if self.validate_name():
																		if self.cross_check_name():
																				print("4.022*****************NAME*****************", self.name)
																				return
																		#return

														values = remove_extra_spaces(self.contents[index - 3].strip())
														print("values---->", values)
														for val in values:
																print("NAME---val", val)
																if ':' in val:
																		continue
																self.name = val
																if self.validate_name():
																		return





		def parse_within_line(self):
				words = ["has successfully completed", 'for successfully completing', ', on having successfully completed', 'for successfully completing this course']
				print("parse_name_within_line*********")
				for content in self.contents:
						for kw in line_keywords:
								if kw in content:
										print(f"Content-->{content}, kw-->{kw}")

										#print("1***START***NAME", content, "**kw**", kw)
										valid_words = validate_line(content, kw)
										print("2***START***NAME", valid_words)
										if valid_words is None:
												continue
										#print("3***START***NAME", valid_words)
										#if ':' in valid_words[0]:
										#		continue
										print("4***START***NAME", self.name)
										self.name = valid_words[0]
										print("5***START***NAME", self.name)

										for word in words:
												print("WORD---->", word)
												if word.lower() in self.name.lower():
														print("WORD_MATCH---->", word)
														self.name = self.name.split(word)[0]
														break
				
										if '(' in self.name:
												self.name = self.name.split('(')[0]
	
										print("6***START***NAME", self.name)
										if self.validate_name():
												#print("****END***NAME")
												return

		def parse_line_without_keywords(self):
				print("***parse_line_without_keywords***")
				kw = ', CPA'
				keywords = [', CPA', '#CPA'] 
				ignore_keywords = ['Participant Name:', 'LECTURER:']
				for content in self.contents:
						for kw in keywords:
								if kw in content:
										if	content.lower() in ['instructor']:
												continue
										print("=========parse_line_without_keywords=====1", content.split(kw)[0])
										self.name = content.split(kw)[0].strip()
										print("=========parse_line_without_keywords=====2", self.name)
										for kwi in ignore_keywords:
												if kwi in self.name:
														self.name = self.name.split(kwi)[-1].strip()
														print("=========parse_line_without_keywords=====3", self.name)
														if self.validate_name():
																return
														else:
																self.name = ""
																continue
												else:
														print("=======parse_line_without_keywords====4", self.name)
														if self.validate_name():
																print("=======parse_line_without_keywords====5", self.name)
																return
														print("=======parse_line_without_keywords====6", self.name)


		def parse_approx_name(self, exception=False):
				print("***parse_approx_name***")
				import probablepeople as pp
				#print("***parse_approx_name***")
				for content in self.contents:
						print("Content---->", content.strip())
						values = content.split("	")
						for val in values:
								#content = val
								if val.strip() == "":
										continue
								flag = False
								print("1_FLAG--->NAME", flag)
								for kw in ["Presenters", "Author", 'Instructor', 'Presenter']:
										val = val.strip().replace("\\", "")
										print("VALIDATION===>", kw in val.strip())
										#print("2_FLAG--->NAME", flag)
										if kw in val.strip():
												flag = True
												break
								print("3_FLAG--->NAME", flag)
								if flag:
										continue
								print("****************START**********************")
								print("NAME_Content---->", val.strip())
								p = pp.parse(val)
								print("NAME_Content---->", p)
								username = ""
								firstname = ""
								surname		= ""
								middlename = ""
								#print(p)
								for index, word in enumerate(p):
							 
										if word[1] == "GivenName":
												firstname = firstname + word[0]
												username = username + " " + firstname
										if word[1] == "MiddleInitial":
												middlename = middlename + word[0]
												username = username + " " + middlename
										if word[1] == "Surname":
												surname = surname + word[0]
												username = username + " " + surname
								
										if exception:
												if len(p) > 3:
														continue
												if any(char.isdigit() for char in word[0]):
														continue
												if word[1] == "CorporationName":
														username = username + " " + word[0]
							 
								
										#print(f"USERNAME---1--->{username}")
										if firstname != "" and surname != "":
												#print(f"USERNAME---2--->{username}")
												self.name = username.strip()
												#print(f"USERNAME---3--->{self.name}")
												#print(f"USERNAME---3.1--->{self.validate_name()}")
												if self.validate_name():
														#print(f"USERNAME---4--->{self.name}")
														return

								#print("USERNAME------<*", username) 
								if	username:
										u_names = username.split(' ')
										u_names = list( filter( None, u_names ) )
										print("USERNAME------<", u_names) 
										if len(u_names) < 3 and len(u_names) > 1:
												self.name = username.strip()
												regex = re.compile('[:]') 
												if (regex.search(username.strip()) == None):
														if self.validate_name():
																return username
														else:	
																self.name = ""
												else:
														self.name = ""
								print("USERNAME------<*!", username) 
								print("****************END**********************")


		"""										
		def parse_approx_name1(self, exception=False):
				print("***parse_approx_name***")
				import probablepeople as pp
				#print("***parse_approx_name***")
				for content in self.contents:
						print("Content---->", content.strip())
						if content.strip() == "":
								continue
						flag = False
						print("1_FLAG--->NAME", flag)
						for kw in ["Presenters", "Author", 'Instructor']:
								content = content.strip().replace("\\", "")
								#print("VALIDATION===>", kw in content.strip())
								#print("2_FLAG--->NAME", flag)
								if kw in content.strip():
										flag = True
										break
						#print("3_FLAG--->NAME", flag)
						if flag:
								continue
						print("NAME_Content---->", content.strip())
						p = pp.parse(content)
						print("NAME_Content---->", p)
						username = ""
						firstname = ""
						surname		= ""
						middlename = ""
						#print(p)
						for index, word in enumerate(p):
					 
								if word[1] == "GivenName":
										firstname = firstname + word[0]
										username = username + " " + firstname
								if word[1] == "MiddleInitial":
										middlename = middlename + word[0]
										username = username + " " + middlename
								if word[1] == "Surname":
										surname = surname + word[0]
										username = username + " " + surname
	
								if exception:
										if word[1] == "CorporationName":
												username = username + " " + word[0]
					 

								print(f"USERNAME---1--->{username}")
								if firstname != "" and surname != "":
										print(f"USERNAME---2--->{username}")
										self.name = username.strip()
										print(f"USERNAME---3--->{self.name}")
										print(f"USERNAME---3.1--->{self.validate_name()}")
										if self.validate_name():
												print(f"USERNAME---4--->{self.name}")
												return
						print("USERNAME------<", username) 
		"""

		def extract(self):
				self.parse_between_lines()
				print("***************************NAME******************************0", self.name)
				if self.name == '':
						self.parse_within_line()
				print("***************************NAME******************************0.1", self.name)
				if self.name == '':
						self.parse_line_without_keywords()
				print("***************************NAME******************************0.2", self.name)
				if self.name == '':
						print("***************************NAME******************************1", self.name)
						self.parse_approx_name()
						print("***************************NAME******************************2", self.name)
				if self.name == "":
						self.parse_approx_name(True)
				print("***************************NAME******************************3", self.name)
				return True

