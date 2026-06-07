"""
AssemblyAI Audio Transcriber Module
Handles parsing local audio and video files into text with Speaker Diarization.
"""

import os
import assemblyai as aai
from typing import List, Dict, Any
from dotenv import load_dotenv

class AudioTranscriber:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize AssemblyAI with the API key
        api_key = os.getenv("ASSEMBLYAI_API_KEY")
        if not api_key:
            print("Warning: ASSEMBLYAI_API_KEY is not set. Audio processing will fail.")
        else:
            aai.settings.api_key = api_key
            
        self.transcriber = aai.Transcriber()

    def process_audio(self, file_path: str, source_name: str) -> List[Dict[str, Any]]:
        """
        Transcribes an audio file and returns the text with Speaker Diarization.
        Returns our standard document list format.
        """
        if not os.getenv("ASSEMBLYAI_API_KEY"):
            return []

        print(f"Transcribing audio: {source_name}...")
        
        try:
            # We enable speaker_labels to get speaker diarization (Speaker A, Speaker B)
            config = aai.TranscriptionConfig(speaker_labels=True)
            transcript = self.transcriber.transcribe(file_path, config=config)

            if transcript.status == aai.TranscriptStatus.error:
                print(f"Transcription failed: {transcript.error}")
                return []

            # Format the text with speaker labels
            formatted_text = ""
            
            # If the audio has multiple speakers, format it clearly
            if transcript.utterances:
                for utterance in transcript.utterances:
                    formatted_text += f"Speaker {utterance.speaker}: {utterance.text}\n"
            else:
                # Fallback if diarization didn't pick up distinct speakers
                formatted_text = transcript.text

            if not formatted_text.strip():
                print(f"Warning: No speech detected in {source_name}")
                return []

            # Wrap in our standard format
            return [{
                "text": formatted_text.strip(),
                "metadata": {
                    "source": source_name,
                    "page": 1,
                    "type": "audio",
                    "duration_seconds": getattr(transcript, 'audio_duration', 0)
                }
            }]

        except Exception as e:
            print(f"Error processing audio {source_name}: {str(e)}")
            return []
