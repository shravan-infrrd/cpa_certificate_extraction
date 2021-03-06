#text_file = "./text_files/22.txt"
import re
from lib.common_methods import remove_extra_spaces, validate_line, hasNumbers


pre_keywords = ['National Registry of CPE Sponsors Number:', 'National Registry of CPE Sponsors Numbcr:', 'Sponsorship Numbers:', 'NASBA Sponsor Registry Number:', 'Number:'] 
post_keywords = ['National Registry of CPE Sponsors Number']
line_keywords = ['Sponsor number :', 'NASBA National Registry of CPE Sponsors - Sponsor 10 Number', 'Sponsor Id#.', 'NASBA Sponsor registry number', 'NASBA Sponsor', 'NASBA -', 'National Registry of Sponsors If) Number -', 'Sponsor Id#', 'National Registry of CPE Sponsors ID#', 'National Registry of CPE Sponsors ID Number:', 'National Registry of CPE Sponsors 1D Number:', 'Natonal Registy', 'CPF Spongors ID Number', 'National Registry Sponsor No.', 'NASBA Sponsor ID', 'National Registry of CPE Sponsors ID:', 'National Registry Sponsor Number', 'Spenser License Numher', 'NASBA SPONSOR #', 'National Registry:', 'National Registry of CPE Sponsors ID Number', 'Natora Reg sty of CPE Socrac:s D8', 'CPE Credits earned:', 'NASBA Sponsor Registry Number', 'National Registry of CPE Sponsors 1D:', 'National Registry of CPE Sponsors [D:', 'Natona Reg stry of CPF Sponsors ID Number', 'Sponsors ID Number', 'Sponsors 1D Number:', 'Sponsors 1D Number', 'NASBA #', "NASBA's National Registry of CPE Sponsors - ID", 'Registry ID Nuanber:', 'NASBAsponsor#', 'NY Sponsor |O Number', 'CPE Sponsor ID #', 'NASBA Registry Provider #:', 'NASBA-', 'NASBA CPE SPONSOR REGISTRY NUMBER', 'NASBA SPONSOR', 'Nat cral Registry of CPE Sporsors ID#', 'CPE Sporsors ID#', 'Sponsor IO Number', 'NASBA National Registry of CPE Sponsors - Sponsor IO Number', 'NASBA National Registry of CPE Sponsors - Sponsor ID Number', 'Sponsor ID Number', 'Sponsor IO Number', 'ID Nnver', 'National Registry Sponsor Number:', 'FICPA Etrecs Provicer Number', 'Provider Number', 'Study C Numbe-', 'NASBASponsor Registry Number', 'QASSelf-Study:', 'NASBA:', 'Sponsor ID', 'NASBARegistry Sponsor Number', 'NASBA Registry ID:', 'Registry Identification Number:', 'NASBA ID', 'National Registry of CPE Sponsors #', 'NASBA Sponsor Number:', "NASBA's National Registry of CPE Sponsors -", 'National Registry of CPE Sponsors Number', 'Nationa) Registry of CPE Sponsors De', 'National Registry of CPE Sponsors [D#', 'NASBAIndentification #', 'NASBA Indentification #', 'Natora Reg sty of CP Sporsors [ID Numpe:', 'National Registry of CPE Sponsors Number:', 'Soonsers D:', 'National Registry of CPE Sponsors ID number', 'Sponsor Identification Number:', 'National Registry of CPE Sponsors #:', 'NACUBO sponsor ID is', 'National Registry of CPE Sponsors: ', 'NASBARegistry Provider #:', 'National Registry of CPE Sponsors', 'Sponsor Number:', 'Sponsor Id#:', 'Sponsor NASBA Number:', 'NASBASponsor Number', 'National Registry of CPF Sponsors ID:', 'Sponsor License Number', 'NASBA Regisiry Sponsor Number.', 'Sponsor ID #: ', 'NASBASponsor ID:', 'National Registm:', 'CPE Sponsors ID Number:', 'NASBAProvider #', 'Sponsorsaip ID Num>der', 'I.D. Number #', 'NASBA      #', 'NASBAsponsor #', 'NASBA sponsor Registry Number', 'National Registry ID#', 'National Registry.', 'Nat onal Registry of CPE Sponsors ID#', 'Sponsorsaip ID Number', 'NASBA —', 'NAS BA Sponsor Registry Number', 'SponsorId#:', 'National Registry of CPE Sponsors |ID#', 'NASBA', 'National Regletry:', 'Sponsor ID:', 'NASBA Registry Sponsor Number:', 'NASBA Registry Sponsor Number.', "Sponsor |d#:", "Sponsor Io#:", 'NASBA Sponsor registty number', 'Texas License:', 'NASBA National Registtry of CPE Sponsors and QAS Self Study ID Number', 'NASB A National Reoisiry of CPX Sponsors and QQ AN Selt Study TDD) Number', 'NASBA Registry 1D:', 'National RegistrySponsorNumber:', 'NASBA National Registey of CPE Sponsors - Sponsor 10 Number', '[.D. Number #', 'I.D. Number #', 'NASBA sponsor ID number:', 'commended Number of CPE Credits:']


