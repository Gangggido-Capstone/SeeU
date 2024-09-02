import React, { useState } from "react";
import "../../css/SearchBar.css";

const SearchBar = ({ onSearch }) => {
    const [query, setQuery] = useState("");

    const handleSearch = (event) => {
        event.preventDefault();
        onSearch(query);
    };

    return (
        <form onSubmit={handleSearch} className='search-bar'>
            <input
                type='text'
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder='검색'
                className='search-input'
            />
            <button type='submit' className='search-button'>
                검색
            </button>
        </form>
    );
};

export default SearchBar;
