package com.NLP.resume.assay.controller;

import com.NLP.resume.assay.dto.SaveAssayRequest;
import com.NLP.resume.assay.dto.SaveAssayResponse;
import com.NLP.resume.assay.service.AssayService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;


@RequiredArgsConstructor
@RestController
public class AssayController {

  private final AssayService assayService;

  @PostMapping("/resume/assay/save")
  public ResponseEntity<SaveAssayResponse> signUp(@Valid @RequestBody SaveAssayRequest request, Authentication authentication) {
    try {
      String user_id = authentication.getName();
      request.setUser_id(user_id);

      SaveAssayResponse response = assayService.saveAssay(request); // 파라미터 1개만 전달
      return ResponseEntity.ok(response);
    } catch (Exception e) {
      return ResponseEntity.badRequest().build();
    }
  }
}