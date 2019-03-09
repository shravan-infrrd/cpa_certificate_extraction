from utils import list_all_files
from scanned_to_machined import read_scanned_pdf, read_scanned_image

from lib.parse_data import parse_all_fields
from os import path
import os
import uuid

from flask import Flask, request
import json
from flask_pymongo import PyMongo
import copy


app = Flask('mongo')
app.config['MONGO_DBNAME'] = 'cpa_database'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/cpa_database'

mongo = PyMongo(app)


path = "/Users/shravanc/flask/flask_apps/cpa/UserSamples"
files = list_all_files(path)
upload_path = "/Users/shravanc/flask/flask_apps/cpa_certificate_extraction/development/uploads"

def save_in_db(data):
    certificate_data = copy.deepcopy(data)
    mongo.db.certificates.insert(certificate_data)


for fp in files:
    if fp.startswith('.'):
        continue
    file_name_without_ext = os.path.basename(fp).split('.')[0]
      
    filename = path + '/' + fp
    doc_dir_location = os.path.join(upload_path, file_name_without_ext)
    if not os.path.exists(doc_dir_location):
        os.makedirs(doc_dir_location)
    result = read_scanned_pdf( filename, doc_dir_location)


    text_file_path = os.path.join(upload_path, file_name_without_ext, 'texts', 'stitched.txt')

    with open( text_file_path ) as fp:
        contents = fp.readlines()
    parse_all_fields(contents, result)
    save_in_db(result) 
    print("===COMPLETED===")
