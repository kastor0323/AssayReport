# resume_evaluator.py
import os
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
import json

app = Flask(__name__)
CORS(app)

class ResumeEvaluator:
    def __init__(self, reference_csv_path=None):
        """
        자소서 평가기 초기화
        Args:
            reference_csv_path: 합격 자소서 분석 결과 CSV 파일 경로
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        if reference_csv_path is None:
            reference_csv_path = os.path.join(base_dir, 'jobkorea_keyword_analysis.csv')
        elif not os.path.isabs(reference_csv_path) and not os.path.exists(reference_csv_path):
            reference_csv_path = os.path.join(base_dir, reference_csv_path)
            
        self.reference_df = pd.read_csv(reference_csv_path, encoding='utf-8-sig')
        self.kiwi = Kiwi()
        self.load_company_vision_data(base_dir)
        
        # NLTK 데이터 다운로드 (처음 실행시에만 필요)
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            nltk.download('punkt')
            nltk.download('stopwords')
            nltk.download('averaged_perceptron_tagger')

    def load_company_vision_data(self, base_dir):
        """100대 기업 비전 데이터 로드"""
        try:
            json_path = os.path.join(base_dir, 'data', 'top_100_companies.json')
            with open(json_path, 'r', encoding='utf-8') as f:
                self.company_vision_data = json.load(f)
            
            # 기업명-정보 맵 생성
            self.company_info_map = {}
            for industry, companies in self.company_vision_data.items():
                for co in companies:
                    co['industry'] = industry
                    self.company_info_map[co['name']] = co
            
            print(f"100대 기업 비전 데이터 로드 완료 ({len(self.company_info_map)}개 기업)")
        except Exception as e:
            print(f"기업 비전 데이터 로드 오류: {e}")
            self.company_info_map = {}

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
        
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        total_chars = len(re.findall(r'[a-zA-Z가-힣]', text))
        is_english = english_chars / max(total_chars, 1) > 0.5

        if is_english:
            cleaned = re.sub(r'[^\w\s]', ' ', text)
            cleaned = re.sub(r'\s+', ' ', cleaned).strip().lower()
            words = [word for word in cleaned.split() if len(word) >= 2 and word.isalpha()]
            return words
        else:
            try:
                tokens = self.kiwi.tokenize(text)
                words = [token.form for token in tokens
                         if token.tag.startswith(('N', 'V', 'J')) and len(token.form) >= 2]
                return words
            except Exception as e:
                return []

    def get_category(self, text):
        """질문 텍스트가 어떤 핵심 카테고리에 속하는지 판별"""
        text_lower = text.lower()
        
        # 카테고리별 탐색 키워드 목록
        category_keywords = {
            '지원동기': ['지원동기', '지원 동기', '회사선택', '선택한 이유', '왜 지원', '지원하게 된'],
            '성장과정': ['성장과정', '성장 과정', '어린 시절', '가족관계', '학창시절'],
            '장단점': ['장단점', '장점', '단점', '강점', '약점', '성격'],
            '입사포부': ['입사포부', '입사 후 포부', '입사후포부', '미래계획', '비전', '목표', '10년 후', '기여할'],
            '자기소개': ['자기소개', '자기 소개', '자신을 소개'],
            '경험': ['경험', '도전', '극복', '협업', '리더십', '실패', '갈등', '문제해결', '성공', '팀워크', '소통', '프로젝트', '인턴'],
            '직무역량': ['역량', '직무', '전공', '과목', '준비', '전문성', '수행', '기술'],
            '가치관': ['가치관', '윤리의식', '도덕성', '인생관', '삶의 목표', '존경하는 인물']
        }
        
        for cat, keywords in category_keywords.items():
            for kw in keywords:
                if kw in text_lower:
                    return cat
        return None

    def word_based_similarity(self, q1, q2):
        """두 질문 간 단어 기반 유사도 계산"""
        q1_cleaned = self.clean_text(q1)
        q2_cleaned = self.clean_text(q2)

        # q2가 핵심 카테고리 단어인 경우, q1을 해당 카테고리로 매핑하여 비교
        categories = ['경험', '지원동기', '성장과정', '장단점', '입사포부', '자기소개', '직무역량', '가치관']
        if q2_cleaned in categories:
            q1_cat = self.get_category(q1_cleaned)
            if q1_cat == q2_cleaned:
                return 1.0
            else:
                return 0.0

        if q2_cleaned and q1_cleaned and q2_cleaned in q1_cleaned:
            return 1.0

        words1 = set(self.extract_words(q1_cleaned))
        words2 = set(self.extract_words(q2_cleaned))

        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0


    def find_best_matching_question(self, user_question, job_title, position):
        """사용자 질문과 가장 유사한 합격 자소서 질문 찾기 (다단계 매칭Fallback 적용)"""
        # 1단계: 특정 직무 + 특정 직위 매칭
        filtered_df = self.reference_df[
            (self.reference_df['직무'] == job_title) & 
            (self.reference_df['직위'] == position)
        ]
        best_match_keyword, max_similarity, best_match_data = self._find_best_in_df(user_question, filtered_df)
        
        # 2단계: 직무만 일치하는 경우 (인턴/신입 등 직위 통합)
        if best_match_data is None or max_similarity < 0.2:
            filtered_df_job = self.reference_df[self.reference_df['직무'] == job_title]
            k, s, d = self._find_best_in_df(user_question, filtered_df_job)
            if d is not None and s > max_similarity:
                best_match_keyword, max_similarity, best_match_data = k, s, d
                
        # 3단계: 전체 데이터에서 공통 질문 유형 매칭 (지원동기, 포부 등 공통 항목)
        if best_match_data is None or max_similarity < 0.2:
            k, s, d = self._find_best_in_df(user_question, self.reference_df)
            if d is not None and s > max_similarity:
                best_match_keyword, max_similarity, best_match_data = k, s, d
        
        return best_match_keyword, max_similarity, best_match_data

    def _find_best_in_df(self, user_question, df):
        """데이터프레임 내에서 최적의 매칭 질문 검색"""
        if df is None or df.empty:
            return None, 0, None
        
        max_similarity = 0
        best_match_keyword = None
        best_match_data = None
        
        for idx, row in df.iterrows():
            if pd.isna(row['핵심단어']):
                continue
                
            similarity = self.word_based_similarity(user_question, row['핵심단어'])
            if similarity > max_similarity:
                max_similarity = similarity
                best_match_keyword = row['핵심단어']
                best_match_data = row
        
        return best_match_keyword, max_similarity, best_match_data

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
            cleaned_answer = re.sub(r'[^\w\s가-힣]', ' ', answer_text)
            cleaned_answer = re.sub(r'\s+', ' ', cleaned_answer).strip()
            
            english_chars = len(re.findall(r'[a-zA-Z]', cleaned_answer))
            total_chars = len(re.findall(r'[a-zA-Z가-힣]', cleaned_answer))
            is_english = english_chars / max(total_chars, 1) > 0.5
            
            if is_english:
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
                try:
                    tokens = self.kiwi.tokenize(cleaned_answer)
                    nouns = [token.form for token in tokens 
                            if token.tag.startswith('N') and len(token.form) >= 2]
                    korean_nouns.extend(nouns)
                except:
                    continue
        
        all_words = korean_nouns + english_words
        if not all_words: return []
        counter = Counter(all_words)
        return [word for word, count in counter.most_common(top_n)]

    def calculate_keyword_matching_score(self, user_answer, reference_keywords):
        """키워드 매칭 점수 계산"""
        # 사용자 답변에서 키워드 추출 (매칭 품질을 위해 상위 100개로 확대)
        user_keywords = self.extract_keywords_multilingual([user_answer], top_n=100)
        
        if not reference_keywords or pd.isna(reference_keywords):
            return 0.0, []
        
        # CSV의 답변 키워드는 쉼표로 구분된 문자열
        reference_keyword_list = [kw.strip() for kw in str(reference_keywords).split(',')]
        reference_keyword_set = set(reference_keyword_list)
        user_keyword_set = set(user_keywords)
        
        # 교집합 추출
        matched_keywords = user_keyword_set.intersection(reference_keyword_set)
        matched_count = len(matched_keywords)
        
        if matched_count >= 16: score = 100
        elif matched_count >= 12: score = 80 + (matched_count - 12) * 5
        elif matched_count >= 8: score = 60 + (matched_count - 8) * 5
        elif matched_count >= 4: score = 40 + (matched_count - 4) * 5
        elif matched_count >= 1: score = 20 + (matched_count - 1) * 5
        else: score = 0
        
        return score, list(matched_keywords)

    def calculate_vision_alignment_score(self, user_answer, company_name):
        """
        회사 비전 및 성향 정합성 분석 (단순 키워드 -> 서사 구조 분석)
        """
        if not company_name or company_name not in self.company_info_map:
            return 0.0, []
        
        company_info = self.company_info_map[company_name]
        vision_text = company_info['vision']
        core_values = company_info['core_values']
        
        # 1. 성향 테마 정의 (비전/핵심가치 기반)
        disposition_themes = {
            "기술/혁신": ["기술", "혁신", "초격차", "R&D", "품질", "엔지니어", "전문성", "자부심"],
            "미래/선도": ["미래", "선도", "글로벌", "최고", "변화", "이끌다", "앞서가다", "시장"],
            "인재/협력": ["인재", "협력", "상생", "소통", "팀워크", "공헌", "사람", "성장"],
            "실행/도전": ["도전", "실행", "열정", "완수", "책임", "끈기", "목표", "달성"]
        }
        
        # 2. 서사 구조 패턴 분석 (Storyline Alignment)
        narrative_patterns = {
            "경험_근거": [r"(.+?)(바탕으로|통해|경험하며|수행하며|과정에서)"],
            "기술_자부심": [r"(.+?)(역량을|자부심을|기술력을|전문성을)"],
            "비전_지향": [r"(.+?)(이끌어|선도하는|기여하는|목표로|실현하기 위해)"]
        }
        
        user_words = self.extract_words(user_answer)
        user_text = self.clean_text(user_answer)
        
        # 3. 점수 산출 로직
        disposition_score = 0
        matched_themes = []
        
        # 3-1. 테마 적합도
        for theme, keywords in disposition_themes.items():
            match_count = len([w for w in user_words if w in keywords])
            if match_count >= 1:
                disposition_score += 15
                matched_themes.append(theme)
        
        # 3-2. 서사 구조 완성도
        pattern_score = 0
        for pattern_name, regex_list in narrative_patterns.items():
            for regex in regex_list:
                if re.search(regex, user_text):
                    pattern_score += 15
                    break
        
        # 3-3. 비전 액션 동사 매칭
        action_verbs = ["이끌다", "선도하다", "기여하다", "혁신하다", "창출하다", "실현하다", "완수하다"]
        action_match = len([v for v in action_verbs if v in user_text])
        action_score = min(action_match * 5, 10)
        
        total_vision_score = min(disposition_score + pattern_score + action_score, 100)
        result_keywords = matched_themes + [v for v in action_verbs if v in user_text]
            
        return total_vision_score, result_keywords

    def evaluate_resume(self, user_data):
        """사용자 자소서 평가"""
        company_name = user_data.get('회사명', '')
        job_title = user_data['직무']
        position = user_data['직위']
        qa_pairs = user_data['qa_pairs']
        
        evaluation_results = []
        
        for i, qa in enumerate(qa_pairs):
            user_question = qa['question']
            user_answer = qa['answer']
            
            best_keyword, _, best_data = self.find_best_matching_question(
                user_question, job_title, position
            )
            
            keyword_score = 0
            matched_essay_keywords = []
            if best_data is not None:
                keyword_score, matched_essay_keywords = self.calculate_keyword_matching_score(
                    user_answer, best_data['답변키워드_TOP20']
                )
            
            vision_score = 0
            matched_vision_keywords = []
            if company_name:
                vision_score, matched_vision_keywords = self.calculate_vision_alignment_score(
                    user_answer, company_name
                )
            
            total_score = (keyword_score * 0.7) + (vision_score * 0.3)
            
            evaluation_results.append({
                '질문번호': i + 1,
                '사용자질문': user_question,
                '가장유사한질문': best_keyword if best_keyword else 'N/A',
                '매칭된합격키워드': ', '.join(matched_essay_keywords),
                '매칭된비전키워드': ', '.join(matched_vision_keywords),
                '합격키워드점수': round(keyword_score, 1),
                '비전정합성점수': round(vision_score, 1),
                '문항종합점수': round(total_score, 1)
            })
        
        result_df = pd.DataFrame(evaluation_results)
        average_score = result_df['문항종합점수'].mean()
        
        if average_score >= 80: grade = "우수 (S)"
        elif average_score >= 60: grade = "보통 (A)"
        elif average_score >= 40: grade = "미흡 (B)"
        else: grade = "부족 (C)"
        
        return {
            '회사명': company_name,
            '산업분야': self.company_info_map.get(company_name, {}).get('industry', '기타'),
            '평균점수': round(average_score, 1),
            '등급': grade,
            '상세결과': evaluation_results
        }

@app.route('/evaluate', methods=['POST'])
def evaluate_resume():
    try:
        data = request.get_json()
        evaluator = ResumeEvaluator()
        result = evaluator.evaluate_resume(data)
        if result is None: return jsonify({'error': '평가 실패'}), 400
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port)
