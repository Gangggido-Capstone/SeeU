package com.han.youtube.Dto;

import com.han.youtube.Domain.ReceiveId;
import lombok.Getter;
import lombok.NoArgsConstructor;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

@NoArgsConstructor
@Getter
public class ReceiveIdDto {
    private String videoId;
    private String watchdata;
    private LinkedHashMap<String, Object> snippet;
    private List<List<Object>> scoreList;
    private String visualization;
    private Map<String, Float> objectFrequency;
//    private List<String> objectOrder;

    public ReceiveIdDto(String videoId, String watchdata, LinkedHashMap<String, Object> snippet, List<List<Object>> scoreList, String visualization, Map<String, Float> objectFrequency) {
        this.videoId = videoId;
        this.watchdata = watchdata;
        this.snippet = snippet;
        this.scoreList = scoreList;
        this.visualization = visualization;
        this.objectFrequency = objectFrequency;
    }

    public ReceiveId toEntity(String videoId, String watchdata, LinkedHashMap<String, Object> snippet, List<List<Object>> scoreList, String visualization, Map<String, Float> objectFrequency) {
        return ReceiveId.builder()
                .videoId(videoId)
                .watchdata(watchdata)
                .snippet(snippet)
                .scoreList(scoreList)
                .visualization(visualization)
                .objectFrequency(objectFrequency)
                .build();
    }
}
