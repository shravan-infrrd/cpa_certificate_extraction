from dateparser.search import search_dates
from lib.common_methods import remove_extra_spaces, validate_line, hasNumbers

line_keywords = ['Date:', 'Dated', 'Date Completed:', 'Presentation Date:', 'Date Attended:', 'Completion Date:', 'Event Date:', 'Session End Date', 'Oate Attended:', 'Completion Date', 'Session End Date', 'awarded this certificate on']
post_keywords = ['Date Attended', 'Date of Completion', 'event on']
pre_keywords  = ['Date Certified', 'Date', 'Date of Course', 'Dace of Course', 'Program Date(s)', 'Course Date']


class ParseCompletionDate():

    def __init__(self, contents):
        self.contents = contents
        self.date     = ""

    def validate_date(self, dates):
        return True

    def parse_completion_date(self):
        for content in self.contents:
            print("Content->>>", content)
            dates = search_dates(content, settings={'PREFER_LANGUAGE_DATE_ORDER': False})
            print("Completion Date-->", dates)
            if dates is None:
                continue
            else:
                if self.validate_date(dates):
                    self.date = str(dates[0])
            
  

    def extract(self):
        self.parse_completion_date()

