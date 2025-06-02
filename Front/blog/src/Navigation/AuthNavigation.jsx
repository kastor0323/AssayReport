import React from 'react';
import { Link } from 'react-router-dom';
import '../scss/Navigation/Navigations.scss';

const AuthNavigation = () => {
  return (
    <nav className="auth-navigation">
      <div className="nav-container">
        <div className="nav-logo">
          <Link to="/login">블로그</Link>
        </div>
        <div className="nav-menu">
          <Link to="/login" className="nav-item">로그인</Link>
          <Link to="/signup" className="nav-item">회원가입</Link>
        </div>
      </div>
    </nav>
  );
};

export default AuthNavigation; 