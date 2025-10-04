import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './components/HomePage';
import ChatResponse from './components/ChatResponse';



function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/response" element={<ChatResponse />} />
      </Routes>
    </Router>
  );
}

export default App;
