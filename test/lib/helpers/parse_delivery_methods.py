#text_file = "./text_files/22.txt"
from lib.common_methods import remove_extra_spaces, validate_line, hasNumbers


pre_keywords = ['Delivery method:'] 
post_keywords = []
line_keywords = ['Program Location:']


class ParseDeliveryMethod():

    def __init__(self, contents):
        self.contents = contents
        self.delivery_method = ""


    def get_high_score_value(self, values):
        for val in values:
            if 'CPE' not in val:
                return val
  
    def get_valid_value(self, index):
        for i in range(index+1, index+2):
            if ':' not in self.contents[i].strip():
                values = remove_extra_spaces( self.contents[ i ].strip())
                self.delivery_method = self.get_high_score_value(values)
                #self.delivery_method = remove_extra_spaces( self.contents[ i ].strip())[0]
                if self.delivery_method == '':
                    continue
                else:
                    return 


    def parse_between_lines(self):
        print("===========================1=============================")
        for index, content in enumerate( self.contents ):
            for kw in pre_keywords:
                if kw in content.strip():
                    self.get_valid_value(index)
                    

        print(f"===========================3=============================")
        if self.delivery_method == "":
            for content in self.contents:
                for kw in post_keywords:
                    if kw in content.strip():
                        values = remove_extra_spaces( self.contents[index-1].strip() )
                        if ':' not in values[0]:
                            self.delivery_method = values[0]


    def parse_within_lines(self): 
        for index, content in enumerate(self.contents):
            for kw in line_keywords:
                valid_words = validate_line(content, kw)
                if valid_words is None:
                    continue
                self.delivery_method = valid_words[0]
                
    def extract(self):
        self.parse_within_lines()
        if self.delivery_method == "":
            self.parse_between_lines()
        return True


