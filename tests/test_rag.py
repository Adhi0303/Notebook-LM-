import os
import sys

# Add the src directory to the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.generation.rag import RAGEngine

def main():
    print("========================================")
    print("  NOTEBOOK LM - RAG CHAT BOT  ")
    print("========================================\n")

    print("[SYSTEM] Initializing Chat Engine...")
    engine = RAGEngine()
    print("[SYSTEM] Ready! Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
                
            if not user_input.strip():
                continue

            print("\nAI is thinking...")
            answer = engine.ask(user_input)
            
            print("\n--- AI RESPONSE ---")
            print(answer)
            print("-------------------\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
