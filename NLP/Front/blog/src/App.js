import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';

// Navigation Components
import AppNavigation from './Navigation/AppNavigation';
import AuthNavigation from './Navigation/AuthNavigation';

// Screen Components
import LogIn from './Screens/LoginPage';
import SignUp from './Screens/SignUpPage';
import Main from './Screens/MainPage';
import Record from './Screens/RecordPage';
import RecordDetail from './Screens/RecordDetailPage';

function App() {
  const [user, setUser] = useState(null);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('isLoggedIn');
    setUser(null);
  };

  return (
    <Router>
      <div className="App">
        {user ? (
          <AppNavigation user={user} onLogout={handleLogout} />
        ) : (
          <AuthNavigation />
        )}
        
        <Routes>
          {user ? (
            // 로그인된 사용자 라우트
            <>
              <Route path="/resume/assay" element={<Main user={user} />} />
              <Route path="/resume/assay/record" element={<Record />} />
              <Route path="/resume/assay/record/:id" element={<RecordDetail />} />
              <Route path="*" element={<Navigate to="/resume/assay" replace />} />
            </>
          ) : (
            // 로그인되지 않은 사용자 라우트
            <>
              <Route path="/resume/login" element={<LogIn onLogin={handleLogin} />} />
              <Route path="/resume/signup" element={<SignUp onLogin={handleLogin} />} />
              <Route path="*" element={<Navigate to="/resume/login" replace />} />
            </>
          )}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
