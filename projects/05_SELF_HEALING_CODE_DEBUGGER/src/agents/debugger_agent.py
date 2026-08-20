from typing import Dict, Any, List
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from src.guardrails.code_validator import validate_python_code
from src.tools.sandbox_executor import execute_code_in_sandbox
from src.prompts.system_prompts import CODER_SYSTEM_PROMPT, DEBUGGER_SYSTEM_PROMPT

load_dotenv()

# Primary and Fallback LLM Chains
primary_coder = ChatGroq(model="qwen/qwen3.6-27b", temperature=0.1)
fallback_coder_groq = ChatGroq(model="groq/compound", temperature=0.1)
fallback_coder_gemini = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0.1)

coder_llm = primary_coder.with_fallbacks([fallback_coder_groq, fallback_coder_gemini])

primary_debugger = ChatGroq(model="qwen/qwen3.6-27b", temperature=0.0)
fallback_debugger_groq = ChatGroq(model="groq/compound", temperature=0.0)
fallback_debugger_gemini = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0.0)

debugger_llm = primary_debugger.with_fallbacks([fallback_debugger_groq, fallback_debugger_gemini])


# Structured Response Schemas
class CodeGenerationOutput(BaseModel):
    """Structured response schema for Coder Agent."""
    explanation: str = Field(default="", description="Brief high-level explanation of the code or bug fix.")
    code: str = Field(description="The complete, self-contained Python code including function definitions and executable assertion test cases.")

class DebuggerAnalysisOutput(BaseModel):
    """Structured response schema for Debugger Agent."""
    root_cause: str = Field(default="", description="Detailed root-cause analysis of the traceback or syntax error.")
    feedback: str = Field(description="Clear, step-by-step instructions and guidance for patching the code.")


coder_structured_llm = coder_llm.with_structured_output(CodeGenerationOutput)
debugger_structured_llm = debugger_llm.with_structured_output(DebuggerAnalysisOutput)


class CodeDebugState(BaseModel):
    task_description: str         # Problem specification
    code: str = ""                # Generated/patched code string
    execution_status: str = ""    # "SUCCESS", "RUNTIME_ERROR", "SYNTAX_ERROR", "TIMEOUT", "SECURITY_VIOLATION"
    stdout: str = ""              # Captured stdout
    stderr: str = ""              # Captured traceback / error message
    feedback: str = ""            # Debugger analysis & repair feedback
    revision_count: int = 0       # Active revision count (max 3)
    status: str = ""              # "SUCCESS", "MAX_REVISIONS_EXCEEDED", "SECURITY_BLOCKED"

