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
    numberInfo = mongo.db.numbers.find_one({'number': request.form['To']})

    # Verify that the dialed phone number is in the database
    if not numberInfo:
        app.logger.info("WARNING: Number {} not in database.".format(request.form['To']))
        err = plivoxml.Response()
        err.addSpeak(body="There has been an error. Please contact somebody.")
        return Response(str(err), mimetype='text/xml')

    # Get basic data from the POST
    caller_number = request.form['From']
    dialed_number = request.form['To']
    route_type = numberInfo['defaultRoute'][0]['type']
    bridge_name = uuid()

    # Get list of numbers to ring
    if route_type == "ringOne":
        connect_to_number = numberInfo['defaultRoute'][0]['number']
        connect_to_number_digits = readable_digits(connect_to_number)
        numbers_to_try = [connect_to_number]

    if DEBUG:
        log_state('incoming_call', locals())

    r = plivoxml.Response()
    r.addSpeak(body="I will attempt to connect you to " + connect_to_number_digits)

    r.addConference(
        body=bridge_name,
        waitSound=base_url_for(
            'wait_sound',
            user_id=user_id
            ),
        callbackUrl=base_url_for(
            'bridge_enter_exit',
            user_id=user_id,
            bridge_name=bridge_name,
            caller_number=caller_number,
            dialed_number=dialed_number,
            numbers_to_try='+'.join(numbers_to_try)
            ),
        action=base_url_for(
            'action_by_caller',
            user_id=user_id,
            bridge_name=bridge_name,
            caller_number=caller_number,
            dialed_number=dialed_number
            )
        )

    return Response(str(r), mimetype='text/xml')


@app.route('/v1/<ObjectId:user_id>/bridge_enter_exit/', methods=['POST'])
def bridge_enter_exit(user_id):
    '''
    On enter: Attempt to connect incoming call to one of the numbers in list.
    On exit: Redirect to different URL to close the bridge.
    '''
    return "OK"


@app.route('/v1/<ObjectId:user_id>/bridge/<bridge_name>/action_by_caller/', methods=['POST'])
def action_by_caller(user_id, bridge_name):
    '''
    Fired when an action is taken by the caller within phone call.
    '''
    app.logger.info("action by caller within call {}\ninfo: {}".format(
        bridge_name,
        request.form
        ))
    return "OK"


if __name__ == '__main__':
    app.run(debug=DEBUG)
