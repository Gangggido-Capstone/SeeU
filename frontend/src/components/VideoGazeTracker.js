import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import InitSeeso from "./InitSeeso";
import "../../css/VideoGazeTracker.css";

const VideoGazeTracker = () => {
    const { videoId } = useParams(); // URL에서 유튜브 동영상 ID(videoId)를 추출
    const [player, setPlayer] = useState(null); // 유튜브 플레이어 객체를 저장하는 상태
    const [currentTime, setCurrentTime] = useState(0); // 현재 재생 시간을 저장하는 상태
    const [isPlaying, setIsPlaying] = useState(false); // 재생 상태를 저장하는 상태
    const [isApiReady, setIsApiReady] = useState(false); // YouTube API 로드 상태를 저장하는 상태
    const [startTracking, setStartTracking] = useState(() => {}); // seeso 시선 추적 시작
    const [stopTracking, setStopTracking] = useState(() => {}); // seeso 시선 추적 정지
    const [gazeData, setGazeData] = useState({
        x: NaN,
        y: NaN,
        attention: 3,
    }); // 시선 좌표
    const [videoGaze, setVideoGaze] = useState({
        x: NaN,
        y: NaN,
        attention: 3,
    }); // 교정된 시선 좌표
    const [videoFrame, setVideoFrame] = useState({
        top: 0,
        left: 0,
        height: 0,
        width: 0,
    }); // 영상 위치와 크기
    const [videoGazeData, setVideoGazeData] = useState([]); // 시선 좌표와 시간을 저장할 배열

    useEffect(() => {
        // YouTube IFrame Player API가 로드되었을 때 호출되는 함수
        const onYouTubeIframeAPIReady = () => {
            // YouTube 플레이어 생성
            const ytPlayer = new window.YT.Player("youtube-player", {
                videoId: videoId, // 유튜브 영상 ID
                events: {
                    onReady: onPlayerReady, // 플레이어 준비 완료 이벤트
                    onStateChange: onPlayerStateChange, // 플레이어 상태 변경 이벤트 (재생, 일시정지 등)
                },
            });
            setPlayer(ytPlayer); // 생성된 유튜브 플레이어를 상태에 저장
        };

        // YouTube IFrame Player API가 이미 로드되었는지 확인
        if (!window.YT) {
            // API가 로드되지 않았을 경우, 스크립트를 동적으로 로드
            const tag = document.createElement("script");
            tag.src = "https://www.youtube.com/iframe_api"; // 유튜브 API 경로
            const firstScriptTag = document.getElementsByTagName("script")[0];
            firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

            // API 로드 완료 시, 콜백 함수 실행
            window.onYouTubeIframeAPIReady = () => {
                console.log("YouTube IFrame API 로드 완료"); // API 로드 완료를 콘솔에 출력
                setIsApiReady(true); // API 로드 상태를 true로 설정
                onYouTubeIframeAPIReady(); // 플레이어 생성
            };
        } else {
            console.log("YouTube IFrame API가 이미 로드되었습니다"); // 이미 API가 로드된 경우
            setIsApiReady(true); // API 로드 상태를 true로 설정
            onYouTubeIframeAPIReady(); // 플레이어 생성
        }

        // 컴포넌트가 언마운트될 때 플레이어를 해제 (메모리 누수 방지)
        return () => {
            if (player) {
                player.destroy(); // YouTube 플레이어 해제
            }
        };
    }, [videoId]); // videoId가 변경될 때마다 이 효과 함수 실행

    useEffect(() => {
        const videoElement = document.getElementById("youtube-player");
        if (videoElement) {
            const video = videoElement.getBoundingClientRect(); // 영상 위치와 크기
            setVideoFrame({
                top: video.top,
                left: video.left,
                height: video.height,
                width: video.width,
            });
        }
    }, [player]);

    // YouTube 플레이어가 준비되었을 때 호출되는 함수
    const onPlayerReady = (event) => {
        console.log("Player is ready"); // 플레이어가 준비되었음을 콘솔에 출력
    };

    // YouTube 플레이어의 상태가 변경될 때마다 호출되는 함수 (재생, 일시정지 등)
    const onPlayerStateChange = (event) => {
        if (event.data === window.YT.PlayerState.PLAYING) {
            // 동영상이 재생 중일 때
            setIsPlaying(true); // 재생 상태를 true로 설정

            const interval = setInterval(() => {
                const time = event.target.getCurrentTime(); // 현재 재생 시간
                setCurrentTime(time);
            }, 300);

            return () => clearInterval(interval); // 정리 함수로 인터벌을 해제
        } else {
            setIsPlaying(false); // 동영상이 일시정지 또는 종료된 경우 재생 상태를 false로 설정
        }
    };

    // 교정된 시선 좌표 및 시간 기록 로직
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

        setVideoGaze({
            x: videoX,
            y: videoY,
            attention: attention,
        });

        if (isPlaying) {
            // 현재 시간에 해당하는 좌표가 이미 기록되어 있지 않은 경우만 저장
            const alreadyRecorded = videoGazeData.some(
                (record) => record.time === currentTime
            );
            if (!alreadyRecorded) {
                setVideoGazeData((prevRecords) => [
                    ...prevRecords,
                    {
                        time: currentTime,
                        x: videoX,
                        y: videoY,
                        attention: attention,
                    },
                ]);

                // 저장 데이터 확인용 로그
                console.log(
                    `Time: ${currentTime}, X: ${videoX}, Y: ${videoY}, , attention: ${attention}`
                );
            }
        }
    }, [gazeData, videoFrame, currentTime, isPlaying]);

    // 시선 추적 데이터를 받는 콜백 함수
    const handleGaze = (gazeData) => {
        setGazeData(gazeData); // 시선 좌표를 상태에 저장
    };

    // 재생 버튼을 클릭했을 때 호출되는 함수
    const handlePlay = () => {
        if (player && player.playVideo) {
            // 플레이어가 준비되었고, playVideo 함수가 있을 경우
            player.playVideo(); // 동영상을 재생
            startTracking(); // 시선 추적 시작
        } else {
            console.error("Player is not ready or playVideo is not available"); // 플레이어가 준비되지 않은 경우 에러 출력
        }
    };

    // 정지 버튼을 클릭했을 때 호출되는 함수
    const handlePause = () => {
        if (player && player.pauseVideo) {
            // 플레이어가 준비되었고, pauseVideo 함수가 있을 경우
            player.pauseVideo(); // 동영상을 정지
            stopTracking(); // 시선 추적 정지
        } else {
            console.error("Player is not ready or pauseVideo is not available"); // 플레이어가 준비되지 않은 경우 에러 출력
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
                hour12: false, // 24시간 형식 적용
            })
            .replace(/\./g, "-")
            .replace(/\s/g, "")
            .replace(/:/g, "-");
    };

    const aaa = (videoGazeData) => {
        videoGazeData;
    };
    const saveCSVToServer = async () => {
        // 시간
        const formattedDate = getFormattedKSTDate();

        try {
            // 전송할 데이터 구성
            const dataToSend = {
                videoId: videoId,
                videoFrame: videoFrame,
                watchDate: formattedDate,
                gazeData: videoGazeData,
            };

            const response = await fetch(
                "http://localhost:8080/api/save-gaze-data",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(dataToSend), // JSON 형태로 서버에 전송
                }
            );

            const result = await response.text();

            if (response.ok) {
                console.log("파일이 서버에 성공적으로 저장되었습니다.");
                console.log(result); // 성공 메시지 출력
            } else {
                console.error("서버에 파일 저장 실패");
                console.error(result); // 실패 메시지 출력
            }
        } catch (error) {
            console.error("서버 요청 중 오류 발생:", error);
        }
    };

    // 시선 데이터 저장 & 분석 코드 작성 중....
    const handleAnalysis = () => {
        if (player && player.pauseVideo) {
            // 플레이어가 준비되었고, pauseVideo 함수가 있을 경우
            player.pauseVideo(); // 동영상을 정지
            stopTracking(); // 시선 추적 정지

            // 여기에 csv 파일 저장 코드 추가
            saveCSVToServer(); // 서버로 데이터 저장 요청
        } else {
            console.error("Player is not ready or pauseVideo is not available"); // 플레이어가 준비되지 않은 경우 에러 출력
        }
    };

    const handleBack = () => {
        stopTracking(); // 뒤로가기 시 시선 추적 중지
    };

    return (
        <div className='video-player-wrapper'>
            <div>test</div>
            <iframe
                id='youtube-player' // YouTube Player API와 연결하기 위한 ID
                credentialless='true' // Cross-Origin 관련 속성
                title='YouTube video player'
                src={`https://www.youtube.com/embed/${videoId}?enablejsapi=1`} // enablejsapi=1 옵션을 통해 JavaScript API 활성화
                allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture'
                allowFullScreen
                loading='lazy'
                className='youtube-iframe'
            />

            <div className='info-container'>
                {/* 시선 추적을 위한 컴포넌트 */}
                <InitSeeso
                    onTrackingStart={(start) => setStartTracking(() => start)}
                    onTrackingStop={(stop) => setStopTracking(() => stop)}
                    GazeData={handleGaze}
                />

                {/* 시선 좌표를 화면에 표시 */}
                <p>
                    시선 좌표: x: {videoGaze.x}, y: {videoGaze.y}, attention:{" "}
                    {videoGaze.attention}
                </p>

                {/* 재생 및 정지 버튼 */}

                <div className='video-controls'>
                    <button onClick={handlePlay}>재생</button>
                    <button onClick={handlePause}>정지</button>
                    <button onClick={handleAnalysis}>분석</button>
                    <a href='/' className='back-button' onClick={handleBack}>
                        홈
                    </a>
                </div>
            </div>
        </div>
    );
};

export default VideoGazeTracker;
