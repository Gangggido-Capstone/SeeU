import React from "react";
import { Link } from "react-router-dom";
import "../../css/VideoList.css";

const VideoList = ({ videos }) => {
    return (
        <div className='grid-container'>
            {videos.map((video) => (
                <div className='grid-item' key={video.id}>
                    <Link to={`/play-video/${video.id}`}>
                        <img
                            src={video.snippet.thumbnails.high.url}
                            alt={video.snippet.title}
                        />
                        <div className='title'>{video.snippet.title}</div>
                        <div className='views'>
                            조회수{" "}
                            {Number(
                                video.statistics.viewCount
                            ).toLocaleString()}
                            회
                        </div>
                    </Link>
                </div>
            ))}
        </div>
    );
};

export default VideoList;
