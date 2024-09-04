// import React from "react";
// import { useParams } from "react-router-dom";
// import "../../css/VideoPlayerWrapper.css";
// const VideoPlayerWrapper = () => {
//     const { videoId } = useParams();

//     return (
//         <div className='video-player-container'>
//             <h1 className='page-title'>영상 재생 및 시선 추적 페이지</h1>
//             {/* 시선 추적을 위한 컴포넌트
//             <InitSeeso /> */}

//             {/* Seeso Iframe */}
//             <iframe
//                 title='Seeso Tracker'
//                 src='/seeso'
//                 sandbox='allow-scripts allow-same-origin use-credentials'
//                 style={{
//                     width: "100%",
//                     height: "100%",
//                     border: "none",
//                     position: "absolute",
//                     top: 0,
//                     left: 0,
//                     zIndex: 999,
//                 }}></iframe>

//             {/* YouTube Iframe */}
//             <iframe
//                 title='YouTube video player'
//                 src={`https://www.youtube.com/embed/${videoId}`}
//                 frameborder='0'
//                 allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture'
//                 allowFullScreen
//                 loading='lazy'
//                 style={{
//                     position: "relative",
//                     width: "100%",
//                     height: "50vh",
//                     border: "none",
//                 }}
//             />

//             <div className='back-button-container'>
//                 <a href='/' className='back-button'>
//                     뒤로가기
//                 </a>
//             </div>
//         </div>
//     );
// };

// export default VideoPlayerWrapper;

// import React from "react";
// import { useParams } from "react-router-dom";
// import "../../css/VideoPlayerWrapper.css";

// const VideoPlayerWrapper = () => {
//     const { videoId } = useParams();

//     return (
//         <div className='video-player-container'>
//             <h4 className='page-title'>영상 재생 및 시선 추적 페이지</h4>

//             {/* Seeso Iframe */}
//             <iframe
//                 title='Seeso Tracker'
//                 src='/seeso'
//                 sandbox='allow-scripts allow-same-origin use-credentials'
//                 style={{
//                     width: "100vw",
//                     height: "100vh",
//                     border: "none",
//                     position: "absolute",
//                     top: 0,
//                     left: 0,
//                     zIndex: 1,
//                 }}></iframe>

//             {/* YouTube Iframe */}
//             <iframe
//                 title='YouTube video player'
//                 src={`https://www.youtube.com/embed/${videoId}`}
//                 frameborder='0'
//                 allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture'
//                 allowFullScreen
//                 loading='lazy'
//                 style={{
//                     position: "absolute",
//                     width: "50vw",
//                     height: "50vh",
//                     top: "25vh",
//                     left: "25vw",
//                     border: "none",
//                     zIndex: 2,
//                 }}
//             />

//             <div className='back-button-container'>
//                 <a href='/' className='back-button'>
//                     뒤로가기
//                 </a>
//             </div>
//         </div>
//     );
// };

// export default VideoPlayerWrapper;

import React from "react";
import { useParams } from "react-router-dom";
import InitSeeso from "./InitSeeso"; // 시선 추적 API 컴포넌트
import "../../css/VideoPlayerWrapper.css"; // 필요한 경우 CSS 파일로 스타일을 분리

const VideoPlayerWrapper = () => {
    const { videoId } = useParams();

    return (
        <div className='video-player-wrapper'>
            <h4 className='page-title'>영상 재생페이지</h4>
            {/* 시선 추적을 위한 컴포넌트 */}
            <InitSeeso />

            {/* YouTube Iframe */}
            <iframe
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
                    className='back-button'
                    style={{
                        display: "block",
                        margin: "20px auto 0", // 영상 아래에 중앙에 위치하도록 설정
                        textAlign: "center",
                        zIndex: 2, // 시선 추적 캔버스보다 위에 표시되도록 설정
                    }}>
                    뒤로가기
                </a>
            </div>
        </div>
    );
};

export default VideoPlayerWrapper;
