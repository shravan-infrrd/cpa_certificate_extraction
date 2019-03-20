import json
import logging
from decimal import Decimal

from flask import Flask, request
from flask import send_from_directory
from flask import jsonify
from flask_cors import CORS
from flask_restful import Api
from healthcheck import HealthCheck

import timeit
import constant
from constant import DE_APPLICATION_NAME, PDF_UPLOAD_DIRECTORY
from controllers.extract_data import ExtractData
from controllers.cpa import Cpa
# from exceptions.exception_logger import create_logger
# from log import configure_logger, DE_LOG_FILE_PATH

import json
import copy



class DataExtractorJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return json.JSONEncoder.default(self, o)


class DEConfig:
    RESTFUL_JSON = {"cls": DataExtractorJSONEncoder}

de_health = HealthCheck()

app = Flask(DE_APPLICATION_NAME)
# configure_logger(app.logger, logging.INFO, DE_LOG_FILE_PATH)
# create_logger(DE_LOG_FILE_PATH)
app.config.from_object(DEConfig)
CORS(app)


api = Api(app, catch_all_404s=True)

# Extract data API for Machines and Scanned PDF.
@app.route('/', methods=["GET"])
def home_page_route():
    resp = send_from_directory("static", "index.html")
    return resp

@app.route('/pdf_file/<file_name>', methods=['GET'])
def render_pdf_file(file_name):
    base_path = "uploads/" + file_name + '/pages'
    file_name = 'stitched.pdf'
    print('BASE_PATH-', base_path, "File_name->", file_name)
    return send_from_directory(base_path, file_name)

@app.route('/text_file/<file_name>', methods=['GET'])
def render_text_file(file_name):
    base_path = "uploads/" + file_name + '/texts'
    file_name = 'stitched.txt'
    print('BASE_PATH-', base_path, "File_name->", file_name)
    return send_from_directory(base_path, file_name)

def build_data(doc):
    return {
        'name': doc['name'],
        'program_name': doc['program_name'],
        'delivery_method': doc['delivery_method']
    }

@app.route('/list', methods=['GET'])
def list_data():
    docs = mongo.db.certificates.find()
    lists = []
    for doc in docs:
        lists.append( build_data(doc) )
        """
        lists.append({"id": "hello",
                      'program_name': doc['program_name'],
                      'delivery_method': doc['delivery_method'],
                      'name': doc['name']
        })
        """
    data = {"data": lists}
    return jsonify(data)



api.add_resource(ExtractData, "/find")
api.add_resource( Cpa, "/extract")



# Flask route to expose Health Check information
app.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: de_health.run())

@app.before_request
def log_request():
    app.logger.info("Request:\n{}".format(request.get_json()))


@app.after_request
def log_response(response):
    #app.logger.info("Response:\n{}".format(response.data.decode()))
    return response


if __name__ == "__main__":
    app.run(debug=False, host=constant.HOST, port=constant.PORT_NUMBER)
