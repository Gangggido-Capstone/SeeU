import React from "react";
import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";
import MainPage from "./components/MainPage";
import EyeTrackingApp from "./components/EyeTrackingApp";
import SettingsPage from "./components/SettingsPage";
import "./App.css";

const App = () => {
    return (
        <Router>
            <div className="App">
                <DisplayLogo />
                <Routes>
                    <Route path="/" element={<MainPage />} />
                    <Route path="/eye-tracking" element={<EyeTrackingApp />} />
                    <Route path="/settings" element={<SettingsPage />} />
                </Routes>
            </div>
        </Router>
    );
};

// 로고 메인 페이지만
const DisplayLogo = () => {
    const location = useLocation();
    const isMainPage = location.pathname === '/';

    return (
        <>
            {isMainPage && <img src="/eye_logo.gif" alt="Logo" className="logo" />}
        </>
    );
};

export default App;
