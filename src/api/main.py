from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil

# Import our backend logic
from ingest import run_ingestion
from src.generation.rag import RAGEngine
from src.generation.podcast_generator import PodcastGenerator
from src.generation.podcast_studio import PodcastStudio

app = FastAPI(title="NotebookLM Clone API")

# Allow CORS for Next.js frontend (which will run on localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure data output directories exist
os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# Pydantic models for request bodies
class ChatRequest(BaseModel):
    message: str
    user_id: str = "julian_vane"  # Hardcoded user for memory demo

class PodcastRequest(BaseModel):
    filename: str

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """Uploads a file, saves it, and ingests it into Milvus."""
    try:
        file_path = os.path.join("data", file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Trigger the ingestion pipeline (PyMuPDF -> Chunker -> Gemini -> Milvus)
        # Note: If it's a PDF we would need our PDF processor, but run_ingestion currently reads text.
        # Let's assume text files for now based on the ingest.py implementation, or we can update ingest.py later.
        run_ingestion(file_path, collection_name="notebook_documents")
        
        return {"filename": file.filename, "status": "Successfully ingested into Vector DB!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat_with_documents(request: ChatRequest):
    """Answers a question using RAG and Mem0."""
    try:
        engine = RAGEngine()
        response = engine.ask(query=request.message)
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/podcast")
async def generate_podcast(request: PodcastRequest):
    """Generates a multi-speaker podcast from a document."""
    try:
        file_path = os.path.join("data", request.filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
            
        with open(file_path, "r", encoding="utf-8") as f:
            document_text = f.read()

        # Step 1: Generate Script
        generator = PodcastGenerator()
        script_json = generator.generate_script(document_text)

        # Step 2: Generate Audio
        studio = PodcastStudio()
        output_file = studio.generate_podcast_audio(script_json)

        return {"status": "success", "audio_url": f"/{output_file}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sources")
async def list_sources():
    """Returns a list of all documents in the data folder."""
    try:
        if not os.path.exists("data"):
            return {"sources": []}
        files = os.listdir("data")
        # Format for frontend
        sources = [{"id": i, "name": f, "type": "Document"} for i, f in enumerate(files)]
        return {"sources": sources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
