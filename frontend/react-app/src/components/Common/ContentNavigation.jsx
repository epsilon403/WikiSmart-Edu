// Navigation bar for switching between Wikipedia content, Summary, and Translation pages
import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import './ContentNavigation.css';

const ContentNavigation = ({ article }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { logout, user } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const currentPath = location.pathname;

  return (
    <div className="content-navigation">
      <nav className="top-nav">
        <div className="nav-content">
          <h1 onClick={() => navigate('/extract')} style={{ cursor: 'pointer' }}>
            📚 WikiSmart-Edu
          </h1>
          <div className="nav-right">
            <span className="user-name">Welcome, {user?.username}!</span>
            <button onClick={handleLogout} className="logout-btn">Logout</button>
          </div>
        </div>
      </nav>

      <div className="article-title-bar">
        <h1 className="article-main-title">
          {article?.data?.title || article?.data?.file_name || 'Article'}
        </h1>
        <button onClick={() => navigate('/extract')} className="back-btn">
          ← Back to Extract
        </button>
      </div>

      <div className="tabs-navigation">
        <button
          className={`nav-tab ${currentPath === '/article/content' ? 'active' : ''}`}
          onClick={() => navigate('/article/content', { state: { article } })}
        >
          📖 Wikipedia Content
        </button>
        <button
          className={`nav-tab ${currentPath === '/article/summary' ? 'active' : ''}`}
          onClick={() => navigate('/article/summary', { state: { article } })}
        >
          📝 Summary (Groq)
        </button>
        <button
          className={`nav-tab ${currentPath === '/article/translation' ? 'active' : ''}`}
          onClick={() => navigate('/article/translation', { state: { article } })}
        >
          🌐 Translation (Gemini)
        </button>
      </div>
    </div>
  );
};

export default ContentNavigation;
