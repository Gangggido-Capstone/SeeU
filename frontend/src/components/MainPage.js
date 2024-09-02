import React, { useState, useEffect } from "react";
import VideoList from "./VideoList";
import SearchBar from "./SearchBar";
import { fetchPopularVideos, searchVideos } from "./api/youtubeApi";

const MainPage = () => {
    const [videos, setVideos] = useState([]);
    const [searchResults, setSearchResults] = useState([]);

    useEffect(() => {
        loadPopularVideos();
    }, []);

    const loadPopularVideos = async () => {
        try {
            const data = await fetchPopularVideos();
            setVideos(data);
        } catch (error) {
            console.error("Error loading popular videos", error);
        }
    };

    const handleSearch = async (query) => {
        try {
            const data = await searchVideos(query);
            setSearchResults(data);
        } catch (error) {
            console.error("Error during search", error);
        }
    };

    return (
        <div>
            <SearchBar onSearch={handleSearch} />
            <VideoList
                videos={searchResults.length > 0 ? searchResults : videos}
            />
        </div>
    );
};

export default MainPage;
