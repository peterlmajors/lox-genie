import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useLocation } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import './ChatResponse.css';

import { sendMessage, fetchUserAvatar } from '../../services/api';
import NFLTicker from '../shared/NFLTicker';
import Footer from '../shared/Footer';
import { Avatar } from '@mui/material';
import PersonIcon from '@mui/icons-material/Person';

function ChatResponse() {
  const location = useLocation();
  const initialQuestion = location.state?.question || '';
  const username = location.state?.username || '';
  const preloadedAvatarUrl = location.state?.avatarUrl || null;
  const [currentMessage, setCurrentMessage] = useState('');
  const [conversationHistory, setConversationHistory] = useState([]);
  const [shimmerDuration, setShimmerDuration] = useState(15);
  const [isLoading, setIsLoading] = useState(false);
  const [initialResponse, setInitialResponse] = useState('');
  const [threadId, setThreadId] = useState(null);
  const [userAvatarUrl, setUserAvatarUrl] = useState(preloadedAvatarUrl);
  const chatContainerRef = useRef(null);

  const generateInitialResponse = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await sendMessage(initialQuestion, null);
      setInitialResponse(data.response);
      setThreadId(data.thread_id);
    } catch (error) {
      console.error('Error generating response:', error);
      setInitialResponse("I'm sorry, I couldn't generate a response at the moment. Please try again.");
    } finally {
      setIsLoading(false);
    }
  }, [initialQuestion]);

  // Fetch user avatar on component mount (only if not preloaded)
  useEffect(() => {
    // If avatar was preloaded, skip fetching
    if (preloadedAvatarUrl) {
      console.log('Using preloaded avatar URL');
      return;
    }
    
    if (!username) {
      console.log('No username provided for avatar fetch');
      return;
    }
    
    console.log('Fetching avatar for username:', username);
    
    const loadUserAvatar = async () => {
      const avatarUrl = await fetchUserAvatar(username);
      console.log('Avatar URL received:', avatarUrl);
      if (avatarUrl) {
        setUserAvatarUrl(avatarUrl);
      }
    };
    
    loadUserAvatar();
    
    // Cleanup: revoke blob URL on unmount to prevent memory leaks
    return () => {
      if (userAvatarUrl) {
        URL.revokeObjectURL(userAvatarUrl);
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [username, preloadedAvatarUrl]);

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
  }, [initialQuestion, generateInitialResponse]);

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
      const questionToAsk = currentMessage;
      setCurrentMessage('');
      
      // Add question to conversation history immediately with loading state
      const newConversation = {
        question: questionToAsk,
        response: null, // null indicates loading
        isLoading: true
      };
      setConversationHistory(prev => [...prev, newConversation]);
      setIsLoading(true);
      
      try {
        const data = await sendMessage(questionToAsk, threadId);
        
        // Update the last conversation with the response
        setConversationHistory(prev => {
          const updated = [...prev];
          updated[updated.length - 1] = {
            question: questionToAsk,
            response: data.response,
            isLoading: false
          };
          return updated;
        });
        setThreadId(data.thread_id);
      } catch (error) {
        console.error('Error generating response:', error);
        // Update the last conversation with error message
        setConversationHistory(prev => {
          const updated = [...prev];
          updated[updated.length - 1] = {
            question: questionToAsk,
            response: `Error: ${error.message || "I'm sorry, I couldn't generate a response at the moment. Please try again."}`,
            isLoading: false
          };
          return updated;
        });
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
                  {userAvatarUrl ? (
                    <Avatar src={userAvatarUrl} sx={{ width: 40, height: 40, mr: 2 }} />
                  ) : (
                    <Avatar sx={{ bgcolor: 'rgba(255, 255, 255, 0.1)', width: 40, height: 40, mr: 2 }}>
                      <PersonIcon sx={{ color: 'rgba(255, 255, 255, 0.7)' }} />
                    </Avatar>
                  )}
                  <span className="username-display">{username}</span>
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
                  {userAvatarUrl ? (
                    <Avatar src={userAvatarUrl} sx={{ width: 40, height: 40, mr: 2 }} />
                  ) : (
                    <Avatar sx={{ bgcolor: 'rgba(255, 255, 255, 0.1)', width: 40, height: 40, mr: 2 }}>
                      <PersonIcon sx={{ color: 'rgba(255, 255, 255, 0.7)' }} />
                    </Avatar>
                  )}
                  <span className="username-display">{username}</span>
                </div>
                <p className="question-text">{conversation.question}</p>
              </div>
              
              <div className="genie-response" style={{ '--shimmer-duration': `${shimmerDuration}s` }}>
                <div className="response-header">
                  <img src="/logo512.png" alt="Lox Genie Logo" className="genie-logo-icon" />
                </div>
                <div className="response-content">
                  {conversation.isLoading ? (
                    <div className="loading-indicator">
                      <span> Lox Genie is thinking...</span>
                    </div>
                  ) : (
                    <ReactMarkdown>{conversation.response}</ReactMarkdown>
                  )}
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