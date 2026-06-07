# 🗺️ NotebookLM Clone: AI Engineering Project Roadmap & Learning Guide

This document serves as your complete roadmap from start to finish. It breaks down the project into distinct **Phases** and **Modules**. For each module, we highlight the core **AI Engineering Concepts** you will learn, and the specific **Tools/Tech** we will use. 

Use this document to track your learning journey. As we build each module, refer back to the concepts listed here to understand *why* we are doing it.

---

## Phase 0: Project Foundation & Environment (Completed)
*Laying the groundwork for a modern AI engineering project.*

*   **Tools Used:** `uv` (Package Manager), `python-dotenv`.
*   **Concepts Learned:**
    *   **Dependency Locking:** Using `uv.lock` to guarantee reproducible environments.
    *   **Virtual Environments:** Isolating Python packages to prevent system-wide conflicts.
    *   **Environment Variables:** Securely managing API keys (OpenAI, Zep, Firecrawl, etc.) without hardcoding them into source code.

---

## Phase 1: Data Ingestion & Extraction (The "ETL" Pipeline)
*The first step of RAG is getting your unstructured data (PDFs, Videos, Websites) and turning it into clean, structured text.*

### Module 1.1: Document Parsing
*   **Tools:** `PyMuPDF` (`fitz`)
*   **AI Engineering Concepts:**
    *   **Unstructured Data Processing:** Extracting plain text from complex graphical formats like PDFs.
    *   **Metadata Extraction:** Capturing page numbers, document titles, and creation dates. This metadata is the secret sauce for generating accurate *citations* later.

### Module 1.2: Advanced Web Scraping
*   **Tools:** `firecrawl-py`
*   **AI Engineering Concepts:**
    *   **DOM Parsing to Markdown:** Converting messy HTML structure into clean Markdown, which LLMs naturally understand and process highly efficiently.
    *   **Bypassing Anti-Bot Measures:** Handling dynamic Javascript rendering and standard web security layers.

### Module 1.3: Audio & Video Processing
*   **Tools:** `AssemblyAI`, `yt-dlp`
*   **AI Engineering Concepts:**
    *   **ASR (Automatic Speech Recognition):** The underlying technology (like Whisper) that converts spoken audio waves into text.
    *   **Speaker Diarization:** The ML process of answering "who spoke when?" (e.g., tagging sentences with Speaker A vs. Speaker B).

---

## Phase 2: Knowledge Representation & Storage
*How does an AI "read" and store this data so it can search it instantly?*

### Module 2.1: Semantic Text Chunking
*   **Tools:** Standard Python text processing or LangChain text splitters.
*   **AI Engineering Concepts:**
    *   **Context Windows:** Understanding why we can't feed a 500-page book to an LLM all at once.
    *   **Chunking Strategies:** Splitting text by tokens or characters.
    *   **Chunk Overlap:** Why we leave a 10-20% overlap between chunks so we don't accidentally split a crucial sentence in half and lose context.

### Module 2.2: Vector Embeddings
*   **Tools:** `openai` (Embedding Models like `text-embedding-3-small`)
*   **AI Engineering Concepts:**
    *   **Embeddings:** Translating human language into dense mathematical vectors (arrays of thousands of numbers).
    *   **High-Dimensional Space:** Understanding how words or paragraphs with similar semantic meanings end up physically close to each other in this mathematical space.

### Module 2.3: Vector Database Integration
*   **Tools:** `pymilvus` (Milvus Vector DB)
*   **AI Engineering Concepts:**
    *   **Vector Search (ANN - Approximate Nearest Neighbors):** Algorithms (like HNSW) used by databases to search millions of vectors in milliseconds without comparing every single one.
    *   **Metadata Filtering:** Combining semantic search ("Find paragraphs about dogs") with exact filtering ("Only look at Page 4 of Document A").

---

## Phase 3: The Core RAG Engine (Retrieval-Augmented Generation)
*Connecting the user's question to the database, and the database to the LLM.*

### Module 3.1: Semantic Retrieval
*   **Tools:** `pymilvus`, `openai`
*   **AI Engineering Concepts:**
    *   **Query Embedding:** Converting the user's chat message into a vector.
    *   **Distance Metrics:** Using Cosine Similarity or L2 Distance to find the closest matching document chunks to the user's query vector.
    *   **Top-K Retrieval:** Fetching the top 3 or 5 most relevant chunks to act as our "context".

### Module 3.2: Generation & Citation Prompting
*   **Tools:** `openai` (e.g., `gpt-4o-mini`)
*   **AI Engineering Concepts:**
    *   **In-Context Learning (Grounding):** Forcing the LLM to only answer based on the provided text to prevent **Hallucinations** (making things up).
    *   **System Prompts & Prompt Engineering:** Crafting strict rules for the LLM. e.g., *"You must cite your sources using the metadata provided in brackets [Doc: X, Page: Y]."*

---

## Phase 4: Agentic Conversational Memory
*Making the AI remember you across multiple sessions, not just the current question.*

### Module 4.1: Temporal Knowledge Graphs
*   **Tools:** `zep-python`
*   **AI Engineering Concepts:**
    *   **Stateless vs. Stateful LLMs:** Understanding that LLMs inherently have amnesia between turns.
    *   **Episodic Memory:** Simply appending the past 10 chat messages into the prompt (basic memory).
    *   **Semantic Memory / Knowledge Graphs:** Using Zep to automatically extract Entities (names, places) and Relationships from conversations over time, storing them as a graph, and injecting only the relevant nodes into the prompt.

---

## Phase 5: The AI Podcast Studio
*Transforming text into multi-speaker generative audio.*

### Module 5.1: Podcast Script Generation
*   **Tools:** `openai`
*   **AI Engineering Concepts:**
    *   **Multi-Persona Prompting:** Instructing an LLM to play two distinct roles (e.g., an enthusiastic host and an expert guest) and generating structured JSON or dialogue scripts.

### Module 5.2: Text-to-Speech (TTS) Synthesis
*   **Tools:** `Kokoro` (or similar TTS engine)
*   **AI Engineering Concepts:**
    *   **Generative Audio:** Synthesizing human-like voice from text.
    *   **Prosody & Voice Cloning:** Modifying the speed, pitch, and emotion of the generated voice.

---

## Phase 6: User Interface & Assembly
*Bringing it all together into a clean, reactive frontend.*

### Module 6.1: Streamlit Integration
*   **Tools:** `streamlit`
*   **AI Engineering Concepts:**
    *   **State Management (`st.session_state`):** Keeping track of uploaded files, chat history, and system status across page reloads.
    *   **Streaming Responses:** Fetching AI responses token-by-token (like ChatGPT) instead of waiting 10 seconds for the entire block of text to load.

---

### How to use this guide:
As we begin coding **Phase 1**, keep this document open. You can ask me questions like: *"Can you explain deeper how Chunk Overlap works before we write the code for it?"* or *"How exactly does PyMuPDF extract the metadata?"* 
