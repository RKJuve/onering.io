from uuid import uuid1
from flask import url_for
import msgpack

from config import app, BASE_URL

packer = msgpack.Packer(use_bin_type=True)


# - - - - - - - - - - #
#  Utility Functions  #
# - - - - - - - - - - #

def base_url_for(*args, **kwargs):
    return BASE_URL + url_for(*args, **kwargs)


def log_state(location, values):
    to_log = ""
    for value in values:
        if isinstance(values[value], str):
            to_log += "{}: {}\n".format(value, values[value])
    app.logger.info(to_log)


def readable_digits(digits):
    if len(digits) > 10:
        # digits = digits[:-10] + ',' + digits[-10:-7] + ',' + digits[-7:-4] + ',' + digits[-4:]
        digits = digits[:-10] + ',' + digits[-10:]
    if len(digits) > 7:
        # digits = digits[:-7] + ',' + digits[-7:-4] + ',' + digits[-4:]
        digits = digits[:-7] + ',' + digits[-7:]
    if len(digits) > 4:
        # digits = digits[:-4] + ',' + digits[-4:]
        digits = digits[:-4] + ',' + digits[-4:]
    return ' '.join(list(digits))


def uuid():
    return str(uuid1())


def pack(data):
    return msgpack.packb(data, use_bin_type=True)


def unpack(data):
    return msgpack.unpackb(data, encoding='utf-8')