class ParseSponsorId():

		def __init__(self, contents):
				self.contents = contents
				self.ids = []
				self.sponsor_id = ""

		def validate_sponsor_id(self):
				print("VALIDATION________SPONSOR_ID_________", self.sponsor_id, "_______")
				if not hasNumbers(self.sponsor_id):
						self.sponsor_id = ""
						return False


				if len(self.sponsor_id.strip()) <= 4 :
						self.sponsor_id = ""
						return False
				return True

		def get_sponsor_id(self):
				s_ids = re.findall('\d+', self.sponsor_id)
				print("s_ids====>", s_ids)
				if s_ids:
						return s_ids[0]
				else:
						return self.sponsor_id

		def parse_between_lines(self):
				for index, content in enumerate( self.contents ):
						for kw in pre_keywords:
								if kw in content.strip():

										values = remove_extra_spaces( self.contents[index+1].strip())
										if len(values) > 0:
												for val in values:
														if ':' not in val:
																self.sponsor_id = val
																if self.validate_sponsor_id():
																		#self.ids.append(self.sponsor_id)
																		self.sponsor_id = self.get_sponsor_id()
																		self.ids.append( {'name': 'NASBA', 'id': self.sponsor_id, 'score': ''} )
																		return
																		#continue
										if self.sponsor_id == "":
												try:
														values = remove_extra_spaces( self.contents[index+2].strip())
														if len(values) > 0:
																for val in values:
																		if ':' not in val:
																				self.sponsor_id = val
																				if self.validate_sponsor_id():
																						self.sponsor_id = self.get_sponsor_id()
																						#self.ids.append(self.sponsor_id)
																						self.ids.append( {'name': 'NASBA', 'id': self.sponsor_id, 'score': '' } )
																						return
																						#continue
												except:
														continue
										"""
										if ':' not in self.contents[index+1].strip():
												self.sponsor_id = remove_extra_spaces( self.contents[index+1].strip())[0]
										if self.sponsor_id == "":
												if ':' not in contents[index+2].strip():
														self.sponsor_id = remove_extra_spaces( self.contents[index+2].strip() )[0]
										"""

				if self.sponsor_id == "":
						for index, content in enumerate(self.contents):
								for kw in post_keywords:
										if kw in content.strip():
												values = remove_extra_spaces( self.contents[index-1].strip() )
												for val in values:
														if ':' not in val:
																self.sponsor_id = val
																if self.validate_sponsor_id():
																		#self.ids.append(self.sponsor_id)
																		self.sponsor_id = self.get_sponsor_id()
																		self.ids.append( {'name': 'NASBA', 'id': self.sponsor_id, 'score': '' } )
																		return
												#if ':' not in values[0]:
												#		 self.sponsor_id = values[0]


		def parse_within_lines(self): 
				for index, content in enumerate(self.contents):
						for kw in line_keywords:
								if kw in content:
										print(f"****SPONSOR_ID******>kw-->{kw}, content-->{content}" )
										valid_words = validate_line(content, kw)
										print(f"***Valid_words--->{valid_words}")
										if valid_words is None:
												print("***SPONSOR_id***1")
												continue	
										elif len(valid_words) == 0:
												print("***SPONSOR_id***2")
												continue
										print("***SPONSOR_id***3")
										self.sponsor_id = valid_words[0]
										sponsor_id = re.findall(r"\d{1} \d{4} \d{1}", self.sponsor_id)
										if len(sponsor_id) > 0:
												self.sponsor_id = self.sponsor_id.replace(' ', '')
										words = self.sponsor_id.split(' ')
										self.sponsor_id = words[0].split(')')[0]
										if self.validate_sponsor_id():
												print("***SPONSOR_id***4")
												print("***SPONSOR_id***4.5")
												self.sponsor_id = self.get_sponsor_id()
												#self.ids.append(self.sponsor_id)

												self.ids.append( {'name': 'NASBA', 'id': self.sponsor_id, 'score': '' } )
												return

								
		def extract(self):
				self.parse_within_lines()
				if self.sponsor_id == "":
						self.parse_between_lines()
				return True


