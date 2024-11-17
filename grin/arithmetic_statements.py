from typing import Dict, Any, Optional
from .base_statement import Statement
from .token import GrinToken
from .exceptions import GrinVariableError

class ArithmeticStatement(Statement):
    def __init__(self, tokens: list[GrinToken]):
        self.var_token = tokens[1]
        self.value_token = tokens[2]

    def get_numeric_value(self, value: Any) -> float:
        if isinstance(value, (int, float)):
            return float(value)
        raise GrinVariableError("Non-numeric value in arithmetic operation")

class AddStatement(ArithmeticStatement):
    def execute(self, variables: Dict[str, Any], line_number: int) -> Optional[int]:
        var_value = self.get_value(self.var_token, variables)
        value = self.get_value(self.value_token, variables)
        variables[self.var_token.text()] = self.get_numeric_value(var_value) + self.get_numeric_value(value)
        return line_number + 1

class SubStatement(ArithmeticStatement):
    def execute(self, variables: Dict[str, Any], line_number: int) -> Optional[int]:
        var_value = self.get_value(self.var_token, variables)
        value = self.get_value(self.value_token, variables)
        variables[self.var_token.text()] = self.get_numeric_value(var_value) - self.get_numeric_value(value)
        return line_number + 1

class MultStatement(ArithmeticStatement):
    def execute(self, variables: Dict[str, Any], line_number: int) -> Optional[int]:
        var_value = self.get_value(self.var_token, variables)
        value = self.get_value(self.value_token, variables)
        variables[self.var_token.text()] = self.get_numeric_value(var_value) * self.get_numeric_value(value)
        return line_number + 1

class DivStatement(ArithmeticStatement):
    def execute(self, variables: Dict[str, Any], line_number: int) -> Optional[int]:
        var_value = self.get_value(self.var_token, variables)
        value = self.get_value(self.value_token, variables)
        divisor = self.get_numeric_value(value)
        if divisor == 0:
            raise GrinVariableError("Division by zero")
        variables[self.var_token.text()] = self.get_numeric_value(var_value) / divisor
        return line_number + 1
