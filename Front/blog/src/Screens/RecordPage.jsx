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
                <p className="record-score">점수: {record.score}</p>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default RecordPage; 