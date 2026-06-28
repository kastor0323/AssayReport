"""
잡코리아 합격자소서 스크래핑 프로그램
1.잡코리아에 접속 후 아이디와 패스워드를 입력한다.
2. 로그인이 성공되면 Beautiful soup을 통해 합격 자소서를 스크래핑을 시작
3. 산업군과 경력 회사로 구분하여 데이터를 출력한다.
Python 3.13.3 호환
"""

import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import os
import datetime
from urllib.parse import urljoin, urlparse
import logging
import getpass
import json

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 수집 기간: 최근 3년 이내 (스크랩 연도 - 3, 해당 연도 포함)
CUTOFF_YEAR = datetime.datetime.now().year - 3

class JobkoreaScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        self.load_company_data()

    def load_company_data(self):
        """기업 데이터 로드"""
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(base_dir, 'data', 'companies.json')
            with open(json_path, 'r', encoding='utf-8') as f:
                companies = json.load(f)

            self.company_to_industry = {}
            for co in companies:
                self.company_to_industry[co['name']] = co['industry']
            logger.info(f"기업 데이터 로드 완료 ({len(self.company_to_industry)}개 기업)")
        except Exception as e:
            logger.error(f"기업 데이터 로드 오류: {e}")
            self.company_to_industry = {}

    def get_industry_by_company(self, company_name):
        """회사명으로 산업군 찾기. Top 100 기업이 아니면 None 반환."""
        if not company_name:
            return None
        if company_name in self.company_to_industry:
            return self.company_to_industry[company_name]
        for co_name, industry in self.company_to_industry.items():
            if co_name in company_name or company_name in co_name:
                return industry
        return None

    def login_to_jobkorea(self, user_id, password):
        """잡코리아 로그인"""
        try:
            logger.info("잡코리아 로그인 시도...")
            
            # 먼저 메인 페이지에 접속해서 쿠키를 받아옴
            main_url = "https://www.jobkorea.co.kr/"
            response = self.session.get(main_url)
            
            if response.status_code != 200:
                logger.error(f"메인 페이지 접속 실패: {response.status_code}")
                return False
            
            # 로그인 페이지로 이동
            login_url = "https://www.jobkorea.co.kr/Login/Login_Tot.asp?rDBName=GG&re_url=%2f%3fschTxt%3d%26Page%3d"
            response = self.session.get(login_url)
            
            if response.status_code != 200:
                logger.error(f"로그인 페이지 접속 실패: {response.status_code}")
                return False
            
            soup = BeautifulSoup(response.content, 'html.parser')
            logger.info(f"로그인 페이지 응답 코드: {response.status_code}")
            
            # 로그인 폼에서 필요한 데이터 찾기
            login_form = soup.find('form')
            if not login_form:
                logger.error("로그인 폼을 찾을 수 없습니다")
                return False
            
            # 폼 액션 URL 찾기
            action_url = login_form.get('action', '/Login/Login.asp')
            if not action_url.startswith('http'):
                action_url = "https://www.jobkorea.co.kr" + action_url
            
            # 로그인 폼 데이터 준비 - 잡코리아 실제 필드명 사용
            login_data = {
                'M_ID': user_id,
                'M_PWD': password,
                'rDBName': 'GG',
                'LoginType': 'Members'
            }
            
            # 폼에서 추가 hidden 필드들 찾기
            hidden_inputs = soup.find_all('input', type='hidden')
            for hidden_input in hidden_inputs:
                name = hidden_input.get('name')
                value = hidden_input.get('value', '')
                if name and name not in login_data:
                    login_data[name] = value
            
            # 로그인 요청
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': login_url
            }
            
            response = self.session.post(action_url, data=login_data, headers=headers, allow_redirects=True)
            logger.info(f"로그인 응답 코드: {response.status_code}")
            logger.info(f"최종 URL: {response.url}")
            
            # 실제 로그인 성공 여부를 확인하기 위해 합격자소서 페이지 접근 시도
            passassay_url = "https://www.jobkorea.co.kr/starter/passassay"
            test_response = self.session.get(passassay_url)
            
            logger.info(f"합격자소서 페이지 접근 코드: {test_response.status_code}")
            
            if test_response.status_code == 200:
                soup = BeautifulSoup(test_response.content, 'html.parser')
                
                # 로그인이 필요하다는 메시지가 있는지 확인
                login_required_indicators = [
                    '로그인이 필요',
                    '로그인 후 이용',
                    '회원가입',
                    'login',
                    '로그인하세요'
                ]
                
                page_text = soup.get_text()
                needs_login = any(indicator in page_text for indicator in login_required_indicators)
                
                # 합격자소서 관련 내용이 있는지 확인
                passassay_indicators = [
                    '합격자소서',
                    '자기소개서',
                    '면접후기',
                    '회사명',
                    '지원직무'
                ]
                
                has_passassay_content = any(indicator in page_text for indicator in passassay_indicators)
                
                if has_passassay_content and not needs_login:
                    logger.info("✅ 로그인 성공! (합격자소서 페이지 접근 가능)")
                    return True
                elif needs_login:
                    logger.error("❌ 로그인 실패: 여전히 로그인이 필요함")
                    return False
                else:
                    logger.warning("⚠️ 로그인 상태 불분명, 계속 진행...")
                    return True  # 일단 성공으로 간주하고 진행
            else:
                logger.error(f"❌ 합격자소서 페이지 접근 실패: {test_response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"로그인 오류: {e}")
            return False

    def extract_company_name_from_link(self, soup):
        """기업 홈 이동 링크에서 회사명 추출 - NLP_Project 방식"""
        company_name = ""
        
        try:
            # NLP_Project에서 사용한 셀렉터들을 BeautifulSoup용으로 변환
            company_link_selectors = [
                'a[title="기업 홈 이동"]',
                'a[href*="/Recruit/Co_Read/C/"]',
                'a[target="_blank"][title="기업 홈 이동"]'
            ]
            
            for selector in company_link_selectors:
                try:
                    company_link = soup.select_one(selector)
                    if company_link:
                        company_name = company_link.get_text(strip=True)
                        if company_name and len(company_name) > 1:
                            logger.info(f"기업 홈 링크에서 회사명 추출: {company_name}")
                            return company_name
                except Exception as e:
                    logger.debug(f"셀렉터 {selector} 오류: {e}")
                    continue
                    
            logger.warning("❌ 회사명을 찾을 수 없습니다.")
            return ""
            
        except Exception as e:
            logger.error(f"기업 홈 링크에서 회사명 추출 오류: {e}")
            return ""

    def extract_position_text_from_em(self, soup):
        """em 태그에서 직무 관련 텍스트 추출 - NLP_Project 방식"""
        position_text = ""
        
        try:
            # 1. em 태그에서 텍스트 추출 (우선순위)
            em_elements = soup.find_all("em")
            for elem in em_elements:
                try:
                    text = elem.get_text(strip=True)
                    if text and len(text) > 3:
                        position_text = text
                        logger.info(f"em 태그에서 텍스트 추출: {text}")
                        return position_text
                except:
                    continue
            
            # 2. em 태그에서 못 찾으면 title에서 추출
            if not position_text:
                try:
                    # BeautifulSoup에서는 soup.title.string 사용
                    title_tag = soup.find('title')
                    if title_tag:
                        position_text = title_tag.get_text(strip=True)
                        logger.info(f"제목에서 텍스트 추출: {position_text}")
                    else:
                        position_text = ""
                except:
                    position_text = ""
                    
            # 3. 그래도 없으면 h1, h2 태그에서 찾기
            if not position_text:
                for tag_name in ['h1', 'h2']:
                    try:
                        header_elem = soup.find(tag_name)
                        if header_elem:
                            text = header_elem.get_text(strip=True)
                            if text and len(text) > 3:
                                position_text = text
                                logger.info(f"{tag_name} 태그에서 텍스트 추출: {text}")
                                break
                    except:
                        continue
                        
        except Exception as e:
            logger.error(f"텍스트 추출 오류: {e}")
            position_text = ""
        
        return position_text

    def extract_position_info(self, text):
        """텍스트에서 연도/기간, 상태, 직업 분리 - NLP_Project 방식 그대로"""
        year_period = ""
        status = ""
        job = ""
        
        try:
            # 연도/기간 추출
            year_period_match = re.search(r"\d{4}년?\s*[상하]반기", text)
            if year_period_match:
                year_period = year_period_match.group(0)
            
            # 상태 추출 (인턴, 신입만)
            status_keywords = ["인턴", "신입"]
            for keyword in status_keywords:
                if keyword in text:
                    status = keyword
                    break
            
            # 직업 추출 - NLP_Project 방식 그대로
            words = text.split()
            for word in words:
                # 상태 키워드 제외
                if word in status_keywords:
                    continue
                # 연도/기간 관련 단어 제외
                if any(time_word in word for time_word in ["년", "반기", "202"]):
                    continue
                # 길이가 2글자 이상이고 한글, 영문, 숫자, 특수문자 포함
                if len(word) >= 2 and re.match(r'^[\w가-힣·&]+$', word):
                    job = word
                    break
            
            logger.info(f"텍스트 분석 결과 - 기간: '{year_period}', 상태: '{status}', 직업: '{job}'")
            
        except Exception as e:
            logger.error(f"텍스트 분석 오류: {e}")
        
        return year_period, status, job

    def extract_company_info_improved(self, soup):
        """NLP_Project 방식을 적용한 개선된 회사 정보 추출"""
        company_name = ""
        period = ""
        position = ""
        job_role = ""
        
        try:
            # 1. 회사명 추출 - NLP_Project 방식 적용
            company_name = self.extract_company_name_from_link(soup)
            
            # 2. 직무 관련 텍스트 추출 - em 태그 우선
            position_text = self.extract_position_text_from_em(soup)
            
            # 3. 추출된 텍스트에서 정보 분리
            if position_text:
                period, position, job_role = self.extract_position_info(position_text)
            
            # 4. 기본값 설정
            if not period:
                current_year = datetime.datetime.now().year
                period = f"{current_year}년"
                
            logger.info(f"개선된 추출 결과 - 회사: '{company_name}', 기간: '{period}', 직위: '{position}', 직무: '{job_role}'")
            
        except Exception as e:
            logger.error(f"개선된 회사 정보 추출 오류: {e}")
        
        return company_name, period, position, job_role

    def clean_question_text(self, question_text):
        """질문 텍스트 전처리 - 불필요한 접두사 제거"""
        if not question_text:
            return ""
        
        # 'Q1.', 'Q2.' 등 제거
        question_text = re.sub(r'^Q\d+\.?\s*', '', question_text)
        
        # '질문Q1.', '질문Q2.' 등 제거  
        question_text = re.sub(r'^질문Q\d+\.?\s*', '', question_text)
        
        # '보기' 등 불필요한 부분 제거
        question_text = re.sub(r'보기$', '', question_text)
        
        return question_text.strip()

    def clean_answer_text(self, answer_text):
        """답변 텍스트 전처리 - 불필요한 접두사/접미사 제거"""
        if not answer_text:
            return ""
        
        # 앞의 '답변' 제거
        answer_text = re.sub(r'^답변\s*', '', answer_text)
        
        # 뒤의 글자수 정보 제거 (예: '글자수1,320자2,066Byte')
        answer_text = re.sub(r'글자수[\d,]+자[\d,]+Byte$', '', answer_text)
        
        return answer_text.strip()

    def extract_clean_qa_pairs(self, soup):
        """NLP_Project 방식의 Q&A 추출 및 정리"""
        questions = []
        answers = []

        try:
            # 자소서 본문 영역만 선택
            main_content = None
            content_selectors = [
                ".qnaLists",  # 메인 Q&A 리스트
                ".passAssayContent",  # 자소서 내용
                ".essay_content",  # 에세이 내용
                "#passAssayQnaLists",  # Q&A 리스트 ID
                ".passAssayView .qna"  # 자소서 뷰의 Q&A
            ]

            for selector in content_selectors:
                try:
                    main_content = soup.select_one(selector)
                    if main_content:
                        logger.info(f"메인 콘텐츠 영역 발견: {selector}")
                        break
                except:
                    continue

            if not main_content:
                logger.info("메인 콘텐츠 영역을 찾을 수 없어 전체 페이지에서 추출 시도")
                main_content = soup

            # dt(질문), dd(답변) 태그 쌍으로 추출
            question_elements = main_content.find_all('dt')
            answer_elements = main_content.find_all('dd')

            logger.info(f"질문 요소 수: {len(question_elements)}, 답변 요소 수: {len(answer_elements)}")

            for i in range(min(len(question_elements), len(answer_elements))):
                try:
                    # 질문 처리
                    question_elem = question_elements[i]
                    question_text = self.extract_text_from_element(question_elem)

                    # 답변 처리
                    answer_elem = answer_elements[i]
                    answer_text = self.extract_text_from_element(answer_elem)

                    # 유효한 질문/답변인지 확인 (엄격한 필터링)
                    if self.is_valid_essay_qa(question_text, answer_text):
                        # 텍스트 정리
                        cleaned_question = self.clean_question_text(question_text)
                        cleaned_answer = self.clean_answer_text(answer_text)
                        
                        questions.append(cleaned_question)
                        answers.append(cleaned_answer)
                        logger.info(f"유효한 Q{len(questions)}: {cleaned_question[:30]}...")
                    else:
                        logger.info(f"무효한 데이터 제외: Q='{question_text}', A='{answer_text[:30]}'")

                except Exception as e:
                    logger.error(f"Q&A {i+1} 처리 오류: {e}")
                    continue

            return questions, answers

        except Exception as e:
            logger.error(f"Q&A 추출 오류: {e}")
            return [], []

    def extract_text_from_element(self, element):
        """텍스트 추출"""
        try:
            # .tx 클래스가 있으면 우선 사용
            tx_elem = element.select_one('.tx')
            if tx_elem:
                return tx_elem.get_text(strip=True)
        except:
            pass
        # 전체 텍스트 사용
        return element.get_text(strip=True)

    def is_valid_essay_qa(self, question, answer):
        """유효한 자소서인지 검증"""
        # 1차: 불필요한 키워드 완전 차단
        invalid_keywords = [
            '공지사항', 'FAX', 'Email', 'email', '전화번호', '고객센터',
            '이용약관', '개인정보', '잡코리아', '알바몬', 'jobkorea',
            '02-565-9351', '평일 09:00', '토요일 09:00', '19:00', '15:00',
            '설문이벤트', '당첨자', '발표', '채용담당자', '채용 트렌드',
            '키워드', '사칭 연락', '주의하세요', 'YYYYMMDD', '25.05',
            '(평일', '토요일)', 'x알바몬', '무료'
        ]

        question_lower = question.lower()
        answer_lower = answer.lower()

        for keyword in invalid_keywords:
            if keyword.lower() in question_lower or keyword.lower() in answer_lower:
                return False

        # 2차: 숫자나 날짜만 있는 것 제외
        if answer.replace(' ', '').replace('-', '').replace(':', '').isdigit():
            return False

        return True  # 나머지는 모두 허용
    
    def extract_essay_content(self, essay_url):
        """개별 자소서 내용 추출 - NLP_Project 통합 버전"""
        logger.info(f"자소서 추출 시작: {essay_url}")
        
        try:
            response = self.session.get(essay_url)
            if response.status_code != 200:
                logger.error(f"페이지 접속 실패: {response.status_code}")
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            essay_data = {
                'url': essay_url,
                'company': '',
                'year_period': '',
                'status': '',
                'job': '',
                'questions': [],
                'answers': [],
                'essay_id': ''
            }
            
            # URL에서 essay_id 추출
            if "/View/" in essay_url:
                essay_data['essay_id'] = essay_url.split("/View/")[-1].split("?")[0]
            
            # 회사명 추출 - NLP_Project 방식
            company_name = self.extract_company_name_from_link(soup)
            essay_data['company'] = company_name

            # Top 100 기업 필터: 해당 기업이 아니면 스킵
            industry = self.get_industry_by_company(company_name)
            if not industry:
                logger.info(f"Top 100 기업 아님 (스킵): {company_name}")
                return None
            essay_data['industry'] = industry
            
            # 직무 관련 텍스트 추출 - NLP_Project 방식
            position_text = self.extract_position_text_from_em(soup)
            
            # 직무 정보 파싱 - NLP_Project 방식
            try:
                year_period, status, job = self.extract_position_info(position_text)
                essay_data['year_period'] = year_period
                essay_data['status'] = status
                essay_data['job'] = job
                logger.info(f"추출된 정보 - 기간: '{year_period}', 상태: '{status}', 직업: '{job}'")
            except ValueError as e:
                logger.error(f"언패킹 오류: {e}")
                essay_data['year_period'] = ""
                essay_data['status'] = ""
                essay_data['job'] = ""

            # 연도 필터: 스크랩 연도 기준 3년 이내만 수집 (해당 연도 포함)
            year_match = re.search(r'(\d{4})', essay_data['year_period'])
            if year_match:
                essay_year = int(year_match.group(1))
                if essay_year < CUTOFF_YEAR:
                    logger.info(f"3년 범위 초과 (스킵): {essay_data['year_period']} (기준: {CUTOFF_YEAR}년 이상)")
                    return None
            
            # 실제 자소서 Q&A만 추출 - NLP_Project 방식
            questions, answers = self.extract_clean_qa_pairs(soup)
            essay_data['questions'] = questions
            essay_data['answers'] = answers
            
            return essay_data if questions else None
            
        except Exception as e:
            logger.error(f"자소서 내용 추출 오류: {e}")
            return {
                'url': essay_url,
                'company': '',
                'year_period': '',
                'status': '',
                'job': '',
                'questions': [],
                'answers': [],
                'essay_id': ''
            }
    
    def get_essay_links_from_page(self, page_url):
        """페이지에서 자소서 링크 추출"""
        try:
            response = self.session.get(page_url)
            if response.status_code != 200:
                logger.error(f"페이지 접속 실패: {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            essay_links = []
            
            # 자소서 링크 찾기
            selectors = [
                'a[href*="/starter/PassAssay/View/"]',
                'a[href*="PassAssay/View"]',
                'a[href*="passassay/View"]',
                'a[href*="passassay/view"]'
            ]
            
            for selector in selectors:
                try:
                    links = soup.select(selector)
                    for link in links:
                        href = link.get('href')
                        if href:
                            # 상대 URL을 절대 URL로 변환
                            full_url = urljoin(page_url, href)
                            if any(keyword in full_url for keyword in ['PassAssay/View', 'passassay/View', 'passassay/view']):
                                essay_links.append(full_url)
                    
                    if essay_links:
                        break
                except:
                    continue
            
            # 중복 제거
            essay_links = list(set(essay_links))
            logger.info(f"페이지에서 {len(essay_links)}개 자소서 링크 발견")
            
            return essay_links
            
        except Exception as e:
            logger.error(f"링크 추출 오류: {e}")
            return []
    
    def scrape_jobkorea_with_login(self, user_id, password, start_page=1, end_page=10):
        """메인 스크래핑 함수"""
        all_essays = []
        
        try:
            # 로그인
            logger.info("=== 로그인 시도 ===")
            if not self.login_to_jobkorea(user_id, password):
                logger.error("로그인 실패. 프로그램을 종료합니다.")
                return []
            
            logger.info("\n=== 합격자소서 페이지로 이동 ===")
            base_url = "https://www.jobkorea.co.kr/starter/PassAssay?schPart=&schWork=&schEduLevel=&schCType=13&schGroup=&isSaved=1&isFilterChecked=1&OrderBy=0&schTxt=&Page="
            
            for page in range(start_page, end_page + 1):
                logger.info(f"\n페이지 {page}/{end_page} 처리 중...")
                
                page_url = base_url + str(page)
                
                # 자소서 링크 찾기
                essay_links = self.get_essay_links_from_page(page_url)
                
                if not essay_links:
                    logger.warning("자소서 링크를 찾을 수 없습니다.")
                    continue
                
                # 각 자소서 처리 (페이지당 최대 3개)
                for i, essay_url in enumerate(essay_links[:3]):
                    logger.info(f"\n  {i+1}/{min(len(essay_links), 3)} 자소서 처리...")
                    logger.info(f"  URL: {essay_url}")
                    
                    essay_data = self.extract_essay_content(essay_url)
                    
                    if essay_data and essay_data['questions']:
                        all_essays.append(essay_data)
                        logger.info(f"    ✅ 성공!")
                        logger.info(f"       회사: '{essay_data['company']}'")
                        logger.info(f"       연도: '{essay_data['year_period']}'")
                        logger.info(f"       상태: '{essay_data['status']}'")
                        logger.info(f"       직업: '{essay_data['job']}'")
                        logger.info(f"       문항수: {len(essay_data['questions'])}")
                    else:
                        logger.warning(f"    ❌ 실패 또는 유효한 데이터 없음")
                    
                    time.sleep(2)  # 요청 간격
        
        except Exception as e:
            logger.error(f"스크래핑 오류: {e}")
        
        return all_essays

def save_to_excel(essays, save_directory='./data/', start_page=1, end_page=10):
    """데이터를 CSV/JSON으로 저장"""
    os.makedirs(save_directory, exist_ok=True)

    if not essays:
        logger.warning("저장할 데이터가 없습니다.")
        return

    df_data = []
    successful_essays = 0

    for essay in essays:
        if essay and essay['questions'] and essay['answers']:
            successful_essays += 1
            for question, answer in zip(essay['questions'], essay['answers']):
                df_data.append({
                    '회사명': essay['company'],
                    '연도': essay['year_period'],
                    '직무분야': essay.get('industry', '기타'),
                    '직무명': essay['job'],
                    '질문 내용': question,
                    '답변': answer,
                })

    if not df_data:
        logger.warning("변환할 데이터가 없습니다.")
        return

    df = pd.DataFrame(df_data)

    logger.info(f"\n=== 데이터 품질 상세 분석 ===")
    logger.info(f"총 행 수: {len(df)}")
    logger.info(f"성공적으로 처리된 자소서: {successful_essays}/{len(essays)}")

    companies_filled = df[df['회사명'].str.len() > 0]
    logger.info(f"회사명 채워진 행: {len(companies_filled)}/{len(df)} ({len(companies_filled)/len(df)*100:.1f}%)")

    if len(companies_filled) > 0:
        unique_companies = df['회사명'].value_counts()
        logger.info(f"유니크 회사 수: {len(unique_companies)}")
        logger.info("상위 회사들:")
        for company, count in unique_companies.head(5).items():
            if company:
                logger.info(f"  - {company}: {count}개 문항")

    avg_question_len = df['질문 내용'].str.len().mean()
    avg_answer_len = df['답변'].str.len().mean()
    logger.info(f"평균 질문 길이: {avg_question_len:.0f}자")
    logger.info(f"평균 답변 길이: {avg_answer_len:.0f}자")

    # 기존 CSV 로드 후 누적 병합
    csv_path = os.path.join(save_directory, 'jobkorea_scraping_result.csv')

    COLS = ['회사명', '연도', '직무분야', '직무명', '질문 내용', '답변']

    if os.path.exists(csv_path):
        try:
            existing_df = pd.read_csv(csv_path, encoding='utf-8-sig')
            if set(COLS).issubset(set(existing_df.columns)):
                existing_df = existing_df[COLS]
                logger.info(f"\n기존 데이터 {len(existing_df)}행 + 신규 데이터 {len(df)}행 → 병합 중...")
                combined_df = pd.concat([existing_df, df[COLS]], ignore_index=True)
            else:
                logger.warning("기존 CSV 컬럼 불일치 (구 버전). 새로 생성합니다.")
                combined_df = df[COLS]
        except Exception as e:
            logger.error(f"기존 CSV 로드 실패, 새로 생성합니다: {e}")
            combined_df = df[COLS]
    else:
        combined_df = df[COLS]
        logger.info("\n최초 파일 생성")

    before_dedup = len(combined_df)
    combined_df = combined_df.drop_duplicates(subset=['회사명', '연도', '직무명', '질문 내용'], keep='first')
    after_dedup = len(combined_df)
    removed_count = before_dedup - after_dedup

    if removed_count > 0:
        logger.info(f"중복 데이터 {removed_count}행 제거 → 최종 {after_dedup}행")
    else:
        logger.info(f"중복 데이터 없음 → 최종 {after_dedup}행")

    # CSV 저장 (NaN → 빈 문자열로 정규화)
    combined_df = combined_df.fillna('')
    combined_df[COLS].to_csv(csv_path, index=False, encoding='utf-8-sig')
    logger.info(f"\n💾 파일 저장 완료:")
    logger.info(f"   📄 CSV: jobkorea_scraping_result.csv (누적 {after_dedup}행)")

    # JSON 저장 (회사+연도+직무명 단위로 그룹화)
    json_path = os.path.join(save_directory, 'jobkorea_scraping_result.json')
    json_records = []
    for (company, year, job), group in combined_df.groupby(['회사명', '연도', '직무명'], sort=False):
        qa_list = [
            {'질문 내용': row['질문 내용'], '답변': row['답변']}
            for _, row in group.iterrows()
        ]
        json_records.append({
            '회사명': company,
            '연도': year,
            '직무분야': group.iloc[0]['직무분야'],
            '직무명': job,
            'qa': qa_list
        })
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_records, f, ensure_ascii=False, indent=2)
    logger.info(f"   📄 JSON: jobkorea_scraping_result.json ({len(json_records)}개 그룹)")

def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description="잡코리아 합격자소서 스크래핑")
    parser.add_argument("--id", help="잡코리아 아이디")
    parser.add_argument("--password", help="잡코리아 비밀번호")
    parser.add_argument("--start", type=int, default=1, help="시작 페이지 (기본값: 1)")
    parser.add_argument("--end", type=int, default=5, help="끝 페이지 (기본값: 5)")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    save_directory = os.path.join(base_dir, 'data')
    os.makedirs(save_directory, exist_ok=True)

    print("=== 잡코리아 합격자소서 스크래핑 프로그램 ===")
    print("NLP_Project 방식 완전 통합 버전 (Python 3.13.3 호환)")

    user_id = args.id
    password = args.password

    # 인자로 받지 못한 경우에만 대화형 입력
    if not user_id:
        print("로그인 정보를 입력해주세요.\n")
        user_id = input("잡코리아 아이디: ").strip()
    if not user_id:
        print("❌ 아이디를 입력해주세요.")
        return

    if not password:
        password = getpass.getpass("잡코리아 비밀번호: ").strip()
    if not password:
        print("❌ 비밀번호를 입력해주세요.")
        return

    start_page = args.start
    end_page = args.end

    if start_page < 1 or end_page < start_page:
        print("❌ 올바른 페이지 범위를 입력해주세요.")
        return
    
    logger.info(f"\n=== 잡코리아 합격자소서 스크래핑 ({start_page}~{end_page}페이지) ===")
    start_time = datetime.datetime.now()
    
    try:
        scraper = JobkoreaScraper()
        essays = scraper.scrape_jobkorea_with_login(user_id, password, start_page=start_page, end_page=end_page)
        
        if essays:
            logger.info(f"\n✅ 총 {len(essays)}개의 자소서를 수집했습니다!")
            save_to_excel(essays, save_directory, start_page, end_page)
            
            # 완료 시간 계산
            end_time = datetime.datetime.now()
            duration = end_time - start_time
            
            logger.info(f"\n🎉 스크래핑 완료!")
            logger.info(f"⏱️ 소요 시간: {duration}")
            logger.info(f"📊 수집 페이지 범위: {start_page}~{end_page}")
            logger.info(f"📝 총 자소서 수: {len(essays)}")
            
        else:
            logger.warning("수집된 자소서가 없습니다.")
            
    except Exception as e:
        logger.error(f"실행 오류: {e}")

if __name__ == "__main__":
    main()
