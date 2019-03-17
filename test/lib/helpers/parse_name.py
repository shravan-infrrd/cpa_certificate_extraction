#text_file = "./text_files/21.txt"
from lib.common_methods import remove_extra_spaces, validate_line, hasNumbers

preceding_keywords = ['This certifies that', 'certifies that', 'Attendee', 'Certifies That', 'Attendee Name:', 'This certificate is presented to', 'Presents this Certificate of Completion to', 'Gg CalCPA                                    GS FOUNDATION', 'This certificate is presentedto:', 'Certificate of Completion', 'This certificate is presented to:', 'PRESENTED TO', "Participant's Name", "FOUNDATION", 'presented to', 'Freserted to', 'granted to', 'This is to ceruty that', 'Is hereby awardedto', 'Is hereby awarded to', 'awarded to', 'awardedto', 'Certificate of C completion']
following_keywords = ['Has successfully completed the QuickBooks', "Participant's Name", 'for successfully completing', 'has successfully completed', 'Has Successfully Completed the Course:', 'Has successfully completed']
#name_keywords = ['Attendee’s Name:', '\ Attendee’s Name:', 'V Attendee’s Name:', 'Awardedto:', 'Participant Name:', 'This certificate is presented to', 'Awarded to:']
line_keywords = ['Attendee’s Name:', '\ Attendee’s Name:', 'V Attendee’s Name:', 'Awardedto:', 'Participant Name:', 'This certificate is presented to', 'Awarded to:', 'This certifies that', 'Attendee:', 'NAME OF ATTENDEE.', 'Nameof Participant:']

invalid_words = ['Freserted to', 'Presented to', 'this', 'that', 'Awarded to', 'Program', 'CPE', 'Firm:']

class ParseName():

    def __init__(self, contents):
        self.contents = contents
        self.name = ""

    def validate_name(self):
        print("***NAME***validation called", self.name)
        for kw in invalid_words:
            #print(f"keyword --> {kw.lower()} ===> {self.name.lower()}")
            if kw.lower() in self.name.lower():
                print("True condition", kw, '**', self.name)
                self.name = ""
                return False
        print("****NAEM***FOUND***", self.name)
        if len(self.name.split(' ')) >= 4:
            self.name = ""
            return False
        if hasNumbers(self.name):
            self.name = ""
            return False
        return True

    def parse_between_lines(self):
        for index, content in enumerate(self.contents):
            #Note: Parse Next Line
            for kw in preceding_keywords:
                #print(f"START***NAME**content=={content},***kw=={kw}")
                if kw.lower() in content.strip().lower():
                    #print("1*****************NAME*****************", kw)
                    values = remove_extra_spaces( self.contents[index + 1].strip() )
                    #print("2*****************NAME*****************", values)
                    for val in values:
                      
                        self.name = val
                        word = 'successfully completed'
                        if word.lower() in self.name.lower():
                            if len(self.name.split(' ')) > 4:
                                if word in self.name:
                                    self.name = self.name.split(word)[0]
                                    if len(self.name.split(' ')) > 4:
                                        self.name = ""
                                        continue
                                    if self.validate_name():
                                        return
                                #print("2.1*****************NAME*****************", self.name)
                                self.name = ""
                                continue
                        #print("3*****************NAME*****************", self.name)
                        if len(self.name.split(' ')) > 4:
                            self.name = ""
                            continue
                        if self.validate_name():
                            return

                    try:
                        if self.name == "":
                            values = remove_extra_spaces( self.contents[index + 2].strip() )
                            if len(values) == 0:
                                values = remove_extra_spaces( self.contents[index + 3].strip() )
                                
                            #print("4*****************NAME*****************", values, type(values))
                            for val in values:
                                self.name = val
                                word = 'successfully completed'
                                if word.lower() in self.name.lower():
                                    if len(self.name.split(' ')) > 4:
                                        if word in self.name:
                                            self.name = self.name.split(word)[0]
                                            if len(self.name.split(' ')) > 4:
                                                self.name = ""
                                                continue
                                            if self.validate_name():
                                                return
                                        #print("4.1*****************NAME*****************", self.name)
                                        self.name = ""
                                        continue
                                #print("5*****************NAME*****************", val)
                                if len(self.name.split(' ')) >= 4:
                                    self.name = ""
                                    continue
                                if self.validate_name():
                                    return
                    except:
                          continue

                #print("5*****************NAME*****************")
                if self.name == "":

                    #Note: Parse Previous Line
                    for kw in following_keywords:
                        #print("5*****************NAME*****************", kw)
                        if kw in content.strip():
                        #if kw == content.strip():
                            #print(f"***NAME****content=={content}===kw{kw}")
                            values = remove_extra_spaces(self.contents[index - 1].strip())
                            #print("values---->", values)
                            for val in values:
                                #print("NAME---val", val)
                                if ':' in val:
                                    continue
                                self.name = val
                                word = 'successfully completed'
                                if word.lower() in self.name.lower():
                                    self.name = self.name.split(word)[0]
                                if self.validate_name():
                                    return
                            values = remove_extra_spaces(self.contents[index - 2].strip())
                            #print("values---->", values)
                            for val in values:
                                #print("NAME---val", val)
                                if ':' in val:
                                    continue
                                self.name = val
                                if self.validate_name():
                                    return
                            """
                            if len(values) == 0:
                                continue
                            self.name = values[0] # .split('  ')[0]
                            if self.validate_name():
                                return
                            """


    def parse_within_line(self):
        for content in self.contents:
            for kw in line_keywords:
                if kw in content:
                    #print("1***START***NAME", content, "**kw**", kw)
                    valid_words = validate_line(content, kw)
                    #print("2***START***NAME", valid_words)
                    if valid_words is None:
                        continue
                    #print("3***START***NAME", valid_words)
                    if ':' in valid_words[0]:
                        continue
                    #print("4***START***NAME", self.name)
                    word = 'has successfully completed'
                    self.name = valid_words[0]
                    #print("5***START***NAME", self.name)
                    if word.lower() in self.name.lower():
                        self.name = self.name.split(word)[0]
                    print("6***START***NAME", self.name)
                    if self.validate_name():
                        print("****END***NAME")
                        return

    def parse_line_without_keywords(self):
        kw = ', CPA'
        ignore_keywords = ['Participant Name:']
        for content in self.contents:
            if kw in content:
                self.name = content.split(kw)[0]
                for kwi in ignore_keywords:
                    if kwi in self.name:
                        self.name = self.name.split(kwi)[-1]
                return


    def extract(self):
        self.parse_between_lines()
        if self.name == '':
            self.parse_within_line()
        if self.name == '':
            self.parse_line_without_keywords()
        return True

