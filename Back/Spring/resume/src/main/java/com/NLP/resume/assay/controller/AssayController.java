package com.NLP.resume.assay.controller;

import com.NLP.resume.member.domain.User;
import com.NLP.resume.member.dto.SignUpRequest;
import com.NLP.resume.member.dto.SignUpResponse;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

public class AssayController {

  @PostMapping("/resume/signup")
  public ResponseEntity<SignUpResponse> signUp(@Valid @RequestBody SignUpRequest request) {
    try {
      User newUser = request.toEntity();
      User savedUser = userService.signUp(newUser);

      return ResponseEntity.ok(
          new SignUpResponse("회원가입 성공", savedUser.getUser_id(), true)
      );
    } catch (Exception e) {
      // 이미 존재하는 아이디 예외 체크 (예외 메시지로 판단)
      if (e.getMessage() != null && e.getMessage().contains("이미 존재하는 아이디")) {
        return ResponseEntity
            .status(HttpStatus.CONFLICT) // 409 Conflict
            .body(new SignUpResponse("이미 존재하는 아이디입니다", request.getUser_id(), false));
      }

      // 기타 서버 에러
      return ResponseEntity
          .status(HttpStatus.INTERNAL_SERVER_ERROR)
          .body(new SignUpResponse("회원가입 중 오류가 발생했습니다: " + e.getMessage(),
              request.getUser_id(), false));
    }
  }
}
