from typing import Dict, Any, Optional
from .base_statement import Statement
from .token import GrinToken
from .exceptions import GrinVariableError

class PrintStatement(Statement):
    def __init__(self, tokens: list[GrinToken]):
        self.value_token = tokens[1]

    def execute(self, variables: Dict[str, Any], line_number: int) -> Optional[int]:
        value = self.get_value(self.value_token, variables)
        if value is None:
            raise GrinVariableError(f"Variable {self.value_token.text()} not defined")
        print(value)
        return line_number + 1

class InNumStatement(Statement):
    def __init__(self, tokens: list[GrinToken]):
        self.var_token = tokens[1]

    def execute(self, variables: Dict[str, Any], line_number: int) -> Optional[int]:
        try:
            value = input()
            if '.' in value:
                variables[self.var_token.text()] = float(value)
            else:
                variables[self.var_token.text()] = int(value)
            return line_number + 1
        except ValueError:
            raise GrinVariableError("Invalid numeric input")

class InStrStatement(Statement):
    def __init__(self, tokens: list[GrinToken]):
        self.var_token = tokens[1]

    def execute(self, variables: Dict[str, Any], line_number: int) -> Optional[int]:
        variables[self.var_token.text()] = input()
        return line_number + 1
