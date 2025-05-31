package com.NLP.resume.member.domain;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

/*
    클래스 설명 : 해당 클래스는 DB Table에 대한 설정
 */
@Builder
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
@Entity
@Table(name = "user")
public class User {

    @Id
    @Column(unique = true, nullable = false)
    private String user_id; //유저아이디 = 이메일

    @Column(nullable = false)
    private String password; //비밀번호(암호화되어 저장)

    @Column(nullable = false)
    private String name; //이름
}