package com.NLP.resume.member.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class SignUpResponse {
    private String message;
    private String user_id;
    private boolean success;
}
