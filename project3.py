from grin.lexing import to_tokens
from grin.interpreter import GrinInterpreter, create_statement
from grin.statements import LabeledStatement

def read_program() -> list[str]:
    """Read program lines until a '.' is encountered"""
    lines = []
    while True:
        try:
            line = input()
            if not line.strip():  # Skip empty lines
                continue
            lines.append(line)
            if line.strip() == '.':
                break
        except EOFError:
            break
    return lines

def process_line(line: str, line_number: int, interpreter: GrinInterpreter) -> None:
    """Process a single line of the program"""
    if line.strip() == '.':
        return

    # Get tokens for the line
    tokens = list(to_tokens(line_number, line))
    if not tokens:  # Skip empty lines
        return

    # Check for label
    label = None
    token_start = 0
    
    if len(tokens) >= 2 and tokens[1].text() == ':':
        label = tokens[0].text()
        token_start = 2

    # Get the remaining tokens for the statement
    statement_tokens = tokens[token_start:]
    if statement_tokens:  # Only process if there are tokens
        try:
            statement = create_statement(statement_tokens)
            labeled_stmt = LabeledStatement(label, statement)
            interpreter.add_statement(labeled_stmt)
        except Exception as e:
            print(f"Error on line {line_number}: {str(e)}")
            raise

def execute_program(lines: list[str]) -> None:
    """Execute the GRIN program"""
    interpreter = GrinInterpreter()
    
    try:
        # Process each line
        for line_number, line in enumerate(lines, 1):
            if line.strip():  # Skip empty lines
                process_line(line, line_number, interpreter)
        
        # Run the program
        interpreter.run()
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

def main() -> None:
    """Main entry point for the GRIN interpreter"""
    try:
        program_lines = read_program()
        if program_lines:
            execute_program(program_lines)
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()
