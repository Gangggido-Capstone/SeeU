import React from "react";
import { useParams } from "react-router-dom";
import InitSeeso from "./InitSeeso";
import "../../css/VideoGazeTracker.css";

const VideoGazeTracker = () => {
    const { videoId } = useParams();

    return (
        <div className='video-player-wrapper'>
            <h4 className='page-title'>영상 재생페이지</h4>
            {/* 시선 추적을 위한 컴포넌트 */}
            <InitSeeso />

            {/* YouTube Iframe */}
            <iframe
                credentialless ='true'
                title='YouTube video player'
                src={`https://www.youtube.com/embed/${videoId}`}
                allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture'
                allowFullScreen
                loading='lazy'
                className='youtube-iframe'
            />

            <div className='back-button-container'>
                <a
                    href='/'
                    className='back-button'>
                    뒤로가기
                </a>
            </div>
        </div>
    );
};

export default VideoGazeTracker;
