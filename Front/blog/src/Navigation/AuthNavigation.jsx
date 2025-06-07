import React from 'react';
import { Link } from 'react-router-dom';
import '../scss/Navigation/Navigations.scss';

const AuthNavigation = () => {
  return (
    <nav className="auth-navigation">
      <div className="nav-container">
        <div className="nav-logo">
          <Link to="/resume/login">자소서 컨설팅</Link>
        </div>
      </div>
    </nav>
  );
};

export default AuthNavigation; 