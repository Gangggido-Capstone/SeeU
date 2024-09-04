import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import MainPage from "./MainPage";
import VideoPlayerWrapper from "./VideoPlayerWrapper";
import InitSeeso from "./InitSeeso";

const EyeTrackingApp = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path='/' element={<MainPage />} />
                <Route
                    path='/play-video/:videoId'
                    element={<VideoPlayerWrapper />}
                />
                <Route path='/seeso' element={<InitSeeso />} />
                <Route path='/youtube' element={<VideoPlayerWrapper />} />
            </Routes>
        </BrowserRouter>
    );
};

export default EyeTrackingApp;
