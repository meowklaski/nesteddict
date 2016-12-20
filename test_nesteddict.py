from __future__ import absolute_import
from nesteddict import NestedDict
import pytest


class TestNestedDict:
    def test_init(self):
        d = NestedDict()
        assert(isinstance(d, dict))

    def test_kwargs_init(self):
        d = NestedDict(a=[2, 3, 4], b=24, c='hello')
        assert(d == {'a': [2, 3, 4], 'b': 24, 'c': 'hello'})

    def test_iter_init(self):
        d = NestedDict([(1, 2), (3, 4), ('hello', 'goodbye')])
        assert(d == {1: 2, 3: 4, 'hello': 'goodbye'})

    def test_setter(self):
        d = NestedDict()
        d[1, 'a', 34] = [1, 2]
        assert(d == {1: {'a': {34: [1, 2]}}})

        d[1, 'a', 34].extend([4, 3])
        assert(d == {1: {'a': {34: [1, 2, 4, 3]}}})

        d[1, 'a'] = 'hello'
        assert(d == {1: {'a': 'hello'}})

    def test_shallow_setter(self):
        d = NestedDict()
        d[1] = 'a'
        assert(d == {1: 'a'})

    def test_getter(self):
        d = NestedDict()
        d['a', 'b', 'c'] = 'hello'
        d['a', 'b', 'd'] = 'goodbye'

        assert(d['a', 'b', 'c'] == 'hello')
        assert(d['a', 'b'] == {'c': 'hello', 'd': 'goodbye'})

    def test_shallow_get(self):
        d = NestedDict()
        d[1, 2, 3] = 4

        assert(d.get(1) == {2: {3: 4}})
        assert(d.get(2) is None)
        assert(d.get(2, 'arbitrary') == 'arbitrary')

    def test_nested_get(self):
        d = NestedDict()
        d[1, 2, 3] = 4
        assert(d.get([1, 3]) is None)
        assert(d.get([1, 3], 'arbitrary') == 'arbitrary')
        assert(d.get([1, 2, 3]) == 4)

    def test_get_errors(self):
        d = NestedDict()
        d['a', 'b', 'c'] = 23
        with pytest.raises(KeyError, message="Expecting KeyError"):
            val = d['a', 'c']

        with pytest.raises(KeyError, message="Expecting KeyError"):
            val = d['b']

        with pytest.raises(TypeError, message="Expecting TypeError"):
            val = d['a', 'b', 'c', 'd']

    def test_update(self):
        """ This maintains `dict`s functionality, only merging the
            top-level keys.
        """
        d, e, = NestedDict(), NestedDict()
        d[1, 2, 3] = [1, 2]
        d[2, 'k'] = 16
        e[1, 2, 4] = [3, 4]
        e[3] = 'hello'
        d.update(e)
        assert(d == {1: {2: {4: [3, 4]}}, 2: {'k': 16}, 3: 'hello'})

