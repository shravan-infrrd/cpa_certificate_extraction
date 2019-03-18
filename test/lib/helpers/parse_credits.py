import re
from lib.common_methods import remove_extra_spaces, validate_line, hasNumbers


line_keywords = ['ofContinuing ProfessionalEducation Credits:', 'CPE credit1', 'CPE Hours', 'Credit', 'hours of CPE']
#line_keywords = ['ofContinuing ProfessionalEducation Credits:', 'CPE credit1', 'CPE Hours', 'Interactive Credit in CPE Hours:', 'For a total of', 'Total CPF. Hours:', 'Total CPE Hours:', 'Total CPF. Hours:', 'Has Successfully Completed', 'Hours of Recommended CPE Credit:', 'CPE Credit Hours:', 'CPE Hours:', 'Number of CPE Credits', 'Total Credit Earned:', 'Duration:', 'CPE Credits:' ]
post_line_keywords = ['Interactive Credit in CPE Hours:', 'For a total of', 'Total CPF. Hours:', 'Total CPE Hours:', 'Total CPF. Hours:', 'Has Successfully Completed', 'Hours of Recommended CPE Credit:', 'CPE Credit Hours:', 'CPE Hours:', 'Number of CPE Credits', 'Total Credit Earned:', 'Duration:', 'CPE Credits:', 'Credit Hours:', 'CPE credit:', 'Credits:', 'CPE Credit Hours.']
keywords = ['Numberof CPE Credits', 'Earned CPE credit(s)', 'Awarded CPE Credit Hours', 'Earned CPE Credit(s)', 'Number of CPE Credits', 'Earned CPE credit(s)']
post_keywords = ['Recommended for:', 'CPE CREDIT EARNED', 'CPECredits', 'Credas']

class ParseCredits():

    def __init__(self, contents, fos):
        self.contents = contents
        self.credits = ""
        self.fos = fos
        self.field_of_study = []

    def validate_credits(self):
        if len(self.credits) > 4:
            self.credits = ""
            return False
        return True


    def parse_with_fos_keyword(self, fos):
        for content in self.contents:
            content = content.lower().strip()
            if fos in content:
                cred = re.findall('\d*\.?\d+', content)
                if cred:
                    self.credits = cred[0]
                    return
            

    def parse_first_part_of_line(self):
        for content in self.contents:
            for kw in line_keywords:
                if kw in content:
                    #print("***CREDITS***====>", content, "***KW***", kw)
                    valid_words = validate_line(content.strip(), kw) #remove_extra_spaces( content.split(kw)[0].strip() )
                    #print("valid_words-->", valid_words)
                    #print(remove_extra_spaces( content.split(kw)[0].strip() ))
                    #print("***END***")
                    valid_words = remove_extra_spaces( content.split(kw)[0].strip() )
                    for val in valid_words:
                        if ':' not in val:
                            if hasNumbers( val ):
                                self.credits = val
                                return

    def parse_second_part_of_line(self):
        for content in self.contents:
            for kw  in post_line_keywords:
                if kw in content:
                    valid_words = validate_line(content.strip(), kw)
                    #print("content-->", content)
                    #print("ParseSecondPartOfLine------>", kw, valid_words)
                    if valid_words is None:
                        continue
                    self.credits = valid_words[0]

        if not hasNumbers(self.credits):
            self.credits = ""
        
    def parse_within_lines(self):
        #print("1*************PARSING*CREDITS*****************")
        self.parse_first_part_of_line()
        #print("2*************PARSING*CREDITS*****************")
        if self.credits != "":
            return
        #print("3*************PARSING*CREDITS*****************")
        self.parse_second_part_of_line()
        #print("4*************PARSING*CREDITS*****************")

    def parse_between_lines(self):
        
        #print("5*************PARSING*CREDITS*****************")
        for index, content in enumerate(self.contents):
            for kw in keywords:
                if kw in content:
                    values = remove_extra_spaces( self.contents[ index -1 ].strip() )
                    for val in values:
                        if hasNumbers( val ):
                            self.credits = val
                            return

        #print("6*************PARSING*CREDITS*****************")
        for index, content in enumerate(self.contents):
            for kw in post_keywords:
                if kw in content:
                    values = remove_extra_spaces( self.contents[ index + 1 ].strip() )
                    for val in values:
                        if hasNumbers(val):
                            self.credits = val
                            return
                try: 
                    values = remove_extra_spaces( self.contents[ index + 2 ].strip() )
                    for val in values:
                        if hasNumbers(val):
                            self.credits = val
                            if self.validate_credits():
                                return
                except:
                    continue


    def extract_credits(self, fos):
        for content in self.contents:
            content = content.lower().strip()
            if fos.lower() in content:
                print(f"Content--->{content}, fos---->{fos}")
                print("Credits*******>", content.split(fos.lower()))
                if '(' in content:
                    credit = content.split(fos.lower())[1]
                else:
                    credit = content.split(fos.lower())[0]

                extracted_credit = re.findall('\d*\.?\d+', credit)
                if extracted_credit:
                    return extracted_credit[0]
                else:
                    return credit
                """
                credit = re.findall("\d+\.\d+", credit)
                if not credit:
                    credit = re.findall("\d+", credit)

                return credit
                """
  
                #return content.split(fos)

    def find_credits(self, fos):
        print("*****FIND_CREDITS*****", fos.lower())
        for content in self.contents:
            content = content.lower().strip()
            if fos.lower() in content:
                print(f"Content--->{content}, fos--->{fos}")
                credit = re.findall('\d*\.?\d+', content)
                print("Found Credits---->", credit)
                if credit:
                    return credit[0]

        self.parse_between_lines()
        if self.credits != "":
            cred = re.findall('\d*\.?\d+', self.credits)
            return cred[0]

        self.parse_within_lines()
        if self.credits != "":
            cred = re.findall('\d*\.?\d+', self.credits)
            return cred[0]
        return ""

    def build_field_of_study(self):
        if len(self.fos) == 1:
            #self.find_credits(self.fos[0])
            self.field_of_study.append({"name": self.fos[0], "credits": self.find_credits(self.fos[0]), "score": ""})
        else:
            for fos in self.fos:
                credits = self.extract_credits(fos)
                if credits != "":
                    try:
                        if int(credits) < 20:
                            self.field_of_study.append({"name": fos, "credits": self.extract_credits(fos), "score":""})
                    except:
                        #self.field_of_study.append({"name": fos, "credits": self.extract_credits(fos), "score":""})
                        pass

                        
    def extract(self):
        self.build_field_of_study()
        """
        if len(self.fos) == 1:
            self.parse_between_lines()
            if self.credits != "":
                return True
            self.parse_within_lines()
            fos = self.fos[0]
            fod['credits'] = self.credits
            self.fos = [fos]
            return True
        """

