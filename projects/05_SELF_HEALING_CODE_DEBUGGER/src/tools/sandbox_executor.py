import sys
import subprocess
import tempfile
import os
from typing import Dict, Any

def execute_code_in_sandbox(code_str: str, timeout_seconds: float = 5.0) -> Dict[str, Any]:
    """Executes Python code in an isolated subprocess with strict timeout and output interception."""
    if not code_str or not code_str.strip():
        return {
            "success": False,
            "status": "EMPTY_CODE",
            "returncode": -1,
            "stdout": "",
            "stderr": "No code provided to sandbox."
        }

    # Write code to a temporary python script file
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as temp_file:
        temp_file_path = temp_file.name
        temp_file.write(code_str)

    try:
        # Run code in isolated subprocess using active python executable
        result = subprocess.run(
            [sys.executable, temp_file_path],
            capture_output=True,
            text=True,
            timeout=timeout_seconds
        )

        success = (result.returncode == 0)
        status = "SUCCESS" if success else "RUNTIME_ERROR"

        return {
            "success": success,
            "status": status,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "status": "TIMEOUT",
            "returncode": -1,
            "stdout": "",
            "stderr": f"Execution timed out after {timeout_seconds} seconds (infinite loop detected)."
        }
    except Exception as e:
        return {
            "success": False,
            "status": "SYSTEM_ERROR",
            "returncode": -1,
            "stdout": "",
            "stderr": f"Sandbox error: {str(e)}"
        }
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
