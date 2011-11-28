
Prototypal Inheritance In Python
=======

This is an experimental project to bring prototypal inheritance
(JavaScript style) to Python.

I am doing this for a few reasons:

 1. To see if it's possible
 2. To see if a reasonable API can be made for it
 3. As a useful library for problem domains where prototype inheritance makes more sense than normal Python inheritance
 4. I was bored


Using prototypal inheritance
------

Obtain the `piip` library from GitHub and install it in your project.

Start coding prototypically:

```python

from piip import pobject, pattributes


# pobject is the root protypal object. Extend from it with new():

my_first_object = pobject.new()


# you can assign attributes to an object and those values will be
# visible to children:

my_first_object.var_one = "hello"
my_second_object = my_first_object.new()

print(my_second_object.var_one)  # "hello"


# By default, if you assign a function to an object, the function will
# be totally unbound, like a "staticmethod":

def static_method(a, b): # NO self!
    return a + b

my_first_object.unbound_method = static_method
print(my_first_object.unbound_method(5, 6))  # "11"


# You can create bound methods with the bind function:

def my_bound_func(self, b):
    return self.a + b

my_first_object.bind(my_bound_func)
my_first_object.a = 5
print(my_first_object.my_bound_func(6))  # "11"


# This is especially nice as a decorator:

@my_first_object.bind
def another_bound_func(self):
    return self.x * 2

my_first_object.x = 3
print(my_first_object.another_bound_func())  # "6"


# And of course, bound functions behave sanely on new objects:
another_obj = my_first_object.new()
another_obj.x = 5
print(another_obj.another_bound_func())  # "10"

```
