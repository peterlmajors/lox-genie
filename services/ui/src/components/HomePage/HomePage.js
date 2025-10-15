import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';
import { 
  questionPlaceholder, 
  usernamePlaceholder,
  headerText,
  sleeperFeatureDescription,
  nflDataFeatureDescription,
  redditFeatureDescription
} from './placeholderText';
import NFLTicker from '../shared/NFLTicker';
import Footer from '../shared/Footer';
import { verifySleeperUsername, fetchUserAvatar, generateWish } from '../../services/api';
import { useUser } from '../../contexts/UserContext';

function HomePage() {
    const [question, setQuestion] = useState('');
    const [additionalInput, setAdditionalInput] = useState('');
    const [usernameError, setUsernameError] = useState('');
    const [isVerifying, setIsVerifying] = useState(false);
    const [isGeneratingWish, setIsGeneratingWish] = useState(false);
    const [isUsernameValid, setIsUsernameValid] = useState(false);
    const [isFadingOut, setIsFadingOut] = useState(false);
    const navigate = useNavigate();
    const { updateUser } = useUser();
    const messageTimeoutRef = useRef(null);
    const fadeTimeoutRef = useRef(null);
  
    // Auto-fade messages after 5 seconds
    useEffect(() => {
      // Clear existing timeouts
      if (messageTimeoutRef.current) {
        clearTimeout(messageTimeoutRef.current);
      }
      if (fadeTimeoutRef.current) {
        clearTimeout(fadeTimeoutRef.current);
      }

      // If there's an error or success message, start fade timer
      if (usernameError || isUsernameValid) {
        setIsFadingOut(false);
        
        // Start fade-out after 4.5 seconds
        messageTimeoutRef.current = setTimeout(() => {
          setIsFadingOut(true);
        }, 4500);

        // Clear message completely after 5 seconds
        fadeTimeoutRef.current = setTimeout(() => {
          setUsernameError('');
          setIsUsernameValid(false);
          setIsFadingOut(false);
        }, 5000);
      }

      // Cleanup on unmount
      return () => {
        if (messageTimeoutRef.current) {
          clearTimeout(messageTimeoutRef.current);
        }
        if (fadeTimeoutRef.current) {
          clearTimeout(fadeTimeoutRef.current);
        }
      };
    }, [usernameError, isUsernameValid]);

    // Handle submit
    const handleSubmit = async (e) => {
      e.preventDefault();
      if (!question.trim() || !additionalInput.trim()) {
        return;
      }

      // Verify username if not already valid
      if (!isUsernameValid) {
        const isValid = await handleVerifyUsername();
        if (!isValid) {
          return;
        }
      }

      setIsVerifying(true);

      // Fetch avatar with 10-second timeout
      let avatarUrl = null;
      try {
        const avatarPromise = fetchUserAvatar(additionalInput);
        const timeoutPromise = new Promise((resolve) => 
          setTimeout(() => resolve(null), 10000)
        );
        
        avatarUrl = await Promise.race([avatarPromise, timeoutPromise]);
      } catch (error) {
        console.error('Error fetching avatar:', error);
        // Continue with null avatar
      }

      setIsVerifying(false);

      // Navigate to the response page with the question, username, and avatar URL
      navigate('/response', { 
        state: { 
          question: question, 
          username: additionalInput,
          avatarUrl: avatarUrl 
        } 
      });
    };
  
    // Handle key press
    const handleKeyPress = (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSubmit(e);
      }
    };

    // Handle username change
    const handleUsernameChange = (e) => {
      setAdditionalInput(e.target.value);
      // Clear error and validation state when user starts typing
      if (usernameError) {
        setUsernameError('');
      }
      // Reset validation state when username changes
      setIsUsernameValid(false);
    };

    // Verify username
    const handleVerifyUsername = async () => {
      if (!additionalInput.trim()) {
        setUsernameError('Please enter a Sleeper username');
        return false;
      }

      setIsVerifying(true);
      setUsernameError('');

      const result = await verifySleeperUsername(additionalInput);

      setIsVerifying(false);

      if (!result.success) {
        setUsernameError(result.error);
        setIsUsernameValid(false);
        return false;
      }

      // Store user data in context
      updateUser(additionalInput, result.userData);
      setIsUsernameValid(true);
      return true;
    };

    // Handle generate wish
    const handleGenerateWish = async () => {
      // Check if username is valid first
      if (!isUsernameValid) {
        // Try to verify username first
        const isValid = await handleVerifyUsername();
        if (!isValid) {
          setUsernameError('Please enter a valid Sleeper username before generating a wish');
          return;
        }
      }

      setIsGeneratingWish(true);
      try {
        const result = await generateWish();
        setQuestion(result.question);
      } catch (error) {
        console.error('Error generating wish:', error);
        setUsernameError(error.message || 'Failed to generate wish. Please try again.');
      } finally {
        setIsGeneratingWish(false);
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
              <button 
                type="button"
                className="wish-button"
                onClick={handleGenerateWish}
                disabled={isGeneratingWish || !additionalInput.trim()}
                title={!additionalInput.trim() ? "Enter a Sleeper username first" : "Generate a random fantasy football question"}
              >
                <span className="button-text">
                  {isGeneratingWish ? 'Pondering...' : 'Generate Wish'}
                </span>
                <span className="button-icon">🎲</span>
              </button>
              <div className="username-input-wrapper">
                <input
                  type="text"
                  className={`sleeper-username ${usernameError ? 'error' : ''} ${isUsernameValid && !usernameError ? 'valid' : ''}`}
                  placeholder={usernamePlaceholder}
                  value={additionalInput}
                  onChange={handleUsernameChange}
                />
                {usernameError && (
                  <div className={`username-error ${isFadingOut ? 'fade-out' : ''}`}>{usernameError}</div>
                )}
                {isUsernameValid && !usernameError && (
                  <div className={`username-success ${isFadingOut ? 'fade-out' : ''}`}>✓ Username verified</div>
                )}
              </div>
              <button 
                type="submit" 
                className="genie-button"
                disabled={!question.trim() || !additionalInput.trim() || isVerifying}
              >
                <span className="button-text">
                  {isVerifying ? 'Loading...' : 'Ask the Genie'}
                </span>
                <span className="button-icon">✨</span>
              </button>
            </div>
          </form>
          
          <div className="genie-features">
            <div className="feature">
              <span className="feature-icon">
                <img src="/sleeper-transparent-logo.png" alt="Sleeper Logo" className="sleeper-logo-icon"/>
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
                <img src="/reddit-transparent-logo.png" alt="Reddit Logo" className="reddit-logo" />
              </span>
              <span className="feature-description">{redditFeatureDescription}</span>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}
  
export default HomePage;