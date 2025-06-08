package com.NLP.resume.assay.service;

import com.NLP.resume.assay.domain.Assay;
import com.NLP.resume.assay.dto.SaveAssayRequest;
import com.NLP.resume.assay.dto.SaveAssayResponse;
import com.NLP.resume.assay.repository.AssayRepository;
import org.springframework.transaction.annotation.Transactional;
import lombok.RequiredArgsConstructor;
import org.apache.coyote.BadRequestException;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.ArrayList;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class AssayService {

  private final AssayRepository assayRepository;

  @Transactional
  public SaveAssayResponse saveAssay(SaveAssayRequest request) throws BadRequestException {
    try {
      List<String> questions = new ArrayList<>();
      List<String> answers = new ArrayList<>();

      for (SaveAssayRequest.QuestionAnswer qa : request.getQuestionAnswers()) {
        questions.add(qa.getQuestion());
        answers.add(qa.getAnswer());
      }

      String questionsStr = String.join("|||", questions);
      String answersStr = String.join("|||", answers);
      LocalDateTime now = LocalDateTime.now().truncatedTo(ChronoUnit.MINUTES);

      Assay assay = Assay.builder()
              .user_id(request.getUser_id()) // 컨트롤러에서 설정된 값 사용
              .record_date(now)
              .assay_title(request.getAssay_title())
              .questions(questionsStr)
              .answers(answersStr)
              .score(request.getScore())
              .job(request.getJob())
              .state(request.getState())
              .build();

      Assay savedAssay = assayRepository.save(assay);
      return new SaveAssayResponse(savedAssay);

    } catch (Exception e) {
      throw new BadRequestException("자소서 저장 중 오류가 발생했습니다: " + e.getMessage());
    }
  }


  // 사용자 별 assay 기록 가져오기
  @Transactional(readOnly = true)
  public List<SaveAssayResponse> getAssaysByUserId(String userId) {
    List<Assay> assays = assayRepository.findByUserId(userId);
    return assays.stream()
            .map(SaveAssayResponse::new)
            .collect(Collectors.toList());
  }

  @Transactional(readOnly = true)
  public SaveAssayResponse getAssayDetail(int assay_id, String user_id) throws BadRequestException {
    // ID와 사용자로 조회
    Assay assay = assayRepository.findByAssayIdAndUserId(assay_id, user_id)
            .orElseThrow(() -> new BadRequestException("해당 자소서를 찾을 수 없습니다."));

    return new SaveAssayResponse(assay);
  }

  // 질문-답변 분리 유틸리티 메서드 (필요시 사용)
  private List<SaveAssayRequest.QuestionAnswer> parseQuestionAnswers(String questions, String answers) {
    List<SaveAssayRequest.QuestionAnswer> qaList = new ArrayList<>();

    if (questions == null || answers == null) {
      return qaList;
    }

    String[] questionArray = questions.split("\\|\\|\\|");
    String[] answerArray = answers.split("\\|\\|\\|");

    for (int i = 0; i < Math.min(questionArray.length, answerArray.length); i++) {
      SaveAssayRequest.QuestionAnswer qa = SaveAssayRequest.QuestionAnswer.builder()
              .question(questionArray[i].trim())
              .answer(answerArray[i].trim())
              .build();
      qaList.add(qa);
    }

    return qaList;
  }
}
