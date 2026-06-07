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
from src.generation.podcast_studio import PodcastStudio

def main():
    print("========================================")
    print("  NOTEBOOK LM - PODCAST STUDIO (AUDIO)  ")
    print("========================================\n")

    # 1. Load the document
    doc_path = os.path.join("sample_data", "fake_ai_essay.txt")
    if not os.path.exists(doc_path):
        print(f"Error: Could not find document at {doc_path}")
        return

    with open(doc_path, "r", encoding="utf-8") as f:
        document_text = f.read()

    print(f"Loaded document: {doc_path} ({len(document_text)} characters)")

    # 2. Generate the JSON script (Module 5.1)
    generator = PodcastGenerator()
    script = generator.generate_script(document_text)

    if not script:
        print("Failed to generate script. Aborting audio synthesis.")
        return

    print(f"Script generated! Found {len(script)} lines of dialogue.\n")

    # 3. Synthesize the Audio (Module 5.2)
    studio = PodcastStudio()
    output_audio_path = os.path.join("outputs", "final_podcast.mp3")
    
    studio.generate_podcast_audio(script, output_audio_path)

if __name__ == "__main__":
    main()
