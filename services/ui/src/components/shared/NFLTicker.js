import React from 'react';
import { nflStories } from '../../assets/nflStories';
import './NFLTicker.css';

const NFLTicker = () => {
  // Create a continuous string of all stories with separators
  const createTickerContent = () => {
    return nflStories.map((story, index) => (
      <React.Fragment key={index}>
        <span className="ticker-story">{story}</span>
        <span className="ticker-separator">***</span>
      </React.Fragment>
    ));
  };

  return (
    <div className="nfl-ticker-container">
      <div className="ticker-label">
        NFL NEWS
      </div>
      <div className="ticker-content ticker-content-with-label">
        <div className="ticker-scroll-wrapper">
          <div className="ticker-scroll">
            {/* Render stories twice for seamless loop */}
            {createTickerContent()}
            {createTickerContent()}
          </div>
        </div>
      </div>
    </div>
  );
};

export default NFLTicker;
