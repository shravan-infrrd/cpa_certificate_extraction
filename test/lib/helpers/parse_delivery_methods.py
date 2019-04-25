#text_file = "./text_files/22.txt"
from lib.common_methods import remove_extra_spaces, validate_line, hasNumbers
from lib.delivery_format_mapping import map_with_given_list

pre_keywords = ['Delivery method:', 'CPEDelivery Method', 'CPE Delivery Method']
post_keywords = ['Delivery Method']
line_keywords = ['Field of Study.', 'Program Location:', 'Format:', 'Delivery Method:', 'Instructional Delivery Method -', 'Method Used:', 'Delivery Method', 'Delivery Method Used:', 'Instructional Delivery Method:', 'Program Oelivery Mode', 'Instructional Method:', 'DELIVERY METHOD:', 'NASBARegistry Sponsor Number', 'Oeltvery Method', 'Delivers Method:', 'Program Delivery Mode', 'Instructional delivery method-', 'Instructional/Delivery Method:', 'Instructional delivery method:']

delivery_method_lists = [ 'Interactive Self Study', 'Group live', 'Group Internet based', 'QAS Self study', 'Blended learning', 'Nano learning', 'Group Internet-Based', 'Self-Study', 'Self Study', 'Group-Intemet Based', 'Group-live', 'Group - Internet-Based', 'Group-Live', 'Group Internet', 'Webcast', 'Live Presentation', 'Group Intemet Based', 'Group - Internet Based', 'Internet Based', 'Group [nternet- Based', 'Group Program', 'Group Study', 'Conferences', 'Internet-Based', 'Group ‘rternet basea', 'Group Lve', 'Virtual group live', 'Group-Internet', 'Webinar', 'Group - Live', 'Virtual Instructor-Led', 'GroupInternet', 'GroupLive', 'Group/Live', 'Group: Live', 'Group intemet-based', 'Group-Internel Based', 'Group-Interet Based', 'Group-Intemet Based', 'Group-Infernel Based', 'Groupod', 'roup - Intemet-Bas', 'intemet', 'internel', 'interet', 'Group-Intermet Based', 'Group-Interet Based', 'Group-Internel Based', 'Live seminar', 'Group   Internct-Based', 'QAS Study']

invalid_keywords = ['CPE']

class ParseDeliveryMethod():

		def __init__(self, contents, sponsor):
				self.contents = contents
				self.delivery_method = ""
				self.sponsor = sponsor

		def delivery_method_for_ey(self, content):
				methods = content.split('[]')
				for method in methods:
						if '[X]' in method:
								print("***DELIVERY_METHOD_FOR_EY***", method.split('[X]')[-1])
								data = method.split('[X]')[-1]
								self.delivery_method = data
								return

		def validate_delivery_method(self):
				if self.delivery_method is None:
						self.delivery_method = ""
						return False

				for dml in delivery_method_lists:
						#print("dml====>", dml.lower(), "====>", self.delivery_method)
						if dml.lower() in self.delivery_method.lower():
								return True
				for kw in invalid_keywords:
						if kw.lower() in self.delivery_method.lower():
								self.delivery_method = ""
								return False
				self.delivery_method = ""
				return False


		def get_valid_value(self, index):
				for i in range(index+1, index+2):
						#if ':' not in self.contents[i].strip():
						values = remove_extra_spaces( self.contents[ i ].strip())
						print("1-Before-get_valid_value", values)
						for val in values:
								self.delivery_method = val
								if self.delivery_method is None:
										continue
								if self.validate_delivery_method():
										return


		def parse_between_lines(self):
				print("===========================1=============================")
				for index, content in enumerate( self.contents ):
						for kw in pre_keywords:
								if kw in content.strip():
										#print("*****START*****", content)
										#print("DeliveryMethod**>", kw)
										self.get_valid_value(index)
										#print("*****END*******", kw)
										#print("2-Before-get_valid_value")
										if self.validate_delivery_method():
												return
										

				print(f"===========================3=============================")
				if self.delivery_method == "":
						for index, content in enumerate(self.contents):
								for kw in post_keywords:
										if kw in content.strip():
												#print("Index1-->", self.contents[index].strip())
												#print("Index2-->", self.contents[index-1].strip())
												values = remove_extra_spaces( self.contents[index-1].strip() )
												#print("*****START****", content)
												#print("values->", values)
												#print("*****END******", kw)
												for val in values:
														if ':' not in val:
																self.delivery_method = val
																if self.validate_delivery_method():
																		return
												"""
												if ':' not in values[0]:
														self.delivery_method = values[0]
														print("3-Before-get_valid_value")
														if self.validate_delivery_method():
																return
												"""

		def parse_within_lines(self): 
				for index, content in enumerate(self.contents):
						for kw in line_keywords:
								if kw in content.strip():
										valid_words = validate_line(content, kw)
										if valid_words is None:
												continue
										self.delivery_method = valid_words[0]
										#print("4-Before-get_valid_value")
										if self.validate_delivery_method():
												return
								
		def extract_from_list(self):
				print("***DELIVERY_METHOD***extract_from_list***")
				for dm in delivery_method_lists:
						for content in self.contents:
									if dm.lower() in content.lower():
											print("***>DM***>", dm)
											if self.sponsor.strip() == "EY":
													print("***DELIVERY_METHOD_FOR_EY***1")
													self.delivery_method_for_ey(content)
													if self.validate_delivery_method():
															return
											self.delivery_method = dm
											return


		def extract(self):
				self.parse_within_lines()
				print(f"1***DELIVERY_METHOD****{self.delivery_method}")
				if self.delivery_method == "":
						self.parse_between_lines()
				print(f"2***DELIVERY_METHOD****{self.delivery_method}")
				if self.delivery_method == "":
						self.extract_from_list()
				print(f"3***DELIVERY_METHOD****{self.delivery_method}")
				if self.delivery_method != "":
						self.delivery_method = map_with_given_list(self.delivery_method)
				print(f"4***DELIVERY_METHOD****{self.delivery_method}")
				return True


