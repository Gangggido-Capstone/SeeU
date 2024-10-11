package com.han.youtube.Dto;

import com.han.youtube.Domain.ReceiveId;
import lombok.Getter;
import lombok.NoArgsConstructor;
import java.util.LinkedHashMap;

@NoArgsConstructor
@Getter
public class ReceiveIdDto {
    private String videoId;
    private String watchdata;
    private LinkedHashMap<String, Object> snippet;

    public ReceiveIdDto(String videoId, String watchdata, LinkedHashMap<String, Object> snippet) {
        this.videoId = videoId;
        this.watchdata = watchdata;
        this.snippet = snippet;
    }

    public ReceiveId toEntity(String videoId, String watchdata, LinkedHashMap<String, Object> snippet) {
        return ReceiveId.builder()
                .videoId(videoId)
                .watchdata(watchdata)
                .snippet(snippet)
                .build();
    }
}