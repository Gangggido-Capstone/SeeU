package com.han.youtube.service;

import com.google.api.services.youtube.model.VideoSnippet;
import com.han.youtube.Domain.ReceiveId;
import com.han.youtube.Dto.GazeDataResult;
import com.han.youtube.Dto.ReceiveIdDto;
import com.han.youtube.Repository.MongoRepository;

import lombok.RequiredArgsConstructor;
import org.json.JSONArray;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.google.api.services.youtube.model.Video;

import java.io.*;
import java.nio.file.Paths;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class GazeDataService {

    @Autowired
    private YoutubeService youtubeService;
    private final MongoRepository mongoRepository;

    public GazeDataResult runPythonScript(String videoId, String filePath) {
        try {
            String pythonPath = "python";  // 시스템 환경에 맞게 "python3"으로 변경 필요할 수 있음

            // 파이썬 파일 경로 설정
            File currentDir = new File("");
            String rootPath = currentDir.getAbsoluteFile().getParent();  // youtube-seeso-demo 경로
            String fileDirectory = Paths.get(rootPath, "analysis").normalize().toString();
            String scriptPath = Paths.get(fileDirectory,"video_analysis.py").toString();

            System.out.println("파일 경로: " + scriptPath);  // 경로 출력 (디버깅용)

            List<String> arguments = new ArrayList<>();
            arguments.add(pythonPath);
            arguments.add(scriptPath);
            arguments.add(videoId);
            arguments.add(filePath);

            ProcessBuilder pb = new ProcessBuilder(arguments);
            Process process = pb.start();

            // 표준 출력 및 에러 출력 처리
            BufferedReader stdInput = new BufferedReader(new InputStreamReader(process.getInputStream()));
            BufferedReader stdError = new BufferedReader(new InputStreamReader(process.getErrorStream()));
            StringBuilder jsonOutput = new StringBuilder();
            StringBuilder ffmpegOutput = new StringBuilder();  // FFmpeg 로그 저장
            String s;
            boolean jsonStarted = false;  // JSON 시작점 찾기

            System.out.println("Python Output:");
            while ((s = stdInput.readLine()) != null) {
                System.out.println(s);  // Python의 표준 출력 확인

                // JSON이 시작되는 지점부터 문자열을 추출
                if (s.trim().startsWith("{")) {
                    jsonStarted = true;  // JSON 시작
                }

                // JSON 데이터 저장
                if (jsonStarted) {
                    jsonOutput.append(s.trim());  // JSON 부분만 추출
                } else {
                    // JSON 외의 모든 출력 (FFmpeg 로그 포함)
                    ffmpegOutput.append(s).append("\n");  // FFmpeg 로그 저장
                }
            }

            // 표준 에러 출력 처리 (FFmpeg 에러 포함)
            System.out.println("Python Errors (if any):");
            while ((s = stdError.readLine()) != null) {
                System.out.println(s);  // Python 에러 로그 확인
                ffmpegOutput.append(s).append("\n");  // FFmpeg 에러 로그 저장
            }

            int exitCode = process.waitFor();
            System.out.println("Python script exited with code: " + exitCode);

            // FFmpeg 로그 출력
            System.out.println("FFmpeg Output:");
            System.out.println(ffmpegOutput.toString());  // FFmpeg 관련 출력 확인

            // JSON 파싱
            String jsonString = jsonOutput.toString();
            System.out.println("Parsed JSON: " + jsonString);  // 추출된 JSON 확인
            JSONObject result = new JSONObject(jsonString);

            // JSONArray를 List로 변환
            JSONArray jsonArray = result.getJSONArray("attention_score_list");
            List<Object> attentionScoreList = new ArrayList<>();
            for (int i = 0; i < jsonArray.length(); i++) {
                attentionScoreList.add(jsonArray.get(i));
            }

            String videoPoint = result.getString("video_point");

            // 변환된 리스트와 video_point를 GazeDataResult 객체로 반환
            return new GazeDataResult(attentionScoreList, videoPoint);

        } catch (Exception e) {
            e.printStackTrace();
            return null;  // 예외가 발생한 경우 null 반환
        }
    }

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

        // ============= Python 스크립트 실행 후 결과 받아오기 =============

        GazeDataResult result = runPythonScript(videoId, filePath);

        if (result != null) {
            // 결과 출력
            System.out.println("Attention Score List: " + result.getAttentionScoreList());
            System.out.println("Video Point: " + result.getVideoPoint());
        } else {
            System.out.println("Python 스크립트 실행 중 오류가 발생했습니다.");
        }

        // ============================================================


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
