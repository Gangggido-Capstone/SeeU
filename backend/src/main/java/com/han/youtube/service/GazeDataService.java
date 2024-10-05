package com.han.youtube.service;

import org.springframework.stereotype.Service;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;
import java.util.Map;

@Service
public class GazeDataService {
    public void saveGazeData(Map<String, Object> payload) throws IOException {
        String videoId = (String) payload.get("videoId");
        String watchDate = (String) payload.get("watchDate");

        // 비디오 크기 값 videoFrame.get("width"), videoFrame.get("height")
        Map<String, Object> videoFrame = null;
        if (payload.get("videoFrame") instanceof Map) {
            videoFrame = (Map<String, Object>) payload.get("videoFrame");
        }

        // 시선 데이터
        List<Map<String, Object>> gazeData = null;
        if (payload.get("gazeData") instanceof List) {
            gazeData = (List<Map<String, Object>>) payload.get("gazeData");
        }

        // CSV 파일 경로 설정
        String filePath = "C:/youtube-seeso-demo/Data/GazeData/" + videoId + "_" + watchDate.replace(":", "-") + ".csv";

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath))) {
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
                        .append(record.get("attention") != null ? record.get("attention").toString() : "null")
                        .append("\n");
            }

            writer.flush();  // 파일에 데이터 저장
        }
    }
}
