from abc import ABC, abstractmethod


# Define the decorator
def ensure_bye_after(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.bye()
        return result

    return wrapper


# Abstract Parent Class
class Parent(ABC):
    @ensure_bye_after
    def hey(self):
        pass

    def bye(self):
        print("Goodbye from Parent")


# Child Class
class Child(Parent):
    def hey(self):
        print("Hello from Child")


# Another Child Class
class AnotherChild(Parent):
    def hey(self):
        print("Hello from AnotherChild")


# Example Usage
child = Child()
child.hey()
# Output:
# Hello from Child
# Goodbye from Parent

another_child = AnotherChild()
another_child.hey()
# Output:
# Hello from AnotherChild
# Goodbye from Parent
