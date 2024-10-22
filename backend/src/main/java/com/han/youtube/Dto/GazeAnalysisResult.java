package com.han.youtube.Dto;

import lombok.Getter;
import java.util.List;

@Getter
public class GazeAnalysisResult {
    private List<Object> attentionScoreList;
    private String gazeVisualization;

    public GazeAnalysisResult(List<Object> attentionScoreList, String gazeVisualization) {
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
