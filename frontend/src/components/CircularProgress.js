import React from "react";
import "../../css/CircularProgress.css";

const CircularProgress = ({ score }) => {
  const percentage = parseFloat(score).toFixed(2);

  return (
    <div className="circular-progress" style={{ "--progress": percentage }}>
      <span className="percentage">{percentage}%</span>
    </div>
  );
};

export default CircularProgress;
