import os

from flask import Flask
from flask.ext.pymongo import PyMongo
import redis


DEBUG = (os.getenv('PRODUCTION', 'false') != 'true')
AUTH_ID = os.getenv('PLIVO_AUTH_ID', 'your AUTH_ID')
AUTH_TOKEN = os.getenv('PLIVO_AUTH_TOKEN', 'your AUTH_TOKEN')
BASE_URL = os.getenv('ONERING_BASE_URL', 'network accessible url')
RING_URL = os.getenv('ONERING_RING_URL', 'network accessible url for ringtone')

app = Flask("onering", static_folder='./static', static_url_path='')
app.secret_key = os.getenv('ONERING_SECRET_KEY', os.urandom(24))

mongo = PyMongo(app)

redis = redis.StrictRedis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=0
    )
