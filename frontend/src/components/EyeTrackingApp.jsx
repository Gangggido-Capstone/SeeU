import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import MainPage from "./MainPage";
import VideoGazeTracker from "./VideoGazeTracker";
import InitSeeso from "./InitSeeso";
import SettingsPage from "./SettingsPage";
import RecordPage from "./RecordPagePage";

const EyeTrackingApp = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path='/' element={<MainPage />} />
                <Route
                    path='/play-video/:videoId'
                    element={<VideoGazeTracker />}
                />
                <Route path='/seeso' element={<InitSeeso />} />
                <Route path='/youtube' element={<VideoGazeTracker />} />
                <Route path='/settings' element={<SettingsPage />} />{" "}
                {/* SettingsPage 추가 */}
                <Route path='/record' element={<RecordPage />} />{" "}
                {/* RecordPagePage 추가 */}
            </Routes>
        </BrowserRouter>
    );
};

export default EyeTrackingApp;
