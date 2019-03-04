#text_file = "./text_files/22.txt"
from lib.common_methods import remove_extra_spaces, validate_line, hasNumbers


pre_keywords = ['field of study:', 'Course', 'For the successful completion of', 'sponsored by YH Advisors, Inc.', 'FOR THE PROGRAM ENTITLED', 'Field of Study', 'for successfully completing', 'bicld of Study']
post_keywords = ['Field of Study', 'Subject Area', 'Field ofStudy']
line_keywords = ['Field of Study:', 'Best Practices in', 'FieldofStudy:', 'Course Field of Study:', 'for successfully completing', 'Fieldof Study:']


class ParseFieldOfStudy():

    def __init__(self, contents):
        self.contents = contents
        self.field_of_study = ""


    def parse_between_lines(self):
        for index, content in enumerate( self.contents ):
            for kw in pre_keywords:
                if kw in content.strip():
                    if ':' not in self.contents[index+1].strip():
                        values = remove_extra_spaces( self.contents[index+1].strip())
                        if len(values) > 0:
                            self.field_of_study = values[0]
                    if self.field_of_study == "":
                        if ':' not in self.contents[index+2].strip():
                            values = remove_extra_spaces( self.contents[index+2].strip() )
                            if len(values) > 0:
                                self.field_of_study = values[0] 

        if self.field_of_study == "":
            for content in self.contents:
                for kw in post_keywords:
                    if kw in content.strip():
                        values = remove_extra_spaces( self.contents[index-1].strip() )
                        if ':' not in values[0]:
                            self.field_of_study = values[0]

    def parse_within_lines(self): 
        for index, content in enumerate(self.contents):
            for kw in line_keywords:
                valid_words = validate_line(content, kw)
                if valid_words is None:
                    continue
                self.field_of_study = valid_words[0]
                
    def extract(self):
        self.parse_within_lines()
        if self.field_of_study == "":
            self.parse_between_lines()
        return True


