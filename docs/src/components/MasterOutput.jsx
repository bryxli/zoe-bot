import React from "react";

const MasterOutput = () => {
    const test = ["a","b","c"]
    const value = test[Math.floor(Math.random() * test.length)];
  return (
    <div>
    <p>{value}</p>
    </div>
  );
};

export default MasterOutput;
