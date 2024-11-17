from typing import Optional, Dict, Any
from grin.token import GrinToken, GrinTokenKind

class Statement:
    """Base class for all GRIN statements"""
    def execute(self, variables: Dict[str, Any]) -> Optional[str]:
        """
        Execute the statement and return control flow instruction if any
        Returns:
            None: Continue to next statement
            "END": End program
            "RETURN": Return from subroutine
            "label": Jump to label
            "GOSUB:label": Call subroutine
        """
        raise NotImplementedError()

class LabeledStatement:
    """A statement that may have a label"""
    def __init__(self, label: Optional[str], statement: Statement):
        self.label = label
        self.statement = statement

class LetStatement(Statement):
    """Assigns a value to a variable"""
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
    """Prints a value"""
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
    """Reads a number from input"""
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
    """Reads a string from input"""
    def __init__(self, variable: GrinToken):
        self.variable = variable

    def execute(self, variables: Dict[str, Any]) -> Optional[str]:
        variables[self.variable.text()] = input()
        return None

class ArithmeticStatement(Statement):
    """Performs arithmetic operations"""
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
    """Jumps to a label or line number, optionally with a condition"""
    def __init__(self, target: GrinToken, condition: Optional[str] = None, left: Optional[GrinToken] = None, right: Optional[GrinToken] = None):
        self.target = target
        self.condition = condition
        self.left = left
        self.right = right

    def execute(self, variables: Dict[str, Any]) -> Optional[str]:
        if self.condition:
            left_value = variables[self.left.text()] if self.left.kind() == GrinTokenKind.IDENTIFIER else self.left.value()
            right_value = variables[self.right.text()] if self.right.kind() == GrinTokenKind.IDENTIFIER else self.right.value()
            
            if self.condition == '<' and left_value < right_value:
                return self._get_target(variables)
            elif self.condition == '>' and left_value > right_value:
                return self._get_target(variables)
            elif self.condition == '=' and left_value == right_value:
                return self._get_target(variables)
            else:
                return None
        else:
            return self._get_target(variables)

    def _get_target(self, variables: Dict[str, Any]) -> str:
        if self.target.kind() == GrinTokenKind.IDENTIFIER:
            if self.target.text() not in variables:
                raise RuntimeError(f"Variable '{self.target.text()}' not defined")
            target = variables[self.target.text()]
        else:
            target = self.target.value()

        if isinstance(target, int):
            return str(target)
        elif isinstance(target, str):
            return target
        else:
            raise RuntimeError(f"Invalid GOTO target: {target}")

class GosubStatement(Statement):
    """Calls a subroutine"""
    def __init__(self, target: GrinToken):
        self.target = target

    def execute(self, variables: Dict[str, Any]) -> str:
        return f"GOSUB:{self.target.text()}"

class ReturnStatement(Statement):
    """Returns from a subroutine"""
    def execute(self, variables: Dict[str, Any]) -> str:
        return "RETURN"

class EndStatement(Statement):
    """Ends the program"""
    def execute(self, variables: Dict[str, Any]) -> str:
        return "END"
