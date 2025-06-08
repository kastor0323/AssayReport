import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getAssayDetail } from '../Api/AuthApi';
import '../scss/Screens/Record.scss';

const RecordDetailPage = () => {
  const { id } = useParams();
  const [detail, setDetail] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchDetail = async () => {
      try {
        const response = await getAssayDetail(id);
        setDetail(response.data);
      } catch (err) {
        setError('상세 정보를 불러오는 데 실패했습니다.');
      }
    };
    fetchDetail();
  }, [id]);

  if (error) {
    return <div className="error-message">{error}</div>;
  }
  if (!detail) {
    return <div>로딩 중...</div>;
  }

  return (
    <div className="record-detail-container">
      <div className="record-detail-content">
        <h1>{detail.assay_title}</h1>
        <div className="detail-row"><strong>날짜:</strong> {detail.record_date ? detail.record_date.split('T')[0] : ''}</div>
        <div className="detail-row"><strong>직업:</strong> {detail.job}</div>
        <div className="detail-row"><strong>경력:</strong> {detail.state}</div>
        <div className="detail-row"><strong>점수:</strong> {detail.score}</div>
        <div className="detail-row"><strong>자소서 내용</strong></div>
        <div className="detail-content-box">
          {detail.questionAnswers && detail.questionAnswers.length > 0 ? (
            detail.questionAnswers.map((qa, idx) => (
              <div key={idx} style={{ marginBottom: '24px' }}>
                <div style={{ fontWeight: 'bold', marginBottom: '8px' }}>{qa.question}</div>
                <div style={{ background: '#f8f9fa', padding: '12px', borderRadius: '8px' }}>{qa.answer}</div>
              </div>
            ))
          ) : (
            <div>자소서 내용이 없습니다.</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default RecordDetailPage; 