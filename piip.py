
class NoSuchAttribute(Exception):
    def __init__(self, k):
        self.k = k


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
        self.prototype = prototype

    def _p_get_rec(self, k):
        try:
            o = object.__getattribute__(self, k)
        except AttributeError:
            o = self.prototype._p_get_rec(k)
        return o

    def __getattribute__(self, k):
        try:
            o = object.__getattribute__(self, k)
        except AttributeError:
            o = self.prototype._p_get_rec(k)
        if hasattr(o, '__name__') and o.__name__ == '_p_late_binding':
            return o(self)
        else:
            return o


pobject = PObjectBase(Bottom())

def bind(self, func):
    setattr(self, func.__name__, late_bind(func))

pobject.bind = late_bind(bind)


@pobject.bind
def new(self):
    return PObjectBase(self)


def pattributes(o):
    d = dict(o.__dict__)
    d.pop('prototype', None)
    return d
