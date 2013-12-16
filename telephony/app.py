import plivo
import plivoxml

from flask import request, Response

from config import app, mongo, DEBUG, AUTH_ID, AUTH_TOKEN, RING_URL
from util import readable_digits, log_state, base_url_for, uuid


p = plivo.RestAPI(AUTH_ID, AUTH_TOKEN)


@app.route('/v1/<ObjectId:user_id>/incoming/', methods=['POST'])
def incoming_call(user_id):
    '''
    Entry point for new, incoming calls.
    '''
    pass


if __name__ == '__main__':
    app.run(debug=DEBUG)
