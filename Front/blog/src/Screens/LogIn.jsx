import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../scss/Screens/Auth.scss';

const LogIn = ({ onLogin }) => {
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

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!formData.user_id || !formData.password) {
      setError('아이디와 비밀번호를 입력해주세요.');
      return;
    }

    // 간단한 로그인 로직 (실제로는 API 호출)
    const userData = {
      id: 1,
      name: '사용자',
      user_id: formData.user_id
    };

    onLogin(userData);
    navigate('/main');
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

export default LogIn; 