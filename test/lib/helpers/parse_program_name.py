#text_file = "./textfiles/21.txt"
import re
from lib.common_methods import remove_extra_spaces, validate_line, find_pattern


preceding_keywords = ['has successfully completed', 'CERTIFICATE OF ATTENDANCE', 'has successfully completed the online course', 'Online Certification training:', 'Certificate of Attendance', 'Certificate of Completion', 'for participation in', 'for participation in', 'successfully completed', 'completion ot the course', 'entitled', 'for successfully completing', 'completed', 'For Successfully Completing', 'has successfully completed:', 'Has Successfully Completed the Course:', 'Has Successfully Completed the Course:', 'For successful completion of', 'for the successful completion of', 'has completed', 'has completed the group Internet-based course']

"""
Is hereby awardedto (the institute of internal)
"""
following_keywords = ['Course Name'] #, 'Is hereby awardedto', 'Is hereby awarded to']
line_keywords = ['Course Title:', 'for successfully completing', 'for successfully completing:', 'Program Title:', 'PROGRAM TITLE:', 'For successful completion of', 'Title.', 'Title:']

invalid_keywords = ['presented to', 'Awarded to', 'Date', 'Freserted to', 'successful', 'granted', 'Association of Cortificd', 'Association of Certified', 'Field of Study', 'Please', 'Program Location', 'CPE', 'Credits', 'CTEC']
possible_keywords = ['Conference', 'Event', 'Webcast', 'Seminar']

priority_keywords = ['(Part |)', 'Part |', 'PART 1', 'Module 1', 'Module |']

