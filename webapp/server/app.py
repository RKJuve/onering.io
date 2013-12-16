import flask
from flask import session, redirect, url_for, escape, request, render_template
# import pymongo
from flask.ext.pymongo import PyMongo
from bson.objectid import ObjectId

from util import login_required, api_login_required, json_response, json_oid


app = flask.Flask("onering", static_folder='../build', static_url_path='')
app.secret_key = 'A0Zrsds739dgs8j/3yX R~XHH!jmN]LWX/,?RT'
mongo = PyMongo(app)


@app.route('/')
# @login_required
def root():
    return render_template('index.html')


@app.route('/main.js')
def mainjs():
    response = flask.send_from_directory('../build', 'main.jgz')
    response.headers['Content-Encoding'] = 'gzip'
    return response


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


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('email', None)
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
    # GET
    if request.method == 'GET':
        # Authorization
        app.logger.debug(session)
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


@app.route('/v1/vendors/<ObjectId:vendor_id>', methods=['GET'])
def vendor(vendor_id):
    vendor = mongo.db.vendors.find_one({'_id': vendor_id})
    return json_response(vendor)


@app.route('/v1/vendors/<ObjectId:vendor_id>', methods=['PUT'])
@api_login_required
def vendors_put(vendor_id):
    # Authorization
    vendor = mongo.db.vendors.find_one({'_id': vendor_id})
    if not vendor['sharedId'] == ObjectId(session['sharedId']):
        return json_response({'message': 'unauthorized'}, status_code=401)
    return json_response(vendor)


@app.route('/v1/vendors', methods=['POST'])
@api_login_required
def vendor_new():
    vendor_data = request.json
    vendor_data['sharedId'] = ObjectId(session['sharedId'])
    oid = mongo.db.vendors.insert(vendor_data)
    vendor = mongo.db.vendors.find_one({'_id': ObjectId(oid)})
    return json_response(vendor)


@app.route('/v1/customers/<ObjectId:customer_id>', methods=['GET'])
def customers_get_(customer_id):
    customer = mongo.db.customers.find_one({'_id': customer_id})
    return json_response(customer)


@app.route('/v1/customers/<ObjectId:customer_id>', methods=['PUT'])
@api_login_required
def customers_put(customer_id):
    # Authorization
    customer = mongo.db.customers.find_one({'_id': customer_id})
    if not customer['sharedId'] == ObjectId(session['sharedId']):
        return json_response({'message': 'unauthorized'}, status_code=401)

    return json_response(customer)


@app.route('/v1/customers', methods=['GET', 'POST'])
@api_login_required
def customers_get_post():
    if request.method == 'GET':
        customers = mongo.db.customers.find({'sharedId': ObjectId(session['sharedId'])})
        return json_response(list(customers))

    elif request.method == 'POST':
        customer_data = request.json
        customer_data['sharedId'] = ObjectId(session['sharedId'])
        oid = mongo.db.customers.insert(customer_data)
        customer = mongo.db.customers.find_one({'_id': ObjectId(oid)})
        return json_response(customer)


###---------------###

@app.route('/v1/invoices/<ObjectId:invoice_id>', methods=['GET'])
def invoice(invoice_id):
    # GET
    invoice = mongo.db.invoices.find_one({'_id': invoice_id})
    return json_response(invoice)


@app.route('/v1/invoices/<ObjectId:invoice_id>', methods=['PUT'])
@api_login_required
def invoice_put(invoice_id):
    # Authorization
    invoice = mongo.db.invoices.find_one({'_id': invoice_id})
    if not invoice['sharedId'] == ObjectId(session['sharedId']):
        return json_response({'message': 'unauthorized'}, status_code=401)

    return json_response(invoice)


# @app.route('/v1/invoices', methods=['PUT', 'POST'])
@app.route('/v1/invoices', methods=['POST', 'GET'])
@api_login_required
def invoice_new():
    if request.method == 'POST':
        invoice_data = request.json
        invoice_data['sharedId'] = ObjectId(session['sharedId'])
        oid = mongo.db.invoices.insert(invoice_data)
        invoice = mongo.db.invoices.find_one({'_id': ObjectId(oid)})
        return json_response(invoice)

    elif request.method == 'GET':
        invoices = mongo.db.invoices.find({'sharedId': ObjectId(session['sharedId'])})
        return json_response(list(invoices))


@app.route('/v1/itemcache', methods=['GET'])
@api_login_required
def itemcache():
    return json_response({})


@app.route('/v1/payments/<ObjectId:payment_id>', methods=['GET'])
@api_login_required
def payment():
    pass


@app.route('/v1/payments', methods=['POST'])
def payment_post():
    json_data = request.json
    json_data['processed'] = False
    mongo.db.payments.insert(json_data)
    return json_response(json_data)


@app.route('/v1/secret/path/to/receive/payment/from/balanced', methods=['POST'])
def payment_new():
    pass


if __name__ == '__main__':
    app.run(debug=True)
