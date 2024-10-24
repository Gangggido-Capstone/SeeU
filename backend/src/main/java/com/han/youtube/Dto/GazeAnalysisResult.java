package com.han.youtube.Dto;

import lombok.Getter;
import lombok.NoArgsConstructor;

import java.util.List;

@NoArgsConstructor
@Getter
public class GazeAnalysisResult {
    private List<List<Object>> attentionScoreList;
    private String gazeVisualization;

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
