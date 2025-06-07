package com.NLP.resume.assay.dto;

import jakarta.persistence.Column;
import lombok.*;
import org.springframework.data.annotation.CreatedDate;

import java.time.LocalDateTime;

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
  private String job;
  private String state;
}
