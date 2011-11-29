
_NOT_FOUND = "_not_found"

class _NoSuchAttribute(AttributeError):
    def __init__(self, k):
        self.k = k


class Bottom(object):
    def _p_get(self, k):
        raise _NoSuchAttribute(k)


class PObjectBase(object):
    def __init__(self, prototype):
        self.prototype = prototype

    def __getattribute__(self, k):
        try:
            o = object.__getattribute__(self, k)
        except AttributeError:
            o = _p_get_recursive(self.prototype, k)
        if hasattr(o, '__name__') and o.__name__ == '_p_late_binding':
            return o(self)
        else:
            return o

    def __str__(self):
        return self.show()


class PErrorBase(PObjectBase, BaseException):
    __init__ = PObjectBase.__init__

pobject = PObjectBase(Bottom())


def late_bind(func):
    def _p_late_binding(self):
        def _p_late_bound(*args, **kwargs):
            return func(*[self] + list(args), **kwargs)
        _p_late_bound.__doc__ = getattr(func, '__doc__', None)
        return _p_late_bound
    return _p_late_binding


def bind(self, func):
    setattr(self, func.__name__, late_bind(func))

pobject.bind = late_bind(bind)


@pobject.bind
def _p_get(self, k):
    try:
        o = object.__getattribute__(self, k)
    except AttributeError:
        o = _NOT_FOUND
    return o


def _p_get_recursive(p, k):
    while True:
        o = p._p_get(k)
        if o is not _NOT_FOUND:
            break
        p = p.prototype
    return o


@pobject.bind
def new(self):
    return PObjectBase(self)


@pobject.bind
def show(self):
    attrs = attributes(self)
    return "<@ %s >" % str(attrs)


def attributes(o):
    d = dict(o.__dict__)
    d.pop('prototype', None)
    return d


def failure(o):
    if not attributes(o).get('_e_typ'):
        class _Failure(PErrorBase):
            pass
        o._e_typ = _Failure
    return o._e_typ


perror = PErrorBase(pobject)

@perror.bind
def throw(self, **kwargs):
    o = self.new()
    for k,v in kwargs.items():
        setattr(o, k, v)
    raise failure(self)(o)


no_such_attribute = perror.new()
no_such_attribute._e_typ = _NoSuchAttribute
