import React from 'react';

const Terms = () => {
  return (
    <div className="container">
      <h1>Terms of Use</h1>
      <div style={{ 
        padding: '20px', 
        backgroundColor: '#f4f4f4', 
        border: '1px solid #ccc',
        marginTop: '20px',
        lineHeight: '1.6'
      }}>
        This application does not save your PPT after use--it is deleted immediately after creating the text file. 
        Text files are only available to the person who uploads them. They are also deleted after use.
      </div>
    </div>
  );
};

export default Terms; 