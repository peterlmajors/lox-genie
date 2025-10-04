import React, { useState, useEffect } from 'react';
import { nflStories } from '../../assets/nflStories';
import './NFLTicker.css';

const NFLTicker = () => {
  const [displayedStories, setDisplayedStories] = useState([]);
  const [isTransitioning, setIsTransitioning] = useState(false);

  // Function to get random stories
  const getRandomStories = () => {
    const shuffled = [...nflStories].sort(() => 0.5 - Math.random());
    return shuffled.slice(0, 3);
  };

  useEffect(() => {
    // Set initial random stories
    setDisplayedStories(getRandomStories());

    // Update stories randomly every 6-12 seconds
    const updateStories = () => {
      setIsTransitioning(true);
      
      // Fade out, then fade in with new stories
      setTimeout(() => {
        setDisplayedStories(getRandomStories());
        setIsTransitioning(false);
      }, 300); // Half of the total transition time
      
      const nextUpdate = Math.random() * 6000 + 6000; // 6-12 seconds
      setTimeout(updateStories, nextUpdate);
    };

    const timer = setTimeout(updateStories, Math.random() * 6000 + 6000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="nfl-ticker-container">
      <div className="ticker-content">
        <div className={`ticker-text ${isTransitioning ? 'fade-out' : 'fade-in'}`}>
          {displayedStories.map((story, index) => (
            <span key={`${story}-${index}`} className="ticker-story">
              {story}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
};

export default NFLTicker;