# 1. Coder Node (Generator / Reflector)
def coder_node(state: CodeDebugState) -> Dict[str, Any]:
    task = state.task_description
    existing_code = state.code
    feedback = state.feedback
    count = state.revision_count

    if feedback and existing_code:
        count += 1
        print(f"👨‍💻 [CODER AGENT - REPAIR MODE] Patching code based on feedback (Attempt #{count})...")
        prompt = f"""Task Specification: {task}

CURRENT BUGGY CODE:
```python
{existing_code}
```

DEBUGGER FEEDBACK & TRACEBACK ANALYSIS:
{feedback}

INSTRUCTIONS:
Rewrite the Python code to fix the identified bugs and errors. Provide the complete corrected Python code with test assertions."""
    else:
        print(f"👨‍💻 [CODER AGENT - INITIAL GENERATION MODE] Writing solution for task: '{task}'...")
        prompt = f"""Task Specification: {task}

Write a complete, self-contained Python function that implements the requested solution along with executable assertion test cases at the bottom."""

    response = coder_structured_llm.invoke([
        {"role": "system", "content": CODER_SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ])

    extracted_code = response.code.strip() if response and response.code else ""
    print("✅ [CODER AGENT] Code draft generated successfully!")

    return {
        "code": extracted_code,
        "revision_count": count
    }

# 2. Security Guard Node (AST Validator)
def security_guard_node(state: CodeDebugState) -> Dict[str, Any]:
    code = state.code
    print("🛡️ [SECURITY GUARD] Auditing code AST for syntax & security policies...")

    val_res = validate_python_code(code)

    if not val_res["is_valid"]:
        print(f"⚠️ [SECURITY GUARD] Code failed validation: {val_res['error_type']} - {val_res['message']}")
        return {
            "execution_status": val_res["error_type"],
            "stderr": val_res["message"],
            "feedback": f"Code validation failed: {val_res['message']}"
        }

    print("✅ [SECURITY GUARD] AST validation passed cleanly!")
    return {"execution_status": "PENDING_EXECUTION"}

# 3. Sandbox Executor Node
def sandbox_node(state: CodeDebugState) -> Dict[str, Any]:
    code = state.code
    if state.execution_status in ["SYNTAX_ERROR", "SECURITY_VIOLATION"]:
        print("⏩ [SANDBOX] Skipping execution due to AST validation failure.")
        return {}

    print("🏃 [SANDBOX EXECUTOR] Running code in isolated subprocess...")
    exec_res = execute_code_in_sandbox(code, timeout_seconds=5.0)

    if exec_res["success"]:
        print("🎉 [SANDBOX EXECUTOR] Code executed and passed all assertions!")
        return {
            "execution_status": "SUCCESS",
            "stdout": exec_res["stdout"],
            "stderr": "",
            "status": "SUCCESS"
        }
    else:
        print(f"❌ [SANDBOX EXECUTOR] Execution failed ({exec_res['status']})!")
        return {
            "execution_status": exec_res["status"],
            "stdout": exec_res["stdout"],
            "stderr": exec_res["stderr"]
        }

# 4. Debugger Node (Traceback Analyzer)
def debugger_node(state: CodeDebugState) -> Dict[str, Any]:
    if state.execution_status == "SUCCESS":
        return {}

    code = state.code
    stderr = state.stderr
    exec_status = state.execution_status
    revisions = state.revision_count

    print(f"🐞 [DEBUGGER AGENT] Analyzing {exec_status} traceback...")

    prompt = f"""BUGGY PYTHON CODE:
```python
{code}
```

CAPTURED EXECUTION TRACEBACK / ERROR:
{stderr}

Identify the root cause of the error and provide clear, step-by-step instructions on how to patch the code."""

    response = debugger_structured_llm.invoke([
        {"role": "system", "content": DEBUGGER_SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ])

    feedback = getattr(response, "feedback", "") if response else ""

    if revisions >= 3:
        status = "MAX_REVISIONS_EXCEEDED"
    elif exec_status == "SECURITY_VIOLATION":
        status = "SECURITY_BLOCKED"
    else:
        status = "REQUIRES_REVISION"

    return {
        "feedback": feedback,
        "status": status
    }

# 5. Conditional Reflection Edge Router
def should_heal(state: CodeDebugState) -> str:
    exec_status = state.execution_status
    revisions = state.revision_count

    if exec_status == "SUCCESS":
        print("🏁 [SELF-HEALING COMPLETE] Code execution passed all tests! Routing to END.")
        return END
    elif exec_status == "SECURITY_VIOLATION":
        print("🚫 [SECURITY BLOCKED] Security policy violation detected. Halting execution.")
        return END
    elif revisions < 3:
        print(f"🔄 [REFLECTION LOOP] Routing back to CODER AGENT for repair (Attempt {revisions + 1}/3)...")
        return "coder"
    else:
        print(f"⚠️ [MAX REVISIONS HIT] Reached limit of {revisions} repair iterations. Routing to END.")
        return END

# Build State Graph
builder = StateGraph(CodeDebugState)

builder.add_node("coder", coder_node)
builder.add_node("security_guard", security_guard_node)
builder.add_node("sandbox", sandbox_node)
builder.add_node("debugger", debugger_node)

builder.add_edge(START, "coder")
builder.add_edge("coder", "security_guard")
builder.add_edge("security_guard", "sandbox")
builder.add_edge("sandbox", "debugger")

builder.add_conditional_edges("debugger", should_heal, {
    "coder": "coder",
    END: END
})

def init_debugger_agent(checkpointer=None):
    """Returns compiled Self-Healing StateGraph with Checkpointer support."""
    if checkpointer is None:
        checkpointer = MemorySaver()
    return builder.compile(checkpointer=checkpointer)

graph = init_debugger_agent()
