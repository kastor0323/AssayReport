import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../scss/Screens/Auth.scss';
import { signup } from '../Api/AuthApi';


const SignUpPage = ({ onLogin }) => {
  const [formData, setFormData] = useState({
    name: '',
    user_id: '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.name || !formData.user_id || !formData.password || !formData.confirmPassword) {
      setError('모든 필드를 입력해주세요.');
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError('비밀번호가 일치하지 않습니다.');
      return;
    }

    if (formData.password.length < 6) {
      setError('비밀번호는 6자 이상이어야 합니다.');
      return;
    }

    try {
      const response = await signup(formData.user_id, formData.password, formData.name);
      
      if (response.data.success) {
        // 회원가입 성공 시 로그인 페이지로 이동
        navigate('/login');
      } else {
        setError(response.data.message || '회원가입에 실패했습니다.');
      }
    } catch (error) {
      if (error.response && error.response.status === 409) {
        setError('이미 존재하는 아이디입니다.');
      } else {
        setError('회원가입 중 오류가 발생했습니다.');
      }
      console.error('Signup error:', error);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-form">
        <h2>회원가입</h2>
        {error && <div className="error-message">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">이름</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="이름을 입력하세요"
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="user_id">아이디</label>
            <input
              type="user_id"
              id="user_id"
              name="user_id"
              value={formData.user_id}
              onChange={handleChange}
              placeholder="아이디를 입력하세요"
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">비밀번호</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="비밀번호를 입력하세요 (6자 이상)"
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="confirmPassword">비밀번호 확인</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              placeholder="비밀번호를 다시 입력하세요"
              required
            />
          </div>
          <button type="submit" className="auth-btn">회원가입</button>
        </form>
        <div className="auth-link">
          이미 계정이 있으신가요? <Link to="/resume/login">로그인</Link>
        </div>
      </div>
    </div>
  );
};

export default SignUpPage; 