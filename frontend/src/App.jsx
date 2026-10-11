import { useState } from 'react'
import './App.css' // Import the external CSS

function App() {
  const [file, setFile] = useState(null)
  const [question, setQuestion] = useState('')
  const [chat, setChat] = useState([])
  const [loading, setLoading] = useState(false)
  const [indexing, setIndexing] = useState(false)

  const handleUpload = async (e) => {
    e.preventDefault()
    if (!file) {
      alert('Please choose a file first.')
      return
    }

    setIndexing(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      })
      if (!res.ok) throw new Error(`Upload failed: ${res.statusText}`)
      const data = await res.json()
      alert(data.message || 'Indexing complete!')
    } catch (err) {
      console.error(err)
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

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: userPrompt }),
      })

      if (!res.ok) throw new Error(`Server returned ${res.status}`)

      const data = await res.json()

      let answerText = ''
      if (typeof data.answer === 'string') {
        answerText = data.answer
      } else if (data.answer && typeof data.answer === 'object') {
        answerText = data.answer.content || JSON.stringify(data.answer)
      } else {
        answerText = 'No response generated.'
      }

      setChat((prevChat) => [...prevChat, { q: userPrompt, a: answerText }])
    } catch (err) {
      console.error('Chat error:', err)
      setChat((prevChat) => [
        ...prevChat,
        { q: userPrompt, a: `Error: Unable to fetch response (${err.message})` },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <h1 className="app-header">Enterprise RAG System</h1>

      <form onSubmit={handleUpload} className="upload-form">
        <input 
          type="file" 
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])} 
          className="file-input"
        />
        <button type="submit" disabled={indexing} className="primary-btn">
          {indexing ? 'Indexing...' : 'Upload & Index'}
        </button>
      </form>

      <div className="chat-window">
        {chat.length === 0 && (
          <p className="empty-state">Ask a question below to start chatting with your document.</p>
        )}
        
        {chat.map((msg, i) => (
          <div key={i} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div className="chat-message user">
              <div className="message-label">You</div>
              <p className="message-content">{msg.q}</p>
            </div>
            <div className="chat-message ai">
              <div className="message-label">AI Assistant</div>
              <p className="message-content">{msg.a}</p>
            </div>
          </div>
        ))}
        {loading && <p className="loading-indicator">Thinking...</p>}
      </div>

      <form onSubmit={handleChat} className="input-form">
        <input
          className="text-input"
          value={question}
          placeholder="Ask a question..."
          onChange={(e) => setQuestion(e.target.value)}
          disabled={loading}
        />
        <button type="submit" disabled={loading} className="primary-btn">
          {loading ? 'Asking...' : 'Ask'}
        </button>
      </form>
    </div>
  )
}

export default App