package com.NLP.resume.member.dto;

import com.NLP.resume.member.domain.User;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@NoArgsConstructor
@AllArgsConstructor
public class SignUpRequest {

    @NotBlank(message = "이메일은 필수 입력값입니다.")
    private String user_id;

    @NotBlank(message = "비밀번호는 필수 입력값입니다.")
    private String password;

    @NotBlank(message = "이름은 필수 입력값입니다.")
    private String name;

    public User toEntity() {
        return User.builder()
                .user_id(user_id)
                .password(password) // 실제 구현시 암호화 필요
                .name(name)
                .build();
    }
}