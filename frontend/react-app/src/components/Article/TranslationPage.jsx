// Translation Page - translate content using Gemini
import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import ContentNavigation from '../Common/ContentNavigation';
import api from '../../services/auth';
import './TranslationPage.css';

const TranslationPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const article = location.state?.article;
  
  const [selectedLanguage, setSelectedLanguage] = useState('es');
  const [translatedText, setTranslatedText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const languages = [
    { code: 'es', name: 'Spanish', flag: '🇪🇸' },
    { code: 'fr', name: 'French', flag: '🇫🇷' },
    { code: 'de', name: 'German', flag: '🇩🇪' },
    { code: 'it', name: 'Italian', flag: '🇮🇹' },
    { code: 'pt', name: 'Portuguese', flag: '🇵🇹' },
    { code: 'ru', name: 'Russian', flag: '🇷🇺' },
    { code: 'ja', name: 'Japanese', flag: '🇯🇵' },
    { code: 'zh', name: 'Chinese', flag: '🇨🇳' },
    { code: 'ko', name: 'Korean', flag: '🇰🇷' },
    { code: 'ar', name: 'Arabic', flag: '🇸🇦' },
    { code: 'hi', name: 'Hindi', flag: '🇮🇳' },
    { code: 'tr', name: 'Turkish', flag: '🇹🇷' },
  ];

  if (!article) {
    navigate('/extract');
    return null;
  }

  const handleTranslate = async () => {
    setError('');
    setLoading(true);
    
    try {
      const textToTranslate = article.data?.ai_summary_medium || 
                             article.data?.summary || 
                             article.data?.content?.substring(0, 2000) || 
                             article.data?.full_text?.substring(0, 2000);

      if (!textToTranslate) {
        setError('No content available to translate');
        setLoading(false);
        return;
      }

      const response = await api.post('/api/v1/content/translate', {
        text: textToTranslate,
        target_language: languages.find(l => l.code === selectedLanguage)?.name || 'Spanish'
      });

      setTranslatedText(response.data.translated_text);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to translate content');
      console.error('Translation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getSourceText = () => {
    return article.data?.ai_summary_medium || 
           article.data?.summary || 
           article.data?.content?.substring(0, 2000) || 
           article.data?.full_text?.substring(0, 2000) ||
           '';
  };

  return (
    <div className="translation-page">
      <ContentNavigation article={article} />
      
      <div className="translation-container">
        <div className="translation-main">
          <div className="translation-header">
            <h2>🌐 AI Translation Service</h2>
            <p className="translation-subtitle">
              Powered by Google Gemini for accurate, contextual translations
            </p>
            <div className="powered-by">
              <span className="tech-badge">🔮 Powered by Gemini</span>
              <span className="model-badge">🚀 Gemini 1.5 Pro</span>
            </div>
          </div>

          {/* Language Selector */}
          <div className="language-selector-card">
            <h3>🗣️ Select Target Language</h3>
            <div className="languages-grid">
              {languages.map((lang) => (
                <button
                  key={lang.code}
                  className={`language-btn ${selectedLanguage === lang.code ? 'active' : ''}`}
                  onClick={() => setSelectedLanguage(lang.code)}
                >
                  <span className="flag">{lang.flag}</span>
                  <span className="lang-name">{lang.name}</span>
                </button>
              ))}
            </div>
            
            <button 
              className="translate-btn"
              onClick={handleTranslate}
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Translating...
                </>
              ) : (
                <>
                  🌐 Translate to {languages.find(l => l.code === selectedLanguage)?.name}
                </>
              )}
            </button>

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
          </div>

          {/* Translation Results */}
          <div className="translation-results">
            {/* Original Text */}
            <div className="text-panel original-text">
              <div className="panel-header">
                <h3>📄 Original Text</h3>
                <span className="lang-tag">English</span>
              </div>
              <div className="panel-content">
                <p>{getSourceText()}</p>
              </div>
            </div>

            {/* Translated Text */}
            {translatedText && (
              <div className="text-panel translated-text">
                <div className="panel-header">
                  <h3>✨ Translated Text</h3>
                  <span className="lang-tag">
                    {languages.find(l => l.code === selectedLanguage)?.flag}{' '}
                    {languages.find(l => l.code === selectedLanguage)?.name}
                  </span>
                </div>
                <div className="panel-content">
                  <p>{translatedText}</p>
                </div>
                <div className="panel-footer">
                  <button 
                    className="copy-btn"
                    onClick={() => {
                      navigator.clipboard.writeText(translatedText);
                      alert('Translation copied to clipboard!');
                    }}
                  >
                    📋 Copy Translation
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Translation Info */}
          <div className="translation-info">
            <h3>ℹ️ About This Translation</h3>
            <div className="info-grid">
              <div className="info-item">
                <span className="info-icon">🤖</span>
                <div className="info-content">
                  <h4>AI-Powered</h4>
                  <p>Uses Google Gemini's advanced language understanding</p>
                </div>
              </div>
              <div className="info-item">
                <span className="info-icon">🎯</span>
                <div className="info-content">
                  <h4>Context-Aware</h4>
                  <p>Maintains meaning and context in translation</p>
                </div>
              </div>
              <div className="info-item">
                <span className="info-icon">🌍</span>
                <div className="info-content">
                  <h4>Multi-Language</h4>
                  <p>Supports 12+ languages for global reach</p>
                </div>
              </div>
              <div className="info-item">
                <span className="info-icon">⚡</span>
                <div className="info-content">
                  <h4>Real-Time</h4>
                  <p>Fast and efficient translation processing</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <aside className="translation-sidebar">
          <div className="sidebar-card">
            <h3>📊 Translation Stats</h3>
            <div className="stat-item">
              <span className="stat-label">Source Language</span>
              <span className="stat-value">English</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Target Language</span>
              <span className="stat-value">
                {languages.find(l => l.code === selectedLanguage)?.name}
              </span>
            </div>
            <div className="stat-item">
              <span className="stat-label">AI Model</span>
              <span className="stat-value">Gemini 1.5 Pro</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Status</span>
              <span className="stat-value">
                {translatedText ? '✅ Complete' : '⏳ Ready'}
              </span>
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
              onClick={() => navigate('/article/summary', { state: { article } })}
            >
              📝 View Summaries
            </button>
          </div>
        </aside>
      </div>
    </div>
  );
};

export default TranslationPage;
