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
  private int assay_id;

  @Column(nullable = false)
  private String user_id;

  @Column(nullable = false, name = "recordDate")
  @CreatedDate
  private LocalDateTime record_date;

  @Column(nullable = false)
  private String assay_title;

  @Column(nullable = false)
  private double score;

  @Column(length = 100, nullable = false)
  private String job;

  @Column(length = 50, nullable = false)
  private String state;

  @Column(columnDefinition = "LONGTEXT", nullable = false)
  private String question;

  @Column(columnDefinition = "LONGTEXT", nullable = false)
  private String answer;

  // 질문과 답변을 개별 필드로 분리
  @Column(columnDefinition = "LONGTEXT", nullable = false)
  private String questions; // "질문1|||질문2|||질문3" 형태

  @Column(columnDefinition = "LONGTEXT", nullable = false)
  private String answers; // "답변1|||답변2|||답변3" 형태
}


