import React from 'react';
import { useParams, Link } from 'react-router-dom';
import '../scss/Screens/RecordDetail.scss';

const RecordDetailPage = () => {
  const { id } = useParams();
  
  // 임시 데이터 (실제로는 API에서 가져올 데이터)
  const record = {
    id: id,
    title: `기록 ${id}`,
    date: '2024-01-01',
    content: `이것은 기록 ${id}의 상세 내용입니다. 실제 블로그 포스트의 내용이 여기에 표시됩니다.`
  };

  return (
    <div className="record-detail-container">
      <div className="record-detail-content">
        <Link to="/record" className="back-link">← 기록 목록으로 돌아가기</Link>
        <article className="record-detail">
          <h1>{record.title}</h1>
          <p className="record-date">{record.date}</p>
          <div className="record-content">
            {record.content}
          </div>
        </article>
      </div>
    </div>
  );
};

export default RecordDetailPage; 