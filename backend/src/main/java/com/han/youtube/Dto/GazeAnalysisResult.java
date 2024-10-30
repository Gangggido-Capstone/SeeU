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
    private Map<String, Float> objectFrequency; // 객체 빈도수
    private List<Integer> attentionList; // 분할된 영상의 집중 점수 List

    public GazeAnalysisResult(List<List<Object>> attentionScoreList, String gazeVisualization, Map<String, Float> objectFrequency, List<Integer> attentionList) {
        this.attentionScoreList = attentionScoreList;
        this.gazeVisualization = gazeVisualization;
        this.objectFrequency = objectFrequency;
        this.attentionList = attentionList;
    }

    @Override
    public String toString() {
        return "GazeDataResult{" +
                "attentionScoreList=" + attentionScoreList +
                ", gazeVisualization='" + gazeVisualization +
                ", objectFrequency='" + objectFrequency + '\'' +
                '}';
    }
}