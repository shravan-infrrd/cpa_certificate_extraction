#from dateparser.search import search_dates
#import dateparser
from lib.common_methods import remove_extra_spaces, validate_line, hasNumbers, format_date, find_pattern
#from dateutil.parser import parse
import datefinder


line_keywords = ['Date:', 'Dated', 'Date Completed:', 'Presentation Date:', 'Date Attended:', 'Completion Date:', 'Event Date:', 'Session End Date', 'Oate Attended:', 'Completion Date', 'Session End Date', 'awarded this certificate on', 'Date(s) Completed:', 'PROGRAM DATES:', 'Program Date:', 'Date.', 'Date Issued:']
post_keywords = ['Date Attended', 'Date of Completion', 'event on']
pre_keywords  = ['Date Certified', 'Date', 'Date of Course', 'Dace of Course', 'Program Date(s)', 'Course Date']


class ParseDate():

    def __init__(self, contents, name, program_name):
        self.contents = contents
        self.date     = ""
        self.name     = name    
        try:
            self.program_name = program_name.lower().strip()
        except:
            self.program_name = "" #program_name

    def make_corrections(self, date):
        date = date.lower().split(' to ')[-1]
        date = date.lower().split(' at ')[0]
        """
        date = date.lower().replace('october', 'octaber')
        date = date.lower().replace('to', 'to a')
        date = date.lower().replace('octaber', 'october')
        """
        return date


    def parse_within_lines(self):
        for content in self.contents:
            for kw in line_keywords:
                if kw in content:
                    valid_words = validate_line(content, kw)
                    if valid_words is None:
                        continue
                    self.date = valid_words[0]
                    return


    def parse_between_lines(self): 
        for index, content in enumerate(self.contents):
            for kw in post_keywords:
                if kw in content:
                    values = remove_extra_spaces( self.contents[index+1].strip() )
                    #print("POST--->", values)

                    for val in values:
                        if hasNumbers(val) and len(val)>4:
                            self.date = val
                            return

        
        if self.date == "":
            for index, content in enumerate(self.contents):
                for kw in pre_keywords:
                    if kw in content:
                        values = remove_extra_spaces( self.contents[index-1].strip())
                        if len(values) == 0 :
                            values = remove_extra_spaces( self.contents[index-2].strip())
                        #print(f"Date--->{values}")
                        
                        for val in values:
                            if hasNumbers(val) and len(val) > 4:
                                self.date = val.strip()
                                return


    def extract_without_keywords(self):
        parse = False
        for content in self.contents:
            #print(f"Name:------>{self.program_name.lower().strip()}") #===Content:-->{content.lower().strip()}")
            #print(f"Content:--->{content.lower().strip()}")
            #print(f"TRUE/FALSE---DATE--->{find_pattern(self.program_name.lower().strip(), content.lower().strip())}")
            #print(f"TRUE/FALSE->{find_pattern(content.lower().strip(), self.program_name.lower().strip())}")
            #if find_pattern(self.program_name.lower().strip(), content.lower().strip()):
            if find_pattern(content.lower().strip(), self.program_name.lower().strip()):
            #if self.name.lower() in content.lower().strip():
                parse = True
            if parse:
                #if hasNumbers(content):
                #print("FINDING-DATE----->", content)
                content = self.make_corrections(content)
                dates = list(datefinder.find_dates(content))
                #print("Dates------------>", dates)
                if len(dates) > 0:
               
                    self.date = str(dates[-1])
                    #print("DateExtracted---->", self.date)
                    return




    def extract(self):
        self.parse_within_lines()
        if self.date == "":
            self.parse_between_lines()
        
        if self.date == "":
            self.extract_without_keywords()
        print("Date Extraction Complete===>", self.date) 

        if self.date != "":
            self.date = self.make_corrections(self.date)
            print("Date Extraction Complete===>", self.date)
            self.date = format_date(self.date)
            print("Date Extraction Complete===>", self.date)


