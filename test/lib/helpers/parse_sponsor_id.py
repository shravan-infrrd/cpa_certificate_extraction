#text_file = "./text_files/22.txt"
from lib.common_methods import remove_extra_spaces, validate_line, hasNumbers


pre_keywords = [] 
post_keywords = ['National Registry of CPE Sponsors Number']
line_keywords = ['NASBA Sponsor registry number', 'NASBA Sponsor', 'NASBA -', 'National Registry of Sponsors If) Number -', 'Sponsor Id#', 'National Registry of CPE Sponsors ID#', 'National Registry of CPE Sponsors ID Number:', 'National Registry of CPE Sponsors 1D Number:', 'Natonal Registy', 'CPF Spongors ID Number', 'National Registry Sponsor No.', 'NASBA Sponsor ID', 'National Registry of CPE Sponsors ID:', 'National Registry Sponsor Number', 'Spenser License Numher', 'NASBA SPONSOR #', 'National Registry:', 'National Registry of CPE Sponsors ID Number', 'Natora Reg sty of CPE Socrac:s D8', 'CPE Credits earned:', 'NASBA Sponsor Registry Number', 'National Registry of CPE Sponsors 1D:', 'National Registry of CPE Sponsors [D:', 'Natona Reg stry of CPF Sponsors ID Number', 'Sponsors ID Number', 'Sponsors 1D Number:', 'Sponsors 1D Number', 'NASBA #', "NASBA's National Registry of CPE Sponsors - ID", 'Registry ID Nuanber:', 'NASBAsponsor#', 'NY Sponsor |O Number', 'CPE Sponsor ID #', 'NASBA Registry Provider #:', 'NASBA-']


class ParseSponsorId():

    def __init__(self, contents):
        self.contents = contents
        self.sponsor_id = ""

    def validate_sponsor_id(self):
        if not hasNumbers(self.sponsor_id):
            self.sponsor_id = ""
            return False

        if len(self.sponsor_id) <= 4 :
            self.sponsor_id = ""
            return False
        return True

    def parse_between_lines(self):
        for index, content in enumerate( self.contents ):
            for kw in pre_keywords:
                if kw == content.strip():

                    values = remove_extra_spaces( self.contents[index+1].strip())
                    if len(values) > 0:
                        for val in values:
                            if ':' not in val:
                                self.sponsor_id = val
                                if self.validate_sponsor_id():
                                    continue
                    if self.sponsor_id == "":
                        values = remove_extra_spaces( self.contents[index+2].strip())
                        if len(values) > 0:
                            for val in values:
                                if ':' not in val:
                                    self.sponsor_id = val
                                    if self.validate_sponsor_id():
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
                                    return
                        #if ':' not in values[0]:
                        #    self.sponsor_id = values[0]


    def parse_within_lines(self): 
        for index, content in enumerate(self.contents):
            for kw in line_keywords:
                if kw in content:
                    valid_words = validate_line(content, kw)
                    if valid_words is None:
                        continue
                    elif len(valid_words) == 0:
                        continue
                    self.sponsor_id = valid_words[0]
                    words = self.sponsor_id.split(' ')
                    self.sponsor_id = words[0].split(')')[0]
                    if self.validate_sponsor_id():
                        return

                
    def extract(self):
        self.parse_within_lines()
        if self.sponsor_id == "":
            self.parse_between_lines()
        return True


