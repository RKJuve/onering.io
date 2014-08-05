import plivo
import plivoxml

from flask import request, Response
from bson.objectid import ObjectId

from config import app, mongo, redis, DEBUG, AUTH_ID, AUTH_TOKEN, RING_URL
from util import readable_digits, log_state, base_url_for, uuid, pack, unpack, current_time


p = plivo.RestAPI(AUTH_ID, AUTH_TOKEN)


#############################
###  REST ROUTES - PHONE  ###
#############################

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

    elif route_type == "ringMany":
        numbers_to_try = [number for number in numberInfo['defaultRoute'][0]['numbers']]
        connect_to_number_digits = "one of multiple phone numbers."

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
    On exit: Close the bridge with receiver.
    '''

    bridge_name = request.args.get('bridge_name')
    caller_number = request.args.get('caller_number')
    dialed_number = request.args.get('dialed_number')
    numbers_to_try = request.args.get('numbers_to_try').split('+')

    if DEBUG:
        log_state('bridge_enter_exit', locals())

    # Handle exit event
    if request.form['Event'] == "ConferenceExit":
        app.logger.info("caller has hung up?")
        p.hangup_conference({'conference_name': bridge_name})
        return "OK"

    # Handle enter event
    reference_name = 'call_request+{}'.format(bridge_name)
    for number in numbers_to_try:
        call_request = p.make_call({
            'from': caller_number,
            'to': number,
            'answer_url': base_url_for(
                'bridge_success',
                user_id=user_id,
                bridge_name=bridge_name,
                caller_number=caller_number,
                dialed_number=dialed_number,
                success_number=number,
                numbers_tried='+'.join(numbers_to_try)
                )
            })

        if call_request[0] == 201:
            # push call request data into redis
            redis.lpush(reference_name, pack({
                'request_uuid': call_request[1]['request_uuid'],
                'number': number
                }))

    redis.expire(reference_name, 120)
    return "OK"


@app.route('/v1/<ObjectId:user_id>/bridge_success/<bridge_name>/', methods=['POST'])
def bridge_success(user_id, bridge_name):
    '''
    Fired when an endpoint phone picks up.
    '''
    caller_number = request.args.get('caller_number')
    dialed_number = request.args.get('dialed_number')
    numbers_tried = request.args.get('numbers_tried').split('+')
    success_number = request.args.get('success_number')

    r = plivoxml.Response()

    r.addConference(
        body=bridge_name,
        waitSound='',
        callbackUrl=base_url_for(
            'bridge_cancel_other_attempts',
            user_id=user_id,
            bridge_name=bridge_name,
            caller_number=caller_number,
            dialed_number=dialed_number,
            success_number=success_number,
            numbers_tried='+'.join(numbers_tried)
            ),
        action=base_url_for(
            'action_by_receiver',
            user_id=user_id,
            bridge_name=bridge_name,
            caller_number=caller_number,
            dialed_number=dialed_number,
            numbers_tried='+'.join(numbers_tried)
            )
        )

    return Response(str(r), mimetype='text/xml')


@app.route('/v1/<ObjectId:user_id>/bridge_cancel_other_attempts/<bridge_name>/', methods=['POST'])
def bridge_cancel_other_attempts(user_id, bridge_name):
    '''
    When a phone is picked up, stop ringing the others.
    '''
    success_number = request.args.get('success_number')
    reference_name = 'call_request+{}'.format(bridge_name)
    numbers_tried = redis.lrange(reference_name, 0, -1)
    if not numbers_tried:
        app.logger.warning('cannot find cached call data for bridge ' + bridge_name)

    for packed_number_info in numbers_tried:
        number_info = unpack(packed_number_info)
        if not number_info['number'] == success_number:
            p.hangup_request({
                'request_uuid': number_info['request_uuid']
                })
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


@app.route('/v1/<ObjectId:user_id>/bridge/<bridge_name>/action_by_receiver/', methods=['POST'])
def action_by_receiver(user_id, bridge_name):
    '''
    Fired when an action is taken by the receiver within phone call.
    '''
    app.logger.info("action by receiver within call {}\ninfo: {}".format(
        bridge_name,
        request.form
        ))

    # Handle exit event
    if request.form['CallStatus'] == 'completed':
        app.logger.info("receiver has hung up")
        p.hangup_conference({'conference_name': bridge_name})

    return "OK"


@app.route('/v1/<ObjectId:user_id>/wait_sound/', methods=['POST'])
def wait_sound(user_id):
    '''
    When a call is connecting, give caller something to listen to.
    '''
    r = plivoxml.Response()
    r.addPlay(RING_URL, loop=0)
    # r.addSpeak(body="Trying to connect, please wait.", language='en-US')
    return Response(str(r), mimetype='text/xml')


@app.route('/v1/<ObjectId:user_id>/caller_hangup/', methods=['POST'])
def hangup(user_id):
    '''
    Fired when caller hangs up the phone.
    '''
    app.logger.info("caller " + request.form['From'] + " has hung up")
    return "OK"


###########################
###  REST ROUTES - SMS  ###
###########################

@app.route('/v1/<ObjectId:user_id>/sms/', methods=['POST'])
def incoming_sms(user_id):
    sms = {
        "_plivo_uuid": request.form['MessageUUID'],
        "_user_id": user_id,
        "from": request.form['From'],
        "to": request.form['To'],
        "caller_name": "",
        "time_received": current_time(),
        "body": request.form['Text']
    }
    mongo.db.sms.insert(sms)

    return "OK"


if __name__ == '__main__':
    app.run(debug=DEBUG)
