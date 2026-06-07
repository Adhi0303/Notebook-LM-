import os
from typing import List, Dict, Any
from google import genai
from src.generation.retriever import SemanticRetriever

class RAGEngine:
    def __init__(self):
        """
        Initializes the RAG Engine by connecting to the Semantic Retriever
        and the Google Gemini Chat Model.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        
        self.client = genai.Client(api_key=api_key)
        self.retriever = SemanticRetriever()
        
        # We use flash for incredibly fast conversational responses
        self.chat_model = "gemini-2.5-flash"

    def format_context(self, retrieved_chunks: List[Dict[str, Any]]) -> str:
        """
        Takes the raw chunks from Milvus and formats them into a clean string
        that the LLM can easily read.
        """
        if not retrieved_chunks:
            return "No relevant context found."

        formatted_string = ""
        for i, chunk in enumerate(retrieved_chunks):
            formatted_string += f"--- Document {i+1} ---\n"
            formatted_string += f"Source: {chunk['source']} (Chunk {chunk['chunk_index']})\n"
            formatted_string += f"Text:\n{chunk['text']}\n\n"
        
        return formatted_string

    def ask(self, query: str) -> str:
        """
        The Master Function for Phase 3.
        1. Retrieves relevant chunks.
        2. Injects them into the System Prompt.
        3. Generates an answer using Google Gemini.
        """
        print(f"Retrieving context for: '{query}'...")
        # Get top 3 chunks
        chunks = self.retriever.retrieve(query=query, top_k=3)
        context_string = self.format_context(chunks)

        # The System Prompt (AI Engineering Magic)
        system_prompt = f"""
You are an expert AI Research Assistant. Your job is to answer the user's question using ONLY the information provided in the CONTEXT below.

CRITICAL RULES:
1. DO NOT make up information (No Hallucinations). 
2. If the answer is NOT present in the CONTEXT, you must explicitly say: "I'm sorry, but I don't have enough information in your documents to answer that."
3. You must write clearly and beautifully.
4. CITATIONS: Whenever you state a fact from the CONTEXT, you MUST cite the source at the end of the sentence using brackets like this: [Source: filename.txt].

=========================================
CONTEXT:
{context_string}
=========================================

USER QUESTION:
{query}
"""
        print("Generating response from Gemini...")
        try:
            response = self.client.models.generate_content(
                model=self.chat_model,
                contents=system_prompt
            )
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
