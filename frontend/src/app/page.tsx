'use client';

import styles from "./page.module.css";
import { useState, useEffect, useRef } from "react";

export default function AestheticNotebook() {
  const [sources, setSources] = useState<any[]>([]);
  const [activeSource, setActiveSource] = useState<any>(null);
  const [chatInput, setChatInput] = useState("");
  const [chatHistory, setChatHistory] = useState<{role: string, content: string}[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Fetch sources on load
  useEffect(() => {
    fetchSources();
  }, []);

  const fetchSources = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/sources");
      const data = await res.json();
      setSources(data.sources || []);
      if (data.sources && data.sources.length > 0 && !activeSource) {
        setActiveSource(data.sources[0]);
      }
    } catch (e) {
      console.error("Failed to fetch sources", e);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    const file = e.target.files[0];
    
    const formData = new FormData();
    formData.append("file", file);

    try {
      await fetch("http://localhost:8000/api/upload", {
        method: "POST",
        body: formData,
      });
      // Refresh sources after upload
      fetchSources();
    } catch (e) {
      console.error("Upload failed", e);
    }
  };

  const handleChatSubmit = async (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && chatInput.trim()) {
      const userMessage = chatInput.trim();
      setChatInput("");
      setChatHistory(prev => [...prev, {role: "user", content: userMessage}]);
      setIsTyping(true);

      try {
        const res = await fetch("http://localhost:8000/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: userMessage, user_id: "julian_vane" })
        });
        const data = await res.json();
        setChatHistory(prev => [...prev, {role: "assistant", content: data.answer}]);
      } catch (e) {
        setChatHistory(prev => [...prev, {role: "assistant", content: "Error connecting to AI backend."}]);
      } finally {
        setIsTyping(false);
      }
    }
  };

  return (
    <div className={styles.container}>
      
      {/* 1. Global Sidebar */}
      <nav className={styles.globalSidebar}>
        <div className={styles.brand}>Notebook</div>
        
        <div className={`${styles.navItem} ${styles.active}`}>
          <span style={{marginRight: '12px'}}>📓</span> Journal
        </div>
        <div className={styles.navItem}>
          <span style={{marginRight: '12px'}}>📚</span> Library
        </div>
        <div className={styles.navItem}>
          <span style={{marginRight: '12px'}}>🗃️</span> Archive
        </div>
        <div className={styles.navItem}>
          <span style={{marginRight: '12px'}}>🗑️</span> Trash
        </div>

        <button className={styles.newEntryBtn}>
          + New Entry
        </button>
      </nav>

      {/* 2. Context Panel (Sources) */}
      <aside className={styles.contextPanel}>
        <div className={styles.panelHeader}>
          Sources
          <button style={{fontSize: '18px'}}>+</button>
        </div>
        
        <div className={styles.sourceList}>
          {sources.map((s, i) => (
            <div 
              key={i}
              className={`${styles.sourceCard} ${activeSource?.name === s.name ? styles.active : ""}`}
              onClick={() => setActiveSource(s)}
            >
              <div style={{fontWeight: 600, marginBottom: '4px'}}>{s.name}</div>
              <div style={{fontSize: '12px', color: 'var(--secondary)'}}>{s.type}</div>
              {activeSource?.name === s.name && (
                <span style={{fontSize: '10px', background: '#E5E2DA', padding: '2px 6px', borderRadius: '4px', marginTop: '8px', display: 'inline-block'}}>ACTIVE</span>
              )}
            </div>
          ))}
          
          {sources.length === 0 && (
            <div style={{color: 'var(--secondary)', fontSize: '13px', textAlign: 'center', marginTop: '20px'}}>
              No sources added yet.
            </div>
          )}
        </div>

        <input 
          type="file" 
          ref={fileInputRef} 
          style={{display: 'none'}} 
          onChange={handleFileUpload} 
        />
        <button 
          className={styles.addSourceBtn}
          onClick={() => fileInputRef.current?.click()}
        >
          ⊕ Add Source
        </button>
      </aside>

      {/* 3. Reading Pane (Center) */}
      <main className={styles.readingPane}>
        {activeSource ? (
          <div className={styles.documentContainer}>
            <h1 className={styles.docTitle}>{activeSource.name.replace(".txt", "").replace(".pdf", "")}</h1>
            <div className={styles.docMeta}>
              Uploaded Document
              <br/><br/>
              <span style={{background: '#E5E2DA', padding: '4px 12px', borderRadius: '4px', marginRight: '8px'}}>Context Layer</span>
            </div>

            <div className={styles.docContent}>
              <p>
                <i>(Document text loading via vector embeddings...)</i>
                <br/><br/>
                This is a placeholder for the beautiful document reader. In a fully built out version, 
                this would query Milvus for the original text chunks or load the raw PDF via a viewer.
                <br/><br/>
                Try asking the AI about this document using the chat panel on the right!
              </p>
            </div>
          </div>
        ) : (
          <div style={{margin: 'auto', color: 'var(--secondary)', textAlign: 'center'}}>
            <h2 className={styles.docTitle} style={{color: 'var(--primary)', marginBottom: '16px'}}>Welcome to your Sanctuary.</h2>
            Upload a document to the left to begin synthesizing knowledge.
          </div>
        )}
      </main>

      {/* 4. Notebook AI Pane (Right) */}
      <aside className={styles.aiPane}>
        <div className={styles.aiHeader}>
          ✨ Notebook AI
        </div>
        
        <div className={styles.aiContent}>
          {chatHistory.length === 0 ? (
            <>
              <div className={styles.sectionTitle}>GETTING STARTED</div>
              <div className={styles.summaryCard}>
                I am your personal AI research assistant. Upload a source on the left, and ask me any question.
                I will synthesize an answer strictly grounded in your documents.
              </div>
            </>
          ) : (
            chatHistory.map((msg, idx) => (
              <div key={idx} style={{marginBottom: '24px'}}>
                <div className={styles.sectionTitle}>{msg.role === 'user' ? 'YOU' : 'INK AI'}</div>
                <div className={styles.summaryCard} style={msg.role === 'user' ? {background: 'var(--primary)', color: '#fff'} : {}}>
                  {msg.content}
                </div>
              </div>
            ))
          )}
          
          {isTyping && (
            <div style={{color: 'var(--secondary)', fontSize: '13px', fontStyle: 'italic'}}>
              Ink AI is thinking...
            </div>
          )}
        </div>

        <div className={styles.chatInputContainer}>
          <div style={{marginBottom: '12px', fontSize: '13px', fontStyle: 'italic', color: 'var(--secondary)'}}>Ask about the text...</div>
          <input 
            type="text" 
            className={styles.chatInput} 
            placeholder="Ask anything..."
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            onKeyDown={handleChatSubmit}
          />
        </div>
      </aside>

    </div>
  );
}
