import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import MainPage from "./MainPage";
import VideoGazeTracker from "./VideoGazeTracker";
import SettingsPage from "./SettingsPage";
import RecordPage from "./RecordPage";

const EyeTrackingApp = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path='/' element={<MainPage />} />
                <Route path='/play-video/:videoId' element={<VideoGazeTracker />}/>
                <Route path='/youtube' element={<VideoGazeTracker />} />
                <Route path='/settings' element={<SettingsPage />} />
                <Route path='/Records' element={<RecordPage />} />
            </Routes>
        </BrowserRouter>
    );
};

export default EyeTrackingApp;
