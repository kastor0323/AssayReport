package com.NLP.resume.assay.repository;

import com.NLP.resume.assay.domain.Assay;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface AssayRepository extends JpaRepository<Assay, Integer> {

  @Query("SELECT s FROM Assay s WHERE s.user_id = :user_id")
  List<Assay> findByUserId(@Param("user_id") String user_id);
}
