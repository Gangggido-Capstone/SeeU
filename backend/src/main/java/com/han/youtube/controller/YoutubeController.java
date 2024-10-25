package com.han.youtube.controller;

import com.google.api.services.youtube.model.Video;
import com.han.youtube.service.YoutubeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.List;

@RestController
@CrossOrigin(origins = "http://localhost:9000", allowCredentials = "true")
public class YoutubeController {

    private final YoutubeService youtubeService;

    @Autowired
    public YoutubeController(YoutubeService youtubeService) {
        this.youtubeService = youtubeService;
    }

    @GetMapping("/api/popular-videos")
    public List<Video> getPopularVideos() {
        try {
            return youtubeService.getPopularVideos();
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }

    @GetMapping("/api/search-videos")
    public List<Video> searchVideos(@RequestParam(name = "query") String query) {
        try {
            return youtubeService.searchVideos(query);
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }

    // 특정 영상 정보 반환
    @GetMapping("/api/video")
    public Video getVideoById(@RequestParam String videoId) {
        try {
            return youtubeService.getVideoById(videoId);
        } catch (Exception e) {
            e.printStackTrace();
            return null; // 에러 발생 시 null 반환
        }
    }
}
