package com.NLP.resume.assay.repository;

import com.NLP.resume.assay.domain.Assay;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface AssayRepository extends JpaRepository<Assay, Integer> {

  @Query("SELECT s FROM Assay s WHERE s.user_id = :user_id ORDER BY s.assay_id DESC")
  List<Assay> findByUserId(@Param("user_id") String user_id);

  // @Query 어노테이션 추가로 해결
  @Query("SELECT a FROM Assay a WHERE a.assay_id = :assay_id AND a.user_id = :user_id")
  Optional<Assay> findByAssayIdAndUserId(@Param("assay_id") int assay_id, @Param("user_id") String user_id);
}
