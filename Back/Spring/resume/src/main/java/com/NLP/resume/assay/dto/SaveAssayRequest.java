package com.NLP.resume.assay.dto;

import lombok.*;
import java.util.List;

@Builder
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
public class SaveAssayRequest {
  private String user_id;
  private String assay_title;
  private double score;
  private String job;
  private String state;

  // 질문-답변 리스트
  private List<QuestionAnswer> questionAnswers;

  @Builder
  @AllArgsConstructor
  @NoArgsConstructor
  @Getter
  @Setter
  public static class QuestionAnswer {
    private String question;
    private String answer;
  }
}
