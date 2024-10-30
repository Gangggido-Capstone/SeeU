package com.han.youtube.Dto;

import lombok.Getter;
import lombok.NoArgsConstructor;

import java.util.List;
import java.util.Map;

@NoArgsConstructor
@Getter
public class GazeAnalysisResult {
    private List<List<Object>> attentionScoreList; // 비디오 집중 점수
    private String gazeVisualization; // 비디오 파일 경로

    public GazeAnalysisResult(List<List<Object>> attentionScoreList, String gazeVisualization) {
        this.attentionScoreList = attentionScoreList;
        this.gazeVisualization = gazeVisualization;
    }

    @Override
    public String toString() {
        return "GazeDataResult{" +
                "attentionScoreList=" + attentionScoreList +
                ", gazeVisualization='" + gazeVisualization + '\'' +
                '}';
    }
}