class ParseProgramName():

    def __init__(self, contents, name):
        self.contents = contents
        self.name = name
        self.program_name = ""

    def validate_program_name(self):
        print("ValidateProgramName**")
        if self.program_name.strip() == "":
            return False
        print(f"InvalidKEYWORDS---->{invalid_keywords}--->program_name---->{self.program_name}")
        for kw in invalid_keywords:
            print(f"===>INKW-->{kw}=====>pn==>{self.program_name}")
            if find_pattern(kw, self.program_name.lower()):
            #if kw.lower() in self.program_name.lower():
                print("Error--->", kw, "pn", self.program_name)
                self.program_name = ""
                return False
        if self.name.lower() != "":
            if find_pattern(self.name.lower(), self.program_name.lower()):
                if not find_pattern('ethics', self.program_name.lower()):
                    print("Error2--->")
                    self.program_name = ""
                    return False

        return True 

    def check_for_invalid_keywords(self, word):
        for kw in invalid_keywords:
            if find_pattern(kw.lower(), word.lower()):
                print("****CAUTION****")
                print(f"Keyword-->{kw}, word-->{word}")
                return ""
        return word

    def check_invalid_keywords(self, word):
        for kw in invalid_keywords:
            if find_pattern(kw.lower(), word.lower()):
                print("VALIDATION----->", kw, "Content--->", word)
                return False
        return True

    def is_valid_program_name(self, val_1, val_2, val_3):
        #print("***val_1***")
        try:
            print("***val_1***", val_1)
            if val_1[0] != "":
                print("***val_1***", self.check_invalid_keywords(val_1[0]))
                if not self.check_invalid_keywords(val_1[0]):
                    val_1 = []

                else:
                    print("***val_1***", self.check_invalid_keywords(val_1[0]))
                    if ':' in val_1[0]:
                        print("1***val_1***", self.check_invalid_keywords(val_1[0]))
                        print("2***val_1***", find_pattern('ethics', val_1[0]))
                        if find_pattern('ethics', val_1[0]):
                            val_1 = []
        except:
            pass
        #print("***val_2***")
        try:
            print("***val_2***", val_2)
            if val_2[0] != "":
                print("***val_2***", self.check_invalid_keywords(val_2[0]))
                if not self.check_invalid_keywords(val_2[0]):
                    val_2 = []

                else:
                    print("***val_2***", self.check_invalid_keywords(val_2[0]))
                    if ':' in val_2[0]:
                        print("1***val_2***", self.check_invalid_keywords(val_2[0]))
                        print("2***val_2***", find_pattern('ethics', val_2[0]))
                        if find_pattern('ethics', val_2[0]):
                            val_2 = []
        except:
            pass
        #print("***val_3***")
        try:
            print("***val_3***", val_3)
            if val_3[0] != "":
                print("***val_3***", self.check_invalid_keywords(val_3[0]))
                if not self.check_invalid_keywords(val_3[0]):
                    val_3 = []

                else:
                    print("***val_3***", self.check_invalid_keywords(val_3[0]))
                    if ':' in val_3[0]:
                        print("1***val_3***", self.check_invalid_keywords(val_3[0]))
                        print("2***val_3***", find_pattern('ethics', val_3[0]))
                        if find_pattern('ethics', val_3[0]):
                            val_3 = []
        except:
            return [val_1, val_2, val_3]
            #pass
        print("***val_completed***")

        return [val_1, val_2, val_3]
        #return True

    def get_progrma_name(self, val_1, val_2, val_3):
        
        if val_1 and val_2 and val_3:
            print("PN***1***")
            return val_1[0] + " " + val_2[0] + " " + val_3[0]
        if val_1 and val_2:
            print("PN***2***")
            return val_1[0] + " " + val_2[0]
        if val_1 and val_3:
            print("PN***3***")
            return val_1[0] + " " + val_3[0]
        if val_2 and val_3:
            print("PN***4***")
            return val_2[0] + " " + val_3[0]
        if val_1:
            print("PN***5***")
            return val_1[0]
        if val_2:
            print("PN***6***")
            return val_2[0]
        if val_3:
            print("PN***7***")
            return val_3[0]
        
        print("PN***8***")
        return ""

    def parse_between_lines(self):
        for index, content in enumerate(self.contents):
            #Note: Parse Next Line
            for kw in preceding_keywords:
                #if kw == content.strip():
                if kw in content.strip():
                    #print("***START***PROGRAM_NAME*****", content, "***KW***", kw)
                    values_1 = remove_extra_spaces( self.contents[index + 1].strip() )
                    values_2 = remove_extra_spaces(self.contents[index + 2].strip() )
                    values_3 = remove_extra_spaces(self.contents[index + 3].strip() )
                    #print(f"values_1-->{values_1}, values_2-->{values_2}, values_3-->{values_3}")
                    #print("TRUE/FALSE-------->", self.is_valid_program_name(values_1, values_2, values_3))
                    values_1, values_2, values_3 = self.is_valid_program_name(values_1, values_2, values_3)
                    print(f"values_1-->{values_1}, values_2-->{values_2}, values_3-->{values_3}")
                    self.program_name = self.get_progrma_name(values_1, values_2, values_3)
                    if self.program_name is not None:      
                        if self.validate_program_name():
                            return
  
                    """
                    if self.is_valid_program_name(values_1, values_2, values_3):
                        self.program_name = self.get_progrma_name(values_1, values_2, values_3)
                        print(f"*****>{self.program_name}*****")  
                        print(f"************HERE--4--HERE==*{self.program_name}*")
                       
                        if self.validate_program_name():
                            print(f"***************HERE--5--HERE==*{self.program_name}*")
                            return
                        print(f"************HERE--6--HERE==*{self.program_name}*")
                     """
                #print(f"************HERE--7--HERE==*{self.program_name}*")
                if self.program_name == "":
                    #Note: Parse Previous Line
                    #print(f"************HERE--6.5--HERE==*{self.program_name}*")
                    for kw in following_keywords:
                        if kw == content.strip():
                            #print(f"************HERE--7--HERE==*{self.program_name}*")
                            values = remove_extra_spaces(self.contents[index - 1].strip())
                            #print("Program_NAME--follow-->", values, kw)
                            if len(values) == 0:
                                continue
                            self.program_name = values[0] # .split('  ')[0]
                            #print(f"following_keywords*****>{self.program_name}*****")
                            if self.validate_program_name():
                                return


    def parse_within_line(self):
        #print("************PROGRAM***NAME************")
        for content in self.contents:
            for kw in line_keywords:
                valid_words = validate_line(content, kw)
                #print("Program_NAME--->", valid_words)
                if valid_words is None:
                    continue
                self.program_name = valid_words[0]
                return

    
    def find_key_words(self):
        ignore = ['date', 'number', 'location']
        for index, content in enumerate(self.contents):
            for kw in possible_keywords:
                if kw in content:
                    self.program_name = content.strip() + " " + self.contents[index+1]
                    print("ProgramName--PossibleKeywords--->", self.program_name)
                    for kwi in ignore:
                        if find_pattern(kwi.lower(), self.program_name.lower()):
                            print("--Found Error--", kwi)
                            self.program_name = ""
                            break
                    if self.program_name == "":
                        continue
                    else:
                        print("***Found ProgramName***")
                        return
                    return
   
      
    def find_from_priority_keywords(self):

        for content in self.contents:
            for kw in priority_keywords:
                if kw in content:
                    self.program_name = content
                    return

    #def identify_program_name(self):
    def extract(self):
        self.find_from_priority_keywords()
        if self.program_name== "":
            self.parse_between_lines()
        print("--------ProgramName-------", self.program_name)
        if self.program_name == '':
            self.parse_within_line()
        if self.program_name == '':
            self.find_key_words()
        return True
