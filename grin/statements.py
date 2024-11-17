# grin/statements.py

from grin.token import GrinToken, GrinTokenKind
from typing import Optional, Dict, Any

class Statement:
    """Base class for all GRIN statements"""
    def execute(self, variables: Dict[str, Any]) -> Optional[str]:
        raise NotImplementedError()

class LabeledStatement:
    """Wrapper for statements that can have labels"""
    def __init__(self, label: Optional[str], statement: Statement):
        self.label = label
        self.statement = statement

class LetStatement(Statement):
    def __init__(self, variable: GrinToken, value: GrinToken):
        self.variable = variable
        self.value = value

    def execute(self, variables: Dict[str, Any]) -> Optional[str]:
        if self.value.kind() == GrinTokenKind.IDENTIFIER:
            if self.value.text() not in variables:
                raise RuntimeError(f"Variable '{self.value.text()}' not defined")
            variables[self.variable.text()] = variables[self.value.text()]
        else:
            variables[self.variable.text()] = self.value.value()
        return None

class PrintStatement(Statement):
    def __init__(self, value: GrinToken):
        self.value = value

    def execute(self, variables: Dict[str, Any]) -> Optional[str]:
        if self.value.kind() == GrinTokenKind.IDENTIFIER:
            if self.value.text() not in variables:
                raise RuntimeError(f"Variable '{self.value.text()}' not defined")
            print(variables[self.value.text()])
        else:
            print(self.value.value())
        return None

class InNumStatement(Statement):
    def __init__(self, variable: GrinToken):
        self.variable = variable

    def execute(self, variables: Dict[str, Any]) -> Optional[str]:
        try:
            value = float(input())
            variables[self.variable.text()] = value
            return None
        except ValueError:
            raise RuntimeError("Invalid numeric input")

class InStrStatement(Statement):
    def __init__(self, variable: GrinToken):
        self.variable = variable

    def execute(self, variables: Dict[str, Any]) -> Optional[str]:
        variables[self.variable.text()] = input()
        return None

class ArithmeticStatement(Statement):
    def __init__(self, operation: str, variable: GrinToken, value: GrinToken):
        self.operation = operation
        self.variable = variable
        self.value = value

    def execute(self, variables: Dict[str, Any]) -> Optional[str]:
        if self.variable.text() not in variables:
            raise RuntimeError(f"Variable '{self.variable.text()}' not defined")
        
        if self.value.kind() == GrinTokenKind.IDENTIFIER:
            if self.value.text() not in variables:
                raise RuntimeError(f"Variable '{self.value.text()}' not defined")
            operand = variables[self.value.text()]
        else:
            operand = self.value.value()

        if self.operation == 'ADD':
            variables[self.variable.text()] += operand
        elif self.operation == 'SUB':
            variables[self.variable.text()] -= operand
        elif self.operation == 'MULT':
            variables[self.variable.text()] *= operand
        elif self.operation == 'DIV':
            if operand == 0:
                raise RuntimeError("Division by zero")
            variables[self.variable.text()] /= operand
        return None

class GotoStatement(Statement):
    def __init__(self, target: GrinToken):
        self.target = target

    def execute(self, variables: Dict[str, Any]) -> str:
        return self.target.text()

class GosubStatement(Statement):
    def __init__(self, target: GrinToken):
        self.target = target

    def execute(self, variables: Dict[str, Any]) -> str:
        return f"GOSUB:{self.target.text()}"

class ReturnStatement(Statement):
    def execute(self, variables: Dict[str, Any]) -> str:
        return "RETURN"

class EndStatement(Statement):
    def execute(self, variables: Dict[str, Any]) -> str:
        return "END"
