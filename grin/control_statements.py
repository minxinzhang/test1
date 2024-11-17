from typing import Dict, Any, Optional, List
from .base_statement import Statement
from .token import GrinToken, GrinTokenKind
from .exceptions import GrinRuntimeError

class GotoStatement(Statement):
    def __init__(self, tokens: List[GrinToken]):
        if len(tokens) < 2:
            raise GrinRuntimeError("GOTO requires a target")
        self.target_token = tokens[1]
        self.condition = None
        
        if len(tokens) > 2:
            if tokens[2].text() == "IF":
                if len(tokens) < 5:
                    raise GrinRuntimeError("Invalid IF condition")
                self.condition = (tokens[3], tokens[4])

    def execute(self, variables: Dict[str, Any], line_number: int) -> Optional[int]:
        if self.condition:
            if not self._evaluate_condition(variables):
                return None  # Continue to next line if condition is false
                
        target = self.get_value(self.target_token, variables)
        
        if isinstance(target, str):
            return self.program.get_line_number(f'"{target}"')
        elif isinstance(target, (int, float)):
            target = int(target)
            new_line = line_number + target
            self.program.validate_goto_target(new_line)
            return new_line
        else:
            raise GrinRuntimeError(f"Invalid GOTO target type: {type(target)}")

    def _evaluate_condition(self, variables: Dict[str, Any]) -> bool:
        left_val = self.get_value(self.condition[0], variables)
        right_val = self.get_value(self.condition[1], variables)
        
        if type(left_val) != type(right_val):
            if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
                left_val = float(left_val)
                right_val = float(right_val)
            else:
                raise GrinRuntimeError(f"Cannot compare {type(left_val)} with {type(right_val)}")
        
        op = self.condition[1].text()
        
        if op == "<":
            return left_val < right_val
        elif op == "<=":
            return left_val <= right_val
        elif op == ">":
            return left_val > right_val
        elif op == ">=":
            return left_val >= right_val
        elif op == "=":
            return left_val == right_val
        elif op == "<>":
            return left_val != right_val
        else:
            raise GrinRuntimeError(f"Unknown comparison operator: {op}")

class GosubStatement(GotoStatement):
    def execute(self, variables: Dict[str, Any], line_number: int) -> Optional[int]:
        if self.condition and not self._evaluate_condition(variables):
            return None
            
        next_line = super().execute(variables, line_number)
        if next_line is not None:
            self.program.push_return_line(line_number + 1)
        return next_line

class ReturnStatement(Statement):
    def execute(self, variables: Dict[str, Any], line_number: int) -> Optional[int]:
        return_line = self.program.pop_return_line()
        if return_line is None:
            raise GrinRuntimeError("RETURN without matching GOSUB")
        return return_line

class EndStatement(Statement):
    def execute(self, variables: Dict[str, Any], line_number: int) -> Optional[int]:
        return -1  # Signal to stop execution
