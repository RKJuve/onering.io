import os

import redis
from pymongo import MongoClient
import plivo

DEBUG = (os.getenv('PRODUCTION', 'false') != 'true')
AUTH_ID = os.getenv('PLIVO_AUTH_ID', 'MAMJE4NJBKZTHHNZRHYW')
AUTH_TOKEN = os.getenv('PLIVO_AUTH_TOKEN', 'MzBhZjlmN2Y5ZGY5Y2I0ZjY5OTFmNjJhYmM0ZmU2')
QUEUE_NAME = os.getenv('QUEUE_NAME', 'onering-worker-queue')

mongo = MongoClient()

redis = redis.StrictRedis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=0
    )

plivo = plivo.RestAPI(AUTH_ID, AUTH_TOKEN)
