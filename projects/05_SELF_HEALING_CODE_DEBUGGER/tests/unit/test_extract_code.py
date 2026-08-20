import unittest
from src.agents.debugger_agent import CodeGenerationOutput, DebuggerAnalysisOutput

class TestStructuredOutputs(unittest.TestCase):
    def test_code_generation_output_schema(self):
        output = CodeGenerationOutput(
            explanation="Created a helper function",
            code="def add(a, b):\n    return a + b"
        )
        self.assertEqual(output.explanation, "Created a helper function")
        self.assertEqual(output.code, "def add(a, b):\n    return a + b")

    def test_debugger_analysis_output_schema(self):
        output = DebuggerAnalysisOutput(
            root_cause="Zero division error on line 4",
            feedback="Add check for b != 0"
        )
        self.assertEqual(output.root_cause, "Zero division error on line 4")
        self.assertEqual(output.feedback, "Add check for b != 0")

if __name__ == "__main__":
    unittest.main()
