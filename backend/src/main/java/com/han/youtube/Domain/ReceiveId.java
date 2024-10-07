package com.han.youtube.Domain;


import jakarta.persistence.Id;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "Capstone")
@Getter
@NoArgsConstructor
public class ReceiveId {
    @Id
    private String id;
    private String videoId;
    private String watchdata;

    @Builder
    public ReceiveId(String videoId, String watchdata){
        this.videoId = videoId;
        this.watchdata = watchdata;
    }
}
