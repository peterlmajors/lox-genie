/**
 * API service for connecting to Lox Genie FastAPI backend
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

/**
 * Send a message to the Lox Genie and get a response
 * 
 * @param {string} message - User message
 * @param {string|null} threadId - Optional thread ID for conversation continuity
 * @returns {Promise<{response: string, thread_id: string}>}
 */
export const sendMessage = async (message, threadId = null) => {
  // Create an AbortController for timeout handling
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 60000); // 60 second timeout

  try {
    const params = new URLSearchParams({
      message: message,
    });
    
    if (threadId) {
      params.append('thread_id', threadId);
    }

    console.log('Sending message to Lox Genie:', { message, threadId });

    const response = await fetch(`${API_BASE_URL}/genie?${params}`, {
      method: 'POST',
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    console.log('Response status:', response.status);
    console.log('Response ok:', response.ok);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error('Error response data:', errorData);
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('Response data received:', { 
      hasResponse: !!data.response, 
      threadId: data.thread_id,
      responseLength: data.response?.length 
    });

    return {
      response: data.response,
      thread_id: data.thread_id,
    };
  } catch (error) {
    clearTimeout(timeoutId);
    console.error('Error calling Lox Genie API:', error);
    console.error('Error name:', error.name);
    console.error('Error message:', error.message);
    
    // Handle abort/timeout errors
    if (error.name === 'AbortError') {
      throw new Error('Request timeout. The Lox Genie is taking too long to respond. Please try again.');
    }
    
    // Provide user-friendly error messages
    if (error.message.includes('Failed to fetch') || error.message.includes('network')) {
      throw new Error('Cannot connect to Lox Genie API. Make sure the API service is running.');
    } else if (error.message.includes('timeout')) {
      throw new Error('Request timeout. The agent is taking too long to respond. Please try again.');
    } else if (error.message.includes('500')) {
      throw new Error('The agent encountered an error. Please try rephrasing your question.');
    }
    
    throw error;
  }
};

/**
 * Check if the API is healthy
 * 
 * @returns {Promise<boolean>}
 */
export const checkHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
    });
    
    if (response.ok) {
      const data = await response.json();
      return data.status === 'healthy';
    }
    return false;
  } catch (error) {
    console.error('Health check failed:', error);
    return false;
  }
};

/**
 * Verify if a Sleeper username exists
 * 
 * @param {string} username - Sleeper username
 * @returns {Promise<{success: boolean, userData?: object, error?: string}>}
 */
export const verifySleeperUsername = async (username) => {
  try {
    const response = await fetch(`${API_BASE_URL}/users/${username}`, {
      method: 'GET',
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return {
        success: false,
        error: errorData.detail || `Username ${username} not found on Sleeper`,
      };
    }
    
    const userData = await response.json();
    return {
      success: true,
      userData,
    };
  } catch (error) {
    console.error('Error verifying username:', error);
    return {
      success: false,
      error: 'Failed to verify username. Please check your connection.',
    };
  }
};

/**
 * Fetch user avatar from Sleeper
 * 
 * @param {string} username - Sleeper username
 * @returns {Promise<string|null>} Avatar URL or null if not found
 */
export const fetchUserAvatar = async (username) => {
  try {
    const response = await fetch(`${API_BASE_URL}/users/avatar/${username}`, {
      method: 'GET',
    });
    
    if (!response.ok) {
      console.error(`Failed to fetch avatar for ${username}: ${response.status}`);
      return null;
    }
    
    // Check if the response is valid (not the error message)
    const contentType = response.headers.get('content-type');
    if (!contentType || !contentType.includes('image')) {
      console.error(`Invalid response for avatar ${username}`);
      return null;
    }
    
    // Create a blob URL from the response
    const blob = await response.blob();
    return URL.createObjectURL(blob);
  } catch (error) {
    console.error('Error fetching user avatar:', error);
    return null;
  }
};

/**
 * Generate a fantasy football question using AI
 * 
 * @returns {Promise<{question: string}>}
 */
export const generateWish = async () => {
  try {
      const response = await fetch(`${API_BASE_URL}/wish/generate`, {
      method: 'POST',
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return {
      question: data.question,
    };
  } catch (error) {
    console.error('Error generating wish:', error);
    
    // Provide user-friendly error messages
    if (error.message.includes('Failed to fetch') || error.message.includes('network')) {
      throw new Error('Cannot connect to Lox Genie API. Make sure the API service is running.');
    } else if (error.message.includes('500')) {
      throw new Error('Failed to generate wish. Please try again.');
    }
    
    throw error;
  }
};