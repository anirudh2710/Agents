import ast
from typing import Dict, Any, List

# List of forbidden modules and functions for sandboxed safety
FORBIDDEN_MODULES = {"os", "subprocess", "sys", "shutil", "socket", "pty", "ctypes", "pickle", "builtins"}
FORBIDDEN_FUNCTIONS = {"eval", "exec", "__import__", "compile", "open", "input"}

class SecurityASTVisitor(ast.NodeVisitor):
    def __init__(self):
        self.violations: List[str] = []

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            module_base = alias.name.split(".")[0]
            if module_base in FORBIDDEN_MODULES:
                self.violations.append(f"Forbidden import '{alias.name}' detected.")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module:
            module_base = node.module.split(".")[0]
            if module_base in FORBIDDEN_MODULES:
                self.violations.append(f"Forbidden import from '{node.module}' detected.")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            if node.func.id in FORBIDDEN_FUNCTIONS:
                self.violations.append(f"Forbidden function call '{node.func.id}()' detected.")
        elif isinstance(node.func, ast.Attribute):
            if node.func.attr in {"system", "popen", "spawn", "exec", "rmtree"}:
                self.violations.append(f"Forbidden attribute call '.{node.func.attr}()' detected.")
        self.generic_visit(node)

def validate_python_code(code_str: str) -> Dict[str, Any]:
    """Parses Python code using AST to check for syntax errors and security policy violations."""
    if not code_str or not code_str.strip():
        return {"is_valid": False, "error_type": "SYNTAX_ERROR", "message": "Code string is empty."}

    # 1. AST Syntax Check
    try:
        parsed_ast = ast.parse(code_str)
    except SyntaxError as e:
        return {
            "is_valid": False,
            "error_type": "SYNTAX_ERROR",
            "message": f"SyntaxError on line {e.lineno}: {e.msg}\n  {e.text}"
        }

    # 2. AST Security Policy Check
    visitor = SecurityASTVisitor()
    visitor.visit(parsed_ast)

    if visitor.violations:
        return {
            "is_valid": False,
            "error_type": "SECURITY_VIOLATION",
            "message": "Security policy violations found: " + "; ".join(visitor.violations)
        }

    return {"is_valid": True, "error_type": None, "message": "Code AST validation passed cleanly."}
