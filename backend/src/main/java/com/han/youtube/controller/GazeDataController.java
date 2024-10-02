package com.han.youtube.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;

import java.io.FileWriter;
import java.io.IOException;
import java.util.List;
import java.util.Map;

@RestController
@CrossOrigin(origins = "http://localhost:9000")
public class GazeDataController {

    // 시선 데이터 저장 요청을 처리하는 엔드포인트
    @PostMapping("api/save-gaze-data")
    public ResponseEntity<String> saveGazeData(@RequestBody List<Map<String, Object>> gazeRecords) {
        String filePath = "C:/youtube-seeso-demo/Data/GazeData/gaze_data.csv"; // 원하는 경로로 변경 가능

        try (FileWriter writer = new FileWriter(filePath)) {
            // CSV 파일 헤더
            writer.append("Time,X,Y\n");

            // 시선 좌표 데이터를 CSV 파일에 작성
            for (Map<String, Object> record : gazeRecords) {
                writer.append(record.get("time").toString())
                        .append(",")
                        .append(record.get("x").toString())
                        .append(",")
                        .append(record.get("y").toString())
                        .append("\n");
            }

            writer.flush(); // 파일 작성 완료
            return ResponseEntity.ok("파일 저장 성공: " + filePath);
        } catch (IOException e) {
            e.printStackTrace();
            return ResponseEntity.status(500).body("파일 저장 실패");
        }
    }
}