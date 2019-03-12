
from lib.common_methods import remove_extra_spaces, validate_line, hasNumbers

line_keywords = ['Date:', 'Dated', 'Date Completed:', 'Presentation Date:', 'Date Attended:', 'Completion Date:', 'Event Date:', 'Session End Date', 'Oate Attended:', 'Completion Date', 'Session End Date', 'awarded this certificate on']
post_keywords = ['Date Attended', 'Date of Completion', 'event on']
pre_keywords  = ['Date Certified', 'Date', 'Date of Course', 'Dace of Course', 'Program Date(s)', 'Course Date']


class ParseDate():

    def __init__(self, contents):
        self.contents = contents
        self.date     = ""

    def parse_within_lines(self):
        for content in self.contents:
            for kw in line_keywords:
                if kw in content:
                    valid_words = validate_line(content, kw)
                    if valid_words is None:
                        continue
                    self.date = valid_words[0]


    def parse_between_lines(self): 
        for index, content in enumerate(self.contents):
            for kw in post_keywords:
                if kw in content:
                    values = remove_extra_spaces( self.contents[index+1].strip() )
                    print("POST--->", values)

                    for val in values:
                        if hasNumbers(val) and len(val)>4:
                            self.date = val
                            return

                    """
                    try:
                        if not hasNumbers(values[0]):
                            self.date = values[2]
                            return
                    except:
                        continue
                    """
        
        if self.date == "":
            for index, content in enumerate(self.contents):
                for kw in pre_keywords:
                    if kw in content:
                        values = remove_extra_spaces( self.contents[index-1].strip())
                        if len(values) == 0 :
                            values = remove_extra_spaces( self.contents[index-2].strip())
                        print(f"Date--->{values}")
                        
                        for val in values:
                            if hasNumbers(val) and len(val) > 4:
                                self.date = val.strip()
                                return



                        """
                        self.date = values[1].strip()
                        if hasNumbers(self.date):
                            if len(self.date) > 4:
                                self.date = values[0].strip()
                            return
                        else:
                            try:
                                self.date = values[2].strip()
                                if not hasNumbers(self.date):
                                    self.date = values[0].strip()
                            except:
                                self.date = values[0].strip()
                        return
                        """

    def extract(self):
        self.parse_within_lines()
        if self.date == "":
            self.parse_between_lines()

