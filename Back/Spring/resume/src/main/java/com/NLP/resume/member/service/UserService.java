package com.NLP.resume.member.service;

import com.NLP.resume.exception.DuplicateUserIdException;
import com.NLP.resume.member.domain.User;
import com.NLP.resume.member.dto.LoginRequest;
import com.NLP.resume.member.dto.LoginResponse;
import com.NLP.resume.member.repository.UserRepository;
import com.NLP.resume.security.JwtTokenProvider;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtTokenProvider jwtTokenProvider;

    //DB의 user_id colunm 호출
    @Transactional(readOnly = true)
    public boolean existsByUserId(String userId) {
        return userRepository.existsById(userId);  // PK
    }

    // 1. 회원가입 기능
    @Transactional
    public User signUp(User user) {
        //1.회원가입 시 user_id 중복 시 예외처리
        if (existsByUserId(user.getUser_id())) {
            throw new DuplicateUserIdException("이미 존재하는 아이디입니다.");
        }
        //2.회원가입 성공시 password 인코딩 후 DB에 저장
        String encodedPassword = passwordEncoder.encode(user.getPassword());
        user.setPassword(encodedPassword);
        return userRepository.save(user);
    }

    // 2. 로그인 기능
    @Transactional(readOnly = true)
    public LoginResponse login(LoginRequest request) {
        // 1. 아이디로 사용자 찾기
        return userRepository.findById(request.getUser_id())
                .map(user -> {
                    // 2. 비밀번호 확인
                    if (passwordEncoder.matches(request.getPassword(), user.getPassword())) {
                        // 3. 로그인 성공 - JWT 토큰 생성
                        String token = generateToken(user);
                        return LoginResponse.builder()
                                .success(true)
                                .token(token)
                                .user_id(user.getUser_id())
                                .name(user.getName())
                                .message("로그인 성공")
                                .build();
                    } else {
                        // 비밀번호 불일치
                        return LoginResponse.builder()
                                .success(false)
                                .message("비밀번호가 일치하지 않습니다")
                                .build();
                    }
                })
                .orElse(LoginResponse.builder()
                        .success(false)
                        .message("존재하지 않는 사용자입니다")
                        .build());
    }

    // JWT 토큰 생성 메서드 (실제 구현은 JWT 라이브러리 필요)
    private String generateToken(User user) {
        return jwtTokenProvider.createToken(user.getUser_id());
    }
}
