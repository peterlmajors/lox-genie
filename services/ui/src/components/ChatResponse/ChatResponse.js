import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useLocation } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import './ChatResponse.css';
import { generateResponse } from '../../services/gemini';
import NFLTicker from '../shared/NFLTicker';
import Footer from '../shared/Footer';
import { Avatar } from '@mui/material';
import PersonIcon from '@mui/icons-material/Person';

function ChatResponse() {
  const location = useLocation();
  const initialQuestion = location.state?.question || '';
  const [currentMessage, setCurrentMessage] = useState('');
  const [conversationHistory, setConversationHistory] = useState([]);
  const [shimmerDuration, setShimmerDuration] = useState(15);
  const [isLoading, setIsLoading] = useState(false);
  const [initialResponse, setInitialResponse] = useState('');
  const chatContainerRef = useRef(null);

  const generateInitialResponse = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await generateResponse(initialQuestion);
      setInitialResponse(response);
    } catch (error) {
      setInitialResponse("I'm sorry, I couldn't generate a response at the moment. Please try again.");
    } finally {
      setIsLoading(false);
    }
  }, [initialQuestion]);

  // Generate random shimmer duration on component mount
  useEffect(() => {
    const randomDuration = Math.floor(Math.random() * (20 - 10 + 1)) + 10; // Random between 10-20 seconds
    setShimmerDuration(randomDuration);
  }, []);

  // Generate initial response when component mounts
  useEffect(() => {
    if (initialQuestion) {
      generateInitialResponse();
    }
  }, [generateInitialResponse]);

  // Auto-scroll to bottom when new responses are added
  useEffect(() => {
    // Scroll to bottom of the page when new conversations are added
    window.scrollTo({
      top: document.body.scrollHeight,
      behavior: 'smooth'
    });
  }, [conversationHistory, initialResponse]);

  const handleAskAnotherQuestion = async () => {
    if (currentMessage.trim() && !isLoading) {
      setIsLoading(true);
      try {
        const response = await generateResponse(currentMessage, conversationHistory);
        
        const newConversation = {
          question: currentMessage,
          response: response
        };
        
        setConversationHistory(prev => [...prev, newConversation]);
        setCurrentMessage('');
      } catch (error) {
        const newConversation = {
          question: currentMessage,
          response: "I'm sorry, I couldn't generate a response at the moment. Please try again."
        };
        setConversationHistory(prev => [...prev, newConversation]);
        setCurrentMessage('');
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAskAnotherQuestion();
    }
  };

  return (
    <div className="App">
      <NFLTicker/>
      <div className="chat-page-container" ref={chatContainerRef}>
        <div className="genie-content">
          
          <div className="response-container">
            {initialQuestion && (
              <div className="question-display">
                <div className="question-header">
                  <Avatar sx={{ bgcolor: 'rgba(255, 255, 255, 0.1)', width: 40, height: 40, mr: 2 }}>
                    <PersonIcon sx={{ color: 'rgba(255, 255, 255, 0.7)' }} />
                  </Avatar>
                </div>
                <p className="question-text">{initialQuestion}</p>
              </div>
            )}
            
            <div className="genie-response" style={{ '--shimmer-duration': `${shimmerDuration}s` }}>
              <div className="response-header">
                <img src="/logo512.png" alt="Lox Genie Logo" className="genie-logo-icon" />
              </div>
              <div className="response-content">
                {isLoading && !initialResponse ? (
                  <div className="loading-indicator">
                    <span> Lox Genie is thinking...</span>
                  </div>
                ) : (
                  <ReactMarkdown>{initialResponse}</ReactMarkdown>
                )}
              </div>
            </div>
          </div>

          {/* Conversation History */}
          {conversationHistory.map((conversation, index) => (
            <div key={index} className="conversation-item">
              <div className="question-display">
                <div className="question-header">
                  <Avatar sx={{ bgcolor: 'rgba(255, 255, 255, 0.1)', width: 40, height: 40, mr: 2 }}>
                    <PersonIcon sx={{ color: 'rgba(255, 255, 255, 0.7)' }} />
                  </Avatar>
                </div>
                <p className="question-text">{conversation.question}</p>
              </div>
              
              <div className="genie-response" style={{ '--shimmer-duration': `${shimmerDuration}s` }}>
                <div className="response-header">
                  <img src="/logo512.png" alt="Lox Genie Logo" className="genie-logo-icon" />
                </div>
                <div className="response-content">
                  <ReactMarkdown>{conversation.response}</ReactMarkdown>
                </div>
              </div>
            </div>
          ))}

          {/* Text Box with Ask Another Question Button */}
          <div className="simple-chat-container">
            <div className="simple-input-container">
              <input
                type="text"
                className="simple-chat-input"
                value={currentMessage}
                onChange={(e) => setCurrentMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={isLoading}
              />
              <button 
                onClick={handleAskAnotherQuestion}
                className="genie-button compact-button"
                disabled={!currentMessage.trim() || isLoading}
              >
                <span className="button-text">
                  {isLoading ? 'Thinking...' : 'Follow Up'}
                </span>
                <span className="button-icon">✨</span>
              </button>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default ChatResponse;