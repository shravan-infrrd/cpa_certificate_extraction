#text_file = "./text_files/22.txt"
from lib.common_methods import remove_extra_spaces, validate_line, hasNumbers


pre_keywords = [] 
post_keywords = []
line_keywords = []


class ParseSponsors():

    def __init__(self, contents):
        self.contents = contents
        self.sponsor = ""


    def parse_between_lines(self):
        for index, content in enumerate( self.contents ):
            for kw in pre_keywords:
                if kw == content.strip():
                    if ':' not in self.contents[index+1].strip():
                        self.sponsor = remove_extra_spaces( self.contents[index+1].strip())[0]
                    if self.sponsor == "":
                        if ':' not in contents[index+2].strip():
                            self.sponsor = remove_extra_spaces( self.contents[index+2].strip() )[0]

        if self.sponsor == "":
            for content in self.contents:
                for kw in post_keywords:
                    if kw in content.strip():
                        values = remove_extra_spaces( self.contents[index-1].strip() )
                        if ':' not in values[0]:
                            self.sponsor = values[0]


    def parse_within_lines(self): 
        for index, content in enumerate(self.contents):
            for kw in line_keywords:
                valid_words = validate_line(content, kw)
                if valid_words is None:
                    continue
                self.sponsor = valid_words[0]
                
    def extract(self):
        self.parse_within_lines()
        if self.sponsor == "":
            self.parse_between_lines()
        return True


