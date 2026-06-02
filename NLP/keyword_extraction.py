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
        if file_path is None:
            file_path = os.path.join(base_dir, 'data', '잡코리아_합격자소서.xlsx')
        self.file_path = file_path
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
            if os.path.exists(self.file_path):
                if self.file_path.endswith('.xlsx'):
                    df = pd.read_excel(self.file_path, engine='openpyxl')
                else:
                    try:
                        df = pd.read_csv(self.file_path, delimiter='\t', encoding='cp949')
                    except:
                        df = pd.read_csv(self.file_path, delimiter='\t', encoding='euc-kr')
            else:
                df = pd.DataFrame()
                print(f"기존 파일 없음: {self.file_path}")
            
            # 링커리어 데이터 파일 존재 시 병합
            base_dir = os.path.dirname(os.path.abspath(__file__))
            linkareer_path = os.path.join(base_dir, 'data', '링커리어_합격자소서.xlsx')
            if os.path.exists(linkareer_path):
                try:
                    df_linkareer = pd.read_excel(linkareer_path, engine='openpyxl')
                    # 빈 데이터프레임과 concat 시 오류 방지
                    if not df.empty:
                        df = pd.concat([df, df_linkareer], ignore_index=True)
                    else:
                        df = df_linkareer
                    print(f"링커리어 합격자소서 데이터 로드 완료: {len(df_linkareer)}개 행 병합됨")
                except Exception as e:
                    print(f"링커리어 데이터 로드/병합 오류: {e}")
            
            self.df = df.fillna('')
            print(f"합격자소서 통합 데이터 로드 완료: 최종 {len(self.df)}개 행")
        except Exception as e:
            print(f"데이터 로드 오류: {e}")
            self.df = pd.DataFrame()

        # 회사명, 직무명, 부서명 추출하여 예외 처리 단어로 등록
        if not self.df.empty:
            self.company_exceptions = {
                '회사명': self.df['회사명'].unique().tolist() if '회사명' in self.df.columns else [],
                '직무명': self.df['직무'].unique().tolist() if '직무' in self.df.columns else [],
                '부서명': self.df['부서'].unique().tolist() if '부서' in self.df.columns else []
            }
        else:
            self.company_exceptions = {'회사명': [], '직무명': [], '부서명': []}

    def load_company_talent_data(self, base_dir):
        """100대 기업 인재상 JSON 데이터 로드"""
        json_path = os.path.join(base_dir, 'data', 'top_100_companies.json')
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                self.company_talent_data = json.load(f)
            
            # 기업 리스트 및 고유 인재상 키워드 사전화
            self.company_list = []
            self.all_talent_keywords = set()
            for industry, companies in self.company_talent_data.items():
                for co in companies:
                    co['industry'] = industry
                    self.company_list.append(co)
                    self.all_talent_keywords.update(co['core_values'])
            
            print(f"100대 기업 인재상 데이터 로드 완료 ({len(self.company_list)}개 기업, {len(self.all_talent_keywords)}개 고유 인재상 키워드)")
        except Exception as e:
            print(f"100대 기업 데이터 로드 오류: {e}")
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
        """직무별 그룹화, 상위 15개 실무 키워드 및 대기업 100군데 연계 인재상 키워드 10개 추출"""
        if self.df.empty:
            print("데이터프레임이 비어 있어 직무 분석을 수행할 수 없습니다.")
            return None
        
        print("\n=== [직무별 실무 & 대기업 인재상 키워드 분석 시작] ===")
        job_groups = self.df.groupby('직무')
        
        job_analysis_results = []
        
        for job_name, job_group in job_groups:
            if not job_name or job_name.strip() == '':
                continue
            
            print(f"분석 중: {job_name} ({len(job_group)}개 문항)")
            
            # 1. 해당 직무 자소서 답변 데이터 합치기
            all_answers = job_group['답변'].tolist()
            
            # 2. 15개 실무 역량 키워드 추출 (TF 기준 상위 15개)
            job_keywords = self.extract_keywords_multilingual(all_answers, top_n=30)
            # 인재상 키워드와 겹치지 않는 실무 중심 키워드로 정제
            practical_keywords = [w for w in job_keywords if w not in self.all_talent_keywords][:15]
            
            # 자소서 텍스트 전체 토큰화하여 대기업 인재상 매칭용 카운터 빌드
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
            
            # 3. 100대 기업 인재상 키워드 Pool 기반 매칭 빈도 분석
            talent_freq = {}
            for kw in self.all_talent_keywords:
                # 자소서 내 출현 빈도수 기록
                talent_freq[kw] = token_counts.get(kw, 0)
                
            # 빈도 상위 10개 대기업 인재상 키워드 선정
            sorted_talents = sorted(talent_freq.items(), key=lambda x: x[1], reverse=True)
            top_talent_keywords = [kw for kw, freq in sorted_talents[:10]]
            
            # 4. 기업별 인재상 부합도 매칭 점수 계산 (Top 3 대기업 선정)
            company_scores = []
            for company in self.company_list:
                # 회사의 10개 인재상 키워드가 직무 자소서 토큰 빈도에서 차지하는 가중치 합산
                score = sum(token_counts.get(val, 0) for val in company['core_values'])
                company_scores.append((company['name'], score, company['industry']))
                
            # 상위 3개 어울리는 기업 선정
            company_scores.sort(key=lambda x: x[1], reverse=True)
            top_companies = [f"{name}({industry})" for name, score, industry in company_scores[:3]]
            
            # 5. 통합 키워드 프로필 작성 (25개)
            combined_keywords = practical_keywords + top_talent_keywords
            
            job_analysis_results.append({
                '직무': job_name,
                '자소서_개수': len(job_group),
                '실무_키워드_15': ', '.join(practical_keywords),
                '인재상_키워드_10': ', '.join(top_talent_keywords),
                '추천_대기업_Top3': ', '.join(top_companies),
                '통합_키워드_25': ', '.join(combined_keywords)
            })
            
        # 결과를 DataFrame으로 변환 및 파일 저장
        result_df = pd.DataFrame(job_analysis_results)
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_csv = os.path.join(base_dir, 'data', 'job_keywords_analysis.csv')
        output_json = os.path.join(base_dir, 'data', 'job_keywords_analysis.json')
        
        # 기존 결과물 병합 로직 추가
        if os.path.exists(output_csv):
            try:
                existing_df = pd.read_csv(output_csv)
                # 새로운 결과에 없는 직무는 유지, 있는 직무는 덮어쓰기 (또는 합치기)
                # 일단 간단하게 새로운 직무 데이터로 업데이트하고 나머지는 유지
                existing_df = existing_df[~existing_df['직무'].isin(result_df['직무'])]
                result_df = pd.concat([existing_df, result_df], ignore_index=True)
                print(f"기존 분석 결과와 병합 완료 (총 {len(result_df)}개 직무)")
            except Exception as e:
                print(f"기존 결과 병합 오류: {e}")
        
        result_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
        
        # JSON 형식으로도 저장 (구조화된 가독성을 위해)
        result_dict = result_df.set_index('직무').to_dict(orient='index')
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(result_dict, f, ensure_ascii=False, indent=2)
            
        print(f"=== [분석 완료] ===")
        print(f"1. 실무별 키워드 리포트(CSV): {output_csv}")
        print(f"2. 실무별 키워드 리포트(JSON): {output_json}")
        
        return result_df

    def analyze_jobkorea_data(self):
        """
        [기존 API 호환용] 산업분야-직무-직위별 핵심 질문 그룹 분석
        이후 신규 직무별 실무&인재상 키워드 분석을 백그라운드로 호출하여 모두 최신화합니다.
        """
        if self.df.empty:
            print("데이터가 비어 있습니다.")
            return None
            
        separate_results = []
        
        # 산업분야가 없으면 '기타'로 채움
        if '산업분야' not in self.df.columns:
            self.df['산업분야'] = '기타'

        industry_groups = self.df.groupby('산업분야')
        print(f"\n총 {len(industry_groups)}개 산업분야 발견 (기존 포맷 분석)")
        
        for industry_name, industry_group in industry_groups:
            job_groups = industry_group.groupby('직무')
            
            for job_name, job_group in job_groups:
                position_groups = job_group.groupby('직위')
                
                for position_name, position_group in position_groups:
                    # 질문 카테고리별 답변 집계
                    question_answer_map = Counter()
                    unique_categories = set(self.category_map.values())
                    question_answers_pool = {cat: [] for cat in unique_categories}
                    
                    for _, row in position_group.iterrows():
                        question_content = self.clean_text(row['질문'])
                        answer_content = self.clean_text(row['답변'])
                        
                        matched_keyword = None
                        for keyword in self.common_question_keywords:
                            if keyword in question_content:
                                matched_keyword = keyword
                                break
                        
                        if matched_keyword and matched_keyword in self.category_map:
                            mapped_cat = self.category_map[matched_keyword]
                            question_answer_map[mapped_cat] += 1
                            question_answers_pool[mapped_cat].append(answer_content)

                    if not question_answer_map:
                        continue

                    # 가장 많이 나오는 카테고리 선택
                    top_10_questions = question_answer_map.most_common(10)
                    
                    for rank, (question_keyword, count) in enumerate(top_10_questions, 1):
                        all_matched_answers = question_answers_pool[question_keyword]
                        if len(all_matched_answers) > 100:
                            all_matched_answers = random.sample(all_matched_answers, 100)

                        extracted_keywords = self.extract_keywords_multilingual(all_matched_answers, top_n=20)
                        keywords_text = ', '.join(extracted_keywords) if extracted_keywords else ''
                        
                        separate_results.append({
                            '산업분야': industry_name,
                            '직무': job_name,
                            '직위': position_name,
                            '질문순위': rank,
                            '핵심단어': question_keyword,
                            '질문빈도': count,
                            '답변키워드_TOP20': keywords_text
                        })
        
        # 결과를 DataFrame으로 변환 및 저장
        result_df = pd.DataFrame(separate_results)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(base_dir, 'jobkorea_keyword_analysis.csv')
        result_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"기존 규격 파일 저장 완료: {output_file}")
        
        # 신규 기능(직무별 실무&대기업 인재상 키워드 추출) 실행
        self.analyze_by_job_and_talent()
        
        return result_df

if __name__ == "__main__":
    extractor = KeywordExtractor()
    extractor.analyze_jobkorea_data()
