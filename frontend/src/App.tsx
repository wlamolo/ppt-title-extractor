import { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [file, setFile] = useState<File | null>(null)
  const [titles, setTitles] = useState<string>('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string>('')

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setError('')
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
      const response = await axios.post('/api/extract-titles', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      setTitles(response.data.titles)
    } catch (err) {
      setError('Error processing file. Please try again.')
      console.error(err)
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

  return (
    <div className="container">
      <h1>PPT slide title extractor</h1>
      
      <div className="instructions">
        Extract slide titles from your PowerPoint presentations. Simple. Free. No registration required.
      </div>

      <form onSubmit={handleSubmit}>
        <div className="upload-section">
          <label htmlFor="file-input" style={{ display: 'block', marginBottom: '5px' }}>
            Select your PowerPoint file:
          </label>
          <input
            id="file-input"
            type="file"
            accept=".pptx"
            onChange={handleFileChange}
            className="file-input"
          />
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
          <button onClick={handleDownload} style={{ marginTop: '10px' }}>
            save as text file
          </button>
        </div>
      )}

      <div style={{ marginTop: '20px', borderTop: '1px solid #ccc', paddingTop: '10px', fontSize: '12px', color: '#666' }}>
        © 2024 - PPT Title Extractor - <a href="#">terms of use</a> - <a href="#">privacy</a>
      </div>
    </div>
  )
}

export default App 