package com.NLP.resume.assay.dto;

import com.NLP.resume.assay.domain.Assay;
import jakarta.persistence.Column;
import lombok.*;
import org.springframework.data.annotation.CreatedDate;

import java.time.LocalDateTime;

@Builder
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
public class SaveAssayResponse {

  private int assay_id;
  private String user_id;
  private LocalDateTime record_date; //record date ex)2025:05:24:09:00:00
  private String assay_title;
  private String assay_content;
  private double score;
  private String job;
  private String state;

  public SaveAssayResponse(Assay assay) {
    this.assay_id = assay.getAssay_id();
    this.user_id = assay.getUser_id();
    this.record_date = assay.getRecord_date();
    this.assay_title = assay.getAssay_title();
    this.assay_content = assay.getAssay_content();
    this.score = assay.getScore();
    this.job = assay.getJob();
    this.state = assay.getState();
  }
}
