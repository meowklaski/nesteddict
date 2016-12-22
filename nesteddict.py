""" A nested hash-map/dictionary object for Python """

import collections
from functools import reduce
try:
    basestring
except NameError:
    basestring = str

__author__ = "Nick Stanisha <github.com/nickstanisha>"
__version__ = 0.1


def _keys_in_dict(dataDict, parent=[]):
    if not isinstance(dataDict, dict):
        return [tuple(parent)]
    else:
        return reduce(list.__add__, [_keys_in_dict(v, parent + [k]) for k,v in dataDict.items()], [])

def _get_nested(d, keys, default=None):
    if not isinstance(keys, collections.Sequence) or isinstance(keys, basestring):
        raise TypeError(str(type(keys)) + " is not a non-string Sequence") 
    try:
        for key in keys:
            d = d[key]
        return d
    except KeyError:
        return default

def _set_nested(d, keys, value):
    if not isinstance(keys, collections.Sequence) or isinstance(keys, basestring):
        raise TypeError(str(type(keys)) + " is not a non-string Sequence")
    _d = d
    for key in keys[:-1]:
        _d = _d.setdefault(key, {})
    _d[keys[-1]] = value


class NestedDict(dict):
    def get_nested(self, *args):
        if len(args) < 1:
            raise TypeError("get_nested expected at least 1 argument, got 0")
        if len(args) > 2:
            raise TypeError("get_nested expected at most 2 arguments, got {}".format(len(args)))

        keys, default = args if len(args) == 2 else (args[0], None)
        return _get_nested(self, keys, default)

    def set_nested(self, keys, value):
        _set_nested(self, keys, value)

    def nested_keys(self):
        return _keys_in_dict(self)

    def update_nested(self, *args, **kwargs):
        if len(args) > 1:
            raise TypeError("update expected at most 1 arguments, got %d" % len(args))
        if args and isinstance(args[0], dict):
            for keys in _keys_in_dict(args[0]):
                self.set_nested(keys, _get_nested(args[0], keys))
        elif args:
            for keys, value in args[0]:
                self.set_nested(keys, value)
        self.update(**kwargs)

