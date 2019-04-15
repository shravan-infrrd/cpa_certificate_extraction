
import requests
import logging
import time
from flask import Flask, request
from flask import jsonify
from flask_restful import Resource

from controllers.scanned_to_machined import read_scanned_pdf, read_scanned_image
from exceptions.exceptions_handler import *
from utils import formulate_response, is_machine_generated
from constant import PDF_UPLOAD_DIRECTORY, PROJECT_ROOT, REFERENCE_FILE, TEMPORARY_DOWNLOAD_PATH
from os import path
import os
import subprocess
import copy


from lib.parse_certificate import parse_all_fields
from lib.empty_response_format import get_empty_response
from openpyxl import Workbook
import openpyxl
import uuid

class Cpa(Resource):


		def download_file1(self, data):
				url = data['url']
				name = url.split('/')[-1].split('?')[0]
				r = requests.get(data['url'])
				file_name = name.replace(' ', '_')
				extension = os.path.basename(file_name).split('.')[1]

				file_name_without_ext = os.path.basename(file_name).split('.')[0]
				file_name_without_ext = file_name_without_ext + "_" + str(uuid.uuid1())
				file_name = file_name_without_ext + path.splitext(file_name)[1] #+ '.pdf'

				doc_dir_location = os.path.join( PDF_UPLOAD_DIRECTORY, file_name_without_ext)
				if not os.path.exists(doc_dir_location):
								os.makedirs(doc_dir_location)
				file_location = os.path.join(doc_dir_location, file_name)


				r = requests.get(url)
				with open(file_location, 'wb') as f:
						f.write(r.content)

				if extension in ['jpg', 'jpeg', 'png']:
						result = read_scanned_image( file_location, doc_dir_location )
				else:
						result = read_scanned_pdf( file_location, doc_dir_location )
				text_file_path = os.path.join(PDF_UPLOAD_DIRECTORY, file_name_without_ext, 'texts', 'stitched.txt')

				with open( text_file_path ) as fp:
						contents = fp.readlines()
				result = {}
				parse_all_fields(contents, result)
				result['id'] = data['id']
				return result

		def download_file(self, data):
				url = data['url']
				name = url.split('/')[-1].split('?')[0]
				r = requests.get(data['url'])
				file_name = name.replace(' ', '_')
				extension = os.path.basename(file_name).split('.')[1]

				file_name_without_ext = os.path.basename(file_name).split('.')[0]
				file_name_without_ext = file_name_without_ext + "_" + str(uuid.uuid1())
				file_name = file_name_without_ext + path.splitext(file_name)[1] #+ '.pdf'

				doc_dir_location = os.path.join( PDF_UPLOAD_DIRECTORY, file_name_without_ext)
				if not os.path.exists(doc_dir_location):
								os.makedirs(doc_dir_location)
				file_location = os.path.join(doc_dir_location, file_name)


				r = requests.get(url)
				with open(file_location, 'wb') as f:
						f.write(r.content)

				erosion_val = [0, 3]
				max_try = len(erosion_val) - 1

				for index, e_val in enumerate(erosion_val):
						if extension in ['jpg', 'jpeg', 'png']:
								result = read_scanned_image( file_location, doc_dir_location, e_val )
						else:
								result = read_scanned_pdf( file_location, doc_dir_location, e_val )


						text_file_path = os.path.join(PDF_UPLOAD_DIRECTORY, file_name_without_ext, 'texts', 'stitched.txt')
            
						with open( text_file_path ) as fp:
								contents = fp.readlines()
						result = {'id': data['id']}
						parse_all_fields(contents, result)


						if e_val == 0:
								first_result = copy.deepcopy(result)
						if result['field_of_study']:
								return result
						else:
								if index == max_try:
										if result['field_of_study']:
												return result
										else:
												return first_result
								else:
										continue	

				return result

		def post(self):
				try:
						data = request.get_json()
						result = self.download_file(data)
						data = result
						return jsonify(data)
				except:
						empty_response = get_empty_response()
						return jsonify( empty_response )
						#return jsonify({"Error":"for some reason"})



