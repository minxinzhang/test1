from typing import Dict, Any, List, Optional
from grin.token import GrinToken, GrinTokenKind
from grin.statements import (
    Statement, LabeledStatement, LetStatement, PrintStatement,
    InNumStatement, InStrStatement, ArithmeticStatement,
    GotoStatement, GosubStatement, ReturnStatement, EndStatement
)

class GrinInterpreter:
    """GRIN language interpreter"""
    
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.statements: List[LabeledStatement] = []
        self.current_line = 0
        self.return_stack: List[int] = []
        self.label_map: Dict[str, int] = {}

    def add_statement(self, statement: LabeledStatement) -> None:
        """Add a statement to the program and update label map if needed"""
        if statement.label:
            self.label_map[statement.label] = len(self.statements)
        self.statements.append(statement)

    def handle_control_flow(self, result: str) -> None:
        """Handle control flow instructions"""
        if result == "END":
            self.current_line = len(self.statements)  # Force program end
        elif result == "RETURN":
            if not self.return_stack:
                raise RuntimeError("RETURN without GOSUB")
            self.current_line = self.return_stack.pop()
        elif result.startswith("GOSUB:"):
            label = result[6:]
            if label not in self.label_map:
                raise RuntimeError(f"Label '{label}' not found")
            self.return_stack.append(self.current_line + 1)
            self.current_line = self.label_map[label]
        else:  # GOTO
            try:
                target = int(result)
                if target <= 0 or target > len(self.statements) + 1:
                    raise RuntimeError(f"Invalid GOTO target: {target}")
                self.current_line = target - 1  # Adjust for 0-based index
            except ValueError:
                if result not in self.label_map:
                    raise RuntimeError(f"Label '{result}' not found")
                self.current_line = self.label_map[result]

    def run(self) -> None:
        """Execute the program"""
        self.current_line = 0
        while self.current_line < len(self.statements):
            try:
                result = self.statements[self.current_line].statement.execute(self.variables)
                
                if result is None:
                    self.current_line += 1
                else:
                    self.handle_control_flow(result)
                    
            except Exception as e:
                print(f"Error at line {self.current_line + 1}: {str(e)}")
                break


def create_statement(tokens: List[GrinToken]) -> Statement:
    """Create appropriate statement object based on tokens"""
    if not tokens:
        raise ValueError("Empty token list")

    command = tokens[0].text()
    
    # Dictionary mapping commands to their corresponding statement classes and required argument counts
    STATEMENT_TYPES = {
        "LET": (LetStatement, 3),
        "PRINT": (PrintStatement, 2),
        "INNUM": (InNumStatement, 2),
        "INSTR": (InStrStatement, 2),
        "ADD": (lambda t: ArithmeticStatement("ADD", t[1], t[2]), 3),
        "SUB": (lambda t: ArithmeticStatement("SUB", t[1], t[2]), 3),
        "MULT": (lambda t: ArithmeticStatement("MULT", t[1], t[2]), 3),
        "DIV": (lambda t: ArithmeticStatement("DIV", t[1], t[2]), 3),
        "GOTO": (GotoStatement, [2, 6]),  # GOTO can have 1 or 5 arguments (including IF)
        "GOSUB": (GosubStatement, 2),
        "RETURN": (ReturnStatement, 1),
        "END": (EndStatement, 1),
    }

    if command not in STATEMENT_TYPES:
        raise ValueError(f"Unknown command: {command}")

    statement_type, required_tokens = STATEMENT_TYPES[command]
    
    if isinstance(required_tokens, list):
        if len(tokens) not in required_tokens:
            raise ValueError(f"{command} requires {required_tokens[0]-1} or {required_tokens[1]-1} arguments")
    elif len(tokens) != required_tokens:
        raise ValueError(f"{command} requires {required_tokens-1} arguments")

    if command == "GOTO":
        if len(tokens) == 2:
            return GotoStatement(tokens[1])
        elif len(tokens) == 6 and tokens[2].text() == "IF":
            return GotoStatement(tokens[1], tokens[4].text(), tokens[3], tokens[5])
        else:
            raise ValueError(f"Invalid GOTO statement: {' '.join(t.text() for t in tokens)}")
    elif isinstance(statement_type, type):  # If it's a class
        if required_tokens == 1:
            return statement_type()
        elif required_tokens == 2:
            return statement_type(tokens[1])
        else:  # required_tokens == 3
            return statement_type(tokens[1], tokens[2])
    else:  # If it's a lambda function
        return statement_type(tokens)
