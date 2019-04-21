#text_file = "./text_files/22.txt"
from lib.common_methods import remove_extra_spaces, validate_line, hasNumbers, find_pattern
from lib.field_of_study_mapping import find_fos_match

field_of_studies = [ 'Finance-Technical', 'Accounting & Auditing', 'Accounting and Auditing', 'Administrativei Practice', 'Business Management & Organization', 'Communications', 'Computer Science', 'Economics', 'Ethics - Behavioral', 'Ethics - Regulatory', 'Finance', 'Marketing', 'Mathematics', 'Personal Development', 'Personnel/Human Resources', 'Production', 'Specialized Knowledge and Applications', 'Specialized Knowledge & Applications', 'Social Environment of Business', 'Statistics', 'Accounting - Governmental', 'Auditing - Governmental', 'Business Law', 'Management Advisory Services', 'Taxes', 'Communications and Marketing', 'Informational Technology - Technical', 'Information Technology', 'Computer Software & Applications', 'Business Management and Organization', 'SPECIALIZED KNOWLEDGE AND APPLICATIONS', 'Accounting (Governmental)', 'Auditing (Governmental)', 'Auditing (Govemmental)']


special_list = ['Auditing', 'Accounting', 'Specialized Knowledge', 'ACCOUNTING', 'AUDITING', 'BUSINESS MAN AGEMENT', 'MAS', 'TAXES', 'Business Management', 'Tax', 'Audit']

related_studies = ['Computer Software and Applications', 'Accounting & Auditing / Tax', 'Personnel/Human Resource', 'Personnel/HR', 'Regulatory Ethics', 'Professional Development', 'Behavioral Ethics', 'Management Services', 'A&A', 'Yellow Book', 'Professional Ethics', 'Fraud', 'Accounting Governmental', 'Auditing Governmental', 'Business Mgmt and Org', 'State Ethics', 'Cybersecurity Update', 'Taxation', 'Forensic Accounting', 'Forensic Accounting — Technical', 'Communications & Marketing', 'Management Advisory Services Basic Level', 'Ethics (Regulatory)', 'Computer Software & Applications — Non-Technical', 'Laws & Rules Ethics', 'Ethics/Regulatory Ethics', 'Taxes (in NY Taxation)', 'Governmental Accounting', 'Auditing - Webinar','Ethics', 'General Knowledge']


field_of_studies = field_of_studies + related_studies + special_list
#field_of_studies = list(set(field_of_studies))

pre_keywords = [ 'field of study:', 'For the successful completion of', 'sponsored by YH Advisors, Inc.', 'FOR THE PROGRAM ENTITLED', 'Field of Study', 'for successfully completing', 'bicld of Study', 'Course', 'CPE Fueid of Study.', 'field of study', 'Field Of Study:', 'SUBJECT AREA']

post_keywords = ['bicld of Study', 'bield of Study', 'Field of Study', 'Subject Area', 'Field ofStudy', 'NASBA Field of Study:', 'Curriculum:', 'Curriculum']

line_keywords = ['Field of Study:', 'Best Practices in', 'FieldofStudy:', 'Course Field of Study:', 'for successfully completing', 'Fieldof Study:', 'Recommended Field of Study:', 'in the subject area of', 'RecommendedField of Study:', 'Field ofStudy:', 'Ficld of Study:', 'NASBAField of Study:', 'Course Freld of Study:', 'NASBAField of Study', 'NASBA Recognized Field of Study:', 'NASBAField of Study: ', 'Fleld of Study Associated with Credit:', 'Number of CPE Credits']


