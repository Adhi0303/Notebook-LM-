import os
import sys
import time
from dotenv import load_dotenv

# Add the src directory to the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.audio_processing.youtube_transcriber import YouTubeTranscriber

def run_detailed_audio_test():
    print("========================================")
    print("🎥 YOUTUBE AUDIO TRANSCRIBER TESTING 🎥")
    print("========================================")
    
    user_url = input("\nEnter a YouTube URL (or press Enter for default 'Me at the zoo'): ").strip()
    test_url = user_url if user_url else "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    
    # Load environment variables from .env
    load_dotenv()
    
    if not os.getenv("ASSEMBLYAI_API_KEY"):
        print("\n[ERROR] ASSEMBLYAI_API_KEY is not set in .env file.")
        return

    yt_transcriber = YouTubeTranscriber()
    
    print(f"\n[1] Downloading & Transcribing: {test_url}")
    print("This may take a minute depending on video length...")
    
    # Start timer
    start_time = time.time()
    
    # Process the video
    docs = yt_transcriber.process_video(test_url)
    
    # Stop timer
    time_taken = time.time() - start_time
    
    if not docs:
        print("\n[FAIL] Failed to extract or transcribe audio.")
        return
        
    doc = docs[0]
    content = doc['text']
    metadata = doc['metadata']
    
    # Calculate costs (AssemblyAI Standard is $0.37 per hour)
    duration_seconds = metadata.get('duration_seconds', 0)
    cost = (duration_seconds / 3600) * 0.37
    
    print("\n========================================")
    print("📊 TRANSCRIPTION LOG & ANALYTICS")
    print("========================================")
    print(f"Video Title:         {metadata.get('source')}")
    print(f"Audio Duration:      {duration_seconds:.2f} seconds")
    print(f"Processing Time:     {time_taken:.2f} seconds")
    print(f"Estimated Cost:      ${cost:.4f} USD (AssemblyAI Standard)")
    print(f"Total Words:         {len(content.split())} words")
    print("========================================\n")
    
    print("[ FULL TRANSCRIBED AUDIO ]")
    print("-" * 60)
    print(content)
    print("-" * 60)
    print("\n[PASS] Audio pipeline test completed successfully!")

if __name__ == "__main__":
    run_detailed_audio_test()
