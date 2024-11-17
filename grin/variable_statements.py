from typing import Dict, Any, Optional
from .base_statement import Statement
from .token import GrinToken
from .exceptions import GrinVariableError

class LetStatement(Statement):
    def __init__(self, tokens: list[GrinToken]):
        self.var_token = tokens[1]
        self.value_token = tokens[2]

    def execute(self, variables: Dict[str, Any], line_number: int) -> Optional[int]:
        value = self.get_value(self.value_token, variables)
        if value is None:
            raise GrinVariableError(f"Variable {self.value_token.text()} not defined")
        variables[self.var_token.text()] = value
        return line_number + 1
