
class NoSuchAttribute(Exception):
    def __init__(self, k):
        self.k = k


class pdict(dict):
    def __init__(self, proto_dict):
        self.__pdict = proto_dict

    def __getitem__(self, k):
        try:
            return dict.__getitem__(self, k)
        except KeyError:
            return self.__pdict[k]


class root_pdict(dict):
    def __getitem__(self, k):
        raise NoSuchAttribute(k)


class Bottom(object):
    def _p_get_rec(self, k):
        raise NoSuchAttribute(k)


def late_bind(func):
    def _p_late_binding(self):
        def _p_late_bound(*args, **kwargs):
            return func(*[self] + list(args), **kwargs)
        return _p_late_bound
    return _p_late_binding


class PObjectBase(object):
    def __init__(self, prototype):
        self._prototype = prototype

    def _p_get_rec(self, k):
        try:
            o = object.__getattribute__(self, k)
        except AttributeError:
            o = self._prototype._p_get_rec(k)
        return o

    def new(self):
        return PObjectBase(self)

    def __getattribute__(self, k):
        try:
            o = object.__getattribute__(self, k)
        except AttributeError:
            o = self._prototype._p_get_rec(k)
        if hasattr(o, '__name__') and o.__name__ == '_p_late_binding':
            return o(self)
        else:
            return o

    def bind(self, func):
        setattr(self, func.__name__, late_bind(func))


pobject = PObjectBase(Bottom())
