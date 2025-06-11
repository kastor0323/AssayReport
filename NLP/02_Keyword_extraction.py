import pandas as pd
from kiwipiepy import Kiwi
from collections import Counter
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
import random

class KeywordExtractor:
    def __init__(self, file_path='C:/Coding/WorkSpace/NLP/data/잡코리아_합격자소서.xlsx'):
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
        
        # 자소서 핵심 질문 키워드 (이미지 참고 및 일반적인 자소서 질문)
        self.common_question_keywords = [
            '지원동기', '성장과정', '장단점', '입사포부', '자기소개',
            '경험', '도전', '극복', '협업', '리더십', '실패', '갈등',
            '직무역량', '전공', '취업준비', '회사선택', '미래계획', '비전', '핵심역량',
            '강점', '약점', '역량', '직무', '성격', '가치관', '문제해결', '성공', '실패',
            # 추가: 이미지에서 보이는 '성장과정' 키워드와 관련된 일반적인 질문
            '본인의 강점', '본인의 약점', '가장 힘들었던 경험', '가장 어려웠던 일', '가장 보람있었던 경험',
            '직무 수행', '직무 관련', '인턴 경험', '프로젝트 경험', '어학연수', '학업 경험',
            '사회생활', '조직생활', '팀워크', '소통', '리더', '팔로워', '변화', '혁신',
            '윤리의식', '도덕성', '가치관', '인생관', '삶의 목표', '존경하는 인물',
            '지원 직무', '입사 후 목표', '10년 후 모습', '회사에 기여할 수 있는 점'
        ]

    def clean_text(self, text):
        """텍스트 정제 - null bytes 제거"""
        if pd.isna(text) or text == '':
            return ''
        
        text_str = str(text)
        # null bytes 제거
        text_str = text_str.replace('\x00', '')
        text_str = text_str.replace('\0', '')
        
        return text_str.strip()
    
    def extract_words(self, text):
        """텍스트에서 단어 추출 (한글, 영어 단어 모두 포함)"""
        if not text:
            return []
        
        # null bytes 제거
        text = self.clean_text(text)
        
        # 한글, 영어, 공백 제외 문자 제거
        cleaned = re.sub(r'[^\uAC00-\uD7A3a-zA-Z\s]', ' ', text)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip().lower()
        words = cleaned.split()
        
        # 너무 짧은 단어 및 특정 단어 제거 (1글자 단어, '공사' 제외)
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
        """질문에서 핵심 구문 추출 - 단어 기반"""
        if pd.isna(text) or text == '':
            return None
        
        # 기존 패턴 체크 및 핵심 단어 매핑
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
         # 패턴 매칭된 실제 텍스트 반환
        for pattern, key_word in key_pattern_map.items():
            if re.search(pattern, text_lower):
                return key_word
        
        # 패턴이 없으면 질문 전체의 주요 단어들을 반환
        words = self.extract_words(text)
        
        # 불용어 제거 (한국어)
        korean_stopwords = {'이', '그', '저', '것', '수', '때', '등', '및', '또는', '하여', '하는', '되는', '있는', '없는', '위해', '통해', '대해', '관해', '대한', '관한', '있어', '없어', '해서', '해야', '하고', '하며', '하는', '되고', '되며', '되는', '시에', '경우', '같은', '다른', '이런', '그런', '저런', '어떤', '무엇', '언제', '어디', '어떻게', '왜', '누구'}
        
        # 불용어 제거하고 상위 단어들만 사용
        filtered_words = [word for word in words if word not in korean_stopwords and len(word) >= 2]
        
        # 단어가 있다면 첫 번째 단어만 반환, 없으면 원본 텍스트의 처음 20글자 반환
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
            
            # 핵심 구문 추출
            key_phrase1 = self.extract_key_phrases_word_based(q1)
            
            for j, q2 in enumerate(questions[i+1:], i+1):
                if j in processed or q2 == '':
                    continue
                
                # 단어 기반 유사도 계산
                similarity = self.word_based_similarity(q1, q2)
                
                # 유사도가 임계값 이상이면 같은 그룹으로 묶기
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
            
            # null bytes 제거
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
                    print(f"    Kiwi 분석 오류: {e}")
                    continue
        
        all_words = korean_nouns + english_words
        
        if not all_words:
            return []
        
        counter = Counter(all_words)
        return [word for word, count in counter.most_common(top_n)]

    def analyze_jobkorea_data(self):
        """직무-직위별 핵심 질문 단어 기반 그룹화, 상위 5개 질문 선택, 해당 답변의 상위 20개 키워드 추출"""
        
        # 데이터 로드
        try:
            df = pd.read_excel(self.file_path, engine='openpyxl')
            print(f"데이터 로드 완료: {len(df)}개 행")
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(self.file_path, delimiter='\t', encoding='cp949')
                print(f"데이터 로드 완료 (cp949): {len(df)}개 행")
            except:
                df = pd.read_csv(self.file_path, delimiter='\t', encoding='euc-kr')
                print(f"데이터 로드 완료 (euc-kr): {len(df)}개 행")
        
        df = df.fillna('')
        
        separate_results = []
        job_groups = df.groupby('직무')
        print(f"\n총 {len(job_groups)}개 직무 발견")
        
        for job_name, job_group in job_groups:
            position_groups = job_group.groupby('직위')
            print(f"\n[{job_name}] {len(position_groups)}개 직위")
            
            for position_name, position_group in position_groups:
                print(f"  - {position_name}: {len(position_group)}개 데이터")
                
                # 질문 핵심 단어별 답변 집계
                question_answer_map = Counter()
                question_answers_pool = {keyword: [] for keyword in self.common_question_keywords}
                
                for _, row in position_group.iterrows():
                    question_content = self.clean_text(row['질문'])
                    answer_content = self.clean_text(row['답변'])
                    
                    matched_keyword = None
                    for keyword in self.common_question_keywords:
                        if keyword in question_content:
                            matched_keyword = keyword
                            break
                    
                    if matched_keyword:
                        question_answer_map[matched_keyword] += 1
                        question_answers_pool[matched_keyword].append(answer_content)

                if not question_answer_map:
                    print(f"    해당 직무/직위에서 매칭되는 자소서 질문이 없습니다. 스킵합니다.")
                    continue

                # 가장 많이 나오는 질문 5개 선택
                top_5_questions = question_answer_map.most_common(5)
                print(f"    상위 5개 질문 키워드: {top_5_questions}")
                
                for rank, (question_keyword, count) in enumerate(top_5_questions, 1):
                    all_matched_answers = question_answers_pool[question_keyword]
                    # 답변이 너무 많으면 일부만 추출하여 키워드 추출 성능 향상
                    if len(all_matched_answers) > 100: # 예시: 100개 초과 시 랜덤 100개 선택
                        all_matched_answers = random.sample(all_matched_answers, 100)

                    extracted_keywords = self.extract_keywords_multilingual(all_matched_answers, top_n=20)
                    keywords_text = ', '.join(extracted_keywords) if extracted_keywords else ''
                    
                    separate_results.append({
                        '직무': job_name,
                        '직위': position_name,
                        '질문순위': rank,
                        '핵심단어': question_keyword,
                        '질문빈도': count,
                        '답변키워드_TOP20': keywords_text
                    })
        
        # 결과를 DataFrame으로 변환
        result_df = pd.DataFrame(separate_results)
        output_file = 'jobkorea_keyword_analysis.csv'
        result_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        print(f"\n=== 분석 완료 ===")
        print(f"결과가 '{output_file}' 파일로 저장되었습니다.")
        print(f"총 {len(separate_results)}개의 개별 질문 행이 생성되었습니다.")
        
        return result_df

if __name__ == "__main__":
    extractor = KeywordExtractor()
    result = extractor.analyze_jobkorea_data()
