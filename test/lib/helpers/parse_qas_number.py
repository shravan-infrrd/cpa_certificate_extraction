#text_file = "./text_files/22.txt"
import re
from lib.common_methods import remove_extra_spaces, validate_line, hasNumbers


pre_keywords = [] 
post_keywords = []
line_keywords = ['QAS Self-Study:', 'QAS Sponsor ID:', 'QAS:', 'QASSelf-Study:', 'NASBAQASID:', 'QAS ID#', 'QAS ID:', 'QAS.', 'QAS:']


class ParseQasNumber():

    def __init__(self, contents):
        self.contents = contents
        self.qas_number = ""

    def get_qas_id(self):
        qn = re.findall('\d+', self.qas_number)
        if qn:
            return qn[0]
        else: 
            return self.qas_number

    def parse_between_lines(self):
        for index, content in enumerate( self.contents ):
            for kw in pre_keywords:
                if kw == content.strip():
                    if ':' not in self.contents[index+1].strip():
                        self.qas_number = remove_extra_spaces( self.contents[index+1].strip())[0]
                    if self.qas_number == "":
                        if ':' not in contents[index+2].strip():
                            self.qas_number = remove_extra_spaces( self.contents[index+2].strip() )[0]
                            self.qas_number = self.get_qas_id()
                            return

        if self.qas_number == "":
            for content in self.contents:
                for kw in post_keywords:
                    if kw in content.strip():
                        values = remove_extra_spaces( self.contents[index-1].strip() )
                        if ':' not in values[0]:
                            self.qas_number = values[0]
                            self.qas_number = self.get_qas_id()
                            return


    def parse_within_lines(self): 
        for index, content in enumerate(self.contents):
            for kw in line_keywords:
                if kw in content:
                    valid_words = validate_line(content, kw)
                    #print("****START***", content)
                    #print(valid_words)
                    #print("****END*****", kw)
                    if valid_words is None:
                        continue
                    elif len(valid_words) == 0:
                        continue
                    self.qas_number = valid_words[0]
                    self.qas_number = self.get_qas_id()
                    return

                
    def extract(self):
        self.parse_within_lines()
        #if self.qas_number == "":
        #    self.parse_between_lines()
        return True


