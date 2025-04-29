import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import axios from 'axios'
import './App.css'
import Terms from './Terms'

// Configure axios
const axiosInstance = axios.create({
  baseURL: 'http://localhost:8005',
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  }
})

// Add request interceptor for better error handling
axiosInstance.interceptors.request.use(
  config => {
    // For multipart/form-data, let the browser set the Content-Type
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type']
    }
    return config
  },
  error => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// Add response interceptor for better error handling
axiosInstance.interceptors.response.use(
  response => response,
  error => {
    console.error('Response error:', error)
    if (!error.response) {
      throw new Error('Network error - Please check if the server is running and try again')
    }
    throw error
  }
)

function MainApp() {
  const [file, setFile] = useState<File | null>(null)
  const [titles, setTitles] = useState<string>('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string>('')
  const [targetAudience, setTargetAudience] = useState<string>('')
  const [feedback, setFeedback] = useState<string>('')
  const [isLoadingFeedback, setIsLoadingFeedback] = useState(false)
  const [feedbackError, setFeedbackError] = useState<string>('')

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0]
      if (!selectedFile.name.endsWith('.pptx')) {
        setError('Please select a .pptx file')
        setFile(null)
        return
      }
      setFile(selectedFile)
      setError('')
      setFeedback('')
      setFeedbackError('')
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) {
      setError('Please select a file')
      return
    }

    const formData = new FormData()
    formData.append('file', file)

    setLoading(true)
    setError('')

    try {
      const response = await axiosInstance.post('/api/extract-titles', formData)
      setTitles(response.data.titles)
    } catch (err: any) {
      console.error('Error details:', err)
      const errorMessage = err.response?.data?.detail || err.message || 'Error processing file. Please try again.'
      setError(`Error: ${errorMessage}`)
    } finally {
      setLoading(false)
    }
  }

  const handleDownload = () => {
    const blob = new Blob([titles], { type: 'text/plain' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'slide-titles.txt'
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
  }

  const handleGetFeedback = async () => {
    if (!titles) {
      setFeedbackError('Please extract titles first before requesting feedback')
      return
    }

    setIsLoadingFeedback(true)
    setFeedbackError('')
    setError('')

    try {
      const response = await axiosInstance.post('/api/get-feedback', {
        titles,
        targetAudience: targetAudience.trim() || 'general audience'
      })
      setFeedback(response.data.feedback)
    } catch (err: any) {
      console.error('Error getting feedback:', err)
      const errorMessage = err.response?.data?.detail || err.message || 'Error getting feedback. Please try again.'
      setFeedbackError(`Error: ${errorMessage}`)
    } finally {
      setIsLoadingFeedback(false)
    }
  }

  return (
    <div className="container">
      <h1>PPT slide title extractor</h1>
      
      <div className="instructions">
        Extract slide titles from your PowerPoint presentations. Simple. Free. No registration required.
      </div>

      <form onSubmit={handleSubmit}>
        <div className="upload-section">
          <label htmlFor="file-input" style={{ display: 'block', marginBottom: '5px' }}>
            Select your PowerPoint file (.pptx):
          </label>
          <input
            id="file-input"
            type="file"
            accept=".pptx"
            onChange={handleFileChange}
            className="file-input"
          />
          <div className="audience-input-section" style={{ marginTop: '10px' }}>
            <label htmlFor="audience-input" style={{ display: 'block', marginBottom: '5px' }}>
              Target Audience (optional):
            </label>
            <input
              id="audience-input"
              type="text"
              value={targetAudience}
              onChange={(e) => setTargetAudience(e.target.value)}
              placeholder="e.g., executives, students, technical team"
              className="audience-input"
            />
          </div>
          <button type="submit" disabled={!file || loading}>
            {loading ? 'processing...' : 'extract titles'}
          </button>
        </div>
      </form>

      {error && <div className="error">{error}</div>}

      {titles && (
        <div className="results">
          <h2>extracted titles:</h2>
          <pre>{titles}</pre>
          <div className="button-group">
            <button 
              onClick={handleDownload}
              className="primary-button"
            >
              save as text file
            </button>
            <button 
              onClick={handleGetFeedback} 
              disabled={isLoadingFeedback}
              className={`feedback-button ${isLoadingFeedback ? 'loading' : ''}`}
            >
              {isLoadingFeedback ? (
                <>
                  <span className="loading-spinner"></span>
                  Getting Feedback...
                </>
              ) : 'Get Narrative Feedback'}
            </button>
          </div>
        </div>
      )}

      {feedbackError && (
        <div className="error-message feedback-error">
          {feedbackError}
        </div>
      )}

      {feedback && (
        <div className="feedback-section">
          <h2>Narrative Feedback</h2>
          <div className="feedback-content">
            {feedback.split('\n').map((paragraph, index) => (
              <p key={index}>{paragraph}</p>
            ))}
          </div>
        </div>
      )}

      <div style={{ marginTop: '20px', borderTop: '1px solid #ccc', paddingTop: '10px', fontSize: '12px', color: '#666' }}>
        © 2025 - PPT Title Extractor - <Link to="/terms">terms of use</Link>
      </div>
    </div>
  )
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainApp />} />
        <Route path="/terms" element={<Terms />} />
      </Routes>
    </Router>
  )
}

export default App 