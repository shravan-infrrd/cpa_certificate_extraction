#text_file = "./text_files/22.txt"
from lib.common_methods import remove_extra_spaces, validate_line, hasNumbers

field_of_studies = ['Administrative Practice', 'Business Management & Organization', 'Communications', 'Computer Science', 'Economics', 'Ethics - Behavioral', 'Ethics - Regulatory', 'Finance', 'Marketing', 'Mathematics', 'Personal Development', 'Personnel/Human Resources', 'Production', 'Specialized Knowledge & Applications', 'Social Environment of Business', 'Statistics', 'Accounting', 'Accounting - Governmental', 'Auditing', 'Auditing - Governmental', 'Business Law', 'Management Advisory Services', 'Taxes', 'Communications and Marketing', 'Specialized Knowledge', 'Information Technology', 'Computer Software & Applications', 'Audit', 'Business Management and Organization']

related_studies = ['Computer Software and Applications', 'Accounting & Auditing / Tax', 'Personnel/Human Resource', 'Personnel/HR', 'Regulatory Ethics', 'Professional Development']

field_of_studies = field_of_studies + related_studies

pre_keywords = [ 'field of study:', 'For the successful completion of', 'sponsored by YH Advisors, Inc.', 'FOR THE PROGRAM ENTITLED', 'Field of Study', 'for successfully completing', 'bicld of Study', 'Course', 'CPE Fueid of Study.']
post_keywords = ['bicld of Study', 'bield of Study', 'Field of Study', 'Subject Area', 'Field ofStudy']
line_keywords = ['Field of Study:', 'Best Practices in', 'FieldofStudy:', 'Course Field of Study:', 'for successfully completing', 'Fieldof Study:', 'Recommended Field of Study:', 'in the subject area of', 'RecommendedField of Study:']


class ParseFieldOfStudy():

    def __init__(self, contents):
        self.contents = contents
        self.field_of_study = ""

    def validate_with_existing_list(self):
        for fos in field_of_studies:
            if self.field_of_study.lower() in fos.lower():
                return True
        #print("Validating with existing list----->", self.field_of_study)
        self.field_of_study = ""
        return False

    def parse_between_lines(self):
        for index, content in enumerate( self.contents ):
            for kw in pre_keywords:
                if kw in content.strip():
                    #if ':' not in self.contents[index+1].strip():
                    values = remove_extra_spaces( self.contents[index+1].strip())
                    if len(values) > 0:
                        self.field_of_study = values[0]
                        #print("1. FieldOfStudy---->", values) #, self.validate_with_existing_list())
                        if self.validate_with_existing_list():
                            return
                        #print(f"1----KW->{kw}----")
                    if self.field_of_study == "":
                        #if ':' not in self.contents[index+2].strip():
                        values = remove_extra_spaces( self.contents[index+2].strip() )
                        #print(f"values-->{values}, -->{len(values)}")
                        if len(values) > 0 and len(values) < 5:
                            self.field_of_study = values[0] 
                            print("2. FieldOfStudy---->", values)
                            if self.validate_with_existing_list():
                                return

        #print("************PRECOMPLETED************")
        if self.field_of_study == "":
            for index, content in enumerate(self.contents):
                for kw in post_keywords:
                    if kw in content.strip():
                        values = remove_extra_spaces( self.contents[index-1].strip() )
                        #if ':' not in values[0]:
                        if len(values) == 0:
                            continue
                        self.field_of_study = values[0]
                        print("3. FieldOfStudy---->", values)
                        if self.validate_with_existing_list():
                            return

    def parse_within_lines(self): 
        for index, content in enumerate(self.contents):
            for kw in line_keywords:
                if kw in content:
                    valid_words = validate_line(content, kw)
                    print("***START***", content, "***valid_words**", valid_words)
                    if valid_words is None:
                        continue
                    self.field_of_study = valid_words[0]
                    if self.validate_with_existing_list():
                        return
               
    def extract_from_list(self):
        for fos in field_of_studies:
            for content in self.contents:
                  if fos.lower() in content.lower():
                      self.field_of_study = fos
                      return

    def extract(self):
        self.parse_within_lines()
        if self.field_of_study == "":
            self.parse_between_lines()
        if self.field_of_study == "":
            self.extract_from_list()
        return True


