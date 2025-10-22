import React from 'react';
import './HomePage.css'; // Assuming a CSS file for HomePage styling

const HomePage = () => {
  return (
    <div className="home-page">
      <h1>Welcome to AI Data Analyst</h1>
      <p>Your intelligent partner for data analysis.</p>
      <div className="features">
        <div className="feature-card">
          <h2>Upload Data</h2>
          <p>Easily upload your datasets in various formats.</p>
        </div>
        <div className="feature-card">
          <h2>Analyze with AI</h2>
          <p>Leverage AI-powered tools to gain insights from your data.</p>
        </div>
        <div className="feature-card">
          <h2>Visualize Results</h2>
          <p>Interactive visualizations to understand your data better.</p>
        </div>
      </div>
    </div>
  );
};

export default HomePage;