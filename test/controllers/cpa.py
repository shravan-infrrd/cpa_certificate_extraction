import logging

from flask import request
from flask import jsonify
from flask_restful import Resource
import requests

from controllers.scanned_to_machined import read_scanned_pdf
from exceptions.exceptions_handler import *
from utils import formulate_response, is_machine_generated
from constant import PDF_UPLOAD_DIRECTORY, PROJECT_ROOT
from os import path
import os
from service.abby_data_extractor import extract_to_docx
import subprocess

from lib.helpers.parse_name import ParseName
from lib.helpers.parse_credits import ParseCredits
from lib.helpers.parse_field_of_study import ParseFieldOfStudy
from lib.helpers.parse_date import ParseDate
from lib.helpers.parse_delivery_methods import ParseDeliveryMethod
from lib.helpers.parse_sponsors import ParseSponsors


import uuid

"""
import spacy
from spacy import displacy
import en_core_web_sm
"""

class Cpa(Resource):

    def download_file(self, data):
        url = data['url']
        name = url.split('/')[-1]
        r = requests.get(data['url'])
        file_name = name.replace(' ', '_')
        print("FILE_NAME--->", file_name)
        file_name_without_ext = os.path.basename(file_name).split('.')[0]
        file_name_without_ext = file_name_without_ext + "_" + str(uuid.uuid1())
        file_name = file_name_without_ext + path.splitext(file_name)[1]
        doc_dir_location = os.path.join( PDF_UPLOAD_DIRECTORY, file_name_without_ext)
        print("DOC_DIR_LOCATION---->", doc_dir_location)
        if not os.path.exists(doc_dir_location):
                os.makedirs(doc_dir_location)
        file_location = os.path.join(doc_dir_location, file_name)
        print("File_LOC----->", file_location)        




        r = requests.get(url)
        with open(file_location, 'wb') as f:
            f.write(r.content)




    def post(self):
        #try:
        data = request.get_json()
        self.download_file(data)
        return jsonify(data)
        #except:
        #    return jsonify({"Error":"for some reason"})



