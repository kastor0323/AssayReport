import React from 'react';
import '../scss/Screens/Main.scss';

const MainPage = ({ user }) => {
  return (
    <div className="main-container">
      <div className="main-content">
        {/* <h1>안녕하세요, {user?.name || '사용자'}님!</h1>
        <p>블로그 메인 페이지에 오신 것을 환영합니다.</p>
        <div className="main-actions">
          <button className="action-btn">새 글 작성</button>
          <button className="action-btn secondary">최근 글 보기</button> */}
        {/* </div> */}
      </div>
    </div>
  );
};

export default MainPage; 