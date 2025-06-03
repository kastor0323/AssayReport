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
              <Route path="/main" element={<Main user={user} />} />
              <Route path="/record" element={<Record />} />
              <Route path="/record/:id" element={<RecordDetail />} />
              <Route path="*" element={<Navigate to="/main" replace />} />
            </>
          ) : (
            // 로그인되지 않은 사용자 라우트
            <>
              <Route path="/login" element={<LogIn onLogin={handleLogin} />} />
              <Route path="/signup" element={<SignUp onLogin={handleLogin} />} />
              <Route path="*" element={<Navigate to="/login" replace />} />
            </>
          )}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
