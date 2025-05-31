package com.NLP.resume.member.controller;

import com.NLP.resume.member.domain.User;
import com.NLP.resume.member.dto.LoginRequest;
import com.NLP.resume.member.dto.LoginResponse;
import com.NLP.resume.member.dto.SignUpRequest;
import com.NLP.resume.member.dto.SignUpResponse;
import com.NLP.resume.member.service.UserService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    // 1. 회원가입
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

    // 2. 로그인
    @PostMapping("/resume/login")
    public ResponseEntity<LoginResponse> loginProcess(@RequestBody LoginRequest loginRequest) {
        try {
            LoginResponse response = userService.login(loginRequest);

            if (response.isSuccess()) {
                return ResponseEntity.ok(response);
            } else {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(response);
            }
        } catch (Exception e) {
            return ResponseEntity
                    .status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(LoginResponse.builder()
                            .success(false)
                            .message("서버 오류가 발생했습니다: " + e.getMessage())
                            .build());
        }
    }


}
