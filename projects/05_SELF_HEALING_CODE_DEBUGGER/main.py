import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(__file__))

from src.agents.debugger_agent import init_debugger_agent

def get_multiline_input() -> str:
    print("User Task > (Paste prompt/code below; press Enter on an empty line or type 'END' to execute)")
    lines = []
    while True:
        try:
            line = input("  | " if lines else "User Task > ")
        except (KeyboardInterrupt, EOFError):
            return "exit"

        if line.strip() == "END":
            break
        if not line.strip() and lines:
            break
        if line.strip().lower() in ["exit", "q", "quit"] and not lines:
            return "exit"

        lines.append(line)

    return "\n".join(lines).strip()

def main():
    print("🛠️ Initializing Self-Healing Code & Debugger Agent (The ReAct Sandbox Loop)...")
    agent = init_debugger_agent()
    print("✅ Debugger Agent ready! Interactive CLI mode active.")
    print("--------------------------------------------------")
    print("Describe the coding task or paste buggy code to generate and self-heal.")
    print("Type 'exit' or 'q' to quit.\n")
    
    while True:
        try:
            user_input = get_multiline_input()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "q", "quit"]:
                print("Goodbye! 👋")
                break
                
            print("\n🚀 Executing Self-Healing Agent Pipeline...\n" + "="*60)
            initial_state = {"task_description": user_input, "revision_count": 0}
            final_state = agent.invoke(initial_state)
            
            print("\n" + "="*60)
            print(f"🎉 PIPELINE COMPLETE! Status: '{final_state.get('status')}'")
            print(f"Revisions Required: {final_state.get('revision_count', 0)}")
            print("="*60 + "\nFINAL VERIFIED CODE:\n")
            print(final_state.get("code", "No code generated."))
            print("\n" + "="*60 + "\n")
            
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye! 👋")
            break

if __name__ == "__main__":
    main()
