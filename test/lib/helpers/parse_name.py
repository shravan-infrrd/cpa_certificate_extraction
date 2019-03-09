#text_file = "./text_files/21.txt"
from lib.common_methods import remove_extra_spaces, validate_line

preceding_keywords = ['This certifies that', 'certifies that', 'Attendee', 'Certifies That', 'Attendee Name:', 'This certificate is presented to', 'Presents this Certificate of Completion to', 'Gg CalCPA                                    GS FOUNDATION', 'This certificate is presentedto:', 'Certificate of Completion', 'This certificate is presented to:', 'PRESENTED TO', "Participant's Name"]
following_keywords = ['Has successfully completed the QuickBooks', "Participant's Name"]
#name_keywords = ['Attendee’s Name:', '\ Attendee’s Name:', 'V Attendee’s Name:', 'Awardedto:', 'Participant Name:', 'This certificate is presented to', 'Awarded to:']
line_keywords = ['Attendee’s Name:', '\ Attendee’s Name:', 'V Attendee’s Name:', 'Awardedto:', 'Participant Name:', 'This certificate is presented to', 'Awarded to:']

class ParseName():

    def __init__(self, contents):
        self.contents = contents
        self.name = ""

    def parse_between_lines(self):
        for index, content in enumerate(self.contents):
            #Note: Parse Next Line
            for kw in preceding_keywords:
                if kw == content.strip():
                    values = remove_extra_spaces( self.contents[index + 1].strip() )
                    if len(values) == 0:
                        values = remove_extra_spaces(self.contents[index + 2].strip() )
                        if len(values) == 0:
                            continue

                    self.name = values[0]

                    if len(self.name.split(' ')) > 4:
                        self.name = ""

            if self.name == "":
                #Note: Parse Previous Line
                for kw in following_keywords:
                    if kw == content.strip():
                        values = remove_extra_spaces(self.contents[index - 1].strip())
                        if len(values) == 0:
                            continue
                        self.name = values[0] # .split('  ')[0]
                        return


    def parse_within_line(self):
        for content in self.contents:
            for kw in line_keywords:
                valid_words = validate_line(content, kw)
                if valid_words is None:
                    continue
                self.name = valid_words[0]


    #def identify_name(self):
    def extract(self):
        self.parse_between_lines()
        if self.name == '':
            self.parse_within_line()
        return True

