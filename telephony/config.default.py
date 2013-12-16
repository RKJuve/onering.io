import os

from flask import Flask
from flask.ext.pymongo import PyMongo
# from bson.objectid import ObjectId


DEBUG = True
AUTH_ID = 'put your auth_id here'
AUTH_TOKEN = 'put your auth_token here'
BASE_URL = 'enter internet-accessible url here'
RING_URL = 'enter internet-accessible url here'

app = Flask("onering", static_folder='./static', static_url_path='')
app.secret_key = os.urandom(24)
mongo = PyMongo(app)
