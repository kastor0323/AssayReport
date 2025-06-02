import React from 'react';
import { Link } from 'react-router-dom';
import '../scss/Screens/Record.scss';

const Record = () => {
  const records = [
    { id: 1, title: '첫 번째 기록', date: '2024-01-01', summary: '첫 번째 기록입니다.' },
    { id: 2, title: '두 번째 기록', date: '2024-01-02', summary: '두 번째 기록입니다.' },
    { id: 3, title: '세 번째 기록', date: '2024-01-03', summary: '세 번째 기록입니다.' }
  ];

  return (
    <div className="record-container">
      <div className="record-content">
        <h1>기록 목록</h1>
        <div className="record-list">
          {records.map(record => (
            <div key={record.id} className="record-item">
              <h3>
                <Link to={`/record/${record.id}`} className="record-link">
                  {record.title}
                </Link>
              </h3>
              <p className="record-date">{record.date}</p>
              <p className="record-summary">{record.summary}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Record; 