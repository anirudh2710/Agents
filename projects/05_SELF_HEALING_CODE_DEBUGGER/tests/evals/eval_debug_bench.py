import asyncio
import os
import sys
from typing import List
from pydantic import BaseModel, Field

# Adjust import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.agents.debugger_agent import init_debugger_agent

BENCHMARK_TASKS = [
    {
        "name": "Off-by-One Array Indexing",
        "prompt": "Write a Python function `get_last_element(lst)` that returns the last element of a non-empty list. Include assertions."
    },
    {
        "name": "Zero Division Edge Case",
        "prompt": "Write a Python function `safe_divide(a, b)` that returns a / b or 0.0 if b is 0. Include assertions for b=0."
    },
    {
        "name": "Type Safety & String Concatenation",
        "prompt": "Write a Python function `format_user_age(name, age)` that returns 'User [name] is [age] years old' handling age as integer or string. Include assertions."
    }
]

async def run_benchmark():
    print("🧪 Running Self-Healing Code & Debugger Benchmark Suite...\n" + "="*70)
    agent = init_debugger_agent()
    
    passed_count = 0
    total_count = len(BENCHMARK_TASKS)
    
    for idx, task in enumerate(BENCHMARK_TASKS, 1):
        print(f"\n📌 [BENCHMARK {idx}/{total_count}] {task['name']}")
        print(f"Task Prompt: {task['prompt']}")
        
        initial_state = {"task_description": task["prompt"], "revision_count": 0}
        config = {"configurable": {"thread_id": f"bench-task-{idx}"}}
        res = agent.invoke(initial_state, config=config)
        
        status = res.get("status")
        exec_status = res.get("execution_status")
        revisions = res.get("revision_count", 0)
        
        if exec_status == "SUCCESS":
            passed_count += 1
            print(f"✅ PASSED (Revisions required: {revisions})")
        else:
            print(f"❌ FAILED (Status: {status}, Error: {res.get('stderr')})")
            
    pass_rate = (passed_count / total_count) * 100
    print("\n" + "="*70)
    print(f"📊 BENCHMARK COMPLETE! Pass Rate: {pass_rate:.1f}% ({passed_count}/{total_count} Passed)")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(run_benchmark())
