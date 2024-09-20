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

    // YouTube 플레이어가 준비되었을 때 호출되는 함수
    const onPlayerReady = (event) => {
        console.log("Player is ready"); // 플레이어가 준비되었음을 콘솔에 출력
    };

    // YouTube 플레이어의 상태가 변경될 때마다 호출되는 함수 (재생, 일시정지 등)
    const onPlayerStateChange = (event) => {
        if (event.data === window.YT.PlayerState.PLAYING) {
            // 동영상이 재생 중일 때
            setIsPlaying(true); // 재생 상태를 true로 설정
            // 1초마다 현재 재생 시간을 가져와 상태에 저장
            const interval = setInterval(() => {
                const time = event.target.getCurrentTime(); // 현재 재생 시간을 가져옴
                setCurrentTime(time); // 현재 재생 시간을 상태에 업데이트
            }, 1000);

            return () => clearInterval(interval); // 정리 함수로 인터벌을 해제
        } else {
            setIsPlaying(false); // 동영상이 일시정지 또는 종료된 경우 재생 상태를 false로 설정
        }
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

    const handleBack = () => {
        stopTracking(); // 뒤로가기 시 시선 추적 중지
    };

    return (
        <div className='video-player-wrapper'>
            <div>
                <h4 className='page-title'>영상 시선 추적 페이지</h4>
            </div>

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
                />

                {/* 영상 재생 시간 및 좌표 */}

                <p>현재 재생 시간: {Math.floor(currentTime)}초</p>

                {/* 재생 및 정지 버튼 */}
                <div className='video-controls'>
                    <button onClick={handlePlay}>재생</button>
                    <button onClick={handlePause}>정지</button>
                </div>

                {/* 뒤로가기 버튼 */}
                <a href='/' className='back-button' onClick={handleBack}>
                    뒤로가기
                </a>
            </div>
        </div>
    );
};

export default VideoGazeTracker;
