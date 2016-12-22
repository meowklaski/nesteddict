""" A nested hash-map/dictionary object for Python """

import collections
try:
    basestring
except NameError:
    basestring = str

__author__ = "Nick Stanisha <github.com/nickstanisha>"
__version__ = 0.1


class NestedDict(object):
    """ An object representing a dictionary of dictionaries of dictionaries ...

        In order to avoid code like this

        >>> if 'a' in dictionary:
        ...     if 'b' in dictionary['a']
        ...         dictionary['a']['b']['c'] = 3
        ...     else:
        ...         dictionary['a']['b'] = {'c': 3}
        ... else:
        ...     dictionary['a'] = {'b': {'c': 3}}

        NestedDict enables the following syntax

        >>> nested_dictionary['a', 'b', 'c'] = 3

        A defaultdict coult be used to accomplish a similar goal, but only to
        a finite depth specified at the time of construction

        >>> # Nested dictionary of depth 4
        >>> d = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

        NestedDict is able to handle nested dictinoaries of arbitrary depth. Additionally,
        since NestedDict extends `dict`, it prints nicely to the console by default

        >>> my_default_dict
        defaultdict(<function <lambda> at 0x10077f840>, {1: defaultdict(<function <lambda>.<locals>.<lambda> at 0x10185a400>, {2: 3})})
        >>> my_nested_dict
        {1: {2: 3}}
    """
    def __init__(self, *args, **kwargs):
        self._dict = dict()
        self.keys = self._dict.keys
        self.update(*args, **kwargs)

    def __str__(self):
        return str(self._dict)

    def __repr__(self):
        return repr(self._dict)

    def __getitem__(self, key):
        if not isinstance(key, collections.Sequence) and not isinstance(key, basestring):
            return self._dict[key]

        d = self._dict
        for k in key:
            d = d[k]
        return d

    def __setitem__(self, key, value):
        if not isinstance(key, collections.Sequence) and not isinstance(key, basestring):
            self._dict[key] = value
        else:
            d = self._dict
            for k in key[:-1]:
                d = d.setdefault(k, {})
            d[key[-1]] = value

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except (KeyError, TypeError):
            return default

    def update(self, *args, **kwargs):
        self._dict.update(**kwargs)

        if len(args) > 1:
            raise TypeError("update expected at most 1 arguments, got {}".format(len(args)))
        if args:
            for keys, value in args[0]:
                self[keys] = value

