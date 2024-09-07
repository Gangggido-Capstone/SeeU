import "./App.css";
import EyeTrackingApp from "./components/EyeTrackingApp.jsx";
import React from "react";

function App() {
    return (
        <div className='App'>
            <img src="/eye_logo.gif" alt="Logo" className="logo" />
            <EyeTrackingApp />
        </div>
    );
}

export default App;
