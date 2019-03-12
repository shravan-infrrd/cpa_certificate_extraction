
from lib.common_methods import remove_extra_spaces, validate_line, hasNumbers


line_keywords = ['ofContinuing ProfessionalEducation Credits:', 'CPE credit1', 'CPE Hours', 'Credit']
#line_keywords = ['ofContinuing ProfessionalEducation Credits:', 'CPE credit1', 'CPE Hours', 'Interactive Credit in CPE Hours:', 'For a total of', 'Total CPF. Hours:', 'Total CPE Hours:', 'Total CPF. Hours:', 'Has Successfully Completed', 'Hours of Recommended CPE Credit:', 'CPE Credit Hours:', 'CPE Hours:', 'Number of CPE Credits', 'Total Credit Earned:', 'Duration:', 'CPE Credits:' ]
post_line_keywords = ['Interactive Credit in CPE Hours:', 'For a total of', 'Total CPF. Hours:', 'Total CPE Hours:', 'Total CPF. Hours:', 'Has Successfully Completed', 'Hours of Recommended CPE Credit:', 'CPE Credit Hours:', 'CPE Hours:', 'Number of CPE Credits', 'Total Credit Earned:', 'Duration:', 'CPE Credits:', 'Credit Hours:']
keywords = ['Numberof CPE Credits', 'Earned CPE credit(s)', 'Awarded CPE Credit Hours', 'Earned CPE Credit(s)', 'Number of CPE Credits', 'Earned CPE credit(s)']
post_keywords = ['Recommended for:', 'CPE CREDIT EARNED', 'CPECredits', 'Credas']

class ParseCredits():

    def __init__(self, contents):
        self.contents = contents
        self.credits = ""



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

                    """
                    if valid_words is None or len(valid_words) == 0:
                        continue
                    if ':' not in valid_words[0]:
                        self.credits = valid_words[0]
                        if not hasNumbers(self.credits):
                            self.credits = ""
                            continue
                        return
                    """

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
                    """
                    self.credits = remove_extra_spaces( self.contents[ index -1 ].strip() )[0]
                    if not hasNumbers( self.credits ):
                        self.credits = remove_extra_spaces( self.contents[ index -1 ].strip() )[1]
                    """

        #print("6*************PARSING*CREDITS*****************")
        for index, content in enumerate(self.contents):
            for kw in post_keywords:
                if kw in content:
                    values = remove_extra_spaces( self.contents[ index + 1 ].strip() )
                    for val in values:
                        if hasNumbers(val):
                            self.credits = val
                            return

                    """
                    #for index, val in enumerate(values):
                    self.credits = values[0]
                    try:
                        if not hasNumbers( self.credits ):
                            try:
                                self.credits = values[2]
                                return
                            except:
                                self.credits = values[1]
                                return
                    except:
                        self.credits = ""
                    """
                        
    def extract(self):
        self.parse_between_lines()
        if self.credits != "":
            return True
        self.parse_within_lines()
        return True


