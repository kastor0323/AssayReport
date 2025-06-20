# resume_evaluator.py
import pandas as pd
from kiwipiepy import Kiwi
from collections import Counter
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class ResumeEvaluator:
    def __init__(self, reference_csv_path='jobkorea_keyword_analysis.csv'):
        """
        자소서 평가기 초기화
        Args:
            reference_csv_path: 합격 자소서 분석 결과 CSV 파일 경로
        """
        self.reference_df = pd.read_csv(reference_csv_path, encoding='utf-8-sig')
        self.kiwi = Kiwi()
        
        # NLTK 데이터 다운로드 (처음 실행시에만 필요)
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            nltk.download('punkt')
            nltk.download('stopwords')
            nltk.download('averaged_perceptron_tagger')
    
    def clean_text(self, text):
        """텍스트 정제"""
        if pd.isna(text) or text == '':
            return ''
        
        text_str = str(text)
        text_str = text_str.replace('\x00', '')
        text_str = text_str.replace('\0', '')
        
        return text_str.strip()
    
    def extract_words(self, text):
        """텍스트에서 단어 추출 (Kiwi 사용)"""
        if pd.isna(text) or text == '':
            return []
        
        text = self.clean_text(text)
        
        # 영어 비율 확인 (extract_keywords_multilingual과 유사한 로직)
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        total_chars = len(re.findall(r'[a-zA-Z가-힣]', text))
        is_english = english_chars / max(total_chars, 1) > 0.5

        if is_english:
            # 영어 텍스트 처리 (기존 로직 유지)
            cleaned = re.sub(r'[^\w\s]', ' ', text)
            cleaned = re.sub(r'\s+', ' ', cleaned).strip().lower()
            words = [word for word in cleaned.split() if len(word) >= 2 and word.isalpha()]
            return words
        else:
            # 한국어 텍스트 처리 (Kiwi 사용)
            try:
                tokens = self.kiwi.tokenize(text)
                # 명사, 동사, 형용사 등 의미 있는 품사 추출
                words = [token.form for token in tokens
                         if token.tag.startswith(('N', 'V', 'J')) and len(token.form) >= 2]
                return words
            except Exception as e:
                print(f"Kiwi extract_words 오류: {e}")
                return []
    
    def word_based_similarity(self, q1, q2):
        """두 질문 간 단어 기반 유사도 계산"""
        # q1과 q2가 문자열이고 NaN이 아닌지 확인
        q1_cleaned = self.clean_text(q1)
        q2_cleaned = self.clean_text(q2)

        # 핵심 키워드에 대한 직접적인 부분 문자열 일치 확인
        # 예: "자기소개를 해보세요"와 "자기소개"의 경우
        if q2_cleaned and q1_cleaned and q2_cleaned in q1_cleaned:
            return 1.0 # 직접적인 키워드 일치에 대해 높은 유사도 부여

        words1 = set(self.extract_words(q1_cleaned))
        words2 = set(self.extract_words(q2_cleaned))

        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def extract_keywords_multilingual(self, answers, top_n=20):
        """한국어/영어 키워드 추출"""
        korean_nouns = []
        english_words = []
        
        try:
            english_stopwords = set(stopwords.words('english'))
        except:
            english_stopwords = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
        
        for answer in answers:
            if pd.isna(answer) or answer == '':
                continue
            
            answer_text = self.clean_text(answer)
            if not answer_text:
                continue
            
            cleaned_answer = re.sub(r'[^\w\s가-힣]', ' ', answer_text)
            cleaned_answer = re.sub(r'\s+', ' ', cleaned_answer).strip()
            
            # 영어 비율 확인
            english_chars = len(re.findall(r'[a-zA-Z]', cleaned_answer))
            total_chars = len(re.findall(r'[a-zA-Z가-힣]', cleaned_answer))
            is_english = english_chars / max(total_chars, 1) > 0.5
            
            if is_english:
                # 영어 텍스트 처리
                try:
                    tokens = word_tokenize(cleaned_answer.lower())
                    pos_tags = pos_tag(tokens)
                    words = [word for word, pos in pos_tags 
                            if pos.startswith(('NN', 'JJ', 'VB')) 
                            and len(word) >= 2 
                            and word not in english_stopwords
                            and word.isalpha()]
                    english_words.extend(words)
                except:
                    words = [word.lower() for word in cleaned_answer.split() 
                            if len(word) >= 2 and word.lower() not in english_stopwords and word.isalpha()]
                    english_words.extend(words)
            else:
                # 한국어 텍스트 처리
                try:
                    tokens = self.kiwi.tokenize(cleaned_answer)
                    nouns = [token.form for token in tokens 
                            if token.tag.startswith('N') and len(token.form) >= 2]
                    korean_nouns.extend(nouns)
                except Exception as e:
                    print(f"Kiwi 분석 오류: {e}")
                    continue
        
        all_words = korean_nouns + english_words
        
        if not all_words:
            return []
        
        counter = Counter(all_words)
        extracted_keywords = [word for word, count in counter.most_common(top_n)]
        return extracted_keywords
    
    def find_best_matching_question(self, user_question, job_title, position):
        """사용자 질문과 가장 유사한 합격 자소서 질문 찾기"""
        # 정규화 제거: 입력값 그대로 사용
        # 해당 직무/직위 데이터 필터링 (정확한 매칭)
        filtered_df = self.reference_df[
            (self.reference_df['직무'] == job_title) & 
            (self.reference_df['직위'] == position)
        ]
        
        if filtered_df.empty:
            print(f"❌ '{job_title} - {position}' 데이터가 없습니다.")
            available_jobs = self.reference_df.groupby(['직무', '직위']).size().reset_index(name='count')
            print("\n📋 사용 가능한 직무/직위:")
            for _, row in available_jobs.iterrows():
                keywords_for_job = self.reference_df[
                    (self.reference_df['직무'] == row['직무']) &
                    (self.reference_df['직위'] == row['직위'])
                ]['핵심단어'].tolist()
                print(f"  - {row['직무']} ({row['직위']}) - 핵심단어: {', '.join(keywords_for_job)}")
            return None
        
        max_similarity = 0
        best_match_keyword = None
        best_match_data = None
        
        # 지원동기, 회사선택 등 핵심 키워드 우선 매칭
        priority_keywords = ['지원동기', '회사선택', '입사동기']
        for keyword in priority_keywords:
            if keyword in user_question.lower():
                matching_rows = filtered_df[filtered_df['핵심단어'] == keyword]
                if not matching_rows.empty:
                    best_match_keyword = keyword
                    best_match_data = matching_rows.iloc[0]
                    return best_match_keyword, 1.0, best_match_data
        
        # 일반적인 유사도 기반 매칭
        for idx, row in filtered_df.iterrows():
            similarity = self.word_based_similarity(user_question, row['핵심단어'])
            if similarity > max_similarity:
                max_similarity = similarity
                best_match_keyword = row['핵심단어']
                best_match_data = row
        
        return best_match_keyword, max_similarity, best_match_data
    
    def calculate_keyword_matching_score(self, user_answer, reference_keywords):
        """키워드 매칭 점수 계산"""
        user_keywords = self.extract_keywords_multilingual([user_answer], top_n=20)
        
        if not reference_keywords or pd.isna(reference_keywords):
            return 0.0, []
        
        reference_keyword_list = [kw.strip() for kw in str(reference_keywords).split(',')]
        reference_keyword_set = set(reference_keyword_list)
        user_keyword_set = set(user_keywords)
        
        if not reference_keyword_set or not user_keyword_set:
            return 0.0, []
        
        # 매칭된 키워드 수 계산
        matched_keywords = user_keyword_set.intersection(reference_keyword_set)
        matched_count = len(matched_keywords)
        
        # 점수 계산 방식 변경
        # 20개 중 매칭된 키워드 수에 따라 점수 부여
        # 16개 이상: 100점
        # 12-15개: 80-95점
        # 8-11개: 60-75점
        # 4-7개: 40-55점
        # 1-3개: 20-35점
        # 0개: 0점
        
        if matched_count >= 16:
            score = 100
        elif matched_count >= 12:
            score = 80 + (matched_count - 12) * 5
        elif matched_count >= 8:
            score = 60 + (matched_count - 8) * 5
        elif matched_count >= 4:
            score = 40 + (matched_count - 4) * 5
        elif matched_count >= 1:
            score = 20 + (matched_count - 1) * 5
        else:
            score = 0
        
        return score, list(matched_keywords)
    
    def evaluate_resume(self, user_data):
        """
        사용자 자소서 평가
        Args:
            user_data: {
                '직무': '직무명',
                '직위': '직위명', 
                'qa_pairs': [
                    {'question': '질문1', 'answer': '답변1'},
                    {'question': '질문2', 'answer': '답변2'},
                    ...
                ]
            }
        Returns:
            dict: {
                '평균점수': float,
                '등급': str,
                '상세결과': list
            }
        """
        job_title = user_data['직무']
        position = user_data['직위']
        qa_pairs = user_data['qa_pairs']
        
        # 해당 직무/직위 데이터 확인
        available_data = self.reference_df[
            (self.reference_df['직무'] == job_title) & 
            (self.reference_df['직위'] == position)
        ]
        
        if available_data.empty:
            print(f"❌ '{job_title} - {position}' 데이터가 없습니다.")
            available_jobs = self.reference_df.groupby(['직무', '직위']).size().reset_index(name='count')
            print("\n📋 사용 가능한 직무/직위:")
            for _, row in available_jobs.iterrows():
                keywords_for_job = self.reference_df[
                    (self.reference_df['직무'] == row['직무']) &
                    (self.reference_df['직위'] == row['직위'])
                ]['핵심단어'].tolist()
                print(f"  - {row['직무']} ({row['직위']}) - 핵심단어: {', '.join(keywords_for_job)}")
            return None
        
        evaluation_results = []
        
        for i, qa in enumerate(qa_pairs):
            user_question = qa['question']
            user_answer = qa['answer']
            
            # 가장 유사한 핵심단어 찾기
            best_keyword, _, best_data = self.find_best_matching_question(
                user_question, job_title, position
            )
            
            if best_data is not None:
                # 키워드 매칭 점수 계산
                keyword_score, matched_keywords = self.calculate_keyword_matching_score(
                    user_answer, best_data['답변키워드_TOP20']
                )
                
                evaluation_results.append({
                    '질문번호': i + 1,
                    '사용자질문': user_question,
                    '사용자답변': user_answer[:50] + "..." if len(user_answer) > 50 else user_answer,
                    '가장유사한질문': best_keyword,
                    '매칭된키워드': ', '.join(matched_keywords),
                    '매칭된키워드수': len(matched_keywords),
                    '종합점수': round(keyword_score, 1)
                })
            else:
                evaluation_results.append({
                    '질문번호': i + 1,
                    '사용자질문': user_question,
                    '사용자답변': user_answer[:50] + "..." if len(user_answer) > 50 else user_answer,
                    '가장유사한질문': 'N/A',
                    '매칭된키워드': '',
                    '매칭된키워드수': 0,
                    '종합점수': 0.0
                })
        
        # 결과 정리
        result_df = pd.DataFrame(evaluation_results)
        average_score = result_df['종합점수'].mean()
        
        # 점수별 등급 결정
        if average_score >= 80:
            grade = "우수 (80점 이상)"
        elif average_score >= 60:
            grade = "보통 (60-79점)"
        elif average_score >= 40:
            grade = "미흡 (40-59점)"
        else:
            grade = "부족 (40점 미만)"
        
        # 결과를 딕셔너리 형태로 반환
        return {
            '평균점수': round(average_score, 1),
            '등급': grade,
            '상세결과': evaluation_results
        }

@app.route('/evaluate', methods=['POST'])
def evaluate_resume():
    try:
        data = request.get_json()
        
        # 필수 필드 확인
        required_fields = ['직무', '직위', 'qa_pairs']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'필수 필드가 누락되었습니다: {field}'}), 400

        # 평가기 초기화
        evaluator = ResumeEvaluator('jobkorea_keyword_analysis.csv')
        
        # 자소서 평가 실행
        result = evaluator.evaluate_resume(data)
        
        if result is None:
            return jsonify({'error': '평가를 완료할 수 없습니다.'}), 400
            
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': f'평가 중 오류가 발생했습니다: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
