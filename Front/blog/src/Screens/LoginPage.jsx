import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { login } from '../Api/AuthApi';
import '../scss/Screens/Auth.scss';

const LoginPage = ({ onLogin }) => {
  const [formData, setFormData] = useState({
    user_id: '',
    password: ''
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
    
    if (!formData.user_id || !formData.password) {
      setError('아이디와 비밀번호를 입력해주세요.');
      return;
    }

    try {
      const response = await login(formData.user_id, formData.password);
      
      if (response.data.success) {
        const userData = {
          user_id: response.data.user_id,
          name: response.data.name
        };        
        onLogin(userData);
      } else {
        setError(response.data.message || '로그인에 실패했습니다.');
      }
    } catch (error) {
      if (error.response && error.response.status === 401) {
        setError('아이디 또는 비밀번호가 일치하지 않습니다.');
      } else {
        setError('로그인 중 오류가 발생했습니다.');
      }
      console.error('Login error:', error);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-form">
        <h2>로그인</h2>
        {error && <div className="error-message">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="user_id">아이디</label>
            <input
              type="text"
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
              placeholder="비밀번호를 입력하세요"
              required
            />
          </div>
          <button type="submit" className="auth-btn">로그인</button>
        </form>
        <div className="auth-link">
          계정이 없으신가요? <Link to="/signup">회원가입</Link>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;