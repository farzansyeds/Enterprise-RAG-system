import { useState } from 'react'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [question, setQuestion] = useState('')
  const [chat, setChat] = useState([])
  const [loading, setLoading] = useState(false)
  const [indexing, setIndexing] = useState(false)

  const handleUpload = async (e) => {
    e.preventDefault()
    if (!file) return alert('Please choose a file first.')

    setIndexing(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await fetch('/api/upload', { method: 'POST', body: formData })
      if (!res.ok) throw new Error(`Upload failed: ${res.statusText}`)
      const data = await res.json()
      alert(data.message || 'Indexing complete!')
    } catch (err) {
      alert(`Upload error: ${err.message}`)
    } finally {
      setIndexing(false)
    }
  }

  const handleChat = async (e) => {
    e.preventDefault()
    if (!question.trim()) return

    const userPrompt = question
    setQuestion('')
    setLoading(true)

    setChat((prev) => [...prev, { role: 'user', content: userPrompt }])

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: userPrompt }),
      })

      if (!res.ok) throw new Error(`Server returned ${res.status}`)
      const data = await res.json()
      
      // let answerText = typeof data.answer === 'string' ? data.answer : 
      //                  (data.answer?.content || JSON.stringify(data.answer))

      let answerText = "";
      
      try {
        let parsedData = data.answer;
        
        // 1. If the backend sent a stringified JSON array, parse it into a real array
        if (typeof parsedData === 'string' && parsedData.trim().startsWith('[')) {
          parsedData = JSON.parse(parsedData);
        }
        
        // 2. Extract just the text from the Gemini complex structure
        if (Array.isArray(parsedData) && parsedData[0] && parsedData[0].text) {
          answerText = parsedData[0].text;
        } 
        // 3. Fallback for standard string responses
        else if (typeof data.answer === 'string') {
          answerText = data.answer;
        } 
        // 4. Fallback for generic objects
        else {
          answerText = data.answer?.content || JSON.stringify(data.answer);
        }
      } catch (err) {
        // Ultimate fallback if parsing completely fails
        answerText = typeof data.answer === 'string' ? data.answer : JSON.stringify(data.answer);
      }

      setChat((prev) => [...prev, { role: 'ai', content: answerText }])
    } catch (err) {
      setChat((prev) => [...prev, { role: 'ai', content: `Error: ${err.message}` }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="saas-dashboard">
      {/* CSS-Only Animated AI Background */}
      <div className="animated-bg">
        <div className="glow-orb orb-1"></div>
        <div className="glow-orb orb-2"></div>
        <div className="particle p1"></div>
        <div className="particle p2"></div>
        <div className="particle p3"></div>
      </div>

      <div className="content-wrapper">
        
        {/* Card 1: Header */}
        <div className="card header-card">
          {/* <div className="header-icon">✨</div> */}
          <div className="header-text">
          <h1><u>Retrieval-Augmented Generation Pipeline</u></h1>
          </div>
        </div>

        {/* Card 2: Pipeline Steps */}
        <div className="card steps-card" style={{ flexWrap: 'wrap' }}>
          <div style={{ width: '100%', marginBottom: '1rem', color: 'var(--text-muted)' }}>
            <b><u>WORKFLOW:</u></b>
          </div>
          
          <div className="step">
            <div className="step-badge active">1</div>
            <div className="step-label">Document<br/>Upload</div>
          </div>
          <div className="step">
            <div className="step-badge active">2</div>
            <div className="step-label">Vector<br/>Embedding</div>
          </div>
          <div className="step">
            <div className="step-badge active">3</div>
            <div className="step-label">ChromaDB<br/>Store</div>
          </div>
          <div className="step">
            <div className="step-badge active">4</div>
            <div className="step-label">Gemini<br/>Inference</div>
          </div>
        </div>

        {/* Card 3: Ingestion */}
        <div className="card ingestion-card">
          <h2><b><i>Knowledge Base Ingestion ⬇️</i></b></h2>
          <p className="subtitle">Upload PDF documents to generate and store semantic vectors.</p>
          
          <form onSubmit={handleUpload} className="upload-box">
            <input 
              type="file" 
              accept=".pdf"
              onChange={(e) => setFile(e.target.files[0])} 
              className="native-file-input"
            />
            <button type="submit" disabled={indexing} className="btn-upload">
              {indexing ? 'Processing...' : 'Index Document'}
            </button>
          </form>
        </div>

        {/* Card 4: Inference / Chat */}
        <div className="card chat-card">
          <div className="chat-window">
            {chat.length === 0 && !loading && (
              <div className="empty-state">
                <span className="brain-icon">🧠</span>
                <p>System initialized. Ask a question to query the vector database.</p>
              </div>
            )}

            {chat.map((msg, i) => (
              <div key={i} className={`message ${msg.role}`}>
                <div className="message-content">{msg.content}</div>
              </div>
            ))}

            {loading && (
              <div className="message ai typing">
                <span className="dot"></span><span className="dot"></span><span className="dot"></span>
              </div>
            )}
          </div>

          <form onSubmit={handleChat} className="chat-input-row">
            <input
              className="query-input"
              value={question}
              placeholder="Query the vector database..."
              onChange={(e) => setQuestion(e.target.value)}
              disabled={loading}
            />
            <button type="submit" disabled={loading} className="btn-send">
              Ask
            </button>
          </form>
        </div>

      </div>
    </div>
  )
}

export default App