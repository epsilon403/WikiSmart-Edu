// Main App component
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, AuthContext } from './context/AuthContext';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import ArticleExtraction from './components/Article/ArticleExtraction';
import ArticleDisplay from './components/Article/ArticleDisplay';
import WikipediaContent from './components/Article/WikipediaContent';
import SummaryPage from './components/Article/SummaryPage';
import TranslationPage from './components/Article/TranslationPage';
import './App.css';

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = React.useContext(AuthContext);
  
  if (loading) {
    return <div>Loading...</div>;
  }
  
  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route 
            path="/extract" 
            element={
              <ProtectedRoute>
                <ArticleExtraction />
              </ProtectedRoute>
            } 
          />
          {/* New organized routes */}
          <Route 
            path="/article/content" 
            element={
              <ProtectedRoute>
                <WikipediaContent />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/article/summary" 
            element={
              <ProtectedRoute>
                <SummaryPage />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/article/translation" 
            element={
              <ProtectedRoute>
                <TranslationPage />
              </ProtectedRoute>
            } 
          />
          {/* Legacy route for backward compatibility */}
          <Route 
            path="/article-display" 
            element={
              <ProtectedRoute>
                <ArticleDisplay />
              </ProtectedRoute>
            } 
          />
          <Route path="/" element={<Navigate to="/extract" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;

