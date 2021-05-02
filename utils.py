from collections import namedtuple
from typing import List
import math
import re

Operator = namedtuple('operator', ['name', 'result', 'precedence', 'arity'])
Add = Operator('+', lambda x, y: x + y, 0,  2)
Sub = Operator('-', lambda x, y: x - y, 0,  2)
Mult = Operator('*', lambda x, y: x * y, 1,  2)
Divide = Operator('/', lambda x, y: x / y, 1,  2)
Mod = Operator('%', lambda x, y: x % y, 1,  2)
Power = Operator('^', lambda x, y: x**y, 2,  2)
Exponential = Operator('exp', lambda x: math.exp(x), 3, 1)
Logarithm = Operator('log', lambda x: math.log(x), 3, 1)
Sine = Operator('sin', lambda x: math.sin(x), 3, 1)
Cosine = Operator('cos', lambda x: math.cos(x), 3, 1)
Tangent = Operator('tan', lambda x: math.tan(x), 3, 1)
Cotangent = Operator('cot', lambda x: 1/math.tan(x), 3, 1)


class Evaluator:
    def __init__(self, expression: str, values: List[float] = None):
        self.expression = expression
        self.values = values
        self.operators_stack = []
        self.operands_stack = []
        self.operators = {op.name: op for op in [Add, Sub, Mult, Divide, Mod, Power, Cosine]}
        self._results = []

    @property
    def split_expression_string(self) -> List[str]:
        regex_pattern_binary = '([' + ''.join(['\\' + key for key, value in self.operators.items() if value.arity == 2]) + '])'
        regex_pattern_parentheses = '([()])'
        regex_pattern_unary = '(' + ')|('.join([key for key, value in self.operators.items() if value.arity == 1]) + ')'
        regex_pattern = regex_pattern_binary + '|' + regex_pattern_parentheses + '|' + regex_pattern_unary
        return [el for el in re.split(regex_pattern, self.expression) if (el is not '' and el is not None)]

    @property
    def results(self):
        if not self._results:
            self.parse_evaluate_expression()
            return self._results
        else:
            return self._results

    @staticmethod
    def apply_operator(operator: Operator, operands_list: List[float]):
        operands = operands_list[-operator.arity:]
        del operands_list[-operator.arity:]
        print(f'applying {operator.name} to {operands}')
        result = operator.result(*operands)
        print(f'result: {result}')
        operands_list.append(result)

    def parse_evaluate_expression(self):
        elements = self.split_expression_string
        for value in self.values:
            parentheses_counter = 0
            for i in range(len(elements)):
                element = elements[i]
                if element == '(':
                    parentheses_counter += 1
                    self.operators_stack.append(element)
                elif element == ')':
                    parentheses_counter -= 1
                    if parentheses_counter < 0:
                        raise Exception(f"Incorrect closing parenthesis: {''.join(elements[:i+1])}")
                    else:
                        while self.operators_stack[-1] != '(':
                            stacked_operator = self.operators.get(self.operators_stack.pop())
                            self.apply_operator(stacked_operator, self.operands_stack)
                        self.operators_stack.pop()
                elif element in self.operators:
                    # print(f'found operator {element}')
                    operator = self.operators[element]
                    if (not self.operators_stack) or self.operators_stack[-1] == '(':
                        self.operators_stack.append(element)
                    elif operator.precedence <= self.operators[self.operators_stack[-1]].precedence:
                        stacked_operator = self.operators[self.operators_stack.pop()]
                        self.apply_operator(stacked_operator, self.operands_stack)
                        self.operators_stack.append(element)
                    else:
                        self.operators_stack.append(element)
                else:
                    # print(f'found operand {element}')
                    self.operands_stack.append(value) if element == 'x' else self.operands_stack.append(float(element))

            while self.operators_stack:
                operator = self.operators[self.operators_stack.pop()]
                self.apply_operator(operator, self.operands_stack)
            if len(self.operands_stack) > 1:
                raise Exception('no operators left. Only one operand should be present')
            else:
                self._results.append(self.operands_stack.pop())

