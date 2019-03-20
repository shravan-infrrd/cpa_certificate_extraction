import os
from enum import Enum

DE_APPLICATION_NAME = "cpa"

""" Constants module which defines all status/error code
    and messages at global level
"""
MONGO_DB_CLIENT = 'mongodb://localhost:27017/cpa_database'
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
TEST_FILES   =  os.path.join(PROJECT_ROOT, 'test_files')
TEMPORARY_DOWNLOAD_PATH = os.path.join(PROJECT_ROOT, 'temporary')
REFERENCE_FILE = os.path.join(PROJECT_ROOT, 'reference_file.xlsx')
TEST_PDF_PATH  = os.path.join(PROJECT_ROOT, 'test_pdf_paths' )


PDF_UPLOAD_DIRECTORY = os.path.join(PROJECT_ROOT, "uploads")
FILE_ERRORS = 404
FILE_ERRORS_DESC = "File Not Found Error"

BAD_REQUEST_ERRORS = 400
BAD_REQUEST_ERRORS_DESC = "Bad Request Error"

INTERNAL_ERVER_ERROR = 500
INTERNAL_ERVER_ERROR_DESC = "Internal Server Error"

INDEX_OUT_OF_BOUND = 6001
INDEX_OUT_OF_BOUND_DESC = "Index out of Bound Error."

INTERNAL_SERVER_ERROR = 500
INTERNAL_SERVER_ERROR_DESC = "Internal Server Error Occurred."

ERR_FILE_READ = 4001
ERR_FILE_READ_DESC = "File not found"

ERR_FILE_WRITE = 4002
ERR_FILE_WRITE_DESC = "File couldn't be saved"

ERR_PANEL_HEADER_EXTRACTION = 1003
ERR_PANEL_HEADER_EXTRACTION_DESC = "Failed to extract panel header"

ERR_PANEL_BODY_EXTRACTION = 1004
ERR_PANEL_BODY_EXTRACTION_DESC = "Failed to extract panel body"

ERR_HOCR_WORD_JSON_CONVERSION = 1005
ERR_HOCR_WORD_JSON_CONVERSION_DESC = "Failed to convert hocr to word json"

ERR_BAD_REQUEST = 5001
ERR_BAD_REQUEST_DESC = "Mandatory Fields weren't present."

ERR_BAD_REQUEST_DOC_TYPE = 5002
ERR_BAD_REQUEST_DOC_TYPE_DESC = "Invalid document type"

ERR_HOCR_PARSER = 5003
ERR_HOCR_PARSER_DESC = "Error while parsing the hocr string"

"""
    PDF Split Constants
"""

RESPONSE_TEMPLATE_JSON = "response_template.json"
EXTRACTED_WORD_JSON = "extracted_word.json"

PORT_NUMBER = 4000

HOST = "0.0.0.0"

APP_ROOT = os.path.dirname(os.path.abspath(__file__))  # refers to application_top
APP_MODEL = os.path.join(APP_ROOT, 'models')  # refers to application_models
APP_CONTROLLER = os.path.join(APP_ROOT, 'controllers')  # refers to application_controllers
APP_RESOURCE = os.path.join(APP_ROOT, 'resources')  # refers to the files used for testing

"""
    Machined vs Scanned Constants
"""
THRESHOLD_FOR_SCANNED_PDF = 10

"""
    Header Meta Info Constants
"""

HEADER_TAB_SPACE_PIXELS = 25
HEADER_LINE_VERTICAL_PIXELS = 8

"""ENUMS"""


class DocType(Enum):
    SCANNED = "scanned"
    MACHINED = "machined"


