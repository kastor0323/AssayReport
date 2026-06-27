import React from 'react';
import { Link } from 'react-router-dom';
import '../scss/Navigation/Navigations.scss';

const AppNavigation = ({ user, onLogout }) => {
  return (
    <nav className="app-navigation">
      <div className="nav-container">
        <div className="nav-logo">
          <Link to="/main">자소서 컨설팅</Link>
        </div>
        <div className="nav-menu">
          <Link to="/resume/assay" className="nav-item">메인</Link>
          <Link to="/resume/assay/record" className="nav-item">기록</Link>
          <div className="nav-user">
            <span className="user-name">{user?.name || '사용자'}</span>
            <button onClick={onLogout} className="logout-btn">로그아웃</button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default AppNavigation; 