import os
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
            '합니다', '있습니다', '때문', '생각', '경험', '회사', '업무', '직무', '지원', '입사', 
            '포부', '동기', '가치', '능력', '역량', '사람', '과정', '노력', '바탕', '배우', 
            '익히', '기르', '향상', '성장', '기여', '발휘', '실현', '준비', '관련', '분야',
            '통해', '위해', '대한', '관한', '대해', '있어', '하고', '하며', '하는', '되는',
            '이', '그', '저', '것', '수', '때', '등', '및', '또는', '하여', '같은',
            '다른', '이런', '그런', '어떤', '무엇', '어떻게', '왜', '누구', '가지', '경우',
            '때문에', '때문이다', '때문이', '확인해보니', '시작', '진행', '참여', '작성',
            '다양', '다양한', '통한', '위한', '기반', '가장', '매우', '정말', '스스로',
            '회사명', '번호판', '부모', '아버지', '어머니', '친구', '시절', '무인도', '식량'
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

    def load_company_talent_data(self, base_dir):
        """기업 인재상 JSON 데이터 로드"""
        json_path = os.path.join(base_dir, 'data', 'companies.json')
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                companies = json.load(f)

            self.company_list = companies
            self.company_talent_data = {co['name']: co for co in companies}
            self.all_talent_keywords = set()
            for co in companies:
                self.all_talent_keywords.update(co['core_values'])

            print(f"기업 인재상 데이터 로드 완료 ({len(self.company_list)}개 기업, {len(self.all_talent_keywords)}개 고유 인재상 키워드)")
        except Exception as e:
            print(f"기업 데이터 로드 오류: {e}")
            self.company_talent_data = {}
            self.company_list = []
            self.all_talent_keywords = set()

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
        """직무명별 그룹화, 실무 키워드 및 인재상 키워드 추출 (보조 분석용)"""
        if self.df.empty:
            print("데이터프레임이 비어 있어 직무 분석을 수행할 수 없습니다.")
            return None

        print("\n=== [직무명별 실무 & 인재상 키워드 분석 시작] ===")
        job_groups = self.df.groupby('직무명')

        job_analysis_results = []

        for job_name, job_group in job_groups:
            if not job_name or job_name.strip() == '':
                continue

            print(f"분석 중: {job_name} ({len(job_group)}개 문항)")

            all_answers = job_group['답변'].tolist()

            job_keywords = self.extract_keywords_multilingual(all_answers, top_n=30)
            practical_keywords = [w for w in job_keywords if w not in self.all_talent_keywords][:15]

            all_tokens = []
            for ans in all_answers:
                if ans:
                    cleaned_ans = self.clean_text(ans)
                    try:
                        tokens = self.kiwi.tokenize(cleaned_ans)
                        all_tokens.extend([t.form for t in tokens if t.tag.startswith('N') and len(t.form) >= 2])
                    except:
                        all_tokens.extend(self.extract_words(cleaned_ans))

            token_counts = Counter(all_tokens)

            talent_freq = {kw: token_counts.get(kw, 0) for kw in self.all_talent_keywords}
            sorted_talents = sorted(talent_freq.items(), key=lambda x: x[1], reverse=True)
            top_talent_keywords = [kw for kw, _ in sorted_talents[:10]]

            company_scores = [
                (co['name'], sum(token_counts.get(v, 0) for v in co['core_values']), co['industry'])
                for co in self.company_list
            ]
            company_scores.sort(key=lambda x: x[1], reverse=True)
            top_companies = [f"{name}({ind})" for name, _, ind in company_scores[:3]]

            combined_keywords = practical_keywords + top_talent_keywords

            job_analysis_results.append({
                '직무': job_name,
                '자소서_개수': len(job_group),
                '실무_키워드_15': ', '.join(practical_keywords),
                '인재상_키워드_10': ', '.join(top_talent_keywords),
                '추천_대기업_Top3': ', '.join(top_companies),
                '통합_키워드_25': ', '.join(combined_keywords)
            })

        result_df = pd.DataFrame(job_analysis_results)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_csv = os.path.join(base_dir, 'data', 'job_keywords_by_position.csv')
        output_json = os.path.join(base_dir, 'data', 'job_keywords_by_position.json')

        result_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(result_df.to_dict(orient='records'), f, ensure_ascii=False, indent=2)

        print(f"직무명별 분석 저장: {output_csv}")
        return result_df

    def analyze_data(self):
        """직무분야별 그룹으로 job_keywords_analysis.csv/json 생성

        컬럼: 직무분야 | 자기소개 개수 | 질문 목적 | 답변키워드_20 | 추출회사명
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
            # 자기소개 개수: 고유 (회사명, 연도, 직무명) 조합 수
            essay_count = industry_group.drop_duplicates(
                subset=['회사명', '연도', '직무명']
            ).shape[0]

            # 질문 목적: 가장 빈번한 질문 카테고리
            category_counter = Counter()
            all_answers_for_keywords = []
            for _, row in industry_group.iterrows():
                question_content = self.clean_text(row['질문 내용'])
                answer_content = self.clean_text(row['답변'])
                if answer_content:
                    all_answers_for_keywords.append(answer_content)

                for keyword in self.common_question_keywords:
                    if keyword in question_content and keyword in self.category_map:
                        category_counter[self.category_map[keyword]] += 1
                        break

            top_purpose = category_counter.most_common(1)[0][0] if category_counter else '기타'

            # 답변키워드_20: 해당 직무분야 전체 답변에서 top 20 키워드
            if len(all_answers_for_keywords) > 200:
                all_answers_for_keywords = random.sample(all_answers_for_keywords, 200)
            keywords = self.extract_keywords_multilingual(all_answers_for_keywords, top_n=20)

            # 추출회사명: 수집된 유니크 회사명
            unique_companies = [c for c in industry_group['회사명'].dropna().unique() if c]

            results.append({
                '직무분야': industry_name,
                '자기소개 개수': essay_count,
                '질문 목적': top_purpose,
                '답변키워드_20': ', '.join(keywords),
                '추출회사명': ', '.join(unique_companies),
            })

        result_df = pd.DataFrame(results)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_csv = os.path.join(base_dir, 'data', 'job_keywords_analysis.csv')
        output_json = os.path.join(base_dir, 'data', 'job_keywords_analysis.json')

        result_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(result_df.to_dict(orient='records'), f, ensure_ascii=False, indent=2)

        print(f"=== [분석 완료] ===")
        print(f"직무분야별 키워드 분석 CSV: {output_csv}")
        print(f"직무분야별 키워드 분석 JSON: {output_json}")

        # 보조 분석: 직무명별 상세 키워드
        self.analyze_by_job_and_talent()

        return result_df

if __name__ == "__main__":
    extractor = KeywordExtractor()
    extractor.analyze_data()
