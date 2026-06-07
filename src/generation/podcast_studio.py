import os
import asyncio
import edge_tts
from typing import List, Dict

class PodcastStudio:
    def __init__(self):
        """
        Initializes the Podcast Studio with Microsoft Edge TTS Voices.
        These are high-quality neural voices that are completely free.
        """
        # Define the voices for our two hosts
        self.host1_voice = "en-US-GuyNeural"   # Male, energetic
        self.host2_voice = "en-US-AriaNeural"  # Female, clear and professional
        
    async def _generate_single_clip(self, text: str, voice: str, output_path: str):
        """Asynchronously generates a single audio clip."""
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        
    def generate_podcast_audio(self, script: List[Dict], final_output_path: str):
        """
        Takes the JSON script and generates a full podcast MP3 file.
        Uses lightweight binary concatenation to combine the clips.
        """
        print("Initializing Podcast Studio...")
        temp_files = []
        
        # Ensure the outputs directory exists
        os.makedirs(os.path.dirname(final_output_path), exist_ok=True)

        try:
            # 1. Generate individual audio clips
            for index, line in enumerate(script):
                speaker = line.get("speaker", "Unknown")
                text = line.get("text", "")
                
                print(f"Recording [{speaker}] (Line {index+1}/{len(script)})...")
                
                # Select the correct voice
                voice = self.host1_voice if "Host 1" in speaker else self.host2_voice
                
                temp_filename = f"temp_clip_{index}.mp3"
                
                # Run the async generation synchronously for this simple loop
                asyncio.run(self._generate_single_clip(text, voice, temp_filename))
                temp_files.append(temp_filename)

            # 2. Stitch the audio clips together
            print("Stitching audio clips together in the editing room...")
            with open(final_output_path, "wb") as master_file:
                for temp_file in temp_files:
                    with open(temp_file, "rb") as clip_file:
                        # Append the raw MP3 bytes to the master file
                        master_file.write(clip_file.read())
            
            print(f"Podcast officially exported to: {final_output_path}")

        finally:
            # 3. Clean up the temporary files
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
