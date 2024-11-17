from grin.lexing import to_tokens
from grin.interpreter import GrinInterpreter, create_statement
from grin.statements import LabeledStatement
from typing import List

def read_program() -> List[str]:
    """Read program lines until a '.' is encountered"""
    lines = []
    while True:
        line = input().strip()
        if line == '.':
            lines.append(line)
            break
        if line:  # Only add non-empty lines
            lines.append(line)
    return lines

def process_line(line: str, line_number: int, interpreter: GrinInterpreter) -> None:
    """Process a single line of the program"""
    if line == '.':
        return

    tokens = list(to_tokens(line, line_number))  # Changed this line
    
    # Handle labeled statements
    label = None
    if len(tokens) >= 2 and tokens[1].kind == 'COLON':
        label = tokens[0].text
        tokens = tokens[2:]  # Remove label and colon from tokens
    
    if tokens:  # Only create statement if there are tokens left
        statement = create_statement(tokens)
        labeled_statement = LabeledStatement(label, statement)
        interpreter.add_statement(labeled_statement)

def execute_program(lines: List[str]) -> None:
    """Execute the GRIN program"""
    interpreter = GrinInterpreter()
    
    for line_number, line in enumerate(lines, start=1):
        try:
            process_line(line, line_number, interpreter)
        except Exception as e:
            print(f"Error on line {line_number}: {str(e)}")
            return

    try:
        interpreter.run()
    except Exception as e:
        print(f"Runtime error: {str(e)}")

def main() -> None:
    """Main entry point for the GRIN interpreter"""
    try:
        program_lines = read_program()
        if program_lines:
            execute_program(program_lines)
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == '__main__':
    main()
