import os
from mem0 import Memory

class MemoryLayer:
    def __init__(self):
        """
        Initializes Mem0 Memory using Google Gemini.
        It uses a local SQLite database by default to store the memory.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")

        config = {
            "llm": {
                "provider": "gemini",
                "config": {
                    "api_key": api_key,
                }
            },
            "embedder": {
                "provider": "gemini",
                "config": {
                    "api_key": api_key,
                }
            },
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "collection_name": "notebook_memory",
                    "embedding_model_dims": 768
                }
            }
        }
        
        # Initialize Mem0. It will automatically create a local SQLite database!
        self.memory = Memory.from_config(config)

    def save_interaction(self, query: str, answer: str, user_id: str = "default_user"):
        """
        Saves the user's question and the AI's answer.
        Mem0 uses the LLM to extract permanent facts and stores them in its database.
        """
        messages = [
            {"role": "user", "content": query},
            {"role": "assistant", "content": answer}
        ]
        print(f"[Memory] Extracting and saving facts for {user_id}...")
        self.memory.add(messages, user_id=user_id)

    def get_memory_context(self, query: str, user_id: str = "default_user") -> str:
        """
        Searches Mem0's database for past facts relevant to the current query.
        Returns a formatted string to inject into the prompt.
        """
        results = self.memory.search(query, filters={'user_id': user_id})
        
        # Mem0 recently changed their search API to return a dict {'results': [...]} instead of a list
        if isinstance(results, dict) and "results" in results:
            memory_list = results["results"]
        else:
            memory_list = results
            
        if not memory_list:
            return "No previous memory found."
        
        facts = [res['memory'] for res in memory_list if isinstance(res, dict) and 'memory' in res]
        
        formatted_memory = "\n".join([f"- {fact}" for fact in facts])
        return formatted_memory
