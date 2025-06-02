package com.NLP.resume.assay.domain;

import jakarta.persistence.*;
import lombok.*;

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

  @Column(nullable = false)
  private String assay_title;

  @Column(nullable = false)
  private String assay_content;

  @Column(nullable = false)
  private double score;
}
