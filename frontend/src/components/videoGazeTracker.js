import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";
import "../../css/VideoPlayer.css";

const VideoPlayer = () => {
    const { videoId } = useParams();
    const [videoData, setVideoData] = useState(null);

    useEffect(() => {
        const fetchVideoData = async () => {
            try {
                const response = await axios.get(
                    `http://localhost:8080/api/video`,
                    {
                        params: { videoId },
                    }
                );
                console.log(response.data); // 응답 데이터 확인
                setVideoData(response.data);
            } catch (error) {
                console.error("Error fetching video data", error);
            }
        };

        fetchVideoData();
    }, [videoId]);

    return (
        <div className='video-player-container'>
            <h1 className='page-title'>영상 재생 페이지</h1>

            {/* YouTube 영상 재생을 위한 iframe */}
            {videoData ? (
                <>
                    <iframe
                        title='YouTube video player'
                        src={`https://www.youtube.com/embed/${videoData.id}`}
                        allowFullScreen
                        style={{
                            position: "relative",
                            width: "100%",
                            height: "50vh",
                            border: "none",
                        }}
                    />
                    <div className='video-details'>
                        <p>{videoData.snippet.title}</p>
                    </div>
                </>
            ) : (
                <p>영상 데이터를 불러오는 중...</p>
            )}

            <div className='back-button-container'>
                <Link to='/' className='back-button'>
                    뒤로가기
                </Link>
            </div>
        </div>
    );
};

export default VideoPlayer;
