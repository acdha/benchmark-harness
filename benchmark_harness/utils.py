from __future__ import absolute_import
from functools import wraps

import json

def json_output(f):
    """Allow functions to return normal Python data structue"""
    @wraps(f)
    def inner(*args, **kwargs):
        res = f(*args, **kwargs)
        print json.dumps(res, indent=4)
    return inner