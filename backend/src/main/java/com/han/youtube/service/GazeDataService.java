package com.han.youtube.service;

import com.google.api.services.youtube.model.VideoSnippet;
import com.han.youtube.Domain.ReceiveId;
import com.han.youtube.Dto.GazeAnalysisResult;
import com.han.youtube.Dto.ReceiveIdDto;
import com.han.youtube.Dto.VideoIdRequest;
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
import java.util.HashMap;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class GazeDataService {

    @Autowired
    private YoutubeService youtubeService;
    private final MongoRepository mongoRepository;


    public List<Integer> listScore(List<List<Object>> scoreList) {
        List<Integer> listscore = new ArrayList<>();

        for (List<Object> score : scoreList) {
            if (score.size() > 3 && score.get(3) instanceof Number) {
                listscore.add(((Number) score.get(3)).intValue());
            }
        }
        return listscore;
    }


    public GazeAnalysisResult runPythonScript(String videoId, String videoCSV, String videoWidth, String videoHeight) {
        try {
            String python = "python";

            // 파이썬 파일 경로 설정
            File currentDir = new File("");
            String rootPath = currentDir.getAbsoluteFile().getParent();  // youtube-seeso-demo 경로
            String fileDirectory = Paths.get(rootPath, "analysis").normalize().toString();
            String scriptPath = Paths.get(fileDirectory, "video_analysis.py").toString();

            int width = (int) Double.parseDouble(videoWidth);
            int height = (int) Double.parseDouble(videoHeight);

            System.out.println("파일 경로: " + scriptPath);

            List<String> arguments = new ArrayList<>();
            arguments.add(python);
            arguments.add(scriptPath);
            arguments.add(videoId);
            arguments.add(videoCSV);
            arguments.add(String.valueOf(width));
            arguments.add(String.valueOf(height));

            ProcessBuilder pb = new ProcessBuilder(arguments);
            pb.redirectErrorStream(true);

            System.out.println("Executing command: " + pb.command());
            Process process = pb.start();

            // 파이썬 표준 출력 및 에러 출력 처리
            BufferedReader stdout = new BufferedReader(new InputStreamReader(process.getInputStream()));
            BufferedReader stderr = new BufferedReader(new InputStreamReader(process.getErrorStream()));
            String line;

            // 출력된 JSON 데이터 저장
            StringBuilder jsonOutput = new StringBuilder();

            // JSON 시작점 찾기
            boolean jsonStarted = false;
            while ((line = stdout.readLine()) != null) {
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

            // 에러 로그 출력 (필요 시)
            while ((line = stderr.readLine()) != null) {
                System.err.println("ERROR: " + line);
            }

            int exitCode = process.waitFor();
            System.out.println("Python script exited with code: " + exitCode);

            // JSON 파싱
            String jsonString = jsonOutput.toString();
            JSONObject result = new JSONObject(jsonString);

            JSONArray jsonArray = result.getJSONArray("attention_score_list");
            List<List<Object>> attentionScoreList = new ArrayList<>();
            for (int i = 0; i < jsonArray.length(); i++) {
                JSONArray innerArray = jsonArray.getJSONArray(i);
                List<Object> innerList = new ArrayList<>();

                for (int j = 0; j < innerArray.length(); j++) {
                    innerList.add(innerArray.get(j));
                }
                attentionScoreList.add(innerList);
            }

            List<Integer> scoreList = listScore(attentionScoreList);


            String videoPoint = result.getString("video_point");

            JSONObject frequencyJson = result.getJSONObject("object_frequency");
            Map<String, Float> objectFrequency = new HashMap<>();
            for (String key : frequencyJson.keySet()) {
                objectFrequency.put(key, (float) frequencyJson.getDouble(key));
            }

//            JSONArray orderArray = result.getJSONArray("object_order");
//            List<String> objectOrder = new ArrayList<>();
//            for (int i = 0; i < orderArray.length(); i++) {
//                objectOrder.add(orderArray.getString(i));
//            }

            return new GazeAnalysisResult(attentionScoreList, videoPoint, objectFrequency, scoreList);

        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }

    }

    // JSON 시작 부분을 찾아서 JSON 문자열을 추출하는 함수
    private String extractJson(String output) {
        int jsonStart = output.indexOf("{");
        if (jsonStart != -1) {
            return output.substring(jsonStart).trim();  // JSON 부분만 추출
        }
        return null;  // JSON 데이터가 없으면 null 반환
    }

    @SuppressWarnings("unchecked")
    @Transactional
    public void saveGazeData(Map<String, Object> payload) throws IOException {
        String videoId = (String) payload.get("videoId");
        String watchDate = (String) payload.get("watchDate");

        // 비디오 크기 값 videoFrame.get("width"), videoFrame.get("height")
        Map<String, Object> videoFrame = null;
        if (payload.get("videoFrame") instanceof Map) {
            videoFrame = (Map<String, Object>) payload.get("videoFrame");
        }
        System.out.println("width: " + videoFrame.get("width"));
        System.out.println("height: " + videoFrame.get("height"));

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
        GazeAnalysisResult result = runPythonScript(videoId, videoCSV, String.valueOf(videoFrame.get("width")), String.valueOf(videoFrame.get("height")));

        if (result != null) {
            System.out.println("Attention Score List: " + result.getAttentionScoreList());
            System.out.println("Video Gaze Visualization: " + result.getGazeVisualization());
            System.out.println("Video Object Frequency: " + result.getObjectFrequency());
//            System.out.println("Video Gaze ObjectOrder: " + result.getObjectOrder());
        } else {
            System.out.println("Python 스크립트 실행 중 오류 발생");
        }

        // youtubeService.getVideoById 사용해서 영상 정보 불러오기
        Video video = youtubeService.getVideoById(videoId);
        if (video != null) {
            VideoSnippet snippet = video.getSnippet();

            // VideoSnippet -> LinkedHashMap
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

            ReceiveIdDto receiveIdDto = new ReceiveIdDto();
            ReceiveId receiveId = receiveIdDto.toEntity(
                    videoId,
                    watchDate,
                    snippetMap,
                    result != null ? result.getAttentionScoreList() : null,
                    result != null ? result.getGazeVisualization() : null,
                    result != null ? result.getObjectFrequency() : null,
                    result != null ? result.getAttentionList() : null

//                    result != null ? result.getObjectOrder() : null
            );


            mongoRepository.save(receiveId);
        } else {
            System.out.println("해당 ID의 영상을 찾지 못했습니다.");
        }
    }

    @Transactional
    public List<ReceiveIdDto> dbData() {
        return mongoRepository.findBy(PageRequest.of(0, 10));
    }

    @Transactional
    public Map averScore(VideoIdRequest videoIdRequest) {

        String videoId = videoIdRequest.getVideoId();

        List<ReceiveId> videoScores = mongoRepository.findByVideoId(videoId);
        System.out.println("비디오 스코어 =" + videoScores);

        int attentionSize = videoScores.get(0).getAttentionList().size();
        List<Double> averageAttentionList = new ArrayList<>();
        System.out.println("사이즈 = " + attentionSize);

        for (int i = 0; i < attentionSize; i++) {
            int sum = 0;
            int count = 0;
            for (ReceiveId receiveId : videoScores) {
                if (i < receiveId.getAttentionList().size()) {
                    sum += receiveId.getAttentionList().get(i);
                    count++;
                }
            }
            averageAttentionList.add(count > 0 ? sum / (double) count : 0.0);  // 평균 계산
        }

        System.out.println("평균집중리스트 = " + averageAttentionList);
        Map<String, Double> adressScoreMap = new HashMap<>();
        List<List<Object>> scoreList = videoScores.get(0).getScoreList();
        System.out.println("스코어 리스트" + scoreList);
        System.out.println("어텐션리스트 사이즈" + averageAttentionList.size());

        for (int i = 0; i < averageAttentionList.size(); i++) {
            String key = (String) scoreList.get(i).get(0);
            Double value = averageAttentionList.get(i);
            System.out.println("키 = " + key);
            System.out.println("벨류 = " + value);
            adressScoreMap.put(key, value);
            System.out.println("어드레스맵 :" + adressScoreMap);
        }

        List<Map.Entry<String, Double>> sortMap = new ArrayList<>(adressScoreMap.entrySet());
        System.out.println("초기 소트맵 : " + sortMap);

        // 내림차순 정렬
        sortMap.sort((sortMap1, sortMap2) -> sortMap2.getValue().compareTo(sortMap1.getValue()));
        System.out.println("정렬 후 소트맵:" + sortMap);


        Map<String, String> sortedMap = new LinkedHashMap<>();
        for (Map.Entry<String, Double> entry : sortMap) {
            sortedMap.put(entry.getKey(), entry.getValue().toString()); // value를 String으로 변환하여 추가
        }

        return sortedMap;
    }

}