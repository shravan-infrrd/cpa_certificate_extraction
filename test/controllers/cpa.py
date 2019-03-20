
import requests
import logging
import time
from flask import Flask, request
from flask import jsonify
from flask_restful import Resource

from controllers.scanned_to_machined import read_scanned_pdf, read_scanned_image
from exceptions.exceptions_handler import *
from utils import formulate_response, is_machine_generated
from constant import PDF_UPLOAD_DIRECTORY, PROJECT_ROOT, REFERENCE_FILE
from os import path
import os
import subprocess


from lib.parse_certificate import parse_all_fields
from openpyxl import Workbook
import openpyxl
import uuid

class Cpa(Resource):

    def download_file(self, data):
        url = data['url']
        name = url.split('/')[-1]
        r = requests.get(data['url'])
        file_name = name.replace(' ', '_')
        print("FILE_NAME--->", file_name)
        file_name_without_ext = os.path.basename(file_name).split('.')[0]
        file_name_without_ext = file_name_without_ext + "_" + str(uuid.uuid1())
        file_name = file_name_without_ext + path.splitext(file_name)[1] + '.pdf'
        doc_dir_location = os.path.join( PDF_UPLOAD_DIRECTORY, file_name_without_ext)
        print("DOC_DIR_LOCATION---->", doc_dir_location)
        if not os.path.exists(doc_dir_location):
                os.makedirs(doc_dir_location)
        file_location = os.path.join(doc_dir_location, file_name)
        print("File_LOC----->", file_location)        




        r = requests.get(url)
        with open(file_location, 'wb') as f:
            f.write(r.content)

        result = read_scanned_pdf( file_location, doc_dir_location )
        text_file_path = os.path.join(PDF_UPLOAD_DIRECTORY, file_name_without_ext, 'texts', 'stitched.txt')

        with open( text_file_path ) as fp:
            contents = fp.readlines()
        result = {}
        parse_all_fields(contents, result)
        return result

    def post(self):
        #try:
        data = request.get_json()
        result = self.download_file(data)
        data = result
        return jsonify(data)
        #except:
        #    return jsonify({"Error":"for some reason"})



