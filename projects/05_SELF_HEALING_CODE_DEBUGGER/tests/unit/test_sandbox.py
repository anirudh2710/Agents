import pytest
from src.tools.sandbox_executor import execute_code_in_sandbox

def test_sandbox_success():
    valid_code = "x = 10\ny = 20\nassert x + y == 30\nprint('SUCCESS')"
    res = execute_code_in_sandbox(valid_code)
    assert res["success"] is True
    assert res["status"] == "SUCCESS"
    assert "SUCCESS" in res["stdout"]
    assert res["returncode"] == 0

def test_sandbox_runtime_error():
    buggy_code = "x = 10 / 0"
    res = execute_code_in_sandbox(buggy_code)
    assert res["success"] is False
    assert res["status"] == "RUNTIME_ERROR"
    assert "ZeroDivisionError" in res["stderr"]

def test_sandbox_assertion_error():
    assertion_bug = "assert 1 == 2"
    res = execute_code_in_sandbox(assertion_bug)
    assert res["success"] is False
    assert "AssertionError" in res["stderr"]

def test_sandbox_timeout():
    infinite_loop = "while True:\n    pass"
    res = execute_code_in_sandbox(infinite_loop, timeout_seconds=1.0)
    assert res["success"] is False
    assert res["status"] == "TIMEOUT"
    assert "timed out" in res["stderr"]
