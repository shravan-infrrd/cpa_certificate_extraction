#text_file = "./text_files/22.txt"
from lib.common_methods import remove_extra_spaces, validate_line, hasNumbers


pre_keywords = ['Delivery method:'] 
post_keywords = ['Delivery Method']
line_keywords = ['Program Location:', 'Format:', 'Delivery Method:', 'Instructional Delivery Method -', 'Method Used:', 'Delivery Method']
delivery_method_lists = ['Group live', 'Group Internet based', 'QAS Self study', 'Blended learning', 'Nano learning', 'Group Internet-Based']

invalid_keywords = ['CPE']

class ParseDeliveryMethod():

    def __init__(self, contents):
        self.contents = contents
        self.delivery_method = ""

    def validate_delivery_method(self):
        if self.delivery_method is None:
            self.delivery_method = ""
            return False

        for dml in delivery_method_lists:
            #print("dml====>", dml.lower(), "====>", self.delivery_method)
            if dml.lower() in self.delivery_method.lower():
                return True
        for kw in invalid_keywords:
            if kw.lower() in self.delivery_method.lower():
                self.delivery_method = ""
                return False
        self.delivery_method = ""
        return False


    def get_high_score_value(self, values):
        #print("Value====>", values)
        for val in values:
            if 'CPE' not in val:
                #print("Value====>", val)
                return val
  
    def get_valid_value(self, index):
        for i in range(index+1, index+2):
            if ':' not in self.contents[i].strip():
                values = remove_extra_spaces( self.contents[ i ].strip())
                #self.delivery_method = self.get_high_score_value(values)
                #self.delivery_method = remove_extra_spaces( self.contents[ i ].strip())[0]
                #print("1-Before-get_valid_value")
                if self.delivery_method is None:
                    continue
                if self.validate_delivery_method():
                    return


    def parse_between_lines(self):
        print("===========================1=============================")
        for index, content in enumerate( self.contents ):
            for kw in pre_keywords:
                if kw in content.strip():
                    #print("*****START*****", content)
                    #print("DeliveryMethod**>", kw)
                    self.get_valid_value(index)
                    #print("*****END*******", kw)
                    #print("2-Before-get_valid_value")
                    if self.validate_delivery_method():
                        return
                    

        print(f"===========================3=============================")
        if self.delivery_method == "":
            for index, content in enumerate(self.contents):
                for kw in post_keywords:
                    if kw in content.strip():
                        #print("Index1-->", self.contents[index].strip())
                        #print("Index2-->", self.contents[index-1].strip())
                        values = remove_extra_spaces( self.contents[index-1].strip() )
                        #print("*****START****", content)
                        #print("values->", values)
                        #print("*****END******", kw)
                        for val in values:
                            if ':' not in val:
                                self.delivery_method = val
                                if self.validate_delivery_method():
                                    return
                        """
                        if ':' not in values[0]:
                            self.delivery_method = values[0]
                            print("3-Before-get_valid_value")
                            if self.validate_delivery_method():
                                return
                        """

    def parse_within_lines(self): 
        for index, content in enumerate(self.contents):
            for kw in line_keywords:
                if kw in content.strip():
                    valid_words = validate_line(content, kw)
                    if valid_words is None:
                        continue
                    self.delivery_method = valid_words[0]
                    #print("4-Before-get_valid_value")
                    if self.validate_delivery_method():
                        return
                
    def extract(self):
        self.parse_within_lines()
        if self.delivery_method == "":
            self.parse_between_lines()
        return True


