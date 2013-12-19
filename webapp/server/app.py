import flask
from flask import session, redirect, url_for, escape, request, render_template
from flask.ext.pymongo import PyMongo
from bson.objectid import ObjectId

from util import login_required, api_login_required, json_response, json_oid
from config import SECRET_KEY

app = flask.Flask("onering", static_folder='../build', static_url_path='')
app.secret_key = SECRET_KEY

mongo = PyMongo(app)


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        existing_user = mongo.db.users.find_one({'email': request.form['email']})
        if existing_user:
            session['email'] = request.form['email']
            session['userId'] = str(existing_user['_id'])
            session['sharedId'] = str(existing_user['sharedId'])
            return redirect(request.args.get('next') or url_for('root'))
        else:
            return "invalid email address"
    else:
        # validation?
        return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # remove the username from the session if it's there
    session.pop('email', None)
    session.pop('_id', None)
    if request.method == "POST":
        return "OK"
    return redirect(url_for('testlogin'))


@app.route('/testlogin')
@login_required
def testlogin():
    if 'email' in session:
        return 'Logged in as {}.'.format(escape(session['email']))
    return 'You are not logged in.'


#####################
###  REST ROUTES  ###
#####################

@app.route('/v1/user/<ObjectId:user_id>', methods=['PUT'])
@api_login_required
def user(user_id):
    # Authorization
    user = mongo.db.users.find_one({'_id': user_id})
    if not user['email'] == session['email']:
        return json_response({'message': 'unauthorized'}, status_code=401)

    # PUT
    oid = mongo.db.users.save(json_oid(request.json))
    user = mongo.db.users.find_one({'_id': ObjectId(oid)})
    return json_response(user)


@app.route('/v1/user', methods=['GET', 'POST'])
def user_new():
    app.logger.info('got here first')
    # GET
    if request.method == 'GET':
        # Authorization
        user = mongo.db.users.find_one({'_id': ObjectId(session['userId'])})
        if not user:
            return json_response({'message': 'cannot find user'}, status_code=500)
        return json_response(user)

    # POST
    elif request.method == 'POST':
        # Check if account already exists
        exists = mongo.db.users.find_one({'email': request.json['email']})
        if exists:
            return json_response({'message': 'email already exists'}, status_code=409)
        new_user_data = request.json
        new_user_data['sharedId'] = ObjectId()
        oid = mongo.db.users.insert(new_user_data)
        user = mongo.db.users.find_one({'_id': ObjectId(oid)})
        return json_response(user)


if __name__ == '__main__':
    app.run(debug=True)
