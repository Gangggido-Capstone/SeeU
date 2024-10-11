package com.han.youtube.Domain;


import com.google.api.services.youtube.model.VideoSnippet;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "Capstone")
@Getter
@NoArgsConstructor
public class ReceiveId {
    private String videoId;
    private String watchdata;
    private VideoSnippet snippet;

    @Builder
    public ReceiveId(String videoId, String watchdata, VideoSnippet snippet) {
        this.videoId = videoId;
        this.watchdata = watchdata;
        this.snippet = snippet;
    }
}