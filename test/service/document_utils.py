import re
import subprocess

import pdfplumber

from constant import DocType, THRESHOLD_FOR_SCANNED_PDF


def get_doc_type(filename):
    try:
        fp = pdfplumber.open(filename)
        page = fp.pages[0]
        if page is not None:
            data = page.extract_text()
            if data is not None:
                data = data.split(' ')
                if len(data) > THRESHOLD_FOR_SCANNED_PDF:
                    return DocType.MACHINED.value
                else:
                    return DocType.SCANNED.value
            else:
                return DocType.SCANNED.value
        return DocType.SCANNED.value
    except Exception as e:
        return DocType.SCANNED.value

#filename = "/Users/shravanc/flask/aditya_birla/test_files/essar.pdf"
#ifilename = "/Users/shravanc/flask/aditya_birla/test_files/nirma_test_file.pdf"

#ftype = get_doc_type(filename)
#print(ftype)
