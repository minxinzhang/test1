# grin/interpreter.py

from typing import Dict, Any, List, Optional
from grin.token import GrinToken, GrinTokenKind
from grin.statements import (
    Statement, 
    LabeledStatement,
    LetStatement,
    PrintStatement,
    InNumStatement,
    InStrStatement,
    ArithmeticStatement,
    GotoStatement,
    GosubStatement,
    ReturnStatement,
    EndStatement
)

class GrinInterpreter:
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.statements: List[LabeledStatement] = []
        self.current_line = 0
        self.return_stack = []
        self.label_map = {}

    def add_statement(self, statement: LabeledStatement) -> None:
        if statement.label:
            self.label_map[statement.label] = len(self.statements)
        self.statements.append(statement)

    def run(self) -> None:
        self.current_line = 0
        while self.current_line < len(self.statements):
            try:
                result = self.statements[self.current_line].statement.execute(self.variables)
                
                if result is None:
                    self.current_line += 1
                elif result == "END":
                    break
                elif result == "RETURN":
                    if not self.return_stack:
                        raise RuntimeError("RETURN without GOSUB")
                    self.current_line = self.return_stack.pop()
                elif result.startswith("GOSUB:"):
                    label = result[6:]
                    if label not in self.label_map:
                        raise RuntimeError(f"Label '{label}' not found")
                    self.return_stack.append(self.current_line)
                    self.current_line = self.label_map[label]
                else:  # GOTO
                    if result not in self.label_map:
                        raise RuntimeError(f"Label '{result}' not found")
                    self.current_line = self.label_map[result]
            except Exception as e:
                print(f"Error at line {self.current_line + 1}: {str(e)}")
                break

def create_statement(tokens: List[GrinToken]) -> Statement:
    if not tokens:
        raise ValueError("Empty token list")

    command = tokens[0].text()
    
    if command == "LET":
        if len(tokens) != 3:
            raise ValueError("LET requires variable and value")
        return LetStatement(tokens[1], tokens[2])
    
    elif command == "PRINT":
        if len(tokens) != 2:
            raise ValueError("PRINT requires one argument")
        return PrintStatement(tokens[1])
    
    elif command == "INNUM":
        if len(tokens) != 2:
            raise ValueError("INNUM requires variable name")
        return InNumStatement(tokens[1])
    
    elif command == "INSTR":
        if len(tokens) != 2:
            raise ValueError("INSTR requires variable name")
        return InStrStatement(tokens[1])
    
    elif command in ["ADD", "SUB", "MULT", "DIV"]:
        if len(tokens) != 3:
            raise ValueError(f"{command} requires variable and value")
        return ArithmeticStatement(command, tokens[1], tokens[2])
    
    elif command == "GOTO":
        if len(tokens) != 2:
            raise ValueError("GOTO requires label")
        return GotoStatement(tokens[1])
    
    elif command == "GOSUB":
        if len(tokens) != 2:
            raise ValueError("GOSUB requires label")
        return GosubStatement(tokens[1])
    
    elif command == "RETURN":
        if len(tokens) != 1:
            raise ValueError("RETURN takes no arguments")
        return ReturnStatement()
    
    elif command == "END":
        if len(tokens) != 1:
            raise ValueError("END takes no arguments")
        return EndStatement()
    
    else:
        raise ValueError(f"Unknown command: {command}")
