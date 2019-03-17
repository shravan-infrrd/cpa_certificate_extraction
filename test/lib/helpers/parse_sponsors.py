#text_file = "./text_files/22.txt"
from lib.common_methods import remove_extra_spaces, validate_line, hasNumbers, find_pattern


pre_keywords = [] 
post_keywords = []
line_keywords = ['iS registered', 'is registeres', 'is registered', '0 roguterod', 'is registeced', 'ts registered', 'SPONSOR:']
special_keywords  = ['sponsored by', 'CPE Sponsor Name']

#sponsor_list = ["AICPA","Deloitte", "Becker Professional Education", "Intuit", "Optiv Security", "FICPA", "KPMG", "EY", "CPA Academy", "Becker", "Beene Garter LLP", "Checkpoint Learning", "PricewaterhouseCoopers LLP", "PWC", "Deloitte LLP", "MACPA", "CPAAcademy.org", "CPAwebengage, Inc.", "Wolters Kluwer", "Grant Thornton LLP", "The Institute of Internal Auditors", "Ernst & Young LLP", "Learning.net", "KPMG LLP", "SC&H Group", "Association of International Certified Professional Accountants", "Thomson Reuters", "RSM", "HoganTaylor LLP", "Western CPE", "MICPA", "Practising Law Institute", "TSCPA", "Plain-English Accounting", "Surgent McCoy CPE, LLC", "Ernst & Young", "Surgent", "OSCPA", "VSCPA", "PricewaterhouseCoopers"]

sponsor_list = ["AICPA", "Deloitte", "Becker Professional Education", "Intuit", "Optiv Security", "FICPA", "KPMG", "EY", "CPA Academy", "Becker", "Beene Garter LLP", "Checkpoint Learning", "PricewaterhouseCoopers LLP", "PWC", "Deloitte LLP", "MACPA", "CPAAcademy.org", "CPAwebengage, Inc.", "Wolters Kluwer", "Grant Thornton LLP", "The Institute of Internal Auditors", "Ernst & Young LLP", "Learning.net", "KPMG LLP", "SC&H Group", "Association of International Certified Professional Accountants", "Thomson Reuters", "RSM", "HoganTaylor LLP", "Western CPE", "MICPA", "Practising Law Institute", "TSCPA", "Plain-English Accounting", "Surgent McCoy CPE, LLC", "Ernst & Young", "Surgent", "OSCPA", "VSCPA", "PricewaterhouseCoopers", "RSM US LLP", "AuditSense", "Becker CPE", "Workiva", "DTTL", "BKD, LLP", "KPMG Executive Education", "Foundation for Accounting Education", "PLI", "ACFE", "Association of Certified Fraud Examiners", "Grant Thornton"]


extra_list= ["ASSOCIATION OF CERTIFIED FRAUD EXAMINERS", 'Plaio-English Accounting', 'pliedu', 'the Institute of Internal Auditors', 'WAthe Institute of Internal Auditors', 'Institute of Internal Auditors', 'THOMSON REUTERS', 'The Virginia Society of CPAs', 'Wes:ern CPE']

sponsor_list = sponsor_list + extra_list

class ParseSponsors():

    def __init__(self, contents):
        self.contents = contents
        self.sponsor = ""

    def validate_sponsor(self):
        for sponsor in sponsor_list:
            if find_pattern(sponsor.lower(), self.sponsor.lower()):
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
                    print(f"***START***SPONSOR***", content, "***KW***", kw)
                    valid_words = remove_extra_spaces( content.split(kw)[0].strip() )
                    print("valid_words*****", valid_words) 
                    if valid_words is None:
                        continue
                    for val in valid_words:
                         if 'ID' not in val:
                             self.sponsor = val
                             if self.validate_sponsor():
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
            for sp in sponsor_list:
                  #print("SPONSOR===>", sp)
                  if find_pattern(sp.lower(), content.lower()):
                      self.sponsor = sp
                      return


                
    def extract(self):
        self.parse_within_lines()
        if self.sponsor == "":
            self.parse_between_lines()
        if self.sponsor == "":
            self.extract_from_list()
        return True


