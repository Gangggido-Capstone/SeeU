import React, { useEffect, useState } from "react";
import axios from "axios";
import CircularProgress from "./CircularProgress"; // CircularProgress 컴포넌트 가져오기
import "../../css/RecordPage.css";

axios.defaults.baseURL = "http://localhost:8080";

const RecordPage = () => {
    const [records, setRecords] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showModal, setShowModal] = useState(false);
    const [selectedRecord, setSelectedRecord] = useState(null);

    useEffect(() => {
        const fetchRecords = async () => {
            try {
                const response = await axios.get("/api/list");
                setRecords(response.data);
                console.log(response.data);
            } catch (error) {
                setError(`시청 기록을 가져오는 데 실패했습니다: ${error.message}`);
            } finally {
                setLoading(false);
            }
        };

        fetchRecords();
    }, []);

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

            {/* 모달 */}
            {showModal && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <h2>분석 결과</h2>

                        {/* scoreList가 비어 있는 경우 처리 */}
                        {selectedRecord && selectedRecord.scoreList?.length > 0 ? (
                            <ul className="score-list">
                                {selectedRecord.scoreList.slice(0, 3).map((item, index) => (
                                    <li key={index} className="score-item">
                                        <video width="320" height="240" controls>
                                            <source src={`../../data/video/${item[0]}`} type="video/mp4" />
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
