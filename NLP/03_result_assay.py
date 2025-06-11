# resume_evaluator.py
import pandas as pd
from kiwipiepy import Kiwi
from collections import Counter
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag

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
        # 해당 직무/직위 데이터 필터링
        filtered_df = self.reference_df[
            (self.reference_df['직무'] == job_title) & 
            (self.reference_df['직위'] == position)
        ]
        
        if filtered_df.empty:
            print(f"❌ '{job_title} - {position}' 데이터가 없습니다.")
            available_jobs = self.reference_df.groupby(['직무', '직위']).size().reset_index(name='count')
            print("\n📋 사용 가능한 직무/직위:")
            for _, row in available_jobs.iterrows():
                # Display core keywords available for each job/position
                keywords_for_job = self.reference_df[
                    (self.reference_df['직무'] == row['직무']) &
                    (self.reference_df['직위'] == row['직위'])
                ]['핵심단어'].tolist()
                print(f"  - {row['직무']} ({row['직위']}) - 핵심단어: {', '.join(keywords_for_job)}")
            return None
        
        max_similarity = 0
        best_match_keyword = None
        best_match_data = None
        
        for idx, row in filtered_df.iterrows():
            # Compare user_question with '핵심단어'
            similarity = self.word_based_similarity(user_question, row['핵심단어']) # Changed column
            if similarity > max_similarity:
                max_similarity = similarity
                best_match_keyword = row['핵심단어'] # Changed to 핵심단어
                best_match_data = row
        
        return best_match_keyword, max_similarity, best_match_data # Returned best_match_keyword
    
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
        
        # Jaccard 유사도 계산
        intersection = user_keyword_set.intersection(reference_keyword_set)
        union = user_keyword_set.union(reference_keyword_set)
        
        jaccard_score = len(intersection) / len(union) if union else 0
        
        return jaccard_score, list(intersection)
    
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
                
                # 키워드 매칭 점수를 10개 기준으로 조정
                matched_keyword_count = len(matched_keywords)
                total_score = min(matched_keyword_count * 10, 100)  # 10개 키워드 = 100점
                
                evaluation_results.append({
                    '질문번호': i + 1,
                    '사용자질문': user_question,
                    '사용자답변': user_answer[:50] + "..." if len(user_answer) > 50 else user_answer,
                    '가장유사한질문': best_keyword,
                    '매칭된키워드': ', '.join(matched_keywords),
                    '매칭된키워드수': matched_keyword_count,
                    '종합점수': round(total_score, 1)
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


def main():
    """메인 실행 함수 - 사용 예시"""
    
    # 평가기 초기화
    evaluator = ResumeEvaluator('jobkorea_keyword_analysis.csv')
    
    # 사용자 자소서 데이터 (예시)
    user_resume_data = {
        '직무': 'AI/ML엔지니어',
        '직위': '신입',
        'qa_pairs': [
            {
                'question': '경험에 대해 말씀해주세요',
                'answer': '저는 AI/ML 엔지니어로서 다양한 프로젝트 경험을 쌓았습니다. 대규모 데이터셋을 활용하여 복잡한 문제를 해결하는 모델 개발에 도전했으며, 목표 달성을 위해 꾸준히 노력했습니다. 특히, 딥러닝 모델 구현 프로젝트를 성공적으로 이끌며 높은 성능을 달성했습니다. 이 과정에서 데이터 수집, 전처리, 모델링, 학습, 성능 최적화에 이르는 전 과정을 담당하며 많은 실패와 도전을 겪었지만, 끊임없는 분석과 노력을 통해 목표를 달성했습니다. 공모전에 참여하여 혁신적인 아이디어를 구현하고, 팀원들과의 협업을 통해 시너지를 창출하며 좋은 결과를 얻었던 경험도 있습니다. 이러한 경험들은 제가 AI/ML 분야에서 직면할 수 있는 다양한 문제에 효과적으로 대응하고, 실제 서비스에 적용 가능한 모델을 개발하는 데 중요한 역량이 될 것이라고 확신합니다. 또한, 새로운 기술을 공부하고 배우는 것을 시작으로, 저의 역량을 계속해서 발전시키는 방향으로 나아가고 싶습니다.'
            },
            {
                'question': '본인의 역량을 설명해주세요',
                'answer': '저의 핵심 역량은 AI/ML 모델의 구현, 최적화 및 시스템 통합 능력입니다. 특히, 효율적인 알고리즘 설계와 데이터 처리 기술을 바탕으로 복잡한 AI 시스템을 구축하는 데 강점이 있습니다. 번호판 자동 인식 시스템 개발 프로젝트에서는 TensorFlow와 Keras를 활용하여 CNN 모델을 구현하고, 임베디드 시스템에 적용하여 실제 환경에서의 성능을 성공적으로 향상시킨 경험이 있습니다. 또한, 학습된 모델을 실제 서비스에 적용하기 위한 기술적인 이해와 데이터 분석 역량 또한 뛰어납니다. 연구 과정에서 발생할 수 있는 다양한 문제들을 해결하기 위해 새로운 기술을 끊임없이 학습하고, 이를 실제 프로젝트에 적용하는 데 주저하지 않습니다. 이러한 역량들은 AI/ML 엔지니어로서 실제 문제를 해결하고, 기술 발전에 기여하는 데 필수적인 요소라고 생각합니다. 보드 기반의 시스템 개발과 차량 관련 데이터 처리 경험도 풍부합니다.'
            },
            {
                'question': '직무에 대한 생각을 말씀해주세요',
                'answer': 'AI/ML 엔지니어 직무는 단순히 코드를 작성하는 것을 넘어, 데이터를 기반으로 실제 비즈니스 가치를 창출하는 것이라고 생각합니다. 경량화된 모델을 통해 최적의 성능을 제공하고, 효율적인 메모리 처리를 통해 시스템의 자원 활용을 극대화하는 것이 중요하다고 봅니다. 또한, 끊임없이 변화하는 기술 환경 속에서 새로운 알고리즘을 연구하고, 이를 실제 서비스에 적용하는 능력이 필요하다고 생각합니다. 저는 석사 과정 동안 다양한 환경에서의 AI 모델 개발을 진행하며, 이러한 직무 역량을 충분히 길러왔습니다. 동반 성장을 추구하는 회사의 목표에 부합하기 위해 지속적으로 저의 스킬을 개발하고, 실제 현장에서 발생할 수 있는 복잡한 문제들을 해결하는 데 기여하고 싶습니다. 최고 수준의 AI/ML 전문가로 성장하여 회사와 함께 AI 산업을 선도하는 데 일조하겠습니다. 개발 역량을 보유하고 있으며, 데이터 처리 능력도 뛰어납니다.'
            },
            {
                'question': '자기소개를 해보세요',
                'answer': '저는 데이터에 대한 깊은 이해와 열정을 가진 AI/ML 엔지니어입니다. 다양한 분야에서 데이터를 다루고 분석하며 문제 해결 능력을 키워왔습니다. 대학교 시절부터 머신러닝, 딥러닝 관련 프로젝트와 논문 연구에 적극적으로 참여하며 이론적 지식과 실무 경험을 동시에 쌓았습니다. 특히, 연구실에서 진행했던 프로젝트들은 저에게 끊임없이 도전하고 배우는 기회를 제공했으며, 새로운 기술과 방법을 탐구하는 데 대한 강한 동기를 부여했습니다. 통계학적 지식과 프로그래밍 능력을 바탕으로 데이터를 효과적으로 분석하고, 이를 통해 의미 있는 인사이트를 도출하는 데 능숙합니다. 학부 시절부터 관련 학회에 꾸준히 참여하며 최신 트렌드를 파악하고, AI 분야의 전문가들과 교류하며 저의 역량을 더욱 확장해왔습니다. 이러한 경험과 지식을 바탕으로 귀사의 AI/ML 엔지니어로서 혁신적인 솔루션을 개발하고, 회사 성장에 기여하고 싶습니다. 여러 분야를 공부하며 쌓은 생각들을 공유하고 싶습니다.'
            }
        ]
    }
    
    # 자소서 평가 실행
    result = evaluator.evaluate_resume(user_resume_data)

    if result is not None:
        print("\n=== 자소서 평가 결과 ===")
        print(f"총점: {result['평균점수']}점")
        print(f"등급: {result['등급']}")
        print("\n=== 상세 결과 ===")
        for item in result['상세결과']:
            print(f"\n[질문 {item['질문번호']}] 점수: {item['종합점수']}점")
            print(f"질문: {item['사용자질문']}")
            print(f"답변: {item['사용자답변']}")
            print(f"유사한 질문: {item['가장유사한질문']}")
            print(f"매칭된 키워드: {item['매칭된키워드']}")
            print(f"매칭된 키워드 수: {item['매칭된키워드수']}")
            print("-" * 50)
    else:
        print("\n❌ 평가를 완료할 수 없습니다.")


if __name__ == "__main__":
    main()
