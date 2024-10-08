package com.han.youtube.service;

import com.han.youtube.Domain.ReceiveId;
import com.han.youtube.Dto.ReceiveIdDto;
import com.han.youtube.Repository.MongoRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

import java.util.List;
import java.util.Map;


@Service
@RequiredArgsConstructor
public class GazeDataService {

    private final MongoRepository mongoRepository;
    public void saveGazeData(Map<String, Object> payload) throws IOException {
        String videoId = (String) payload.get("videoId");
        String watchDate = (String) payload.get("watchDate");

        // 영상 ID, 시간 저장
        ReceiveIdDto receiveIdDto = new ReceiveIdDto();
        ReceiveId receiveId = receiveIdDto.toEntity(videoId,watchDate);
        mongoRepository.save(receiveId);

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
        String filePath = "../Data/GazeData/" + videoId + "_" + watchDate + ".csv";

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
                        .append(record.get("attention") != null ? record.get("attention").toString() : "3")
                        .append("\n");
            }

            writer.flush();  // 파일에 데이터 저장
        }
    }
}
