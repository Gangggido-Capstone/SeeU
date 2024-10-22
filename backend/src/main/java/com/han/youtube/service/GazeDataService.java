package com.han.youtube.service;

import com.google.api.services.youtube.model.VideoSnippet;
import com.han.youtube.Domain.ReceiveId;
import com.han.youtube.Dto.GazeAnalysisResult;
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

    public GazeAnalysisResult runPythonScript(String videoId, String videoCSV) {
        try {
            String python = "python";

            // 파이썬 파일 경로 설정
            File currentDir = new File("");
            String rootPath = currentDir.getAbsoluteFile().getParent();  // youtube-seeso-demo 경로
            String fileDirectory = Paths.get(rootPath, "analysis").normalize().toString();
            String scriptPath = Paths.get(fileDirectory,"video_analysis.py").toString();

            System.out.println("파일 경로: " + scriptPath);

            List<String> arguments = new ArrayList<>();
            arguments.add(python);
            arguments.add(scriptPath);
            arguments.add(videoId);
            arguments.add(videoCSV);

            ProcessBuilder pb = new ProcessBuilder(arguments);
            Process process = pb.start();

            // 파이썬 표준 출력 및 에러 출력 처리
            BufferedReader stdOut = new BufferedReader(new InputStreamReader(process.getInputStream()));
            BufferedReader stdError = new BufferedReader(new InputStreamReader(process.getErrorStream()));
            String line;
            
            // 출력된 JSON 데이터 저장
            StringBuilder jsonOutput = new StringBuilder();

            // JSON 시작점 찾기
            boolean jsonStarted = false;
            while ((line = stdOut.readLine()) != null) {
                System.out.println(line);
                // JSON이 시작되는 지점부터 문자열을 추출
                if (line.trim().startsWith("{")) {
                    jsonStarted = true;  // JSON 시작
                }

                // JSON 데이터 저장
                if (jsonStarted) {
                    jsonOutput.append(line.trim());  // JSON 부분만 추출
                }
            }

            // 표준 에러 출력 처리
            while ((line = stdError.readLine()) != null) {
                System.out.println(line);
            }

            int exitCode = process.waitFor();
            System.out.println("Python script exited with code: " + exitCode);

            // JSON 파싱
            String jsonString = jsonOutput.toString();
            JSONObject result = new JSONObject(jsonString);

            // JSONArray -> List
            JSONArray jsonArray = result.getJSONArray("attention_score_list");
            List<Object> attentionScoreList = new ArrayList<>();
            for (int i = 0; i < jsonArray.length(); i++) {
                attentionScoreList.add(jsonArray.get(i));
            }

            String videoPoint = result.getString("video_point");

            return new GazeAnalysisResult(attentionScoreList, videoPoint);

        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    @Transactional
    public void saveGazeData(Map<String, Object> payload) throws IOException {
        String videoId = (String) payload.get("videoId");
        String watchDate = (String) payload.get("watchDate");

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
        String filePath = Paths.get(rootPath, "Data", "GazeData").normalize().toString();
        String videoCSV = Paths.get(filePath, videoId + "_" + watchDate + ".csv").toString();

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(videoCSV))) {
            System.out.println("rootPath: " + rootPath);
            System.out.println("filePath: " + filePath);
            System.out.println("CSV 파일 경로: " + videoCSV);

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

        // Python 스크립트 실행 후 영상 분석 결과 받아오기
        GazeAnalysisResult result = runPythonScript(videoId, videoCSV);

        if (result != null) {
            System.out.println("Attention Score List: " + result.getAttentionScoreList());
            System.out.println("Video Gaze Visualization: " + result.getGazeVisualization());
        } else {
            System.out.println("Python 스크립트 실행 중 오류 발생");
        }


        List<Object> attentionScore = new ArrayList<>(result.getAttentionScoreList());
        String visualization =result.getGazeVisualization();

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
            ReceiveId receiveId = receiveIdDto.toEntity(videoId, watchDate, snippetMap,attentionScore,visualization);

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
