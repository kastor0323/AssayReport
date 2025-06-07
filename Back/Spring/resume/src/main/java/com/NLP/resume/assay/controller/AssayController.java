package com.NLP.resume.assay.controller;

import com.NLP.resume.assay.dto.SaveAssayRequest;
import com.NLP.resume.assay.dto.SaveAssayResponse;
import com.NLP.resume.assay.service.AssayService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.apache.coyote.BadRequestException;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;


@RequiredArgsConstructor
@RestController
public class AssayController {

  private final AssayService assayService;

  @PostMapping("/resume/assay/save")
  public ResponseEntity<SaveAssayResponse> SaveAssay(@Valid @RequestBody SaveAssayRequest request, Authentication authentication) {
    try {
      String user_id = authentication.getName();
      request.setUser_id(user_id);

      SaveAssayResponse response = assayService.saveAssay(request); // 파라미터 1개만 전달
      return ResponseEntity.ok(response);
    } catch (Exception e) {
      return ResponseEntity.badRequest().build();
    }
  }

  @GetMapping("/resume/assay/get")
  public ResponseEntity<List<SaveAssayResponse>> getAssay(Authentication authentication) {

    String userId = authentication.getName();

    List<SaveAssayResponse> responses = assayService.getAssaysByUserId(userId);
    return ResponseEntity.ok(responses);
  }

  @GetMapping("/resume/assay/record/detail/{record_id}")
  public ResponseEntity<SaveAssayResponse> getAssayDetail(@PathVariable int record_id, Authentication authentication) throws BadRequestException {

    String userId = authentication.getName();
    SaveAssayResponse response = assayService.getAssayDetail(record_id, userId);

    return ResponseEntity.ok(response);
  }
}