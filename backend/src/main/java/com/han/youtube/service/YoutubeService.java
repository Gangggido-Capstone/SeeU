package com.han.youtube.service;

import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.json.gson.GsonFactory;
import com.google.api.services.youtube.YouTube;
import com.google.api.services.youtube.model.SearchListResponse;
import com.google.api.services.youtube.model.SearchResult;
import com.google.api.services.youtube.model.Video;
import com.google.api.services.youtube.model.VideoListResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.security.GeneralSecurityException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

@Service
public class YoutubeService {

    private final YouTube youtube;

    @Value("${youtube.api.key}")
    private String apiKey;

    public YoutubeService() throws GeneralSecurityException, IOException {
        this.youtube = new YouTube.Builder(GoogleNetHttpTransport.newTrustedTransport(), GsonFactory.getDefaultInstance(), request -> {})
                .setApplicationName("youtube-popular-videos")
                .build();
    }

    public List<Video> getPopularVideos() throws IOException {
        List<String> parts = Arrays.asList("snippet", "contentDetails", "statistics");  // List<String>으로 변환
        // YouTube Data API의 "Videos: list" 메서드 호출
        YouTube.Videos.List request = youtube.videos()
                .list(parts)  // 단일 문자열로 필드 전달
                .setChart("mostPopular")
                .setRegionCode("KR") // 한국 기준
                .setMaxResults(20L)  // 최대 10개의 결과만 가져옴
                .setKey(apiKey);

        // API 요청을 실행하고 결과 반환
        VideoListResponse response = request.execute();

        return response.getItems();
    }
    public List<Video> searchVideos(String queryTerm) throws IOException {
        // 1. YouTube Search API를 사용하여 비디오 ID 검색
        YouTube.Search.List search = youtube.search().list(Arrays.asList("snippet"));
        search.setQ(queryTerm);
        search.setKey(apiKey);
        search.setType(Arrays.asList("video"));
        search.setMaxResults(20L);
        search.setRegionCode("KR");

        SearchListResponse searchResponse = search.execute();
        List<SearchResult> searchResults = searchResponse.getItems();

        // 2. 비디오 ID 목록 생성
        List<String> videoIds = new ArrayList<>();
        for (SearchResult result : searchResults) {
            videoIds.add(result.getId().getVideoId());
        }

        // 3. videos.list 메서드를 사용하여 contentDetails 및 statistics 정보 가져오기
        YouTube.Videos.List videoRequest = youtube.videos().list(Arrays.asList("snippet", "contentDetails", "statistics"));
        videoRequest.setId(Collections.singletonList(String.join(",", videoIds)));
        videoRequest.setKey(apiKey);

        VideoListResponse videoResponse = videoRequest.execute();
        return videoResponse.getItems();
    }

    public Video getVideoById(String videoId) throws IOException {

        YouTube.Videos.List request = youtube.videos()
                .list(Arrays.asList("snippet", "contentDetails", "statistics"))
                .setId(Collections.singletonList(videoId))
                .setKey(apiKey); // API 키를 설정합니다.

        VideoListResponse response = request.setId(Collections.singletonList(videoId)).execute();
        List<Video> videoList = response.getItems();

        if (videoList.isEmpty()) {
            return null; // 해당 ID로 영상을 찾지 못한 경우
        }
        return videoList.get(0); // 첫 번째 결과를 반환
    }
}
