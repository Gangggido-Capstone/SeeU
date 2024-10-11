import React from "react";
import EyeTrackingApp from "./components/EyeTrackingApp.jsx";
import "./App.css";
import { BrowserRouter } from "react-router-dom";

function App() {
    return (
        <BrowserRouter> {}
            <div className='App'>
                <EyeTrackingApp />
            </div>
        </BrowserRouter>
    );
}

export default App;
