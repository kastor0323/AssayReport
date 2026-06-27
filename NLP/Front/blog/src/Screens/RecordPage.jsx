import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../scss/Screens/Record.scss';
import { getAssayList } from '../Api/AuthApi';

const RecordPage = () => {
  const [records, setRecords] = useState([]);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchRecords = async () => {
      try {
        const response = await getAssayList();
        setRecords(response.data);
      } catch (err) {
        setError('기록을 불러오는 데 실패했습니다.');
      }
    };
    fetchRecords();
  }, []);

  const handleTitleClick = (assay_id) => {
    navigate(`/resume/assay/record/${assay_id}`);
  };

  const getGradeColor = (score) => {
    if (score >= 80) return '#22c55e'; // 우수
    if (score >= 60) return '#3b82f6'; // 보통
    if (score >= 40) return '#f59e0b'; // 미흡
    return '#ef4444'; // 부족
  };

  return (
    <div className="record-container">
      <div className="record-content">
        <h1>기록 목록</h1>
        {error && <div className="error-message">{error}</div>}
        <div className="record-list">
          {records.length === 0 ? (
            <div>기록이 없습니다.</div>
          ) : (
            records.map(record => (
              <div key={record.assay_id} className="record-item">
                <h3>
                  <span
                    className="record-link"
                    style={{ cursor: 'pointer', color: '#2563eb', textDecoration: 'underline' }}
                    onClick={() => handleTitleClick(record.assay_id)}
                  >
                    {record.assay_title}
                  </span>
                </h3>
                <p className="record-date">날짜: {record.record_date ? record.record_date.split('T')[0] : ''}</p>
                <p className="record-job">직업: {record.job}</p>
                <p className="record-state">경력: {record.state}</p>
                <div className="score-section">
                  <p className="record-score" style={{ color: getGradeColor(record.score) }}>
                    평균 점수: {record.score}점
                  </p>
                  <p className="record-grade" style={{ color: getGradeColor(record.score) }}>
                    등급: {record.grade}
                  </p>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default RecordPage; 