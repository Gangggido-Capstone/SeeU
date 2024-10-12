import React, { useEffect, useState } from "react";
import axios from "axios";

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
                    <li key={record.videoId}>
                        {" "}
                        {}
                        <p>ID: {record.snippet.title}</p>
                        <p>시청시간: {record.watchdata}</p> {}
                        <img src={record.snippet.thumbnails.standard.url} />
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default RecordPage;
