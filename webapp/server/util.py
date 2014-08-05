import json
from functools import wraps

from flask import request, redirect, url_for, session, make_response  # , Response
from bson import json_util
from bson.objectid import ObjectId


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'email' in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def api_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'email' in session:
            return json_response({'message': 'login required'}, status_code=401)
        return f(*args, **kwargs)
    return decorated_function


def json_response(to_json, status_code=200):
    if isinstance(to_json, dict):
        for k in to_json:
            if isinstance(to_json[k], ObjectId):
                to_json[k] = str(to_json[k])

    if isinstance(to_json, list):
        for e in to_json:
            if isinstance(e, dict):
                for k in e:
                    if isinstance(e[k], ObjectId):
                        e[k] = str(e[k])

    r = make_response(json.dumps(to_json, default=json_util.default))
    r.status_code = status_code
    r.mimetype = 'application/json'
    return r


def json_oid(json_data, keys=('_id', 'sharedId')):
    for k in keys:
        if k in json_data:
            json_data[k] = ObjectId(json_data[k])
    return json_data
