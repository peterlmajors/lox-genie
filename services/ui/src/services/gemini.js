import { GoogleGenAI } from "@google/genai";
import { systemPromptTemplate } from "./systemPrompt.js";

export const generateResponse = async (question, conversationHistory = []) => {
  try {
    // Build the conversation context
    let prompt = systemPromptTemplate.replace('{question}', question);

    // Add conversation history for context if available
    if (conversationHistory.length > 0) {
      prompt += `\n\nPrevious conversation context:`;
      conversationHistory.forEach((conv, index) => {
        prompt += `\nQ${index + 1}: ${conv.question}\nA${index + 1}: ${conv.response}`;
      });
    }

    

    return "Hello, world!";
  } catch (error) {
    console.error('Error generating response:', error);
    
    // Check for specific error types
    if (error.message && error.message.includes('API_KEY')) {
      return "API key error. Please check your Gemini API key configuration.";
    } else if (error.message && error.message.includes('quota')) {
      return "API quota exceeded. Please check your Gemini API usage limits.";
    } else if (error.message && error.message.includes('network')) {
      return "Network error. Please check your internet connection and try again.";
    } else if (error.message && error.message.includes('timeout')) {
      return "Request timeout. The API is taking too long to respond. Please try again.";
    }
    
    return "I'm experiencing technical difficulties. Please try again in a moment.";
  }
};
