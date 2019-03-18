#text_file = "./text_files/22.txt"
from lib.common_methods import remove_extra_spaces, validate_line, hasNumbers, find_pattern

field_of_studies = ['Accounting and Auditing', 'Administrative Practice', 'Business Management & Organization', 'Communications', 'Computer Science', 'Economics', 'Ethics - Behavioral', 'Ethics - Regulatory', 'Finance', 'Marketing', 'Mathematics', 'Personal Development', 'Personnel/Human Resources', 'Production', 'Specialized Knowledge and Applications', 'Specialized Knowledge & Applications', 'Social Environment of Business', 'Statistics', 'Accounting - Governmental', 'Auditing', 'Auditing - Governmental', 'Business Law', 'Management Advisory Services', 'Taxes', 'Communications and Marketing', 'Specialized Knowledge', 'Information Technology', 'Computer Software & Applications', 'Audit', 'Business Management and Organization', 'Accounting']

special_list = ['Auditing', 'Accounting', 'Specialized Knowledge']


related_studies = ['Computer Software and Applications', 'Accounting & Auditing / Tax', 'Personnel/Human Resource', 'Personnel/HR', 'Regulatory Ethics', 'Professional Development', 'Behavioral Ethics', 'Management Services', 'A&A', 'Yellow Book', 'Professional Ethics']

field_of_studies = field_of_studies + special_list + related_studies
field_of_studies = list(set(field_of_studies))

pre_keywords = [ 'field of study:', 'For the successful completion of', 'sponsored by YH Advisors, Inc.', 'FOR THE PROGRAM ENTITLED', 'Field of Study', 'for successfully completing', 'bicld of Study', 'Course', 'CPE Fueid of Study.']
post_keywords = ['bicld of Study', 'bield of Study', 'Field of Study', 'Subject Area', 'Field ofStudy', 'NASBA Field of Study:']
line_keywords = ['Field of Study:', 'Best Practices in', 'FieldofStudy:', 'Course Field of Study:', 'for successfully completing', 'Fieldof Study:', 'Recommended Field of Study:', 'in the subject area of', 'RecommendedField of Study:']


class ParseFos():

    def __init__(self, contents):
        self.contents = contents
        self.field_of_study = []

    def validate_with_existing_list(self, field):
        for fos in field_of_studies:
            if field.lower() in fos.lower():
                return True
        return False

    def check_if_present(self, fos):
        for fs in self.field_of_study:
            if fos.lower() in fs.lower():
                print("FIELD_OD_STUDY--->CHECK_FOR_PRESENCE---", fos)
                return True
        return False

    def parse_between_lines(self):
        for index, content in enumerate( self.contents ):
            for kw in pre_keywords:
                if kw in content.strip():
                    #if ':' not in self.contents[index+1].strip():  
                    values = remove_extra_spaces( self.contents[index+1].strip())
                    print("parse_between_lines====>", values)
                    if len(values) > 0:
                        #self.field_of_study = values[0]
                        #print("FOS1. FieldOfStudy---->", values) #, self.validate_with_existing_list())
                        if self.validate_with_existing_list(values[0]):
                            #self.field_of_study.append({"name": values[0] } )
                            if not self.check_if_present(values[0]):
                                self.field_of_study.append(values[0] )
                                continue
                            #return
                        #print(f"1----KW->{kw}----")
                    #if not found:
                    #if ':' not in self.contents[index+2].strip():
                    values = remove_extra_spaces( self.contents[index+2].strip() )
                    #print(f"values-->{values}, -->{len(values)}")
                    if len(values) > 0 and len(values) < 5:
                        #self.field_of_study = values[0] 
                        #print("FOS2. FieldOfStudy---->", values)
                        if self.validate_with_existing_list(values[0]): 
                            if not self.check_if_present(values[0]):
                                self.field_of_study.append( values[0])
                            #self.field_of_study.append({"name": values[0]})
                                continue
                            #return
        if len(self.field_of_study) == 0:
            for index, content in enumerate(self.contents):
                for kw in post_keywords:
                    if kw in content.strip():
                        values = remove_extra_spaces( self.contents[index-1].strip() )
                        #if ':' not in values[0]:
                        if len(values) == 0:
                            continue
                        #self.field_of_study = values[0]
                        #print("FOS3. FieldOfStudy---->", values)
                        if self.validate_with_existing_list(values[0]):
                            if not self.check_if_present(values[0]):
                                self.field_of_study.append(values[0])
                            #return

    def parse_within_lines(self): 
        for index, content in enumerate(self.contents):
            for kw in line_keywords:
                if kw in content:
                    valid_words = validate_line(content, kw)
                    print("FOS***START***", content, "***valid_words**", valid_words)
                    if valid_words is None:
                        continue
                    #self.field_of_study = valid_words[0]
                    if self.validate_with_existing_list(valid_words[0]):
                        if not self.check_if_present(valid_words[0]):  
                            self.field_of_study.append(valid_words[0])
                        #return
               
    def extract_from_list(self):
        for fos in field_of_studies:
            for content in self.contents:
                  #if fos.lower() in content.lower():
                  if find_pattern(fos.lower(), content.lower() ):
                      #print(f"FOS**FIELF_OF_STUDY--->{fos}, --->CONTENT-->{content}")
                      #self.field_of_study.append({"name": fos })
                      if not self.check_if_present(fos):
                          self.field_of_study.append(fos)
                      #return

    def extract(self):
        self.parse_within_lines()
        #print("FOS***1***", self.field_of_study)
        if len(self.field_of_study) == 0:
            #print("FOS***2***", self.field_of_study)
            self.parse_between_lines()
        if len(self.field_of_study) == 0:
            #print("FOS***3***", self.field_of_study)
            self.extract_from_list()
        print("FOS***4***", self.field_of_study)
        self.field_of_study = list(set(self.field_of_study))
        print("FOS***4***", self.field_of_study)
        return True


