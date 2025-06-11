import React, { useState } from 'react';
import '../scss/Screens/Main.scss';
import { postAssay } from '../Api/AuthApi';
import axios from 'axios';
import { FLASK_SERVER_URL } from '../constants/config';

const MainPage = ({ user }) => {
  const [formData, setFormData] = useState({
    jobTitle: '',
    experience: '신입',
    title: '',
    questions: [{ question: '', content: '' }]
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isEvaluating, setIsEvaluating] = useState(false);

  const handleChange = (e, index) => {
    if (index !== undefined) {
      const newQuestions = [...formData.questions];
      newQuestions[index][e.target.name] = e.target.value;
      setFormData({
        ...formData,
        questions: newQuestions
      });
    } else {
      setFormData({
        ...formData,
        [e.target.name]: e.target.value
      });
    }
  };

  const handleAddQuestion = () => {
    setFormData({
      ...formData,
      questions: [...formData.questions, { question: '', content: '' }]
    });
  };

  const evaluateResume = async (qa_pairs) => {
    try {
      const response = await axios.post(`${FLASK_SERVER_URL}/evaluate`, {
        직무: formData.jobTitle,
        직위: formData.experience,
        qa_pairs: qa_pairs
      });
      return response.data;
    } catch (error) {
      console.error('평가 중 오류 발생:', error);
      throw error;
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.jobTitle || !formData.title || formData.questions.some(q => !q.question || !q.content)) {
      setError('모든 필드를 입력해주세요.');
      setSuccess('');
      return;
    }
    setError('');
    setSuccess('');
    setIsEvaluating(true);

    try {
      // 자소서 평가 요청
      const qa_pairs = formData.questions.map(q => ({
        question: q.question,
        answer: q.content
      }));
      
      const evaluationResult = await evaluateResume(qa_pairs);
      
      const payload = {
        assay_title: formData.title,
        score: evaluationResult.평균점수,
        job: formData.jobTitle,
        state: formData.experience,
        questionAnswers: formData.questions.map(q => ({
          question: q.question,
          answer: q.content
        })),
        evaluationDetails: evaluationResult.상세결과
      };

      await postAssay(payload);
      setSuccess('자소서가 성공적으로 저장되었습니다!');
      setFormData({ 
        jobTitle: '', 
        experience: '신입', 
        title: '', 
        questions: [{ question: '', content: '' }] 
      });
    } catch (error) {
      setError('저장 중 오류가 발생했습니다.');
      setSuccess('');
      console.error('Error:', error);
    } finally {
      setIsEvaluating(false);
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

          {formData.questions.map((q, index) => (
            <div key={index} className="question-group">
              <div className="form-group">
                <label htmlFor={`question-${index}`}>질문 {index + 1}</label>
                <input
                  type="text"
                  id={`question-${index}`}
                  name="question"
                  value={q.question}
                  onChange={(e) => handleChange(e, index)}
                  placeholder="자소서 질문을 입력하세요"
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor={`content-${index}`}>답변 {index + 1}</label>
                <textarea
                  id={`content-${index}`}
                  name="content"
                  value={q.content}
                  onChange={(e) => handleChange(e, index)}
                  placeholder="자소서 답변을 입력하세요"
                  required
                  rows="10"
                />
              </div>
            </div>
          ))}

          <button type="button" className="add-btn" onClick={handleAddQuestion}>
            추가하기
          </button>

          <button type="submit" className="submit-btn" disabled={isEvaluating}>
            {isEvaluating ? '평가 중...' : '자소서 평가 받기'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default MainPage; 