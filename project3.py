from grin.lexing import to_tokens
from grin.parsing import parse
from grin.interpreter import GrinInterpreter, create_statement
from grin.statements import LabeledStatement

def read_program() -> list[str]:
    """Read program lines until a '.' is encountered"""
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == '.':
                break
            lines.append(line)
        except EOFError:
            break
    return lines

def process_tokens(tokens, interpreter):
    """Process tokens and add statements to interpreter"""
    label = None
    start_idx = 0
    
    if len(tokens) >= 3 and tokens[1].text() == ":":
        label = tokens[0].text()
        start_idx = 2
    
    statement = create_statement(tokens[start_idx:])
    labeled_statement = LabeledStatement(label, statement)
    interpreter.add_statement(labeled_statement)

def execute_program(lines: list[str]) -> None:
    """Execute the GRIN program"""
    try:
        interpreter = GrinInterpreter()
        
        # Parse and add all statements
        for line in lines:
            if line.strip():
                tokens_list = list(parse([line]))
                for tokens in tokens_list:
                    process_tokens(tokens, interpreter)
        
        # Execute the program
        interpreter.run()
        
    except Exception as e:
        print(f"Error: {str(e)}")

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
