// Article display component: summary, translation
import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import './ArticleDisplay.css';

const ArticleDisplay = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { logout, user } = useAuth();
  const article = location.state?.article;

  if (!article) {
    navigate('/extract');
    return null;
  }

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="display-container">
      <nav className="top-nav">
        <div className="nav-content">
          <h1 onClick={() => navigate('/extract')} style={{ cursor: 'pointer' }}>WikiSmart-Edu</h1>
          <div className="nav-right">
            <span className="user-name">Welcome, {user?.username}!</span>
            <button onClick={handleLogout} className="logout-btn">Logout</button>
          </div>
        </div>
      </nav>

      <div className="content-area">
        <div className="article-card">
          <div className="article-header">
            <h1>{article.data?.title || article.data?.file_name}</h1>
            <button onClick={() => navigate('/extract')} className="back-btn">
              ← Back to Extract
            </button>
          </div>

          <div className="article-content">
            {/* AI Summary - Short (Bullet Points) */}
            {article.data?.ai_summary_short && (
              <div className="summary-section ai-summary">
                <h3>🤖 AI Summary (Key Points)</h3>
                <div className="summary-box">
                  <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>
                    {article.data.ai_summary_short}
                  </pre>
                </div>
              </div>
            )}

            {/* AI Summary - Medium (Paragraphs) */}
            {article.data?.ai_summary_medium && (
              <div className="summary-section ai-summary">
                <h3>📝 AI Summary (Detailed)</h3>
                <div className="summary-box">
                  <p style={{ whiteSpace: 'pre-wrap' }}>
                    {article.data.ai_summary_medium}
                  </p>
                </div>
              </div>
            )}

            {/* Wikipedia Original Summary */}
            {article.data?.summary && (
              <div className="summary-section">
                <h3>📚 Wikipedia Summary</h3>
                <p>{article.data.summary}</p>
              </div>
            )}

            <div className="full-content">
              <h3>📖 Full Content</h3>
              <div className="text-content">
                {article.data?.content || article.data?.full_text}
              </div>
            </div>

            {article.data?.page_count && (
              <div className="metadata">
                <span>📄 Pages: {article.data.page_count}</span>
              </div>
            )}
            
            {article.data?.language && (
              <div className="metadata">
                <span>🌐 Language: {article.data.language.toUpperCase()}</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ArticleDisplay;

