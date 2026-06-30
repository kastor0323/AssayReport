# NLP 합격자소서 분석 파이프라인

링커리어에서 합격 자소서를 수집하고, **직무분야별 자소서 초안 가이드**와 **특정 기업 포지션별 자소서 평가** 두 단계로 활용 가능한 키워드 데이터셋을 생성하는 파이프라인입니다.

---

## 서비스 시나리오

```
[1단계] 처음 자소서 쓸 때          [2단계] 특정 기업 지원 시
─────────────────────               ──────────────────────────────
job_keywords_analysis               job_keywords_by_position
직무분야(IT·전자 등) 단위           직무명 × 질문카테고리 단위

하드스킬 키워드  → 가이드라인       하드스킬 키워드 × 3점 (기술 변별)
소프트스킬 키워드 → 기본 체크       소프트스킬 키워드 × 1점 (인성 기본)
                                    → 자소서 스코어링 엔진
```

---

## 폴더 구조

```
NLP/
├── pipeline.py              # 메인 파이프라인 (스크래핑 → 분석 순차 실행)
├── linked_scraper.py        # 링커리어 스크래퍼 (Selenium + ChromeDriver)
├── keyword_extraction.py    # 키워드 분석 (kiwipiepy + NLTK)
├── resume_evaluator.py      # 자소서 평가 모듈 (Flask API)
├── run.ps1                  # PowerShell 실행 스크립트 (venv 자동 활성화)
├── run.bat                  # CMD 실행 스크립트
├── pyproject.toml           # 패키지 의존성 정의
├── .venv/                   # 가상환경 (직접 수정 X)
└── data/
    ├── linked_scraping_result.csv    # 링커리어 수집 원본 (2,842행+)
    ├── linked_scraping_result.json
    ├── companies.json                # 210개 기업 인재상 데이터
    ├── job_keywords_analysis.csv     # [1단계] 직무분야 × 카테고리별 키워드
    ├── job_keywords_analysis.json
    ├── job_keywords_by_position.csv  # [2단계] 직무명 × 카테고리별 키워드
    └── job_keywords_by_position.json
```

---

## 초기 설정 (처음 한 번만)

### 1. venv 생성 및 패키지 설치

```powershell
cd C:\Coding\WorkSpace\Portfolio\Resume_Project\NLP

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

### 전체 파이프라인 (스크래핑 + 분석)

```powershell
# PowerShell
.\run.ps1

# CMD
run.bat
```

> 스크래핑 완료 후 자동으로 키워드 분석까지 이어집니다.

### 옵션

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `--max-pages` | 50 | 기업당 최대 스크래핑 페이지 수 |
| `--headless` | False | Chrome 헤드리스 실행 |
| `--no-headless` | - | Chrome 브라우저 GUI 표시 (기본값) |

### 키워드 분석만 단독 실행

스크래핑 없이 기존 수집 데이터로 분석만 재실행할 때 사용합니다.

```powershell
python keyword_extraction.py
```

---

## 파이프라인 동작 순서

```
링커리어 스크래퍼  ──▶  linked_scraping_result.csv
                                  │
                                  ▼
                         keyword_extraction.py
                         ┌────────────────────────────┐
                         │ 직무분야 × 카테고리 분석     │──▶ job_keywords_analysis
                         │ 직무명 × 카테고리 분석       │──▶ job_keywords_by_position
                         └────────────────────────────┘
