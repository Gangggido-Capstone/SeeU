package com.han.youtube.Dto;

import com.han.youtube.Domain.ReceiveId;
import lombok.Getter;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@Getter
public class ReceiveIdDto {
    private String videoId;
    private String watchdata;


    public ReceiveId toEntity(String videoId, String watchdata){
        return ReceiveId.builder()
                .videoId(videoId)
                .watchdata(watchdata)
                .build();
    }
}
