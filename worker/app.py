import plivo
import plivoxml
import msgpack

from config import mongo, redis, plivo, DEBUG, QUEUE_NAME


###################
###  MAIN LOOP  ###
###################

def main_loop():
    handlers = {
        "outgoing_sms": outgoing_sms,
        "outgoing_email": outgoing_email
    }

    while True:
        # blocking call - will only return once something is in queue
        task = unpack(redis.blpop(QUEUE_NAME))
        handler = handlers[task['type']]
        handler(task)


#######################
###  TASK HANDLERS  ###
#######################

def outgoing_sms(task):
    params = {
        'src': task['from'],
        'dst': task['to'],
        'text': task['body'],
        'type': 'sms'
    }
    plivo.send_message(params)


def outgoing_email(task):
    pass


##########################
###  HELPER FUNCTIONS  ###
##########################

def pack(data):
    return msgpack.packb(data, use_bin_type=True)


def unpack(data):
    return msgpack.unpackb(data, encoding='utf-8')


if __name__ == "__main__":
    main_loop()
