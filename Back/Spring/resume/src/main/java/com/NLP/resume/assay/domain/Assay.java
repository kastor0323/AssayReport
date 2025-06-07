package com.NLP.resume.assay.domain;

import jakarta.persistence.*;
import lombok.*;
import org.springframework.data.annotation.CreatedDate;

import java.time.LocalDateTime;

@Builder
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
@Entity
@Table(name = "assay")
public class Assay {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(nullable = false)
  private int assay_id; //번호 자동 부여

  @Column(nullable = false)
  private String user_id;

  @Column(nullable = false, name = "recordDate")
  @CreatedDate
  private LocalDateTime record_date; //record date ex)2025:05:24:09:00:00

  @Column(nullable = false)
  private String assay_title;

  @Column(nullable = false)
  private String assay_content;

  @Column(nullable = false)
  private double score;

  // 새로 추가된 필드들
  @Column(length = 100, nullable = false)
  private String job;

  @Column(length = 50, nullable = false)
  private String state; //신입, 인턴
}
