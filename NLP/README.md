# NLP 합격자소서 스크래핑 & 키워드 분석 파이프라인

잡코리아 + 링커리어에서 합격 자소서를 병렬 수집하고, 직무별 키워드 및 대기업 인재상 매칭 분석을 수행하는 파이프라인입니다.

---

## 폴더 구조

```
NLP/
├── pipeline.py              # 메인 파이프라인 (스크래핑 → 분석 순차 실행)
├── jobkorea_scraper.py      # 잡코리아 스크래퍼 (requests + BeautifulSoup)
├── linked_scraper.py        # 링커리어 스크래퍼 (Selenium + ChromeDriver)
├── keyword_extraction.py    # 키워드 분석 (kiwipiepy + NLTK)
├── resume_evaluator.py      # 자소서 평가 모듈
├── run.ps1                  # PowerShell 실행 스크립트 (venv 자동 활성화)
├── run.bat                  # CMD 실행 스크립트 (venv 자동 활성화)
├── pyproject.toml           # 패키지 의존성 정의
├── .venv/                   # 가상환경 (직접 수정 X)
└── data/                    # 수집/분석 결과물 저장 폴더
    ├── 잡코리아_합격자소서.xlsx
    ├── 링커리어_합격자소서.xlsx
    ├── job_keywords_analysis.csv   # 직무별 키워드 분석 결과
    ├── job_keywords_analysis.json
    ├── top_100_companies.json      # 100대 기업 인재상 데이터 (수동 관리)
    └── ...
```

---

## 초기 설정 (처음 한 번만)

### 1. venv 생성 및 패키지 설치

```powershell
cd D:\Coding\Portfolio\AssayReport\NLP

python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
```

> `pyproject.toml`에 명시된 모든 패키지가 자동 설치됩니다.

### 2. PowerShell 실행 정책 허용 (최초 1회)

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

---

## 실행 방법

### 기본 실행 (venv 자동 활성화)

```powershell
cd D:\Coding\Portfolio\AssayReport\NLP

# PowerShell
.\run.ps1

# CMD
run.bat
```

> `.\run.ps1`만 입력하면 venv 활성화 + pipeline.py 실행이 자동으로 됩니다.  
> 아이디/비밀번호는 실행 후 대화형으로 입력합니다.

### 인자 전달 실행

```powershell
.\run.ps1 --id 아이디 --password 비밀번호 --jk-start 1 --jk-end 3 --lk-start 1 --lk-end 2
```

### pipeline.py 전체 옵션

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `--id` | (대화형 입력) | 잡코리아 아이디 |
| `--password` | (대화형 입력) | 잡코리아 비밀번호 |
| `--jk-start` | 1 | 잡코리아 시작 페이지 |
| `--jk-end` | 2 | 잡코리아 끝 페이지 |
| `--lk-start` | 1 | 링커리어 시작 페이지 |
| `--lk-end` | 2 | 링커리어 끝 페이지 |
| `--headless` | True | 링커리어 Chrome 헤드리스 실행 (기본 ON) |
| `--no-headless` | - | 링커리어 Chrome 브라우저 GUI 표시 |

---

## 파이프라인 동작 순서

```
1. 잡코리아 스크래퍼  ──┐
                         ├──▶ (병렬 실행)  ──▶  2. 키워드 분석
2. 링커리어 스크래퍼  ──┘
```

1. **잡코리아 + 링커리어 병렬 스크래핑** — 두 스크래퍼가 동시에 실행되며 실시간 로그 출력
2. **키워드 분석** — 수집된 자소서를 바탕으로 직무별 실무 키워드 15개 + 대기업 인재상 키워드 10개 추출

### 스크래퍼별 특징

| | 잡코리아 | 링커리어 |
|--|---------|---------|
| 방식 | requests + BeautifulSoup | Selenium + ChromeDriver |
| 로그인 | 아이디/비밀번호 필요 | 불필요 (공개 데이터) |
| 수집 대상 | 합격 자소서 전체 | 최근 3년 + 100대 대기업 |

---

## 분석 결과물

| 파일 | 내용 |
|------|------|
| `data/잡코리아_합격자소서.xlsx` | 잡코리아 수집 원본 데이터 (누적 저장) |
| `data/링커리어_합격자소서.xlsx` | 링커리어 수집 원본 데이터 |
| `data/job_keywords_analysis.csv` | 직무별 실무 키워드 15개 + 인재상 키워드 10개 + 추천 대기업 Top3 |
| `data/job_keywords_analysis.json` | 위와 동일 (JSON 포맷) |

---

## 의존성 패키지

```toml
# pyproject.toml 기준
pandas, kiwipiepy, nltk,
beautifulsoup4, requests, lxml, openpyxl,
selenium, webdriver-manager,
flask, flask-cors
```

---

## 주요 이슈 해결 기록

### Windows venv 한글 깨짐
- **원인**: Windows venv 환경에서 stdout 인코딩이 `cp949`로 설정됨
- **해결**: `pipeline.py` 상단에서 `sys.stdout.reconfigure(encoding='utf-8')` 적용, 자식 프로세스에 `PYTHONUTF8=1` 환경변수 전달

### 잡코리아 스크래퍼 파이프라인 멈춤
- **원인**: `jobkorea_scraper.py`에 argparse가 없어 `--id`, `--password` 인자를 무시하고 `input()`으로 대기
- **해결**: `argparse` 추가, 인자 없을 때만 대화형 입력으로 폴백
