"""
YouTube Video Transcriber Module
Extracts audio from YouTube and feeds it to the AudioTranscriber.
"""

import os
import yt_dlp
from typing import List, Dict, Any
from .audio_transcriber import AudioTranscriber

class YouTubeTranscriber:
    def __init__(self):
        self.audio_transcriber = AudioTranscriber()
        # We will save temporary audio files to the outputs folder
        self.temp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'outputs'))
        os.makedirs(self.temp_dir, exist_ok=True)

    def process_video(self, url: str) -> List[Dict[str, Any]]:
        """
        Downloads audio from a YouTube URL and transcribes it.
        Returns the standard document format.
        """
        print(f"Downloading audio from YouTube: {url}...")
        
        # We define a temporary output path
        temp_audio_path = os.path.join(self.temp_dir, 'temp_yt_audio.m4a')
        
        # yt-dlp options to download ONLY the audio (saves bandwidth/time)
        ydl_opts = {
            'format': 'm4a/bestaudio/best',
            'outtmpl': temp_audio_path,
            'quiet': True,
            'no_warnings': True
        }

        try:
            # Download the audio
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                video_title = info_dict.get('title', 'Unknown YouTube Video')

            # Pass the downloaded audio to our AudioTranscriber
            docs = self.audio_transcriber.process_audio(temp_audio_path, source_name=video_title)
            
            # Update the metadata type to 'youtube' and add the url
            if docs:
                docs[0]['metadata']['type'] = 'youtube'
                docs[0]['metadata']['url'] = url

            return docs

        except Exception as e:
            print(f"Error processing YouTube video {url}: {str(e)}")
            return []
            
        finally:
            # Clean up: delete the temporary audio file so we don't waste disk space
            if os.path.exists(temp_audio_path):
                try:
                    os.remove(temp_audio_path)
                except Exception as cleanup_error:
                    print(f"Warning: Could not delete temporary audio file: {cleanup_error}")
