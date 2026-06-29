import os
import re
import time
import json
import logging
import datetime
import argparse
import pandas as pd

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError:
    print("Selenium 패키지가 설치되어 있지 않습니다.")
    print("설치 명령어: pip install selenium pandas openpyxl")
    exit()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 수집 기간: 최근 3년 이내
CUTOFF_YEAR = datetime.datetime.now().year - 3


class LinkareerScraper:
    def __init__(self, headless=False):
        self.options = webdriver.ChromeOptions()
        if headless:
            self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--window-size=1920,1080')
        self.options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        try:
            self.driver = webdriver.Chrome(options=self.options)
            self.wait = WebDriverWait(self.driver, 15)
        except Exception as e:
            logger.error(f"Chrome WebDriver 초기화 실패: {e}")
            raise e

        self.load_company_data()

    def load_company_data(self):
        """기업 데이터 로드"""
        self.company_to_industry = {}
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(base_dir, 'data', 'companies.json')
            with open(json_path, 'r', encoding='utf-8') as f:
                companies = json.load(f)
            for co in companies:
                self.company_to_industry[co['name']] = co['industry']
            logger.info(f"기업 데이터 로드 완료 ({len(self.company_to_industry)}개 기업)")
        except Exception as e:
            logger.error(f"기업 데이터 로드 오류: {e}")

    def wait_for_login(self):
        """사용자 수동 로그인 세션 확보 및 쿠키 강제 안착 로직"""
        login_url = "https://linkareer.com/login"
        logger.info("로그인 페이지로 이동합니다.")
        self.driver.get(login_url)
        
        print("\n" + "="*70)
        print(" [안내] 켜진 크롬 브라우저 창에서 로그인을 진행해 주세요.")
        print(" 로그인이 완전히 완료되어 메인 화면 혹은 마이페이지가 보이면")
        print(" 현재 이 터미널 창(콘솔)으로 돌아와서 [엔터(Enter)]를 눌러주세요.")
        print("="*70 + "\n")
        
        input("▶ 로그인을 완료하셨다면 [Enter] 키를 누르세요...")
        
        # 세션 쿠키 안정화를 위해 메인으로 이동 후 버퍼 생성
        self.driver.get("https://linkareer.com/")
        time.sleep(3)
        logger.info("로그인 세션 동기화 완료. 수집을 시작합니다.")

    def get_industry_by_company(self, company_name):
        """회사명으로 산업군 찾기 (부분 매칭 포함)"""
        if not company_name:
            return None
        company_name = company_name.strip()
        if company_name in self.company_to_industry:
            return self.company_to_industry[company_name]
        for co_name, industry in self.company_to_industry.items():
            if co_name in company_name or company_name in co_name:
                return industry
        return None

    def parse_year_from_period(self, period_text):
        """기간 텍스트에서 연도 추출 (예: '2025 상반기' -> 2025)"""
        if not period_text:
            return None
        match = re.search(r'(\d{4})', period_text)
        if match:
            return int(match.group(1))
        return None

    def is_within_3_years(self, period_text):
        """최근 3년 이내 자소서인지 확인"""
        year = self.parse_year_from_period(period_text)
        if year is None:
            return True
        return year >= CUTOFF_YEAR

    def split_question_and_answer(self, content_text):
        """본문 텍스트 블록에서 질문과 답변을 정밀 분리"""
        if not content_text:
            return None, None

        lines = [line.strip() for line in content_text.split('\n') if line.strip()]
        if not lines:
            return None, None

        first_line = lines[0]
        
        # 합격자 스펙 정보 라인 무시
        if len(first_line.split('/')) >= 3 or '학점' in first_line or '오픽' in first_line or '토익' in first_line:
            if len(lines) > 1:
                lines = lines[1:]
                first_line = lines[0]
            else:
                return None, None

        # 하단 광고 및 안내문 무시
        if "마음에 드는 문장을 스크랩" in first_line or "채용공고&합격자료" in first_line or "앱을 설치하고" in first_line:
            return None, None

        question_patterns = [
            re.compile(r'^\d+[\.\)\s]\s*.+'),
            re.compile(r'^Q\d+[\.\)\s:\-]\s*.+'),
            re.compile(r'^\[.+?\]\s*.+'),
            re.compile(r'^자유\s*양식', re.I),
            re.compile(r'^공고\s*내\s*.+'),
        ]

        is_question_line = any(p.match(first_line) for p in question_patterns)

        if not is_question_line and (first_line.endswith('?') or first_line.endswith('요.') or first_line.endswith('오.')):
            is_question_line = True

        if is_question_line:
            question = first_line
            question = re.sub(r'\s*\[\d+자\s*이내\]', '', question).strip()
            question = re.sub(r'\s*\-\s*“.+”', '', question).strip()
            
            answer_lines = lines[1:]
            answer = '\n'.join(answer_lines).strip()
            return question, answer if answer else None
        else:
            return None, '\n'.join(lines).strip()

    def parse_h1_title(self, title_text):
        """H1 텍스트에서 회사명, 직무, 기간 파싱."""
        period_pattern = re.compile(r'\d{4}\s*[상하]반기')
        parts = [p.strip() for p in title_text.split('/')]

        period = ''
        period_idx = -1
        for i, p in enumerate(parts):
            if period_pattern.search(p):
                period = p
                period_idx = i
                break

        if period_idx == -1:
            company = parts[0] if len(parts) >= 1 else ''
            job = '/'.join(parts[1:]) if len(parts) >= 2 else ''
            period = ''
        else:
            company = parts[0] if len(parts) >= 1 else ''
            job = '/'.join(parts[1:period_idx]) if period_idx >= 2 else (parts[1] if len(parts) >= 2 else '')

        return company.strip(), job.strip(), period.strip()

    def parse_essay_page(self, page_url):
        """링커리어 자소서 상세 페이지 파싱 (오작동 조기종료 버그 완전 해결 판)"""
        logger.info(f"페이지 접속: {page_url}")
        self.driver.get(page_url)
        
        # 1. 제목 정보 추출
        try:
            h1_element = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
            title_text = h1_element.text.strip()
        except Exception as e:
            logger.warning(f"  -> 타이틀(H1) 로딩 실패로 패스 ({page_url})")
            return []

        main_company, main_job, main_period = self.parse_h1_title(title_text)
        logger.info(f"  [메인 타겟] {main_company} / {main_job} / {main_period}")

        # 기업 및 기간 조건 필터
        main_industry = self.get_industry_by_company(main_company)
        if not main_industry:
            logger.info(f"  -> Top 100 기업 아님 (수집 스킵): {main_company}")
            return []

        if not self.is_within_3_years(main_period):
            logger.info(f"  -> 3년 범위 초과 (수집 스킵): {main_period}")
            return []

        essay_id = page_url.split('/')[-1].split('?')[0]
        time.sleep(2.5) # 동적 컴포넌트 데이터 완전 렌더링 대기

        # 2. 자바스크립트를 이용한 원본 텍스트 노드 추출
        script = """
        var results = [];
        var container = document.querySelector('article') || document.querySelector('main') || document.querySelector('[role="main"]') || document.body;

        // 1차: p, li, h1-h4, td 등 시맨틱 태그에서 텍스트 추출
        var seen = new Set();
        var semanticEls = container.querySelectorAll('p, li, h1, h2, h3, h4, td, pre, blockquote');
        for (var i = 0; i < semanticEls.length; i++) {
            var text = (semanticEls[i].innerText || semanticEls[i].textContent || '').trim();
            if (text.length > 5 && !seen.has(text)) {
                seen.add(text);
                results.push(text);
            }
        }

        // 2차: 결과가 부족하면 innerText 전체를 개행 기준으로 분리
        if (results.length < 3) {
            var allText = (container.innerText || container.textContent || '').trim();
            var lines = allText.split(/\\n+/);
            results = [];
            seen = new Set();
            for (var j = 0; j < lines.length; j++) {
                var line = lines[j].trim();
                if (line.length > 5 && !seen.has(line)) {
                    seen.add(line);
                    results.push(line);
                }
            }
        }

        return results;
        """
        
        try:
            raw_texts = self.driver.execute_script(script)
        except Exception as e:
            logger.warning(f"  -> 스크립트 실행 오류 ({page_url}): {e}")
            return []

        if not raw_texts:
            logger.warning(f"  -> {main_company} 페이지 내부에서 수집된 텍스트 데이터가 0건입니다.")
            return []

        current_qa_blocks = []
        
        # 스크랩 광고성 텍스트 매칭 규칙
        ads_pattern = re.compile(r'마음에 드는 문장을 스크랩|채용공고&합격자료|앱을 설치하고|원활한 이용', re.IGNORECASE)
        seen_texts = set()

        for text in raw_texts:
            if text in seen_texts:
                continue
            seen_texts.add(text)

            # [핵심 수정] 본문을 통째로 끊어버리던 break를 제거하고, 순수 안내문구 레이어만 건너뛰도록(continue) 변경
            if ads_pattern.search(text):
                continue

            # 추천 자소서 더보기 박스 텍스트 영역 스킵
            if "보고있는 합격자소서 참고해서" in text or "더 많은 최신 합격 자소서" in text:
                continue

            question, answer = self.split_question_and_answer(text)
            
            if question and answer:
                current_qa_blocks.append({'question': question, 'answer': answer})
            elif answer and not question:
                if current_qa_blocks:
                    if answer not in current_qa_blocks[-1]['answer']:
                        current_qa_blocks[-1]['answer'] += '\n\n' + answer
                else:
                    current_qa_blocks.append({'question': '자유양식', 'answer': answer})

        # 3. 데이터 조립 및 결과 반환
        if not current_qa_blocks:
            logger.warning(f"  -> {main_company} 페이지 최종 문항 결합 결과가 유효하지 않습니다.")
            return []

        clean_qa_list = []
        for qa in current_qa_blocks:
            if qa['question'] == '자유양식' and ('/' in qa['answer'] and '학점' in qa['answer']):
                continue
            clean_qa_list.append(qa)

        if not clean_qa_list:
            return []

        results = [{
            'company': main_company,
            'industry': main_industry,
            'job': main_job,
            'period': main_period,
            'essay_id': essay_id,
            'url': page_url.split('?')[0],
            'qa': clean_qa_list
        }]
        
        logger.info(f"  -> [파싱 성공] {main_company} / {main_job} ({len(clean_qa_list)}개 문항 확보)")
        return results

    def get_essay_links_from_search_page(self, page_num):
        """검색 결과 목록 페이지에서 상세 자소서 URL 추출"""
        url = f"https://linkareer.com/cover-letter/search?page={page_num}"
        logger.info(f"검색 페이지 {page_num} 접속: {url}")
        self.driver.get(url)
        time.sleep(3)

        links = []
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, "a[href^='/cover-letter/']")
            for elem in elements:
                href = elem.get_attribute("href")
                if href and '/search' not in href:
                    clean = href.split('?')[0]
                    if clean not in links:
                        links.append(clean)
            logger.info(f"  -> {len(links)}개 자소서 링크 수집")
        except Exception as e:
            logger.error(f"링크 수집 오류: {e}")

        return links

    def scrape(self, start_page=1, end_page=10):
        """메인 제어 루프"""
        # 프로그램 시작 시 1회 수동 로그인 수행
        self.wait_for_login()
        
        all_results = []
        try:
            for page in range(start_page, end_page + 1):
                links = self.get_essay_links_from_search_page(page)
                for link in links:
                    try:
                        results = self.parse_essay_page(link)
                        all_results.extend(results)
                    except Exception as e:
                        logger.error(f"파싱 오류 ({link}): {e}")
                        try:
                            self.driver.get("about:blank")
                            time.sleep(1)
                        except:
                            pass
        except KeyboardInterrupt:
            logger.info("스크래핑 강제 종료")
        finally:
            try:
                self.driver.quit()
            except:
                pass

        logger.info(f"총 {len(all_results)}개 자소서 세트 수집 완료")
        return all_results


