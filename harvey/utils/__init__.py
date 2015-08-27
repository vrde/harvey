import urllib
import collections
import time
import sys
import hashlib
import traceback

current_milli_time = lambda: int(round(time.time() * 1000))
hasher = lambda s: hashlib.md5(s).hexdigest()


def quote(url):
    return urllib.quote(url.encode('utf-8'), safe='~@#$&*!+=:;,.?/')


def format_exc():
    etype, value, tb = sys.exc_info()
    exc = map(lambda x: x.decode('utf8', errors='ignore'),
              traceback.format_exception(etype, value, tb, 10))
    return u''.join(exc)


def update(d, u):
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d
