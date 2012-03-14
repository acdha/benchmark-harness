from __future__ import absolute_import

from functools import wraps
import json
import sys

from benchmark_harness.stats import display_stats


def format_output(f):
    """Allow functions to return normal Python data structure

    If stdout is a tty, basic stats and a human-meaningful result will be
    displayed. If not, JSON will be returned for a script to process
    """
    @wraps(f)
    def inner(*args, **kwargs):
        res = f(*args, **kwargs)

        if sys.stdout.isatty():
            if 'name' in res.get('meta', {}):
                name = res['meta']['name']
            else:
                name = sys.argv[0]

            display_stats(name, res['times'])
        else:
            print json.dumps(res, indent=4)
    return inner
