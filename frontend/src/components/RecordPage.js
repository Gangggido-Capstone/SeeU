import React, { useEffect, useState } from "react";
import axios from "axios";
import "../../css/RecordPage.css"; // CSS 파일 import

axios.defaults.baseURL = "http://localhost:8080";

const RecordPage = () => {
    const [records, setRecords] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchRecords = async () => {
            try {
                const response = await axios.get("/api/list");
                console.log(response);
                setRecords(response.data);
                console.log(response.data);
            } catch (error) {
                setError(
                    `시청 기록을 가져오는 데 실패했습니다: ${error.message}`
                );
                console.error(error);
            } finally {
                setLoading(false);
            }
        };

        fetchRecords();
    }, []);

    if (loading) {
        return <div>로딩 중...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div>
            <h1>시청 기록</h1>
            <ul>
                {records.map((record) => (
                    <li key={record.videoId} className="list-item">
                        <img
                            src={record.snippet.thumbnails.standard.url}
                            alt="thumbnail"
                            className="thumbnail"
                        />
                        <div className="record-info">
                            <p className="record-title">{record.snippet.title}</p>
                            <p className="record-time">시청시간: {record.watchdata}</p>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default RecordPage;
