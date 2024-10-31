package com.han.youtube.Repository;

import com.han.youtube.Domain.ReceiveId;
import com.han.youtube.Dto.ReceiveIdDto;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface MongoRepository extends org.springframework.data.mongodb.repository.MongoRepository<ReceiveId,String> {

    @Query(sort = "{_id: -1}")
    List<ReceiveIdDto> findBy(Pageable pageable);

    @Query(value = "{}", sort = "{_id: -1}")
    List<ReceiveIdDto> findAllBy();

    List<ReceiveId> findByVideoId(String videoId);
}