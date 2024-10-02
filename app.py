import csv
import json
import logging
from flask import Flask, jsonify, request
import connexion
from Routes.ProjectRoute import project_route
from flask_cors import CORS
import pathlib

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app

app.register_blueprint(project_route, url_prefix='/project')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
