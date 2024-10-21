package com.han.youtube.Dto;

import java.util.List;

public class GazeDataResult {
    private List<Object> attentionScoreList;
    private String videoPoint;

    public GazeDataResult(List<Object> attentionScoreList, String videoPoint) {
        this.attentionScoreList = attentionScoreList;
        this.videoPoint = videoPoint;
    }

    public List<Object> getAttentionScoreList() {
        return attentionScoreList;
    }

    public String getVideoPoint() {
        return videoPoint;
    }

    @Override
    public String toString() {
        return "GazeDataResult{" +
                "attentionScoreList=" + attentionScoreList +
                ", videoPoint='" + videoPoint + '\'' +
                '}';
    }
}
