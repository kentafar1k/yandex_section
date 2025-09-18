class A:
    x = 1

class Calculator:
    def divide(self, x, y):
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError('x and y must be integers')
        if y == 0:
            raise ZeroDivisionError('Cannot divide by zero')
        return x / y

    def add(self, x, y):
        return x + y
