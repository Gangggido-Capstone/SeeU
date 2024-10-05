package com.han.youtube.controller;

import com.han.youtube.service.GazeDataService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api")
public class GazeDataController {

    private final GazeDataService gazeDataService;

    @Autowired
    public GazeDataController(GazeDataService gazeDataService) {
        this.gazeDataService = gazeDataService;
    }

    @PostMapping("/save-gaze-data")
    public ResponseEntity<String> saveGazeData(@RequestBody Map<String, Object> payload) {
        try {
            gazeDataService.saveGazeData(payload);
            return new ResponseEntity<>("CSV 파일이 성공적으로 저장되었습니다.", HttpStatus.OK);
        } catch (Exception e) {
            e.printStackTrace();
            return new ResponseEntity<>("CSV 파일 저장 중 오류가 발생했습니다.", HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}
