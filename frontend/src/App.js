import React, { useState } from 'react';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);
  const [error, setError] = useState(null);

  // API URL - use current origin in production, localhost in development
  const API_URL = process.env.NODE_ENV === 'production' ? '' : 'http://localhost:5001';

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    setError(null);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    if (!selectedFile) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);
    setImageUrl(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch(`${API_URL}/api/upload`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (data.status === 'success') {
        setResult(data.result);
        setImageUrl(data.image_url);
        // Scroll to top to see results
        window.scrollTo({ top: 0, behavior: 'smooth' });
      } else {
        setError(data.error || 'Upload failed');
      }
    } catch (err) {
      setError('Upload failed: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <div className="card">
          <h1>Photography Coach</h1>
          <p className="subtitle">Upload your photo for professional yapping</p>

          <form onSubmit={handleSubmit} className="upload-form">
            <input
              type="file"
              id="fileInput"
              accept="image/*"
              onChange={handleFileSelect}
              style={{ display: 'none' }}
              required
            />
            <label htmlFor="fileInput" className="file-label">
              {selectedFile ? selectedFile.name : 'Choose File'}
            </label>
            <button 
              type="submit" 
              className="btn" 
              disabled={loading || !selectedFile}
            >
              {loading ? 'Uploading...' : 'Upload'}
            </button>
          </form>

          {loading && (
            <div className="loading">
              <div className="spinner"></div>
              <div className="loading-text">Analyzing your photo...</div>
            </div>
          )}

          {error && (
            <div className="error">
              {error}
            </div>
          )}

          {result && (
            <div className="result">
              <pre>{result}</pre>
            </div>
          )}

          {imageUrl && (
            <img src={imageUrl} alt="Uploaded" className="preview" />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
