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
        <div className="detail-row"><strong>평균 점수:</strong> {detail.score}점</div>
        <div className="detail-row"><strong>등급:</strong> {detail.grade}</div>
        
        <div className="detail-row"><strong>자소서 내용 및 평가</strong></div>
        <div className="detail-content-box">
          {detail.questionAnswers && detail.questionAnswers.length > 0 ? (
            detail.questionAnswers.map((qa, idx) => {
              const evaluation = detail.evaluationDetails?.[idx];
              return (
                <div key={idx} className="qa-section">
                  <div className="question-section">
                    <h3>질문 {idx + 1}</h3>
                    <div className="question-content">{qa.question}</div>
                  </div>
                  <div className="answer-section">
                    <h3>답변 {idx + 1}</h3>
                    <div className="answer-content">{qa.answer}</div>
                  </div>
                  {evaluation && (
                    <div className="evaluation-section">
                      <h3>평가 결과</h3>
                      <div className="evaluation-content">
                        <p><strong>점수:</strong> {evaluation.종합점수}점</p>
                      </div>
                    </div>
                  )}
                </div>
              );
            })
          ) : (
            <div>자소서 내용이 없습니다.</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default RecordDetailPage; 