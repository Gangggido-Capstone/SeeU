package com.han.youtube.service;

import com.google.api.services.youtube.model.VideoSnippet;
import com.han.youtube.Domain.ReceiveId;
import com.han.youtube.Dto.GazeDataResult;
import com.han.youtube.Dto.ReceiveIdDto;
import com.han.youtube.Repository.MongoRepository;

import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.google.api.services.youtube.model.Video;

import java.io.*;
import java.nio.file.Path;
import java.nio.file.Paths;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class GazeDataService {

    @Autowired
    private YoutubeService youtubeService;
    private final MongoRepository mongoRepository;

    @Transactional
    public void saveGazeData(Map<String, Object> payload) throws IOException {
        String videoId = (String) payload.get("videoId");
        String watchDate = (String) payload.get("watchDate");
        String video_csv = videoId + "_" + watchDate + ".csv";

        // 비디오 크기 값 videoFrame.get("width"), videoFrame.get("height")
        Map<String, Object> videoFrame = null;
        if (payload.get("videoFrame") instanceof Map) {
            videoFrame = (Map<String, Object>) payload.get("videoFrame");
        }
        System.out.println(videoFrame.get("width"));
        System.out.println(videoFrame.get("height"));
        // 시선 데이터
        List<Map<String, Object>> gazeData = null;
        if (payload.get("gazeData") instanceof List) {
            gazeData = (List<Map<String, Object>>) payload.get("gazeData");
        }

        // CSV 파일 경로 설정
        // 현재 애플리케이션의 루트 경로를 가져오기
        File currentDir = new File("");
        String rootPath = currentDir.getAbsoluteFile().getParent();  // youtube-seeso-demo 경로

        // 항상 Data/GazeData 경로를 지정
        String fileDirectory = Paths.get(rootPath, "Data", "GazeData").normalize().toString();
        String filePath = Paths.get(fileDirectory, videoId + "_" + watchDate + ".csv").toString();

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath))) {
            System.out.println("rootPath: " + rootPath);  // 경로 출력 (디버깅용)
            System.out.println("fileDirectory: " + fileDirectory);  // 경로 출력 (디버깅용)
            System.out.println("CSV 파일 경로: " + filePath);  // 경로 출력 (디버깅용)
            // 헤더
            writer.append("Time,X,Y,Attention\n");

            // 시선 좌표 데이터를 CSV 파일에 작성
            for (Map<String, Object> record : gazeData) {
                writer.append(record.get("time") != null ? record.get("time").toString() : "null")
                        .append(",")
                        .append(record.get("x") != null ? record.get("x").toString() : "null")
                        .append(",")
                        .append(record.get("y") != null ? record.get("y").toString() : "null")
                        .append(",")
                        .append(record.get("attention") != null ? record.get("attention").toString() : "3")
                        .append("\n");
            }

            writer.flush();  // 파일에 데이터 저장
        }

        // youtubeService.getVideoById 사용해서 영상 정보 불러오기
        Video video = youtubeService.getVideoById(videoId);

        if (video != null) {
            VideoSnippet snippet = video.getSnippet();

            // VideoSnippet을 LinkedHashMap으로 변환
            LinkedHashMap<String, Object> snippetMap = new LinkedHashMap<>();
            snippetMap.put("title", snippet.getTitle());
            snippetMap.put("description", snippet.getDescription());
            snippetMap.put("categoryId", snippet.getCategoryId());
            snippetMap.put("channelId", snippet.getChannelId());
            snippetMap.put("channelTitle", snippet.getChannelTitle());
            snippetMap.put("defaultAudioLanguage", snippet.getDefaultAudioLanguage());
            snippetMap.put("publishedAt", snippet.getPublishedAt().toString());
            snippetMap.put("thumbnails", snippet.getThumbnails());
            snippetMap.put("localized", snippet.getLocalized());

            // id 저장
            ReceiveIdDto receiveIdDto = new ReceiveIdDto();
            ReceiveId receiveId = receiveIdDto.toEntity(videoId, watchDate, snippetMap);

            mongoRepository.save(receiveId);
        } else {
            System.out.println("해당 ID의 영상을 찾지 못했습니다.");
        }
    }

    @Transactional
    public List<ReceiveIdDto> dbData(){
        return mongoRepository.findBy(PageRequest.of(0,10));
    }
}
