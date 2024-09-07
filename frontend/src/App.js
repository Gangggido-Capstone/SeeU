import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import MainPage from "./components/MainPage";
import EyeTrackingApp from "./components/EyeTrackingApp";
import SettingsPage from "./components/SettingsPage"; // SettingsPage 추가
import "./App.css"; // 스타일 파일

function App() {
    return (
        <Router>
            <div className="App">
                <img src="/eye_logo.gif" alt="Logo" className="logo" />
                <Routes>
                    <Route path="/" element={<MainPage />} /> {/* 메인 페이지 */}
                    <Route path="/eye-tracking" element={<EyeTrackingApp />} /> {/* EyeTrackingApp 페이지 */}
                    <Route path="/settings" element={<SettingsPage />} /> {/* SettingsPage 추가 */}
                </Routes>
            </div>
        </Router>
    );
}

export default App;
