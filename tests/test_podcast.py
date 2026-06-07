import os
import sys

# Load env variables if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Add the src directory to the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.generation.podcast_generator import PodcastGenerator

def main():
    print("========================================")
    print("  NOTEBOOK LM - PODCAST STUDIO  ")
    print("========================================\n")

    # Load the document
    doc_path = os.path.join("sample_data", "fake_ai_essay.txt")
    if not os.path.exists(doc_path):
        print(f"Error: Could not find document at {doc_path}")
        return

    with open(doc_path, "r", encoding="utf-8") as f:
        document_text = f.read()

    print(f"Loaded document: {doc_path} ({len(document_text)} characters)")

    # Initialize the generator
    generator = PodcastGenerator()
    
    # Generate the script
    script = generator.generate_script(document_text)

    if not script:
        print("Failed to generate script.")
        return

    print("\n--- GENERATED PODCAST SCRIPT ---\n")
    for line in script:
        speaker = line.get("speaker", "Unknown")
        text = line.get("text", "")
        print(f"[{speaker.upper()}]: {text}\n")
    
    print("--------------------------------\n")
    print(f"Success! Generated {len(script)} lines of dialogue.")

if __name__ == "__main__":
    main()
