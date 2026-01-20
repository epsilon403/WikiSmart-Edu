// Article extraction component
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import api from '../../services/auth';
import './ArticleExtract.css';

const ArticleExtract = () => {
  const navigate = useNavigate();
  const [url, setUrl] = useState('');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [extractedData, setExtractedData] = useState(null);
  const [error, setError] = useState('');
  const [extractType, setExtractType] = useState('wikipedia'); // 'wikipedia' or 'pdf'
  const { user, logout } = useAuth();

  const handleUrlSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    setExtractedData(null);

    try {
      const response = await api.post('/api/v1/articles/extract-wiki', { url });
      setExtractedData(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to extract Wikipedia content');
    } finally {
      setLoading(false);
    }
  };

  const handleFileSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a PDF file');
      return;
    }

    setError('');
    setLoading(true);
    setExtractedData(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await api.post('/api/v1/articles/extract-pdf', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setExtractedData(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to extract PDF content');
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setError('');
    } else {
      setError('Please select a valid PDF file');
      setFile(null);
    }
  };

  return (
    <div className="extract-container">
      <nav className="extract-nav">
        <div className="nav-content">
          <h1>WikiSmart-Edu</h1>
          <div className="nav-actions">
            <span className="user-name">Welcome, {user?.username}</span>
            <button onClick={logout} className="logout-btn">Logout</button>
          </div>
        </div>
      </nav>

      <div className="extract-content">
        <div className="extract-card">
          <h2>Extract Content</h2>
          <p className="subtitle">Extract content from Wikipedia or upload a PDF file</p>

          <div className="extract-tabs">
            <button 
              className={`tab ${extractType === 'wikipedia' ? 'active' : ''}`}
              onClick={() => setExtractType('wikipedia')}
            >
              Wikipedia URL
            </button>
            <button 
              className={`tab ${extractType === 'pdf' ? 'active' : ''}`}
              onClick={() => setExtractType('pdf')}
            >
              PDF Upload
            </button>
          </div>

          {error && (
            <div className="error-message">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
              {error}
            </div>
          )}

          {extractType === 'wikipedia' ? (
            <form onSubmit={handleUrlSubmit} className="extract-form">
              <div className="form-group">
                <label htmlFor="url">Wikipedia URL</label>
                <input
                  type="url"
                  id="url"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="https://en.wikipedia.org/wiki/..."
                  required
                />
                <small>Enter a valid Wikipedia article URL</small>
              </div>

              <button type="submit" className="extract-button" disabled={loading}>
                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Extracting...
                  </>
                ) : (
                  'Extract Content'
                )}
              </button>
            </form>
          ) : (
            <form onSubmit={handleFileSubmit} className="extract-form">
              <div className="form-group">
                <label htmlFor="file">PDF File</label>
                <div className="file-input-wrapper">
                  <input
                    type="file"
                    id="file"
                    accept=".pdf"
                    onChange={handleFileChange}
                    required
                  />
                  {file && <span className="file-name">{file.name}</span>}
                </div>
                <small>Upload a PDF file (max 10MB)</small>
              </div>

              <button type="submit" className="extract-button" disabled={loading || !file}>
                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Extracting...
                  </>
                ) : (
                  'Extract Content'
                )}
              </button>
            </form>
          )}

          {extractedData && (
            <div className="result-section">
              <h3>Extraction Successful!</h3>
              <div className="result-info">
                <p><strong>Status:</strong> {extractedData.status}</p>
                <p><strong>Article ID:</strong> {extractedData.article_id}</p>
                {extractedData.data.title && (
                  <p><strong>Title:</strong> {extractedData.data.title}</p>
                )}
                {extractedData.data.page_count && (
                  <p><strong>Pages:</strong> {extractedData.data.page_count}</p>
                )}
              </div>
              
              <div className="content-preview">
                <h4>Content Preview:</h4>
                <p className="preview-text">
                  {extractedData.data.summary || extractedData.data.full_text?.substring(0, 500)}...
                </p>
              </div>
              
              <button 
                onClick={() => navigate('/article', { state: { article: extractedData } })}
                className="view-article-btn"
              >
                View Full Article & AI Summaries
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ArticleExtract;
