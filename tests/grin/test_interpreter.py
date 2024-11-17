import unittest
from typing import List
from grin.interpreter import GrinInterpreter, create_statement
from grin.statements import (
    LabeledStatement, LetStatement, PrintStatement, InNumStatement, InStrStatement,
    ArithmeticStatement, GotoStatement, GosubStatement, ReturnStatement, EndStatement
)
from grin.token import GrinToken, GrinTokenKind

class MockToken:
    def __init__(self, text, kind=GrinTokenKind.IDENTIFIER):
        self._text = text
        self._kind = kind

    def text(self):
        return self._text

    def kind(self):
        return self._kind

class TestGrinInterpreter(unittest.TestCase):
    def setUp(self):
        self.interpreter = GrinInterpreter()

    def test_add_statement(self):
        stmt = LabeledStatement("label1", LetStatement(MockToken("X"), MockToken("5")))
        self.interpreter.add_statement(stmt)
        self.assertEqual(len(self.interpreter.statements), 1)
        self.assertEqual(self.interpreter.label_map["label1"], 0)

    def test_handle_control_flow_end(self):
        self.interpreter.statements = [LabeledStatement(None, EndStatement())] * 5
        self.interpreter.handle_control_flow("END")
        self.assertEqual(self.interpreter.current_line, 5)

    def test_handle_control_flow_return(self):
        self.interpreter.return_stack = [3]
        self.interpreter.handle_control_flow("RETURN")
        self.assertEqual(self.interpreter.current_line, 3)

    def test_handle_control_flow_gosub(self):
        self.interpreter.label_map["test_label"] = 2
        self.interpreter.current_line = 0
        self.interpreter.handle_control_flow("GOSUB:test_label")
        self.assertEqual(self.interpreter.current_line, 2)
        self.assertEqual(self.interpreter.return_stack, [1])

    def test_handle_control_flow_goto(self):
        self.interpreter.label_map["test_label"] = 4
        self.interpreter.handle_control_flow("test_label")
        self.assertEqual(self.interpreter.current_line, 4)

class TestCreateStatement(unittest.TestCase):
    def test_create_let_statement(self):
        tokens = [MockToken("LET"), MockToken("X"), MockToken("5")]
        stmt = create_statement(tokens)
        self.assertIsInstance(stmt, LetStatement)

    def test_create_print_statement(self):
        tokens = [MockToken("PRINT"), MockToken("X")]
        stmt = create_statement(tokens)
        self.assertIsInstance(stmt, PrintStatement)

    def test_create_arithmetic_statement(self):
        tokens = [MockToken("ADD"), MockToken("X"), MockToken("Y")]
        stmt = create_statement(tokens)
        self.assertIsInstance(stmt, ArithmeticStatement)
        self.assertEqual(stmt.operation, "ADD")

    def test_create_goto_statement(self):
        tokens = [MockToken("GOTO"), MockToken("label")]
        stmt = create_statement(tokens)
        self.assertIsInstance(stmt, GotoStatement)

    def test_create_end_statement(self):
        tokens = [MockToken("END")]
        stmt = create_statement(tokens)
        self.assertIsInstance(stmt, EndStatement)

    def test_invalid_command(self):
        tokens = [MockToken("INVALID")]
        with self.assertRaises(ValueError):
            create_statement(tokens)

    def test_incorrect_argument_count(self):
        tokens = [MockToken("LET"), MockToken("X")]
        with self.assertRaises(ValueError):
            create_statement(tokens)

if __name__ == '__main__':
    unittest.main()
