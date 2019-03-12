#text_file = "./text_files/22.txt"
from lib.common_methods import remove_extra_spaces, validate_line, hasNumbers


pre_keywords = [] 
post_keywords = []
line_keywords = ['iS registered', 'is registeres', 'is registered', '0 roguterod', 'is registeced', 'ts registered']
special_keywords  = ['sponsored by']

class ParseSponsors():

    def __init__(self, contents):
        self.contents = contents
        self.sponsor = ""


    def fetch_valid_sponsor(self, words):
        for wrd in words:
            print(f"SPONSORS-------->{wrd}")
            if len(wrd) >= 3:
                return wrd

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
                if kw in content:
                    print(f"***START***", content, "***KW***", kw)
                    valid_words = remove_extra_spaces( content.split(kw)[0].strip() )
                    print(valid_words) 
                    if valid_words is None:
                        continue
                    for val in valid_words:
                        if len(val) >= 3:
                            if 'ID' not in val:
                                self.sponsor = val
                                return
                    try: 
                        valid_words = remove_extra_spaces( content.split(kw)[1].strip() )
                        if valid_words is None:
                            continue
                        for val in valid_words:
                            if len(val) >= 3:
                                if 'ID' not in val:
                                    self.sponsor = val
                                    return
                    except:
                        continue

                    """
                    elif len(valid_words) == 0:
                        continue
                    
                    print(valid_words) 
                    print(f"***END***", kw)
                    #self.sponsor = valid_words[0]
                    self.sponsor = self.fetch_valid_sponsor(valid_words)
                    return
                    """
    
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
                        return

                
    def extract(self):
        self.parse_within_lines()
        if self.sponsor == "":
            self.parse_between_lines()
        return True


