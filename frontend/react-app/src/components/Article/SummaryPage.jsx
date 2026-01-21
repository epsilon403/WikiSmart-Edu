// Summary Page - displays Groq-generated summaries
import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import ContentNavigation from '../Common/ContentNavigation';
import './SummaryPage.css';

const SummaryPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const article = location.state?.article;

  if (!article) {
    navigate('/extract');
    return null;
  }

  const hasShortSummary = article.data?.ai_summary_short;
  const hasMediumSummary = article.data?.ai_summary_medium;

  return (
    <div className="summary-page">
      <ContentNavigation article={article} />
      
      <div className="summary-container">
        <div className="summary-main">
          <div className="summary-header">
            <h2>🤖 AI-Powered Summaries</h2>
            <p className="summary-subtitle">
              Intelligent summaries generated using Groq's high-performance LLM
            </p>
            <div className="powered-by">
              <span className="tech-badge">⚡ Powered by Groq</span>
              <span className="model-badge">🧠 Llama 3.1 8B Instant</span>
            </div>
          </div>

          {!hasShortSummary && !hasMediumSummary && (
            <div className="no-summary-message">
              <div className="empty-icon">📝</div>
              <h3>No summaries available</h3>
              <p>Summaries were not generated for this article.</p>
            </div>
          )}

          {/* Short Summary - Key Points */}
          {hasShortSummary && (
            <div className="summary-card short-summary">
              <div className="summary-card-header">
                <div className="header-left">
                  <span className="summary-icon">🎯</span>
                  <h3>Key Points Summary</h3>
                </div>
                <span className="summary-type-badge">Quick Overview</span>
              </div>
              <div className="summary-card-body">
                <div className="summary-description">
                  Concise bullet points highlighting the most important facts and concepts.
                </div>
                <div className="summary-content">
                  <pre className="bullet-list">{article.data.ai_summary_short}</pre>
                </div>
              </div>
              <div className="summary-card-footer">
                <span className="footer-info">
                  ⏱️ Quick read • Perfect for getting the gist
                </span>
              </div>
            </div>
          )}

          {/* Medium Summary - Detailed */}
          {hasMediumSummary && (
            <div className="summary-card medium-summary">
              <div className="summary-card-header">
                <div className="header-left">
                  <span className="summary-icon">📚</span>
                  <h3>Detailed Summary</h3>
                </div>
                <span className="summary-type-badge">In-Depth</span>
              </div>
              <div className="summary-card-body">
                <div className="summary-description">
                  Comprehensive summary covering main history, key concepts, and significant details.
                </div>
                <div className="summary-content">
                  <div className="paragraph-content">
                    {article.data.ai_summary_medium}
                  </div>
                </div>
              </div>
              <div className="summary-card-footer">
                <span className="footer-info">
                  📖 Medium read • Comprehensive understanding
                </span>
              </div>
            </div>
          )}

          {/* Features info */}
          <div className="summary-features">
            <h3>✨ Summary Features</h3>
            <div className="features-grid">
              <div className="feature-item">
                <span className="feature-icon">🎯</span>
                <div className="feature-content">
                  <h4>Focused Content</h4>
                  <p>Only the most relevant information extracted</p>
                </div>
              </div>
              <div className="feature-item">
                <span className="feature-icon">⚡</span>
                <div className="feature-content">
                  <h4>Lightning Fast</h4>
                  <p>Powered by Groq's ultra-fast inference</p>
                </div>
              </div>
              <div className="feature-item">
                <span className="feature-icon">🧠</span>
                <div className="feature-content">
                  <h4>AI Understanding</h4>
                  <p>Deep comprehension using advanced LLM</p>
                </div>
              </div>
              <div className="feature-item">
                <span className="feature-icon">📝</span>
                <div className="feature-content">
                  <h4>Clear & Concise</h4>
                  <p>Easy to understand explanations</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <aside className="summary-sidebar">
          <div className="sidebar-card">
            <h3>📊 Summary Info</h3>
            <div className="info-stats">
              <div className="stat-item">
                <span className="stat-label">Summaries Generated</span>
                <span className="stat-value">
                  {(hasShortSummary ? 1 : 0) + (hasMediumSummary ? 1 : 0)}
                </span>
              </div>
              <div className="stat-item">
                <span className="stat-label">AI Model</span>
                <span className="stat-value">Llama 3.1</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Provider</span>
                <span className="stat-value">Groq</span>
              </div>
            </div>
          </div>

          <div className="sidebar-card">
            <h3>🔍 Quick Navigation</h3>
            <button 
              className="sidebar-btn"
              onClick={() => navigate('/article/content', { state: { article } })}
            >
              📖 View Full Content
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

export default SummaryPage;
