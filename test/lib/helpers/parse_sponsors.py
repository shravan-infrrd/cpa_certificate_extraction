#text_file = "./text_files/22.txt"
from lib.common_methods import remove_extra_spaces, validate_line, hasNumbers, find_pattern
from lib.sponsor_list import sponsor_lists

pre_keywords = [] 
post_keywords = []
line_keywords = ['iS registered', 'is registeres', 'is registered', '0 roguterod', 'is registeced', 'ts registered', 'SPONSOR:', "1's registered", '1s registered', 'Sponsor:']
special_keywords	= ['sponsored by', 'CPE Sponsor Name', "Program Sponsor's Name and Address", "Sponsor:", 'Name of Provider:']

sponsor_list = ["AICPA", "Deloitte", "Becker Professional Education", "Intuit", "Optiv Security", "FICPA", "KPMG", "EY", "CPA Academy", "Becker", "Beene Garter LLP", "Checkpoint Learning", "PricewaterhouseCoopers LLP", "PWC", "Deloitte LLP", "MACPA", "CPAAcademy.org", "CPAwebengage, Inc.", "Wolters Kluwer", "Grant Thornton LLP", "The Institute of Internal Auditors", "Ernst & Young LLP", "Learning.net", "KPMG LLP", "SC&H Group", "Association of International Certified Professional Accountants", "Thomson Reuters", "RSM", "HoganTaylor LLP", "Western CPE", "MICPA", "Practising Law Institute", "TSCPA", "Plain-English Accounting", "Surgent McCoy CPE, LLC", "Ernst & Young", "Surgent", "OSCPA", "VSCPA", "PricewaterhouseCoopers", "RSM US LLP", "AuditSense", "Becker CPE", "Workiva", "DTTL", "BKD, LLP", "KPMG Executive Education", "Foundation for Accounting Education", "PLI", "ACFE", "Association of Certified Fraud Examiners", "Grant Thornton", "Learnlive Technologies", 'Robert Half', 'The Madray Group', 'The Madray Group, Inc.', 'CPE Solutions, LLC', 'Cliftor LarsonAller LLP', 'SourceMedia Inc.', 'SourceMedia Inc', 'Proformative', 'Perry Glen Moore', 'CPA Crossings', 'CPE DepotInc', 'Financial Accounting Foundation', 'FASB', 'Tennessee Valley Authority', 'Accountants Education Group', 'The CalCPA Education Foundation', 'Sisterson & Co. LLP', 'Sisterson & Co', 'PricewaterhouseCoopersLLP']
sponsor_list = sponsor_list + sponsor_lists
sponsor_list = list(set(sponsor_list))

extra_list= ["ASSOCIATION OF CERTIFIED FRAUD EXAMINERS", 'Plaio-English Accounting', 'pliedu', 'the Institute of Internal Auditors', 'WAthe Institute of Internal Auditors', 'Institute of Internal Auditors', 'THOMSON REUTERS', 'The Virginia Society of CPAs', 'Wes:ern CPE', 'Plain-English Acooanting', 'Plain-English Accoanting', 'schoolefbookkeeping', 'The ASCPA CPE', 'Armanino LLP', "Accounting & Financial Women's Alliance", "Corporate Finance", "Management Concepts", 'Adaptive Insights', 'DCB Holding Ltd', 'Plam-English Accounting', 'AudioSolutionZ', 'Dixon Hughes Goodman LLP', 'STEIN SPERLING', 'Frazier & Deeter, LLC', 'Tate & Tryon', 'HogantTaylor', 'HoganTaylor']

sponsor_list = sponsor_list + extra_list

class ParseSponsors():

		def __init__(self, contents, program_name):
				self.contents = contents
				self.sponsor = ""
				self.program_name = program_name

		def validate_sponsor(self):
				for sponsor in sponsor_list:
						if find_pattern(sponsor.lower(), self.sponsor.lower()):
								print(f"sponsor-->{sponsor}, ===>{self.sponsor}")	
								sp = self.sponsor[ self.sponsor.find(sponsor) : (self.sponsor.find(sponsor) + len(self.sponsor))]
								print("SP===>", sp)
								if sp == "":
										continue
								self.sponsor = sp 
								return True
				return False

		def fetch_valid_sponsor(self, words):
				for wrd in words:
						#print(f"SPONSORS-------->{wrd}")
						if len(wrd) >= 3:
								return wrd

		def parse_between_lines(self):
				for index, content in enumerate( self.contents ):
						for kw in pre_keywords:
								if kw == content.strip():
										if ':' not in self.contents[index+1].strip():
												self.sponsor = remove_extra_spaces( self.contents[index+1].strip())[0]
												if self.validate_sponsor():
														return
										if self.sponsor == "":
												if ':' not in contents[index+2].strip():
														self.sponsor = remove_extra_spaces( self.contents[index+2].strip() )[0]
														if self.validate_sponsor():
																return

				if self.sponsor == "":
						for content in self.contents:
								for kw in post_keywords:
										#if kw in content.strip():
										if find_pattern(kw.lower(), content):
												values = remove_extra_spaces( self.contents[index-1].strip() )
												if ':' not in values[0]:
														self.sponsor = values[0]
														if self.validate_sponsor():
																return


		def parse_within_lines(self): 
				for index, content in enumerate(self.contents):
						for kw in line_keywords:
								if kw in content:
										#print(f"***START***SPONSOR***", content, "***KW***", kw)
										valid_words = remove_extra_spaces( content.split(kw)[0].strip() )
										print("valid_words*****", valid_words) 
										if valid_words is None:
												continue
										print("SPONSOR*****1")
										for val in valid_words:
												print("SPONSOR*****2", val)
												if 'ID' not in val:
														print("SPONSOR*****3")
														self.sponsor = val
														print("SPONSOR*****4", self.validate_sponsor())
														if self.validate_sponsor():
																print("SPONSOR*****5", self.sponsor)
																return
										try: 
												valid_words = remove_extra_spaces( content.split(kw)[1].strip() )
												if valid_words is None:
														continue
												for val in valid_words:
														if len(val) >= 3:
																if 'ID' not in val:
																		self.sponsor = val
																		if self.validate_sponsor():
																				return
										except:
												continue

		
				if self.sponsor == "":
						for content in self.contents:
								for kw in special_keywords:
										if kw in content:
												valid_words = remove_extra_spaces(content.split(kw)[1].strip())
												if valid_words is None:
														continue
												elif len(valid_words) == 0:
														continue
												self.sponsor = self.fetch_valid_sponsor(valid_words)
												if self.validate_sponsor():
														return

		def extract_from_list(self):
				for content in self.contents:
						if self.program_name.lower() not in content.strip().lower():
								for sp in sponsor_list:

										if find_pattern(sp.lower(), content.lower()):
												self.sponsor = sp
												return


								
		def extract(self):
				print("***SPONSORS***1")
				self.parse_within_lines()
				print("***SPONSORS***2")
				if self.sponsor == "":
						print("***SPONSORS***3")
						self.parse_between_lines()
				if self.sponsor == "":
						print("***SPONSORS***4")
						self.extract_from_list()
				print("***SPONSORS***5")
				return True


