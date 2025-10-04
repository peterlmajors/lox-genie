import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';
import { 
  questionPlaceholder, 
  usernamePlaceholder,
  headerText,
  sleeperFeatureDescription,
  nflDataFeatureDescription,
  xApiFeatureDescription
} from './placeholderText';
import NFLTicker from '../shared/NFLTicker';
import Footer from '../shared/Footer';

function HomePage() {
    const [question, setQuestion] = useState('');
    const [additionalInput, setAdditionalInput] = useState('');
    const navigate = useNavigate();
  
    const handleSubmit = (e) => {
      e.preventDefault();
      if (question.trim() && additionalInput.trim()) {
        // Navigate to the response page with the question
        navigate('/response', { state: { question: question } });
      }
    };
  
    const handleKeyPress = (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        if (question.trim()) {
          // Navigate to the response page with the question
          navigate('/response', { state: { question: question } });
        }
      }
    };
  
  return (
    <div className="App">
      <NFLTicker />
      <div className="home-container">
        <div className="genie-content">
          <div className="genie-header">
            <h1 className="genie-title">
              <img src="/logo512.png" alt="Lox Genie Logo" className="genie-logo" />
              <a href="/" className="genie-title-link">Lox Genie</a>
            </h1>
            <p className="genie-subtitle">{headerText}</p>
          </div>
          
          <form onSubmit={handleSubmit} className="question-form">
            <div className="input-container">
              <textarea
                className="home-input question-textarea"
                placeholder={questionPlaceholder}
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                rows={8}
                onKeyPress={handleKeyPress}
              />
            </div>
            
            <div className="button-container">
              <input
                type="text"
                className="sleeper-username"
                placeholder={usernamePlaceholder}
                value={additionalInput}
                onChange={(e) => setAdditionalInput(e.target.value)}
              />
              <button 
                type="submit" 
                className="genie-button"
                disabled={!question.trim() || !additionalInput.trim()}
              >
                <span className="button-text">Ask the Genie</span>
                <span className="button-icon">✨</span>
              </button>
            </div>
          </form>
          
          <div className="genie-features">
            <div className="feature">
              <span className="feature-icon">
                <img src="/sleeper-transparent-logo.png" alt="Sleeper Logo" className="sleeper-logo-icon" />
              </span>
              <span className="feature-description">{sleeperFeatureDescription}</span>
            </div>
            <div className="feature">
              <span className="feature-icon">
                <img src="/football-emoji-transparent.png" alt="Football" className="football-icon" />
              </span>
              <span className="feature-description">{nflDataFeatureDescription}</span>
            </div>
            <div className="feature">
              <span className="feature-icon">
                <img src="/x-light-grey-logo.png" alt="X Logo" className="x-logo-icon" />
              </span>
              <span className="feature-description">{xApiFeatureDescription}</span>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}
  
export default HomePage;