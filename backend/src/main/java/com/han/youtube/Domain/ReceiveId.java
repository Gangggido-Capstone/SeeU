package com.han.youtube.Domain;

import jakarta.persistence.Id;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.LinkedHashMap;
import java.util.List;

@Document(collection = "Capstone")
@Getter
@NoArgsConstructor
public class ReceiveId {
    @Id
    private String id;
    private String videoId;
    private String watchdata;
    private LinkedHashMap<String, Object> snippet;

    private List<Object> scoreList;
    private String visualization;

    @Builder
    public ReceiveId(String videoId, String watchdata, LinkedHashMap<String, Object> snippet, List<Object> scoreList, String visualization) {
        this.videoId = videoId;
        this.watchdata = watchdata;
        this.snippet = snippet;
        this.scoreList = scoreList;
        this.visualization = visualization;
    }
}