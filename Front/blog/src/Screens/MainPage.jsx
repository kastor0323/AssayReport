import React, { useState } from 'react';
import '../scss/Screens/Main.scss';
import { postAssay } from '../Api/AuthApi';

const MainPage = ({ user }) => {
  const [formData, setFormData] = useState({
    jobTitle: '',
    experience: '신입',
    title: '',
    content: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleToggle = () => {
    setFormData({
      ...formData,
      experience: formData.experience === '신입' ? '인턴' : '신입'
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.jobTitle || !formData.title || !formData.content) {
      setError('모든 필드를 입력해주세요.');
      setSuccess('');
      return;
    }
    setError('');
    setSuccess('');
    const payload = {
      assay_title: formData.title,
      content: formData.content,
      score: 75,
      job: formData.jobTitle,
      state: formData.experience
    };
    try {
      await postAssay(payload);
      setSuccess('자소서가 성공적으로 저장되었습니다!');
      setFormData({ jobTitle: '', experience: '신입', title: '', content: '' });
    } catch (error) {
      setError('저장 중 오류가 발생했습니다.');
      setSuccess('');
      console.error('Error:', error);
    }
  };

  return (
    <div className="main-container">
      <div className="main-content">
        <h1>자소서 작성</h1>
        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}
        <form onSubmit={handleSubmit} className="resume-form">
          <div className="row-group">
            <div className="form-group job-group">
              <label htmlFor="jobTitle">희망 직업</label>
              <input
                type="text"
                id="jobTitle"
                name="jobTitle"
                value={formData.jobTitle}
                onChange={handleChange}
                placeholder="희망하시는 직업을 입력하세요"
                required
              />
            </div>
            <div className="form-group exp-group">
              <label htmlFor="experience">경력</label>
              <select
                id="experience"
                name="experience"
                value={formData.experience}
                onChange={handleChange}
                className="dropdown-select"
                required
              >
                <option value="신입">신입</option>
                <option value="인턴">인턴</option>
              </select>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="title">제목</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              placeholder="자소서 제목을 입력하세요"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="content">자소서 내용</label>
            <textarea
              id="content"
              name="content"
              value={formData.content}
              onChange={handleChange}
              placeholder="자소서 내용을 입력하세요"
              required
              rows="10"
            />
          </div>

          <button type="submit" className="submit-btn">자소서 평가 받기</button>
        </form>
      </div>
    </div>
  );
};

export default MainPage; 