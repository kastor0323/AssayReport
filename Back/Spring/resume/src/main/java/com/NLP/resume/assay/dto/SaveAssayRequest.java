package com.NLP.resume.assay.dto;

import lombok.*;

@Builder
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
public class SaveAssayRequest {
  private int assay_id;
  private String user_id;
  private String assay_title;
  private String content;
  private double score;
}
