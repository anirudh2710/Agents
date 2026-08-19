import pytest
from src.guardrails.code_validator import validate_python_code

def test_validate_clean_code():
    clean_code = "def add(a, b):\n    return a + b\n\nassert add(2, 3) == 5"
    res = validate_python_code(clean_code)
    assert res["is_valid"] is True

def test_validate_syntax_error():
    syntax_bug = "def add(a, b\n    return a + b"
    res = validate_python_code(syntax_bug)
    assert res["is_valid"] is False
    assert res["error_type"] == "SYNTAX_ERROR"
    assert "SyntaxError" in res["message"]

def test_validate_security_import_os():
    unsafe_code = "import os\nos.system('echo hacked')"
    res = validate_python_code(unsafe_code)
    assert res["is_valid"] is False
    assert res["error_type"] == "SECURITY_VIOLATION"
    assert "Forbidden import 'os'" in res["message"]

def test_validate_security_eval():
    unsafe_code = "eval('1 + 1')"
    res = validate_python_code(unsafe_code)
    assert res["is_valid"] is False
    assert res["error_type"] == "SECURITY_VIOLATION"
    assert "Forbidden function call 'eval()'" in res["message"]
