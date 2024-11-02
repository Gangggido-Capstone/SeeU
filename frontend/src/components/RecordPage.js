import React, { useEffect, useLayoutEffect, useState } from "react";
import axios from "axios";
import CircularProgress from "./CircularProgress"; // CircularProgress 컴포넌트 가져오기
import "../../css/RecordPage.css";

axios.defaults.baseURL = "http://localhost:8080";

const RecordPage = () => {
    const [records, setRecords] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showModal, setShowModal] = useState(false);
    const [selectedRecord, setSelectedRecord] = useState({ scoreList: [] });
    const [averageScores, setAverageScores] = useState({});
    const [showAverageModal, setShowAverageModal] = useState(false);

    useLayoutEffect(() => {
        const fetchRecords = async () => {
            try {
                const response = await axios.get("/api/list");
                setRecords(response.data);
                setLoading(false)
                console.log(response.data);
            } catch (error) {
                setError(`시청 기록을 가져오는 데 실패했습니다: ${error.message}`);
            }
        };

        fetchRecords();
    }, []);

    const openAverageScoreModal = async (videoId) => {
        try {
            const response = await axios.post("/api/average", { videoId });
            setAverageScores(response.data);
            setShowAverageModal(true);
        } catch (error) {
            console.error("평균 점수를 가져오는 데 실패했습니다:", error);
        }
    };

    const openModal = (record) => {
        setSelectedRecord(record);
        setShowModal(true);
    };

    const closeModal = () => {
        setShowModal(false);
        setSelectedRecord(null);
    };

    if (loading) {
        return <div>로딩 중...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div className="record-page-container">
            <h1>시청 기록</h1>
            <div className="records-container">
                <ul>
                    {records.map((record) => (
                        <li key={record.videoId} className="list-item">
                            {record.snippet?.thumbnails?.standard?.url ? (
                                <img
                                    src={record.snippet.thumbnails.standard.url}
                                    alt="thumbnail"
                                    className="thumbnail"
                                />
                            ) : (
                                <img
                                    src={record.snippet.thumbnails.high.url}
                                    alt="thumbnail"
                                    className="thumbnail"
                                />
                            )}
                            <div className="record-info">
                                <p className="record-title">{record.snippet.title}</p>
                                <p className="record-time">시청시간: {record.watchdata}</p>
                            </div>
                            
                            <button
                                className="analysis-button"
                                onClick={() => openAverageScoreModal(record.videoId)}
                            >
                                도우미
                            </button>

                            <button
                                className="analysis-button"
                                onClick={() => openModal(record)}
                            >
                                분석 결과
                            </button>
                        </li>
                    ))}
                </ul>
                
                {/* 홈 버튼 */}
                <a href="http://localhost:9000" className="home-logo-link">
                    <img src="/home.svg" alt="Home" className="home-logo" />
                </a>
            </div>
            
            {showAverageModal && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <h2>분할된 영상별 평균 점수</h2>
                        <ul className="score-list">
                            {averageScores.slice(0, 5).map((entry, index) => {
                                const [videoName, newValue, score] = entry;
                                return (
                                    <li key={index} className="score-item">
                                        <video width="320" height="240" controls poster={`/data/video/${newValue}`}>
                                            <source src={`/data/video/${videoName}`} type="video/mp4" />
                                            동영상을 지원하지 않는 브라우저입니다.
                                        </video>
                        
                                        <CircularProgress score={score} />
                                    </li>
                                );
                            })}
                        </ul>
                        <button className="close-button" onClick={() => setShowAverageModal(false)}>
                            닫기
                        </button>
                    </div>
                </div>
            )}


            {/* 모달 */}
            {showModal && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <h2>분석 결과</h2>

                        {selectedRecord.visualization ? (
                            <video width="640" height="400" controls>
                                <source src={`/data/video/${selectedRecord.visualization}`} type="video/mp4" />
                                동영상을 지원하지 않는 브라우저입니다.
                            </video>
                        ) : (
                            <p>분석 결과 영상이 없습니다.</p>
                        )}


                        {/* scoreList가 비어 있는 경우 처리 */}
                        {selectedRecord && selectedRecord.scoreList?.length > 0 ? (
                            <ul className="score-list">
                                {selectedRecord.scoreList.slice(0, 3).map((item, index) => (
                                    <li key={index} className="score-item">
                                        <video width="320" height="240" controls poster={item[1] ? `/data/video/${item[1]}` : null}>
                                            <source src={`/data/video/${item[0]}`} type="video/mp4" />
                                            동영상을 지원하지 않는 브라우저입니다.
                                        </video>
                                        {/* 집중력 점수 */}
                                        <CircularProgress score={item[2]} />
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <p>시청자의 시선 데이터가 부족하여 분석 결과가 없습니다.</p>
                        )}
                        <button className="close-button" onClick={closeModal}>
                            닫기
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default RecordPage;
