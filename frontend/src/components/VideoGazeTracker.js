import React, { useEffect, useState, useRef } from "react";
import "regenerator-runtime/runtime";
import EasySeeSo from "seeso/easy-seeso";
import { useNavigate, useParams } from "react-router-dom";
import { showGaze } from "./showGaze.js";
import "../../css/styles.css";
import "../../css/VideoGazeTracker.css";

const VideoGazeTracker = () => {
    const { videoId } = useParams();
    const navigate = useNavigate();

    const [player, setPlayer] = useState(null);
    const [currentTime, setCurrentTime] = useState(0);
    const [isPlaying, setIsPlaying] = useState(false);
    const [startTracking, setStartTracking] = useState(() => {});
    const [stopTracking, setStopTracking] = useState(() => {});
    const [gazeData, setGazeData] = useState({ x: NaN, y: NaN, attention: 3 });
    const [videoGaze, setVideoGaze] = useState({x: NaN, y: NaN, attention: 3});
    const [videoFrame, setVideoFrame] = useState({top: 0, left: 0, height: 0, width: 0});
    const [videoGazeData, setVideoGazeData] = useState([]);
    const intervalRef = useRef(null);
    const [result, setResult] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const licenseKey = process.env.REACT_APP_EYEDID_KEY;

    if (!licenseKey) {
        console.error("환경 변수 REACT_APP_EYEDID_KEY가 설정되지 않았습니다.");
    }

    useEffect(() => {
        const onGaze = (gazeInfo) => {
            showGaze(gazeInfo);
            setGazeData(gazeInfo);
        };

        const onDebug = (FPS, latency_min, latency_max, latency_avg) => {};

        async function initializeSeeso() {
            const seeSo = new EasySeeSo();
            await seeSo.init(
                licenseKey,
                () => {
                    seeSo.setMonitorSize(27);
                    seeSo.setFaceDistance(60);
                    seeSo.setCameraPosition(window.outerWidth / 2, true);
                    setStartTracking(() => () => {
                        if (typeof seeSo.startTracking === 'function') {
                            seeSo.startTracking(onGaze, onDebug);
                        } else {
                            console.error("startTracking 함수가 초기화되지 않았습니다.");
                        }
                    });

                    setStopTracking(() => () => {
                        if (typeof seeSo.stopTracking === 'function') {
                            seeSo.stopTracking();
                        } else {
                            console.error("stopTracking 함수가 초기화되지 않았습니다.");
                        }
                    });
                },
                () => console.log("=== seeso api error ===")
            );
        }

        initializeSeeso();
    }, []);
    
    useEffect(() => {
        const onYouTubeIframeAPIReady = () => {
            const ytPlayer = new window.YT.Player("youtube-player", {
                videoId: videoId,
                events: {
                    onReady: onPlayerReady,
                    onStateChange: onPlayerStateChange,
                },
            });
            setPlayer(ytPlayer);
        };

        if (!window.YT) {
            const tag = document.createElement("script");
            tag.src = "https://www.youtube.com/iframe_api";
            const firstScriptTag = document.getElementsByTagName("script")[0];
            firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
            window.onYouTubeIframeAPIReady = () => {
                console.log("YouTube IFrame API 로드 완료");
                onYouTubeIframeAPIReady();
            };
        } else {
            console.log("YouTube IFrame API가 이미 로드되었습니다");
            onYouTubeIframeAPIReady();
        }

        return () => {
            if (player) {
                player.destroy();
            }
        };
    }, [videoId]);

    useEffect(() => {
        const videoElement = document.getElementById("youtube-player");
        if (videoElement) {
            const video = videoElement.getBoundingClientRect();
            setVideoFrame({
                top: video.top,
                left: video.left,
                height: video.height,
                width: video.width,
            });
        }
    }, [player]);

    const onPlayerReady = (event) => {
        console.log("Player is ready");
    };

    const onPlayerStateChange = (event) => {
        if (event.data === window.YT.PlayerState.PLAYING) {
            setIsPlaying(true);

            if (intervalRef.current) {
                clearInterval(intervalRef.current);
            }

            intervalRef.current = setInterval(() => {
                const time = event.target.getCurrentTime();
                setCurrentTime(time);
            }, 100);
        } else {
            setIsPlaying(false);

            if (intervalRef.current) {
                clearInterval(intervalRef.current);
                intervalRef.current = null;
            }
        }
    };

    useEffect(() => {
        return () => {
            if (intervalRef.current) {
                clearInterval(intervalRef.current);
                intervalRef.current = null;
            }
        };
    }, []);

    useEffect(() => {
        let videoX = gazeData.x - videoFrame.left;
        let videoY = gazeData.y - videoFrame.top;
        let attention = gazeData.eyemovementState;

        if (
            !(0 <= videoX && videoX <= videoFrame.width) ||
            !(0 <= videoY && videoY <= videoFrame.height)
        ) {
            videoX = NaN;
            videoY = NaN;
            attention = 3;
        }

        setVideoGaze({ x: videoX, y: videoY, attention: attention });

        if (isPlaying) {
            const alreadyRecorded = videoGazeData.some(
                (record) => record.time === currentTime
            );
            if (!alreadyRecorded) {
                setVideoGazeData((prevRecords) => [
                    ...prevRecords,
                    {
                        time: currentTime,
                        x: Math.round(videoX),
                        y: Math.round(videoY),
                        attention: attention,
                    },
                ]);
                console.log(
                    `Time: ${currentTime}, X: ${videoX}, Y: ${videoY}, attention: ${attention}`
                );
            }
        }
    }, [gazeData, videoFrame, currentTime, isPlaying]);

    const handlePlay = () => {
        if (player && player.playVideo) {
            if (startTracking) {
                player.playVideo();
                startTracking();
            } else {
                console.error("startTracking 함수가 아직 초기화되지 않았습니다.");
            }
        } else {
        console.error("Player is not ready or playVideo is not available");
        }
    };

    const handlePause = () => {
        if (player && player.pauseVideo) {
            if (stopTracking) {
                player.pauseVideo();
                stopTracking();
            } else {
                console.error("stopTracking 함수가 아직 초기화되지 않았습니다.");
            }
        } else {
            console.error("Player is not ready or pauseVideo is not available");
        }
    };

    const handleBack = () => {
        if (player && player.pauseVideo) {
            if (stopTracking) {
                player.pauseVideo();
                stopTracking();
            } else {
                console.error("stopTracking 함수가 아직 초기화되지 않았습니다.");
            }      
        } else {
            console.error("Player is not ready or pauseVideo is not available");
        }
    };

    const getFormattedKSTDate = () => {
        const now = new Date();
        return now
            .toLocaleString("ko-KR", {
                timeZone: "Asia/Seoul",
                year: "numeric",
                month: "2-digit",
                day: "2-digit",
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit",
                hour12: false,
            })
            .replace(/\./g, "-")
            .replace(/\s/g, "")
            .replace(/:/g, "-");
    };

    const saveCSVToServer = async () => {
        setIsLoading(true);
        const formattedDate = getFormattedKSTDate();

        try {
            const dataToSend = {
                videoId: videoId,
                videoFrame: videoFrame,
                watchDate: formattedDate,
                gazeData: videoGazeData,
            };

            const response = await fetch("http://localhost:8080/api/save-gaze-data", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(dataToSend),
            });

            if (response.ok) {
                console.log("파일이 서버에 성공적으로 저장되었습니다.");

            } else {
                console.error("서버에 파일 저장 실패");
            }

        } catch (error) {
            console.error("Error:", error);
        } 
    };

    const handleAnalysis = () => {
        if (player && player.pauseVideo) {
            if (stopTracking) { 
                player.pauseVideo();
                stopTracking();
                saveCSVToServer();
                // navigate("/Records");
            } else {
                console.error("stopTracking 함수가 아직 초기화되지 않았습니다.");
            }  
        } else {
            console.error("Player is not ready or pauseVideo is not available");
        }
    };
    
    return (
        <div className='video-player-wrapper'>
            <iframe
                id='youtube-player'
                credentialless='true'
                title='YouTube video player'
                src={`https://www.youtube.com/embed/${videoId}?enablejsapi=1&origin=http://localhost:9000`}
                allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture'
                allowFullScreen
                loading='lazy'
                className='youtube-iframe'
            />

            <div className='info-container'>
                <p>
                재생 시간: {Math.floor(currentTime)}초, 시선 좌표: x: {Math.round(videoGaze.x)}, y: {Math.round(videoGaze.y)}
                </p>
                <p></p>
            </div>

            <div className='video-controls'>
                <button onClick={handlePlay}>재생</button>
                <button onClick={handlePause}>정지</button>
                <button onClick={handleAnalysis}>분석</button>
                <a href='/' className='back-button' onClick={handleBack}> 홈 </a>
            </div>

            <div>
                <canvas id='output'></canvas>
            </div>
        </div>
    );
};

export default VideoGazeTracker;
