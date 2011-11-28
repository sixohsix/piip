
from piip import pobject


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
