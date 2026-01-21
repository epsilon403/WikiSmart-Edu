// Article extraction component: Wikipedia URL and PDF upload
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import api from '../../services/auth';
import './ArticleExtraction.css';

const ArticleExtraction = () => {
  const [wikipediaUrl, setWikipediaUrl] = useState('');
  const [pdfFile, setPdfFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('wikipedia');
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  const handleWikipediaSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await api.post('/api/v1/articles/extract-wiki', {
        url: wikipediaUrl
      });
      
      // Redirect to new content page with article data
      navigate('/article/content', { state: { article: response.data } });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to extract Wikipedia article');
    } finally {
      setLoading(false);
    }
  };

  const handlePdfUpload = async (e) => {
    e.preventDefault();
    if (!pdfFile) {
      setError('Please select a PDF file');
      return;
    }

    setError('');
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('file', pdfFile);

      const response = await api.post('/api/v1/articles/extract-pdf', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      // Redirect to new content page with article data
      navigate('/article/content', { state: { article: response.data } });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to extract PDF content');
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.type !== 'application/pdf') {
        setError('Please select a PDF file');
        setPdfFile(null);
        return;
      }
      setPdfFile(file);
      setError('');
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="extraction-container">
      <nav className="top-nav">
        <div className="nav-content">
          <h1>WikiSmart-Edu</h1>
          <div className="nav-right">
            <span className="user-name">Welcome, {user?.username}!</span>
            <button onClick={handleLogout} className="logout-btn">Logout</button>
          </div>
        </div>
      </nav>

      <div className="extraction-card">
        <div className="card-header">
          <h2>Extract Content</h2>
          <p>Extract content from Wikipedia articles or PDF documents</p>
        </div>

        <div className="tabs">
          <button
            className={`tab ${activeTab === 'wikipedia' ? 'active' : ''}`}
            onClick={() => setActiveTab('wikipedia')}
          >
            📰 Wikipedia URL
          </button>
          <button
            className={`tab ${activeTab === 'pdf' ? 'active' : ''}`}
            onClick={() => setActiveTab('pdf')}
          >
            📄 PDF Upload
          </button>
        </div>

        {error && (
          <div className="error-message">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            {error}
          </div>
        )}

        {activeTab === 'wikipedia' ? (
          <form onSubmit={handleWikipediaSubmit} className="extraction-form">
            <div className="form-group">
              <label htmlFor="url">Wikipedia URL</label>
              <input
                type="url"
                id="url"
                value={wikipediaUrl}
                onChange={(e) => setWikipediaUrl(e.target.value)}
                placeholder="https://en.wikipedia.org/wiki/Artificial_intelligence"
                required
              />
              <small className="helper-text">
                Paste a Wikipedia article URL to extract its content
              </small>
            </div>

            <button type="submit" className="extract-btn" disabled={loading}>
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Extracting...
                </>
              ) : (
                <>
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="7 10 12 15 17 10"></polyline>
                    <line x1="12" y1="15" x2="12" y2="3"></line>
                  </svg>
                  Extract Content
                </>
              )}
            </button>
          </form>
        ) : (
          <form onSubmit={handlePdfUpload} className="extraction-form">
            <div className="form-group">
              <label htmlFor="pdf">PDF Document</label>
              <div className="file-upload">
                <input
                  type="file"
                  id="pdf"
                  accept=".pdf"
                  onChange={handleFileChange}
                  required
                />
                <label htmlFor="pdf" className="file-label">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="17 8 12 3 7 8"></polyline>
                    <line x1="12" y1="3" x2="12" y2="15"></line>
                  </svg>
                  {pdfFile ? pdfFile.name : 'Choose PDF file'}
                </label>
              </div>
              <small className="helper-text">
                Upload a PDF document to extract its text content
              </small>
            </div>

            <button type="submit" className="extract-btn" disabled={loading || !pdfFile}>
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Extracting...
                </>
              ) : (
                <>
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="7 10 12 15 17 10"></polyline>
                    <line x1="12" y1="15" x2="12" y2="3"></line>
                  </svg>
                  Extract Content
                </>
              )}
            </button>
          </form>
        )}
      </div>
    </div>
  );
};

export default ArticleExtraction;
