package com.NLP.resume.assay.dto;

import com.NLP.resume.assay.domain.Assay;
import lombok.*;
import java.time.LocalDateTime;
import java.util.List;
import java.util.ArrayList;

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
  private String job;
  private String state;
  private List<QuestionAnswerDto> questionAnswers;

  @Builder
  @AllArgsConstructor
  @NoArgsConstructor
  @Getter
  @Setter
  public static class QuestionAnswerDto {
    private String question;
    private String answer;
  }

  public SaveAssayResponse(Assay assay) {
    this.assay_id = assay.getAssay_id();
    this.user_id = assay.getUser_id();
    this.record_date = assay.getRecord_date();
    this.assay_title = assay.getAssay_title();
    this.score = assay.getScore();
    this.job = assay.getJob();
    this.state = assay.getState();

    // 질문-답변 파싱
    this.questionAnswers = parseQuestionAnswers(assay.getQuestions(), assay.getAnswers());
  }

  private List<QuestionAnswerDto> parseQuestionAnswers(String questions, String answers) {
    List<QuestionAnswerDto> qaList = new ArrayList<>();

    if (questions == null || answers == null) {
      return qaList;
    }

    String[] questionArray = questions.split("\\|\\|\\|");
    String[] answerArray = answers.split("\\|\\|\\|");

    for (int i = 0; i < Math.min(questionArray.length, answerArray.length); i++) {
      QuestionAnswerDto qa = QuestionAnswerDto.builder()
              .question(questionArray[i].trim())
              .answer(answerArray[i].trim())
              .build();
      qaList.add(qa);
    }

    return qaList;
  }
}
