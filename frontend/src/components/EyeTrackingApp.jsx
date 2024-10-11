import React from "react";
import { Route, Routes } from "react-router-dom";
import MainPage from "./MainPage";
import VideoGazeTracker from "./VideoGazeTracker";
import InitSeeso from "./InitSeeso";
import SettingsPage from "./SettingsPage";
import RecordPage from "./RecordPage";

const EyeTrackingApp = () => {
    return (
        <Routes>
            <Route path='/' element={<MainPage />} />
            <Route path='/play-video/:videoId' element={<VideoGazeTracker />} />
            <Route path='/seeso' element={<InitSeeso />} />
            <Route path='/youtube' element={<VideoGazeTracker />} />
            <Route path='/settings' element={<SettingsPage />} />
            <Route path='/Records' element={<RecordPage />} />
        </Routes>
    );
};

export default EyeTrackingApp;