class ParseFos():

		def __init__(self, contents, program_name):
				self.contents = contents
				self.field_of_study = []
				self.program_name = program_name
				self.line_index = -1

		def validate_with_existing_list(self, field):
				#print("validate_with_existing_list----->", field)
				for fos in field_of_studies:
						if fos.lower() in field.lower():
								#print(f"Validation_TRUE---->{fos.lower()}---->{field.lower()}")
								#print( ((len(field) - len(fos)) / len(fos) )) 
								#print( ((len(field) - len(fos)) / len(fos) )  > float(5 ))
								#print( (len(field.strip())) - len(fos.strip()) )
								if (len(field.strip())) - len(fos.strip()) == 0:
										#print("FOS-->VALIDATE_WITH_EXISTING_LIST-----SUCCESS----1")
										return True

								if (( (len(field) - len(fos))) / len(fos)  ) > float(5):
										#print("FOS-->VALIDATE_WITH_EXISTING_LIST-----FAILEDi----1")
										return False
								#print("FOS-->VALIDATE_WITH_EXISTING_LIST-----SUCCESS----2")
								return True
				#print("FOS-->VALIDATE_WITH_EXISTING_LIST-----FAILED----2")
				return False

		def check_if_present(self, fos):
				print('CHECK_IF_PRESENT--->', self.field_of_study)
				for fs in self.field_of_study:
						if fos.lower() in fs.lower():
								return True
				return False

		def parse_between_lines(self):
				for index, content in enumerate( self.contents ):
						for kw in pre_keywords:
								if kw in content.strip():
										#print(f"FOS0. Keyword--->{kw}, Content---->{content}")
										#if ':' not in self.contents[index+1].strip():	
										values = remove_extra_spaces( self.contents[index+1].strip())
										#print("parse_between_lines====>", values)
										if len(values) > 0:
												print("FOS1. FieldOfStudy---->", values)
												if self.validate_with_existing_list(values[0]):
														print("FOS1. FieldOfStudy---->", values[0]) 
														if not self.check_if_present(values[0]):
																print("FOUND----FOS-->", values[0])
																self.field_of_study.append(values[0] )
																#continue
																self.line_index = index
																return "following_line"

										values = remove_extra_spaces( self.contents[index+2].strip() )
										#print(f"values-->{values}, -->{len(values)}")
										if len(values) > 0 and len(values) < 5:
												#print("FOS2. FieldOfStudy---->", values)
												if self.validate_with_existing_list(values[0]): 
														if not self.check_if_present(values[0]):
																self.field_of_study.append( values[0])
																#continue
																self.line_index = index
																return "following_line"

				if len(self.field_of_study) == 0:
						for index, content in enumerate(self.contents):
								for kw in post_keywords:
										#print(f"content->{content}, kw -->{kw}")
										if kw in content.strip():
												values = remove_extra_spaces( self.contents[index-1].strip() )
												#if ':' not in values[0]:
												if len(values) == 0:
														continue
												for val in values:
														if self.validate_with_existing_list(val):
																if not self.check_if_present(val):
																		self.field_of_study.append(val)
																		self.line_index = index
																		return "previous_line"

		def parse_within_lines(self): 
				print("FOS--***parse_within_lines***")
				for index, content in enumerate(self.contents):
						for kw in line_keywords:
								if kw in content:
										print("FOS--START--->", kw)
										valid_words = validate_line(content, kw)
										print("FOS***START***", content, "***valid_words**", valid_words)
										if valid_words is None:
												continue
										print("FOS--parse_within_lines***>1" )
										#self.field_of_study = valid_words[0]
										for val in valid_words:
												print("FOS--parse_within_lines***>2", val, self.validate_with_existing_list(val))
												if self.validate_with_existing_list(val):
														print("FOS--parse_within_lines***>3", val )
														if not self.check_if_present(valid_words[0]):  
																print("FOS--FOS_HERE====>",val,  self.fos_check(val, content))
																if self.fos_check(val, content):
																		self.field_of_study.append(val)
																		return
										"""
										if self.validate_with_existing_list(valid_words[0]):
												if not self.check_if_present(valid_words[0]):  
														self.field_of_study.append(valid_words[0])
												#return
										"""
							
		def fos_check(self, fos, content):	
				print("FOS_CHECK---->", fos)
				if fos in ['Accounting', 'accounting', 'Auditing', 'auditing', 'ACCOUNTING']:
						if content in ['Accounting and Auditing', 'Accounting & Auditing / Tax', 'Accounting Governmental', 'Auditing Governmental', 'Accounting & Auditing', 'ACCOUNTING AND AUDITING', 'Accounting (Governmental)']:
								return False
				if fos in ['Specialized Knowledge']:
						if content in ['Specialized Knowledge and Applications', 'Specialized Knowledge & Applications', 'Specialized Knowledge and Applications', 'Specialized Knowledge & Applications', 'SPECIALIZED KNOWLEDGE AND APPLICATIONS' ]:
								return False
				if fos in ['Business Management']:
						if content in ['Business Management & Organization', 'Business Management and Organization', 'BUSINESS MAN AGEMENT', 'Business Mgmt and Org']:
								return False
				if fos in ['Information Technology']:
						if content in ['Information Technology - Technical', 'Informational Technology - Technical']:
								return False
				return True
			
 
		def extract_from_list(self):
				for fos in field_of_studies:
						#print(f"FOS--->{fos}")
						for index, content in enumerate(self.contents):
									
									if content.strip() == "":
											continue
									if (self.program_name.lower() in content.strip().lower()) or (content.strip().lower() in self.program_name.lower()):
											continue
									content = content.replace('(', '').replace(')', '')
									fos1 = fos.replace('(', '').replace(')', '')
									#if fos.lower() in content.lower():
									if find_pattern(fos1.lower(), content.lower().strip() ):
											#print(f"FOS**FIELF_OF_STUDY--->{fos}, --->CONTENT-->{content.strip()}<--")
											#self.field_of_study.append({"name": fos })
											#print("***FOS***###->1", fos)
											if fos in ['Accounting', 'accounting', 'Auditing', 'auditing', 'ACCOUNTING']:
													if content in ['Accounting and Auditing', 'Accounting & Auditing / Tax', 'Accounting Governmental', 'Auditing Governmental', 'Accounting & Auditing', 'ACCOUNTING AND AUDITING', 'Auditing (Governmental)']:
															continue
											if fos in ['Specialized Knowledge']:
													if content in ['Specialized Knowledge and Applications', 'Specialized Knowledge & Applications', 'Specialized Knowledge and Applications', 'Specialized Knowledge & Applications', 'SPECIALIZED KNOWLEDGE AND APPLICATIONS' ]:
															continue
											if fos in ['Business Management']:
													if content in ['Business Management & Organization', 'Business Management and Organization', 'BUSINESS MAN AGEMENT', 'Business Mgmt and Org']:
															continue
											if fos in ['Information Technology']:
													print("***FOS***###->2", fos)
													print("***FOS***###->2.1", content.strip())
													if content in ['Information Technology - Technical', 'Informational Technology - Technical']:
															print("***FOS***###->3", fos)
															continue
											print("***FOS***###->4", fos)
											print("***FOS***###->5", str(self.line_index))
											print("***FOS***###->6", index)
											if self.line_index != -1:
													print("***FOS***###->7", index - self.line_index)
													if (index - self.line_index ) > 2:
															continue
											if not self.check_if_present(fos):
													print("***FOS***adding FOS successfully***")
													self.field_of_study.append(fos)
													continue
											#return


		def extract(self):
				self.parse_within_lines()
				print("FOS***1***", self.field_of_study)
				if len(self.field_of_study) != 0:
						#self.field_of_study = list(set(self.field_of_study))
						#self.field_of_study = find_fos_match(self.field_of_study)
						return True

				parsed_line = self.parse_between_lines()
				print("FOS***2***", self.field_of_study)
				if len(self.field_of_study) != 0:
						#self.field_of_study = list(set(self.field_of_study))
						#self.field_of_study = find_fos_match(self.field_of_study)
						if parsed_line == "previous_line":
								return True
				print("FOS***3***", self.field_of_study)
				self.extract_from_list()
				print("FOS***4***", self.field_of_study)
				self.field_of_study = list(set(self.field_of_study))
				print("FOS***5***", self.field_of_study)
				#self.field_of_study = find_fos_match(self.field_of_study)
				return True


