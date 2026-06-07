import os
import json
from google import genai
from google.genai import types

class PodcastGenerator:
    def __init__(self):
        """
        Initializes the Podcast Generator with the Google Gemini Chat Model.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        
        self.client = genai.Client(api_key=api_key)
        self.chat_model = "gemini-2.5-flash"

    def generate_script(self, document_text: str) -> list[dict]:
        """
        Generates a 2-person podcast script based on the provided document text.
        Forces the LLM to output a structured JSON array.
        """
        print("Designing the podcast episode...")

        # Multi-Persona System Prompt
        system_prompt = """
You are a world-class podcast producer and scriptwriter. Your job is to turn the provided document into a highly engaging, entertaining, and educational 3-minute podcast script.

THE PERSONAS:
1. "Host 1": The enthusiastic, curious interviewer. They guide the conversation, ask great questions, and represent the listener.
2. "Host 2": The deep-dive expert. They explain complex topics simply, use great analogies, and provide insightful commentary on the document.

RULES:
- The tone should be natural, conversational, and energetic.
- Include natural banter (e.g., "That's exactly right!", "Wait, explain that again...").
- Keep it focused on the core themes of the provided document.
- DO NOT use sound effect cues in the text. Only write the spoken dialogue.

OUTPUT FORMAT:
You MUST output a strict JSON array of objects. Do not include markdown blocks or any other text.
Example format:
[
  {"speaker": "Host 1", "text": "Welcome back to the Deep Dive! Today we have a fascinating document to cover."},
  {"speaker": "Host 2", "text": "Thanks for having me. I'm really excited about this one."}
]
"""

        print("Recording the hosts (Generating JSON script)...")
        
        try:
            # We enforce JSON output using the config
            response = self.client.models.generate_content(
                model=self.chat_model,
                contents=[
                    system_prompt,
                    f"DOCUMENT TEXT TO DISCUSS:\n{document_text}"
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.7 # Slight creativity for banter
                )
            )
            
            # The response text should be a valid JSON string
            script_data = json.loads(response.text)
            return script_data

        except Exception as e:
            print(f"Error generating podcast script: {str(e)}")
            return []
