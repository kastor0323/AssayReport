package com.NLP.resume.assay.service;

import com.NLP.resume.assay.domain.Assay;
import com.NLP.resume.assay.dto.SaveAssayRequest;
import com.NLP.resume.assay.dto.SaveAssayResponse;
import com.NLP.resume.assay.repository.AssayRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.beans.Transient;

@Service
@RequiredArgsConstructor
public class AssayService {

  private final AssayRepository assayRepository;

  @Transient
  public SaveAssayResponse saveAssay(SaveAssayRequest request) {
    try{

      Assay assay = Assay.builder()
          .user_id(request.getUser_id())
          .assay_title(request.getAssay_title())
          .assay_content(request.getContent())
          .score(request.getScore())
          .build();

      Assay savedAssay = assayRepository.save(assay);

      return new SaveAssayResponse(savedAssay);
    } catch (Exception e){
      throw new RuntimeException("자소서 저장 중 오류가 발생했습니다" + e.getMessage());
    }
  }



}
