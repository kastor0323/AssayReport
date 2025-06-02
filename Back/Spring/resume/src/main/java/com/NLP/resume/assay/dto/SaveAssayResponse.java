package com.NLP.resume.assay.dto;

import com.NLP.resume.assay.domain.Assay;
import lombok.*;

import java.time.LocalDateTime;

@Builder
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
public class SaveAssayResponse {

  private int assay_id;
  private String user_id;
  private String assay_title;
  private String assay_content;
  private double score;

  public SaveAssayResponse(Assay assay) {
    this.assay_id = assay.getAssay_id();
    this.user_id = assay.getUser_id();
    this.assay_title = assay.getAssay_title();
    this.assay_content = assay.getAssay_content();
    this.score = assay.getScore();
  }
}
