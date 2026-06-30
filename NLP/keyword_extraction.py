import os
import csv
import pandas as pd
from kiwipiepy import Kiwi
from collections import Counter
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
import random
import json

class KeywordExtractor:
    def __init__(self, file_path=None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = file_path  # 하위 호환용, load_data()에서는 사용 안 함
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
        
        # 데이터 로드
        self.load_data()
        
        # 100대 기업 인재상 데이터 로드
        self.load_company_talent_data(base_dir)

        # 소프트스킬 키워드 (하드스킬 분류 시 기준)
        self.soft_skill_keywords = {
            '협업', '협력', '팀워크', '팀원', '조율', '조화', '동료', '팔로워',
            '소통', '경청', '의사소통', '공감', '배려', '표현',
            '리더십', '리더', '주도', '솔선수범', '자발',
            '의사결정', '갈등관리', '갈등해결',
            '성실', '책임감', '꼼꼼', '적극', '열정', '끈기', '도전정신',
            '긍정', '유연', '창의', '자기개발',
            '멘토', '멘티', '코칭', '피드백',
            '신뢰', '정직', '투명', '겸손', '존중',
            '목표의식', '성취', '배움',
        }

        # 공통 자소서 질문 키워드 및 카테고리 매핑
        self.common_question_keywords = [
            '지원동기', '성장과정', '장단점', '입사포부', '자기소개',
            '경험', '도전', '극복', '협업', '리더십', '실패', '갈등',
            '직무역량', '전공', '취업준비', '회사선택', '미래계획', '비전', '핵심역량',
            '강점', '약점', '역량', '직무', '성격', '가치관', '문제해결', '성공',
            '본인의 강점', '본인의 약점', '가장 힘들었던 경험', '가장 어려웠던 일', '가장 보람있었던 경험',
            '직무 수행', '직무 관련', '인턴 경험', '프로젝트 경험', '어학연수', '학업 경험',
            '사회생활', '조직생활', '팀워크', '소통', '리더', '팔로워', '변화', '혁신',
            '윤리의식', '도덕성', '가치관', '인생관', '삶의 목표', '존경하는 인물',
            '지원 직무', '입사 후 목표', '10년 후 모습', '회사에 기여할 수 있는 점'
        ]

        self.category_map = {
            '경험': '경험', '도전': '경험', '극복': '경험', '협업': '경험', '리더십': '경험',
            '실패': '경험', '갈등': '경험', '문제해결': '경험', '성공': '경험',
            '가장 힘들었던 경험': '경험', '가장 어려웠던 일': '경험', '가장 보람있었던 경험': '경험',
            '인턴 경험': '경험', '프로젝트 경험': '경험', '어학연수': '경험', '학업 경험': '경험',
            '사회생활': '경험', '조직생활': '경험', '팀워크': '경험', '소통': '경험',
            '리더': '경험', '팔로워': '경험', '변화': '경험', '혁신': '경험',
            
            '지원동기': '지원동기', '회사선택': '지원동기',
            '성장과정': '성장과정',
            
            '장단점': '장단점', '성격': '장단점', '강점': '장단점', '약점': '장단점',
            '본인의 강점': '장단점', '본인의 약점': '장단점',
            
            '입사포부': '입사포부', '미래계획': '입사포부', '비전': '입사포부',
            '입사 후 목표': '입사포부', '10년 후 모습': '입사포부', '회사에 기여할 수 있는 점': '입사포부',
            
            '직무역량': '직무역량', '역량': '직무역량', '직무': '직무역량', '전공': '직무역량',
            '취업준비': '직무역량', '핵심역량': '직무역량', '직무 수행': '직무역량', '직무 관련': '직무역량',
            '지원 직무': '직무역량',
            
            '자기소개': '자기소개',
            
            '가치관': '가치관', '윤리의식': '가치관', '도덕성': '가치관', '인생관': '가치관',
            '삶의 목표': '가치관', '존경하는 인물': '가치관'
        }

        # 한국어 불용어 정의
        self.korean_stopwords = {
            # 조사·접속사·종결어미류
            '합니다', '있습니다', '통해', '위해', '대한', '관한', '대해', '있어',
            '하고', '하며', '하는', '되는', '하여', '같은', '다른', '이런', '그런',
            '이', '그', '저', '것', '수', '때', '등', '및', '또는',
            # 범용 명사 (역량 평가와 무관)
            '생각', '사람', '경우', '가지', '내용', '방법', '방식', '상황', '과정',
            '이유', '부분', '문항', '예외', '항목', '해당', '이후', '이전', '현재',
            '최대', '최근', '기존', '추후', '향후', '결과물', '기반', '바탕',
            '시작', '진행', '참여', '작성', '준비', '관련', '분야', '다양', '다양한',
            '통한', '위한', '가장', '매우', '정말', '스스로', '아주', '조금', '많이',
            '모든', '여러', '각각', '서로', '함께', '혼자', '항상', '가끔', '나름',
            '모두', '동안', '이상', '실현', '발휘', '기여', '향상', '익히', '기르',
            '노력', '배우', '능력', '역량', '가치', '포부', '동기', '업무', '직무',
            '지원', '입사', '회사', '경험', '성장', '확인해보니',
            # 하드스킬 컬럼에 잔존하는 일반 명사 추가 제거
            '시간', '추가', '당시', '흥미', '사실', '자신', '필요', '확인',
            '사용', '영향', '자원', '습관', '활용', '정신', '의미', '중요',
            '결과', '목표', '수행', '활동', '이해', '개선', '운영', '완성',
            '대부분', '일반', '보통', '기본', '구체', '직접', '실제', '추후',
            '지속', '반복', '꾸준', '우선', '이미', '아직', '거의', '전혀',
            # 데이터 처리 아티팩트 (반드시 제거)
            '무명', '직무명', '회사명', '부서명',
            # 개인 신상·일상 관련 (자소서 역량 무관)
            '학교', '학년', '평소', '시절', '하루', '운동', '여행', '지인',
            '조언', '부모', '아버지', '어머니', '친구', '번호판', '무인도', '식량',
            '소요', '불편', '대만', '중국인', '취득',
        }

    def load_data(self):
        """데이터 로드 및 회사명/직무명 예외 처리 사전 생성"""
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            lk_path = os.path.join(base_dir, 'data', 'linked_scraping_result.csv')

            if os.path.exists(lk_path):
                self.df = pd.read_csv(lk_path, encoding='utf-8-sig').fillna('')
                print(f"데이터 로드 완료: {len(self.df)}개 행 (linked_scraping_result.csv)")
            else:
                print("linked_scraping_result.csv 파일이 없습니다.")
                self.df = pd.DataFrame()
        except Exception as e:
            print(f"데이터 로드 오류: {e}")
            self.df = pd.DataFrame()

        if not self.df.empty:
            self.company_exceptions = {
                '회사명': self.df['회사명'].unique().tolist() if '회사명' in self.df.columns else [],
                '직무명': self.df['직무명'].unique().tolist() if '직무명' in self.df.columns else [],
                '부서명': []
            }
        else:
            self.company_exceptions = {'회사명': [], '직무명': [], '부서명': []}

    # 질문 카테고리 regex 패턴 (keyword 매칭 실패 시 보조 분류)
    QUESTION_PATTERNS = [
        (r'지원.*?(동기|이유|계기)|선택.*?이유|왜.*?지원',                '지원동기'),
        (r'성장.*?과정|어떻게.*?성장|살아온|자라온|어린 시절',            '성장과정'),
        (r'(장점|단점|강점|약점)|(본인|자신).{0,5}(장|단|강|약)',        '장단점'),
        (r'입사.*?(포부|후|목표|하면)|(10년|5년|3년).*?후|기여.*?점',   '입사포부'),
        (r'미래.*?모습|비전.*?목표|공헌할|기여할',                        '입사포부'),
        (r'자기소개|자신.*?소개|본인.*?소개|간단.*?소개',                 '자기소개'),
        (r'(도전|극복|어려웠|힘들었|실패|갈등|성공|보람).{0,10}(경험|사례|때)',  '경험'),
        (r'(경험|사례|일화).{0,10}(도전|극복|어려|힘들|실패|갈등|협업|성공)', '경험'),
        (r'(프로젝트|인턴|아르바이트|봉사|동아리).{0,10}(경험|활동)',    '경험'),
        (r'(팀|조직|그룹).{0,10}(협업|갈등|프로젝트|경험)',              '경험'),
        (r'직무.{0,5}(역량|관련|스킬|능력)|역량.{0,5}직무',             '직무역량'),
        (r'(전공|학문|공부).{0,10}(활용|관련|적용)|준비.*?과정',         '직무역량'),
        (r'(가치관|인생관|삶의.{0,5}태도|중요하게.*?생각)',              '가치관'),
        (r'존경.*?(인물|사람)|좌우명|신조',                               '가치관'),
    ]

    # 직무분야 → 관련 company industry 매핑 (동음이의어 오염 방지)
    FIELD_TO_INDUSTRIES = {
        'IT·전자':    {'IT·전자'},
        '건설·부동산': {'건설·부동산'},
        '구매·물류':   {'항공·물류'},
        '금융·보험':   {'금융·보험', '공공기관'},
        '식음료':      {'식음료'},
        '유통·서비스': {'유통·서비스'},
        '자동차·기계': {'자동차·기계'},
        '제약·바이오': {'제약·바이오'},
        '철강·소재':   {'철강·소재'},
        '통신·미디어': {'통신·미디어', 'IT·전자'},
        '항공·물류':   {'항공·물류'},
        '화학·에너지': {'화학·에너지'},
        '회계·재무':   {'금융·보험', '공공기관'},
        # 경영기획, 영업·마케팅, 인사·교육 → 전 산업군 사용
    }

    def load_company_talent_data(self, base_dir):
        """기업 인재상 JSON 데이터 로드 + IDF 가중치 사전 계산"""
        import math
        json_path = os.path.join(base_dir, 'data', 'companies.json')
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                companies = json.load(f)

            self.company_list = companies
            self.company_talent_data = {co['name']: co for co in companies}
            self.all_talent_keywords = set()
            for co in companies:
                self.all_talent_keywords.update(co['core_values'])

            # IDF 계산: 특정 인재상 키워드를 가진 회사 수 기반
            # log(N / df) → 희소 키워드일수록 높은 가중치
            N = len(companies)
            value_df = Counter()
            for co in companies:
                for v in set(co['core_values']):
                    value_df[v] += 1
            self.value_idf = {v: math.log(N / df) for v, df in value_df.items()}

            print(f"기업 인재상 데이터 로드 완료 ({len(self.company_list)}개 기업, {len(self.all_talent_keywords)}개 고유 인재상 키워드)")
        except Exception as e:
            print(f"기업 데이터 로드 오류: {e}")
            self.company_talent_data = {}
            self.company_list = []
            self.all_talent_keywords = set()
            self.value_idf = {}

    def clean_text(self, text):
        """텍스트 정제 - null bytes 제거 및 회사명 예외 처리"""
        if pd.isna(text) or text == '':
            return ''
        
        text_str = str(text)
        # null bytes 제거
        text_str = text_str.replace('\x00', '').replace('\0', '')
        
        # 회사명/직무명 예외 처리
        for category, exceptions in self.company_exceptions.items():
            for exception in exceptions:
                if exception and len(exception) > 1:
                    text_str = text_str.replace(exception, f'[{category}]')
        
        return text_str.strip()
    
    def _detect_question_category(self, question_text):
        """질문 텍스트로 카테고리 탐지 (키워드 → regex 순서로 시도)"""
        # 1차: common_question_keywords 직접 매칭
        for keyword in self.common_question_keywords:
            if keyword in question_text and keyword in self.category_map:
                return self.category_map[keyword]
        # 2차: regex 패턴 매칭
        for pattern, category in self.QUESTION_PATTERNS:
            if re.search(pattern, question_text):
                return category
        return '기타'

    def _classify_keywords(self, keywords):
        """키워드 리스트를 하드스킬/소프트스킬로 분리"""
        hard = [w for w in keywords if w not in self.soft_skill_keywords]
        soft = [w for w in keywords if w in self.soft_skill_keywords]
        return hard, soft

    def extract_words(self, text):
        """텍스트에서 단어 추출 (한글, 영어 단어 모두 포함)"""
        if not text:
            return []
        
        # null bytes 제거 및 회사명 예외 처리
        text = self.clean_text(text)
        
        # 한글, 영어, 공백 제외 문자 제거
        cleaned = re.sub(r'[^\uAC00-\uD7A3a-zA-Z\s]', ' ', text)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip().lower()
        words = cleaned.split()
        
        # 회사명 예외 처리된 단어는 제외
        words = [word for word in words if not word.startswith('[') and not word.endswith(']')]
        
        # 1글자 단어 및 '공사' 제외
        words = [word for word in words if len(word) >= 2 and word != '공사']
        
        return words
    
    def word_based_similarity(self, q1, q2):
        """두 질문에서 단어를 추출하여 단어 집합 기반 유사도 계산"""
        words1 = set(self.extract_words(q1))
        words2 = set(self.extract_words(q2))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union
    
    def extract_key_phrases_word_based(self, text):
        """질문에서 핵심 구문 추출"""
        if pd.isna(text) or text == '':
            return None
        
        key_pattern_map = {
            r'지원.*?동기': '지원동기',
            r'성장.*?과정': '성장과정',
            r'장.*?단점': '장단점',
            r'입사.*?포부': '입사포부',
            r'자기소개': '자기소개',
            r'경험.*?사례': '경험',
            r'도전.*?경험': '도전',
            r'극복.*?경험': '극복',
            r'협업.*?경험': '협업',
            r'리더십.*?경험': '리더십',
            r'실패.*?경험': '실패',
            r'갈등.*?해결': '갈등',
            r'직무.*?역량': '직무역량',
            r'전공.*?관련': '전공',
            r'취업.*?준비': '취업준비',
            r'회사.*?선택': '회사선택',
            r'미래.*?계획': '미래계획',
            r'비전.*?목표': '비전',
            r'핵심역량': '핵심역량'
        }
        
        text_lower = text.lower()
        for pattern, key_word in key_pattern_map.items():
            if re.search(pattern, text_lower):
                return key_word
        
        words = self.extract_words(text)
        filtered_words = [word for word in words if word not in self.korean_stopwords and len(word) >= 2]
        return filtered_words[0] if filtered_words else None
    
    def group_questions_word_based(self, questions, answers, similarity_threshold=0.3):
        """단어 기반 질문 그룹핑"""
        groups = []
        processed = set()
        
        for i, q1 in enumerate(questions):
            if i in processed or q1 == '':
                continue
            
            question_group = [q1]
            answer_group = [answers[i]]
            processed.add(i)
            
            key_phrase1 = self.extract_key_phrases_word_based(q1)
            
            for j, q2 in enumerate(questions[i+1:], i+1):
                if j in processed or q2 == '':
                    continue
                
                similarity = self.word_based_similarity(q1, q2)
                if similarity >= similarity_threshold:
                    question_group.append(q2)
                    answer_group.append(answers[j])
                    processed.add(j)
            
            groups.append({
                'representative_question': q1,
                'key_phrase': key_phrase1,
                'questions': question_group,
                'answers': answer_group,
                'count': len(question_group)
            })
        
        return groups
    
    def extract_keywords_multilingual(self, answers, top_n=20):
        """한국어/영어 일반 형태소 키워드 추출"""
        korean_nouns = []
        english_words = []
        
        try:
            english_stopwords = set(stopwords.words('english'))
        except:
            english_stopwords = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'our', 'we'])
        
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
                except Exception:
                    continue
        
        # 불용어 필터링
        all_words = []
        for word in (korean_nouns + english_words):
            if word not in self.korean_stopwords and len(word) >= 2:
                all_words.append(word)
        
        if not all_words:
            return []
        
        counter = Counter(all_words)
        return [word for word, count in counter.most_common(top_n)]

    def analyze_by_job_and_talent(self):
        """직무명별 × 질문카테고리별 키워드 추출 (특정 기업 자소서용)

        컬럼: 직무명 | 질문카테고리 | 답변수 | 하드스킬_키워드 | 소프트스킬_키워드 | 추출회사명
        """
        if self.df.empty:
            print("데이터프레임이 비어 있어 직무 분석을 수행할 수 없습니다.")
            return None

        print("\n=== [직무명별 × 질문카테고리별 키워드 분석 시작] ===")
        job_groups = self.df.groupby('직무명')

        results = []

        for job_name, job_group in job_groups:
            if not job_name or job_name.strip() == '':
                continue

            print(f"분석 중: {job_name} ({len(job_group)}개 문항)")

            unique_companies = [c for c in job_group['회사명'].dropna().unique() if c]

            # 카테고리별 답변 수집 (_detect_question_category 사용)
            category_answers = {}
            for _, row in job_group.iterrows():
                question_content = self.clean_text(row['질문 내용'])
                answer_content = self.clean_text(row['답변'])
                if not answer_content:
                    continue

                matched_category = self._detect_question_category(question_content)

                if matched_category not in category_answers:
                    category_answers[matched_category] = []
                category_answers[matched_category].append(answer_content)

            # 카테고리별 하드/소프트스킬 키워드 추출
            for category, answers in category_answers.items():
                if not answers:
                    continue

                all_kw = self.extract_keywords_multilingual(answers, top_n=30)
                hard_skills, soft_skills = self._classify_keywords(all_kw)

                results.append({
                    '직무명': job_name,
                    '질문카테고리': category,
                    '답변수': len(answers),
                    '하드스킬_키워드': ', '.join(hard_skills[:15]),
                    '소프트스킬_키워드': ', '.join(soft_skills[:10]),
                    '추출회사명': ', '.join(unique_companies),
                })

        result_df = pd.DataFrame(results)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_csv = os.path.join(base_dir, 'data', 'job_keywords_by_position.csv')
        output_json = os.path.join(base_dir, 'data', 'job_keywords_by_position.json')

        result_df = result_df.fillna('')
        result_df.to_csv(output_csv, index=False, encoding='utf-8-sig', quoting=csv.QUOTE_NONNUMERIC)
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(result_df.to_dict(orient='records'), f, ensure_ascii=False, indent=2)

        print(f"직무명별 × 카테고리별 키워드 분석 저장: {output_csv}")
        return result_df

    def analyze_data(self):
        """직무분야별 × 질문카테고리별 job_keywords_analysis.csv/json 생성 (자소서 초안용)

        컬럼: 직무분야 | 질문카테고리 | 자기소개 개수 | 답변키워드_20 | 추출회사명
        """
        if self.df.empty:
            print("데이터가 비어 있습니다.")
            return None

        if '직무분야' not in self.df.columns:
            self.df['직무분야'] = '기타'

        industry_groups = self.df.groupby('직무분야')
        print(f"\n총 {len(industry_groups)}개 직무분야 발견")

        results = []
        for industry_name, industry_group in industry_groups:
            essay_count = industry_group.drop_duplicates(
                subset=['회사명', '연도', '직무명']
            ).shape[0]

            unique_companies = [c for c in industry_group['회사명'].dropna().unique() if c]

            # 카테고리별 답변 수집 (_detect_question_category 사용)
            category_answers = {}
            for _, row in industry_group.iterrows():
                question_content = self.clean_text(row['질문 내용'])
                answer_content = self.clean_text(row['답변'])
                if not answer_content:
                    continue

                matched_category = self._detect_question_category(question_content)

                if matched_category not in category_answers:
                    category_answers[matched_category] = []
                category_answers[matched_category].append(answer_content)

            # 카테고리별 하드/소프트스킬 키워드 추출
            for category, answers in category_answers.items():
                if not answers:
                    continue

                all_kw = self.extract_keywords_multilingual(answers, top_n=30)
                hard_skills, soft_skills = self._classify_keywords(all_kw)

                results.append({
                    '직무분야': industry_name,
                    '질문카테고리': category,
                    '자기소개 개수': essay_count,
                    '하드스킬_키워드': ', '.join(hard_skills[:15]),
                    '소프트스킬_키워드': ', '.join(soft_skills[:10]),
                    '추출회사명': ', '.join(unique_companies),
                })

        result_df = pd.DataFrame(results)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_csv = os.path.join(base_dir, 'data', 'job_keywords_analysis.csv')
        output_json = os.path.join(base_dir, 'data', 'job_keywords_analysis.json')

        result_df = result_df.fillna('')
        result_df.to_csv(output_csv, index=False, encoding='utf-8-sig', quoting=csv.QUOTE_NONNUMERIC)
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(result_df.to_dict(orient='records'), f, ensure_ascii=False, indent=2)

        print(f"=== [분석 완료] ===")
        print(f"직무분야별 × 카테고리별 키워드 분석 CSV: {output_csv}")
        print(f"직무분야별 × 카테고리별 키워드 분석 JSON: {output_json}")

        # 보조 분석: 직무명별 상세 키워드
        self.analyze_by_job_and_talent()

        return result_df

if __name__ == "__main__":
    extractor = KeywordExtractor()
    extractor.analyze_data()
