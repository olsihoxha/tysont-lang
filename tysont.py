from core.context import Context
from core.interpreter import Interpreter
from core.lexer import Lexer
from core.parser import Parser


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()

    if ast.error:
        return None, ast.error

    interpreter = Interpreter()
    context = Context('<program>')
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
