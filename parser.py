import operator

import numpy as np
import sympy as sp


class Syntax_Error(Exception):
    def __init__(self, string, index):
        print(string)
        print(' ' * index + '^')
        print('Invalid syntax')


class Unexpected_Character(Exception):
    def __init__(self, string):
        print(string)
        print('Unexpected character in string')


class Math:
    @staticmethod
    def ctg(num):
        return 1 / sp.tan(num)

    @staticmethod
    def factorial(num):
        if num > 0:
            return Math.factorial(num) * num
        elif num == 0:
            return 1
        raise ValueError('Incorrect argument')

    @staticmethod
    def unary_plus(num):
        return num

    @staticmethod
    def unary_minus(num):
        return -num

    @staticmethod
    def heaviside(num):
        return 1 if num > 0 else 0

    OPERATORS = {'+': (1, operator.add), '-': (1, operator.sub),
                 '*': (2, operator.mul), '/': (2, operator.truediv),
                 '^': (3, pow),
                 'u+': (4, unary_plus),
                 'u-': (4, unary_minus),
                 '!': (5, factorial)
                 }

    FUNCTIONS = {'sin': sp.sin, 'cos': sp.cos,
                 'tan': sp.tan, 'tg': sp.tan,
                 'cot': ctg, 'ctg': ctg,
                 'exp': sp.exp
                 }


class Math_Expression:
    def __init__(self, string, *args):
        self.functions = Math.FUNCTIONS
        self.operators = Math.OPERATORS
        self.string = string
        self.raw_str_len = len(self.string)
        self.variables = [item for item in args]
        self.validated_string = ''.join(self.validate_string())
        self.processed_str_len = len(self.string)
        self.value = np.nan

    def __str__(self):
        return str(self.string) + '\n' + str(self.validated_string)

    # TODO: replace is_previous_operator with index check
    def validate_string(self):
        is_previous_operator = False
        func_name = ''
        for index, token in enumerate(self.string):
            if token == ' ':
                continue
            elif token.isdigit() or token in '()':
                yield token
                is_previous_operator = False
            elif token == '.':
                if any(item.isdigit() for item in self.string[(index - 1) % self.raw_str_len: index + 1]):
                    yield token
                else:
                    raise Syntax_Error(self.string, index)
                is_previous_operator = False
            elif token in self.operators:
                if not is_previous_operator:
                    yield token
                elif is_previous_operator and token in ('+', '-'):
                    yield 'u' + token
                else:
                    raise Syntax_Error(self.string, index)
                is_previous_operator = True
            elif token in self.variables:
                yield token
                is_previous_operator = False
            else:
                func_name += token
                if func_name in self.functions:
                    yield func_name
                    func_name = ''
                is_previous_operator = False

        if func_name:
            raise Unexpected_Character(self.string)

    def subs(self, dict_):
        if isinstance(dict_, dict):
            for key in dict_:
                self.value = (self.validated_string.replace(key, str(dict_[key])))
            return eval(self.value)
        else:
            pass


exp = Math_Expression('. / 2', 'x')
print(exp)
# print(exp.subs({'x': 2}))
