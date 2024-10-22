package com.han.youtube.Dto;

import lombok.Getter;
import lombok.NoArgsConstructor;

import java.util.List;

@NoArgsConstructor
@Getter
public class GazeAnalysisResult {
    private List<Object> attentionScoreList;
    private String gazeVisualization;

    public GazeAnalysisResult(List<Object> attentionScoreList, String gazeVisualization) {
        this.attentionScoreList = attentionScoreList;
        this.gazeVisualization=gazeVisualization;
    }

}