```

---

## 분석 결과 데이터 구조

### job_keywords_analysis.csv — 자소서 초안 작성용 (직무분야 단위)

| 컬럼 | 설명 |
|------|------|
| `직무분야` | IT·전자, 건설·부동산, 금융·보험 등 16개 대분류 |
| `질문카테고리` | 자기소개 / 경험 / 직무역량 / 지원동기 / 장단점 / 입사포부 / 성장과정 / 가치관 |
| `자기소개 개수` | 해당 직무분야 수집 자소서 수 |
| `하드스킬_키워드` | 직무·기술 전문어 (최대 15개) |
| `소프트스킬_키워드` | 협업·소통 등 인성 역량어 (최대 10개) |
| `추출회사명` | 데이터 출처 기업 목록 |

### job_keywords_by_position.csv — 특정 기업 자소서 평가용 (직무명 단위)

| 컬럼 | 설명 |
|------|------|
| `직무명` | 세부 포지션명 (예: DS부문_반도체공정기술) |
| `질문카테고리` | 자기소개 / 경험 / 직무역량 / 지원동기 / 장단점 / 입사포부 / 성장과정 / 가치관 |
| `답변수` | 해당 (직무명, 카테고리) 조합 답변 수 |
| `하드스킬_키워드` | 포지션 특화 기술 키워드 (최대 15개) |
| `소프트스킬_키워드` | 인성 역량 키워드 (최대 10개) |
| `추출회사명` | 데이터 출처 기업명 |

### 스코어링 가중치 (평가 엔진 적용 기준)

| 키워드 유형 | 가중치 | 기준 |
|------------|--------|------|
| 하드스킬 | **3점** | 포지션 특화 기술어 포함 여부 |
| 소프트스킬 | **1점** | 협업·소통 등 인성어 포함 여부 |

> `소프트스킬_키워드`가 비어 있는 경우(기술 집중 포지션)는 정상입니다.
> 데이터 로드 시 반드시 `fillna('')` 처리를 적용하세요.
> ```python
> df = pd.read_csv('job_keywords_by_position.csv', encoding='utf-8-sig').fillna('')
> ```

---

## 키워드 추출 알고리즘

### 카테고리 분류
질문 텍스트를 키워드 매칭 → regex 패턴 순으로 분류합니다.

| 카테고리 | 감지 예시 |
|----------|----------|
| 지원동기 | "지원하게 된 동기", "선택한 이유" |
| 경험 | "도전한 경험", "어려웠던 사례", "프로젝트 경험" |
| 직무역량 | "직무 관련 역량", "전공 활용" |
| 장단점 | "본인의 강점", "단점과 극복" |
| 입사포부 | "입사 후 목표", "10년 후 모습" |

### 하드스킬 / 소프트스킬 분류

- **소프트스킬 판별 기준**: 협업, 소통, 경청, 리더십, 책임감 등 30개 역량어 사전 매칭
- **하드스킬**: 소프트스킬 사전에 없는 모든 전문 명사 → 기술·도메인 키워드로 분류

### IDF 가중치 (기업 추천 점수)
기업 인재상 키워드가 많은 회사에 유리한 편향을 방지하기 위해 IDF(Inverse Document Frequency)를 적용합니다. `혁신`, `도전` 등 210개 기업 모두에 공통된 범용 가치관은 자동으로 하향됩니다.

---

## 의존성 패키지

```
pandas
kiwipiepy
nltk
beautifulsoup4
requests
lxml
selenium
webdriver-manager
flask
flask-cors
```

---

## 주요 이슈 해결 기록

### Windows venv 한글 깨짐
- **원인**: venv 환경에서 stdout 인코딩이 `cp949`로 설정됨
- **해결**: `pipeline.py` 상단에 `sys.stdout.reconfigure(encoding='utf-8')` 적용, 자식 프로세스에 `PYTHONUTF8=1` 환경변수 전달

### 소프트스킬 컬럼 NaN 이슈
- **원인**: pandas가 CSV 빈 셀을 기본적으로 NaN으로 읽음
- **해결**: `to_csv(quoting=csv.QUOTE_NONNUMERIC)`으로 빈 문자열을 `""` 명시 저장, 로드 시 `.fillna('')` 필수 적용

### 추천회사 점수 오류 (동음이의어)
- **원인**: IT 자소서의 `공정`(반도체 공정·工程)이 공공기관 인재상의 `공정`(공정성·公正)과 동일하게 매칭되어 국민연금공단이 IT 추천 1위가 됨
- **해결**: 직무분야별 산업군 필터링(`FIELD_TO_INDUSTRIES` 매핑) + IDF 가중치 적용으로 해결
