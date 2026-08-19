import unittest
from src.agents.debugger_agent import extract_python_code

class TestExtractPythonCode(unittest.TestCase):
    def test_extract_python_code_plain_str(self):
        raw = "```python\ndef foo():\n    return 42\n```"
        code = extract_python_code(raw)
        self.assertEqual(code, "def foo():\n    return 42")

    def test_extract_python_code_generic_block(self):
        raw = "```\ndef bar():\n    return 100\n```"
        code = extract_python_code(raw)
        self.assertEqual(code, "def bar():\n    return 100")

    def test_extract_python_code_no_markdown(self):
        raw = "def baz():\n    return 0"
        code = extract_python_code(raw)
        self.assertEqual(code, "def baz():\n    return 0")

    def test_extract_python_code_list_content(self):
        list_input = [
            "Here is the python solution:\n",
            {"type": "text", "text": "```python\ndef test():\n    assert True\n```"}
        ]
        code = extract_python_code(list_input)
        self.assertEqual(code, "def test():\n    assert True")

if __name__ == "__main__":
    unittest.main()

