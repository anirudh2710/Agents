# 🛠️ Self-Healing Code & Debugger Agent (The ReAct Sandbox Loop)

An enterprise-grade Multi-Agent Code Generation & Self-Healing Pipeline built with **LangGraph**, **Subprocess Sandboxing**, **AST Security Guardrails**, and **Groq (Llama 3.3 70B)**.

Demonstrates **autonomous code generation**, **isolated subprocess execution**, **`stderr` traceback extraction**, **AST security validation**, and an **iterative reflection repair loop**.

---

## 🏗️ Enterprise Package Architecture

```
projects/05_SELF_HEALING_CODE_DEBUGGER/
├── src/
│   ├── agents/          # Self-healing StateGraph (Coder -> Guardrail -> Sandbox -> Debugger Loop)
│   ├── tools/           # Isolated Python subprocess execution with timeouts & output capture
│   ├── guardrails/      # AST syntax checking & security policy enforcement (forbidden imports/calls)
│   └── prompts/         # Specialized Coder, Debugger, and Tester system prompts
├── tests/
│   ├── unit/            # PyTest unit tests for sandbox execution & AST validator
│   └── evals/           # Benchmark evaluation suite measuring self-healing pass rate on buggy prompts
├── main.py              # Interactive real-time CLI terminal application
├── app.ipynb            # Interactive Jupyter notebook
└── README.md            # Architecture documentation & diagrams
```

---

## 🔄 Self-Healing Reflection Workflow

```
                  ┌──────────────────────────────┐
                  │       START (Task Spec)      │
                  └──────────────┬───────────────┘
                                 │
                                 ▼
                  ┌──────────────┴───────────────┐
                  │                           ◄──┐
                  ▼                              │
   ┌──────────────────────────────┐              │
   │    1. CODER (GENERATOR)      │              │  Self-Healing Repair Loop
   └──────────────┬───────────────┘              │  (passes stderr & feedback)
                  │ Passes Code                  │
                  ▼                              │
   ┌──────────────────────────────┐              │
   │  2. SECURITY GUARD (AST)     │              │
   └──────────────┬───────────────┘              │
                  │ Safe Code                    │
                  ▼                              │
   ┌──────────────────────────────┐              │
   │    3. SANDBOX EXECUTOR       │              │
   └──────────────┬───────────────┘              │
                  │ Captures stdout/stderr       │
                  ▼                              │
   ┌──────────────────────────────┐              │
   │    4. DEBUGGER ANALYZER      │              │
   └──────────────┬───────────────┘              │
                  │ Conditional Edge             │
┌─────────────────┴─────────────────┐            │
│                                   │            │
[execution_status != "SUCCESS"       [execution_status == "SUCCESS"
 and revision_count < 3]             or max_revisions reached]
│                                   │
└───────────────────────────────────┴───────────► END
```

---

## 🔑 Shared State Schema (`CodeDebugState`)

```python
class CodeDebugState(TypedDict):
    task_description: str         # Problem specification
    code: str                     # Current Python code draft
    execution_status: str         # "SUCCESS", "RUNTIME_ERROR", "SYNTAX_ERROR", "TIMEOUT", "SECURITY_VIOLATION"
    stdout: str                   # Captured stdout from sandbox
    stderr: str                   # Captured traceback / error logs
    feedback: str                 # Debugger Agent analysis & repair feedback
    revision_count: int           # Active revision count (max 3)
    status: str                   # "SUCCESS", "MAX_REVISIONS_EXCEEDED", "SECURITY_BLOCKED"
```

---

## 💻 Running the Application

### 1. Interactive CLI Terminal Runner
```bash
uv run main.py
```

### 2. Run PyTest Unit Tests
```bash
pytest tests/unit/
```

### 3. Run Self-Healing Benchmark Evaluation Suite
```bash
python tests/evals/eval_debug_bench.py
```

### 4. Interactive Notebook
Open `app.ipynb` in VS Code using the `.venv` kernel and run all cells.
