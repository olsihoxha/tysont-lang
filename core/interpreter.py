#######################################
# INTERPRETER
#######################################
from core.constants import TT_PLUS, TT_MINUS, TT_MUL, TT_DIV
from core.results import RTResults
from core.values import Number


class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def visit_NumberNode(self, node, context):
        num = Number(node.tok.value).set_context(context).set_position(node.pos_start, node.pos_end)
        return RTResults().success(num)

    def visit_BinOpNode(self, node, context):
        res = RTResults()
        left = res.register(self.visit(node.left_node, context))
        if res.error:
            return res
        right = res.register(self.visit(node.right_node, context))
        if res.error:
            return res
        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)
        if error:
            return res.failure(error)
        return res.success(result.set_position(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResults()
        number = res.register(self.visit(node.node, context))
        error = None
        if res.error:
            return res
        if node.op_tok.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))
        if error:
            return res.failure(error)
        return res.success(number.set_position(node.pos_start, node.pos_end))

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')