def save_to_excel(results, save_directory=None):
    """수집 완료 데이터를 CSV/JSON으로 누적 저장"""
    if save_directory is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        save_directory = os.path.join(base_dir, 'data')

    os.makedirs(save_directory, exist_ok=True)

    if not results:
        logger.warning("저장할 데이터가 없습니다.")
        return

    rows = []
    for result in results:
        for qa in result['qa']:
            rows.append({
                '회사명': result['company'],
                '연도': result['period'],
                '직무분야': result['industry'],
                '직무명': result['job'],
                '질문 내용': qa['question'],
                '답변': qa['answer'],
            })

    df_new = pd.DataFrame(rows)
    csv_path = os.path.join(save_directory, 'linked_scraping_result.csv')

    COLS = ['회사명', '연도', '직무분야', '직무명', '질문 내용', '답변']

    if os.path.exists(csv_path):
        try:
            existing_df = pd.read_csv(csv_path, encoding='utf-8-sig')
            if set(COLS).issubset(set(existing_df.columns)):
                existing_df = existing_df[COLS]
                combined_df = pd.concat([existing_df, df_new[COLS]], ignore_index=True)
            else:
                logger.warning("기존 CSV 컬럼 불일치 (구 버전). 새로 생성합니다.")
                combined_df = df_new[COLS]
        except Exception as e:
            logger.error(f"기존 CSV 로드 실패, 새로 생성합니다: {e}")
            combined_df = df_new[COLS]
    else:
        combined_df = df_new[COLS]

    # CSV 저장 (NaN → 빈 문자열로 정규화)
    combined_df = combined_df.fillna('')
    combined_df[COLS].to_csv(csv_path, index=False, encoding='utf-8-sig')
    logger.info(f"CSV 저장 완료: {csv_path} (총 {len(combined_df)}행)")

    # JSON 저장 (회사+연도+직무명 단위로 그룹화)
    json_path = os.path.join(save_directory, 'linked_scraping_result.json')
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
    logger.info(f"JSON 저장 완료: {json_path} ({len(json_records)}개 그룹)")


if __name__ == "__main__":
    print("=== 링커리어 합격자소서 스크래핑 프로그램 (최종 수정본) ===")
    print(f"※ 최근 3년 이내 ({CUTOFF_YEAR}년 이후) + Top 100 대기업 자소서 실시간 정밀 동기화 수집")

    parser = argparse.ArgumentParser(description="링커리어 합격자소서 스크래핑")
    parser.add_argument("--start", type=int, default=1, help="시작 페이지 (기본값 1)")
    parser.add_argument("--end", type=int, default=10, help="종료 페이지 (기본값 10)")
    parser.add_argument("--headless", action="store_true", default=False, help="헤드리스 모드")
    args = parser.parse_args()

    try:
        scraper = LinkareerScraper(headless=args.headless)
        results = scraper.scrape(start_page=args.start, end_page=args.end)
        save_to_excel(results)
        print(f"\n작업 완료! 총 {len(results)}개 대기업 자소서 세트 최종 저장 완료")
    except Exception as e:
        print(f"오류 발생: {e}")