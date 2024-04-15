from sys import version_info
from ast import AST, NodeVisitor, If, IfExp
from typing import Generator, Any, Tuple, Type


if version_info < (3, 8):
    import importlib_metadata # pragma: no cover
if version_info >= (3, 8): 
    import importlib.metadata as importlib_metadata # pragma: no cover


class Visitor(NodeVisitor): 
    def __init__(self):
        self.errors = []

    def visit_If(self, node: If) -> Any:
        if not node.orelse:
            self.generic_visit(node)
            return
        if isinstance(node.orelse[0], If):
            self.errors.append((node.lineno, node.col_offset, 'FNE101 ELIF found'))
        if not isinstance(node.orelse[0], If):
            self.errors.append((node.lineno, node.col_offset, 'FNE100 ELSE found'))
        self.generic_visit(node)

    def visit_IfExp(self, node: IfExp) -> Any:
        self.errors.append((node.lineno, node.col_offset, 'FNE102 ternary ELSE found'))
        self.generic_visit(node)


class Plugin:
    name = __name__
    version = importlib_metadata.version(__name__)

    def __init__(self, tree: AST) -> None:
        self.tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor()
        visitor.visit(self.tree)
        
        for error in visitor.errors:
            yield error + (type(self),)