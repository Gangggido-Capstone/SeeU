import axios from "axios";

const API_BASE_URL = "http://localhost:8080/api";

export const fetchPopularVideos = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/popular-videos`);
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error("Error fetching popular videos", error);
        throw error;
    }
};

export const searchVideos = async (query) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/search-videos`, {
            params: { query },
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error("Error searching videos", error);
        throw error;
    }
};
