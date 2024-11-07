package com.han.youtube.service;

import com.han.youtube.Dto.GazeAnalysisResult;
import com.han.youtube.Dto.ReceiveIdDto;
import com.han.youtube.Dto.VideoIdRequest;

import java.io.IOException;
import java.util.List;
import java.util.Map;

public interface GazeDataService {
    GazeAnalysisResult runPythonScript(String videoId, String videoCSV, String videoWidth, String videoHeight);
    void saveGazeData(Map<String, Object> payload) throws IOException;
    List<ReceiveIdDto> dbData();
    List<List<Object>> averScore(VideoIdRequest videoIdRequest);
}
