package com.han.youtube.Dto;

import com.google.api.services.youtube.model.VideoSnippet;
import com.han.youtube.Domain.ReceiveId;
import lombok.Getter;
import lombok.NoArgsConstructor;


@NoArgsConstructor
@Getter
public class ReceiveIdDto {
    private String videoId;
    private String watchdata;
    private VideoSnippet snippet;

    public ReceiveId toEntity(String videoId, String watchdata, VideoSnippet snippet) {
        return ReceiveId.builder()
                .videoId(videoId)
                .watchdata(watchdata)
                .snippet(snippet)
                .build();
    }
}