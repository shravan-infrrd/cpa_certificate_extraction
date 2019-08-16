import json
import re

import pymongo
from bson import json_util
#from geotext import GeoText
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId

from constant import MONGO_URI
#from log import get_logger



class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return obj


def connect_to_db():
		client = MongoClient(MONGO_URI)
		database = client.cpa_database
		certificates = database.certificates
		return certificates

def fetch_data_from_mongo(doc_id=None):
		try:
				certificates = connect_to_db()
				if doc_id is None:
						documents = certificates.find()
						email_data_lists = []
						for doc in documents:
								email_data_lists.append({'_id': str(doc['_id']), 'file_name': doc['pdf_file_path'].split('/')[-1] })
						return email_data_lists
				else:
						document = certificates.find_one({'_id': ObjectId(doc_id) })
						data = {'file_name': document['pdf_file_path']}
						return json.dumps(document, cls=Encoder)
		except:
				
				pass

