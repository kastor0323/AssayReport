# SMS 프로젝트 (React Native)

## 프로젝트 소개
이 프로젝트는 React Native와 Expo를 사용하여 개발된 SMS(Stock Management System) 애플리케이션입니다. 이 앱은 주식 포트폴리오 괸리 기능을 제공하는 모바일 애플리케이션입니다.

## 기술 스택
- React Native 0.79.2
- Expo 53.0.0
- TypeScript
- React Navigation 6
- Axios
- AsyncStorage

## 프로젝트 구조
```
Front/ReactNative/
├── assets/             # 이미지, 폰트 등 정적 자산
├── src/                # 소스 코드
│   ├── api/            # API 통신 관련 코드
│   ├── components/     # 재사용 가능한 컴포넌트
│   │   ├── account/    # 계좌 관련 컴포넌트
│   │   ├── common/     # 공통 컴포넌트
│   │   │   ├── graphs/ # 그래프 관련 컴포넌트
│   │   │   ├── layout/ # 레이아웃 컴포넌트
│   │   │   ├── modals/ # 모달 컴포넌트
│   │   │   └── ui/     # UI 컴포넌트
│   │   └── portfolio/  # 포트폴리오 관련 컴포넌트
│   ├── constants/      # 상수 정의
│   ├── context/        # React Context API
│   ├── data/           # 로컬 데이터, 모델
│   ├── hoc/            # Higher-Order Components
│   ├── hooks/          # 커스텀 React Hooks
│   ├── navigation/     # 내비게이션 구조
│   ├── screens/        # 화면 컴포넌트
│   │   ├── auth/       # 인증 관련 화면
│   │   ├── main/       # 메인 화면
│   │   └── setup/      # 설정 화면
│   ├── styles/         # 스타일 관련 파일
│   ├── types/          # TypeScript 타입 정의
│   └── utils/          # 유틸리티 함수
├── App.tsx             # 앱 진입점
└── package.json        # 프로젝트 의존성 및 스크립트
```

## 설치 방법

### 필수 조건
- Node.js 16 이상
- npm 또는 yarn
- Expo CLI

### 설치 단계
1. 저장소 클론
   ```
   git clone <저장소 URL>
   cd SMS_Project/Front/ReactNative
   ```

2. 의존성 설치
   ```
   npm install
   # 또는
   yarn install
   ```

3. 애플리케이션 실행
   ```
   npm start
   # 또는
   yarn start
   ```

## 개발 스크립트
- `npm start`: Expo 개발 서버 시작 (포트 3000)
- `npm run android`: Android 에뮬레이터에서 앱 실행
- `npm run ios`: iOS 시뮬레이터에서 앱 실행 (포트 3000)
- `npm run web`: 웹 브라우저에서 앱 실행 (포트 3000)

## 주요 기능
- 사용자 인증 (로그인/회원가입)
- 주식 포트폴리오 관리
- 자산 배분 시각화
- 테마 설정 (라이트/다크 모드)
- 계좌 연동 및 관리

## 기여 방법
1. 저장소 포크
2. 새 기능 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add some amazing feature'`)
4. 브랜치 푸시 (`git push origin feature/amazing-feature`)
5. Pull Request 생성

## 라이센스
Private
