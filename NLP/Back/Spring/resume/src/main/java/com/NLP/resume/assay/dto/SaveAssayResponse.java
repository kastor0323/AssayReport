package com.NLP.resume.assay.dto;

import com.NLP.resume.assay.domain.Assay;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.*;
import java.time.LocalDateTime;
import java.util.List;
import java.util.ArrayList;
import java.util.Map;

@Builder
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
public class SaveAssayResponse {
  private int assay_id;
  private String user_id;
  private LocalDateTime record_date;
  private String assay_title;
  private double score;
  private String grade;
  private String job;
  private String state;
  private List<QuestionAnswer> questionAnswers;
  private List<Map<String, Object>> evaluationDetails;

  @Builder
  @AllArgsConstructor
  @NoArgsConstructor
  @Getter
  @Setter
  public static class QuestionAnswer {
    private String question;
    private String answer;
  }

  public SaveAssayResponse(Assay assay) {
    this.assay_id = assay.getAssay_id();
    this.user_id = assay.getUser_id();
    this.record_date = assay.getRecord_date();
    this.assay_title = assay.getAssay_title();
    this.score = assay.getScore();
    this.grade = assay.getGrade();
    this.job = assay.getJob();
    this.state = assay.getState();

    // 질문-답변 쌍 파싱
    String[] questions = assay.getQuestions().split("\\|\\|\\|");
    String[] answers = assay.getAnswers().split("\\|\\|\\|");
    this.questionAnswers = new ArrayList<>();
    for (int i = 0; i < questions.length; i++) {
      this.questionAnswers.add(new QuestionAnswer(questions[i], answers[i]));
    }

    // 평가 상세 정보 파싱
    try {
      ObjectMapper mapper = new ObjectMapper();
      this.evaluationDetails = mapper.readValue(assay.getEvaluation_details(), List.class);
    } catch (Exception e) {
      this.evaluationDetails = new ArrayList<>();
    }
  }
}
