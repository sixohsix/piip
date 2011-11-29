
from piip import pobject, attributes, perror, no_such_attribute, failure


def test_can_extend_pobj():
    my_o = pobject.new()
    assert my_o is not pobject


def test_can_read_val_of_extended_pobj():
    my_o = pobject.new()
    my_o.asdf = 4
    my_o2 = my_o.new()
    assert my_o2.asdf == 4


def test_can_extend_obj_with_method():
    my_o = pobject.new()

    @my_o.bind
    def my_method(self, a_number):
        return 4 + a_number

    assert 11 == my_o.my_method(7)


def test_bound_methods_are_bound_late_enough():
    my_o = pobject.new()
    my_o.asdf = 4

    @my_o.bind
    def my_method(self, a_number):
        return self.asdf + a_number

    my_o2 = my_o.new()
    my_o2.asdf = 6

    assert 11 == my_o.my_method(7)
    assert 13 == my_o2.my_method(7)


def test_can_get_only_my_attributes():
    my_o = pobject.new()
    my_o.asdf = 4
    my_o2 = my_o.new()
    my_o2.vrrf = 6

    assert attributes(my_o2) == dict(vrrf=6)


def test_can_get_my_prototype():
    my_o = pobject.new()
    my_o2 = my_o.new()
    assert my_o2.prototype is my_o


def test_can_assign_my_prototype():
    my_o = pobject.new()
    my_o.asdf = 7
    other_o = pobject.new()
    other_o.asdf = 9
    my_o2 = my_o.new()
    my_o2.prototype = other_o
    assert 9 == my_o2.asdf


def test_custom_str_format():
    my_o = pobject.new()

    @my_o.bind
    def show(self):
        return "hello!"

    assert "hello!" == str(my_o)


def test_accessing_no_attr_raises_no_such_attribute():
    try:
        pobject.flummox
        assert False
    except failure(no_such_attribute):
        pass


def test_can_raise_and_catch_piip_errors():
    my_err = perror.new()
    ok = False
    try:
        my_err.throw()
        assert False
    except failure(my_err), e:
        ok = True
    except:
        assert False


def test_can_raise_and_catch_piip_errors_with_kwarg():
    my_err = perror.new()
    ok = False
    try:
        my_err.throw(kwarg='kwarg')
        assert False
    except failure(my_err), e:
        assert e.kwarg == 'kwarg'
        ok = True
    except:
        assert False
    assert ok

