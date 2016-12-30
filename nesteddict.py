""" A nested hash-map/dictionary object for Python """

import collections
from functools import reduce

try:
    basestring
except NameError:
    basestring = str

__author__ = "Nick Stanisha <github.com/nickstanisha>"
__version__ = 0.1


def _keys_in_dict(d, path=[]):
    """ Return tuples of subsequent keys of nested dicts.

        I.e. {a:
                 {b: {d: 1},
                  c: 2},
              e: 2}

              -> [('a', 'c'), ('a', 'b', 'd'), ('e',)]

        Parameters
        ----------
        d : dict
            Dictionary whose 'key-tree' is returned.
        path : List[Any, ...]

        Returns
        -------
        List[Tuple[Any, ...], ...] """
    if not isinstance(d, dict):
        return [tuple(path)]
    else:
        return reduce(list.__add__, [_keys_in_dict(v, path + [k]) for k, v in d.items()], [])

def _get_nested(d, keys, default=None):
    """ Get an item within nested dictionaries, given a sequence of keys.

        Parameters
        ----------
        d : dict
        keys : Sequence[Hashable, ...]
            The sequence of subsequent keys used to access the dictionary's items.
        default : Optional[Any]
            The value returned if there is a key error.abs

        Returns
        -------
        Any """
    if not isinstance(keys, collections.Sequence) or isinstance(keys, basestring):
        raise TypeError(str(type(keys)) + " is not a non-string Sequence")
    try:
        for key in keys:
            d = d[key]
        return d
    except KeyError:
        return default

def _set_nested(d, keys, value):
    """ Set a value in a nested dictionary given a sequence of keys, creating
        nested dictionaries where possible.

        Parameters
        ----------
        d : dict
            Dictionary in which the value is set.
        keys : Sequence[Hashable, ...]
            The sequence of subsequent keys used to access the dictionary's items.
        value : Any
            The value to be set.

        Raises
        ------
        KeyError
            The sequence of keys specified is not available for setting. """
    if not isinstance(keys, collections.Sequence) or isinstance(keys, basestring):
        raise TypeError(str(type(keys)) + " is not a non-string Sequence")
    try:
        for n, key in enumerate(keys[:-1]):
            d = d.setdefault(key, {})
        d[keys[-1]] = value
    except (TypeError, AttributeError):
        raise KeyError("The nested-dictionary key sequence: {} " 
        " is not available to be set".format(" -> ".join(str(i) for i in keys[:n+1])))


class NestedDict(dict):
    def get_nested(self, *args):
        """ Get an item within nested dictionaries, given a sequence of keys.

            Parameters
            ----------
            keys : Sequence[Hashable, ...]
                The sequence of subsequent keys used to access the dictionary's items.

            Returns
            -------
            Any """
        if len(args) < 1:
            raise TypeError("get_nested expected at least 1 argument, got 0")
        if len(args) > 2:
            raise TypeError("get_nested expected at most 2 arguments, got {}".format(len(args)))

        keys, default = args if len(args) == 2 else (args[0], None)
        return _get_nested(self, keys, default)

    def set_nested(self, keys, value):
        """ Set an value in a nested dictionary given a sequence of keys, creating
            nested dictionaries where possible.

            Parameters
            ----------
            keys : Sequence[Hashable, ...]
                The sequence of subsequent keys used to access the dictionary's items.
            value : Any
                The value to be set.

            Raises
            ------
            KeyError
                The sequence of keys specified is not available for setting. """
        _set_nested(self, keys, value)

    def nested_keys(self):
        """ Return tuples of subsequent keys of nested dicts.

            I.e. {a:
                    {b: {d: 1},
                     c: 2},
                  e: 2}

                -> [('a', 'c'), ('a', 'b', 'd'), ('e',)]

            Returns
            -------
            List[Tuple[Any, ...], ...] """
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

