// Wikipedia Content Page - displays original content in Wikipedia style
import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import ContentNavigation from '../Common/ContentNavigation';
import './WikipediaContent.css';

const WikipediaContent = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const article = location.state?.article;

  if (!article) {
    navigate('/extract');
    return null;
  }

  return (
    <div className="wikipedia-page">
      <ContentNavigation article={article} />
      
      <div className="wikipedia-container">
        <div className="wikipedia-content">
          {/* Wikipedia summary section */}
          {article.data?.summary && (
            <div className="wiki-summary-box">
              <div className="summary-icon">ℹ️</div>
              <div className="summary-content">
                <h3>About this article</h3>
                <p>{article.data.summary}</p>
              </div>
            </div>
          )}

          {/* Main content */}
          <div className="wiki-article-body">
            <div className="content-text">
              {(article.data?.content || article.data?.full_text)?.split('\n\n').map((paragraph, idx) => (
                <p key={idx} className="wiki-paragraph">
                  {paragraph}
                </p>
              ))}
            </div>
          </div>

          {/* Metadata footer */}
          <div className="wiki-metadata">
            {article.data?.page_count && (
              <span className="meta-item">
                <strong>📄 Pages:</strong> {article.data.page_count}
              </span>
            )}
            {article.data?.language && (
              <span className="meta-item">
                <strong>🌐 Language:</strong> {article.data.language.toUpperCase()}
              </span>
            )}
            {article.data?.title && (
              <span className="meta-item">
                <strong>📚 Source:</strong> Wikipedia
              </span>
            )}
          </div>
        </div>

        {/* Sidebar for additional info */}
        <aside className="wikipedia-sidebar">
          <div className="sidebar-card">
            <h3>📖 Article Information</h3>
            <div className="info-grid">
              <div className="info-item">
                <span className="info-label">Title</span>
                <span className="info-value">{article.data?.title || article.data?.file_name}</span>
              </div>
              {article.data?.language && (
                <div className="info-item">
                  <span className="info-label">Language</span>
                  <span className="info-value">{article.data.language.toUpperCase()}</span>
                </div>
              )}
              <div className="info-item">
                <span className="info-label">Content Type</span>
                <span className="info-value">
                  {article.data?.content ? 'Wikipedia Article' : 'PDF Document'}
                </span>
              </div>
            </div>
          </div>

          <div className="sidebar-card">
            <h3>🔍 Quick Actions</h3>
            <button 
              className="sidebar-btn"
              onClick={() => navigate('/article/summary', { state: { article } })}
            >
              📝 View Summary
            </button>
            <button 
              className="sidebar-btn"
              onClick={() => navigate('/article/translation', { state: { article } })}
            >
              🌐 Translate Article
            </button>
          </div>
        </aside>
      </div>
    </div>
  );
};

export default WikipediaContent;
