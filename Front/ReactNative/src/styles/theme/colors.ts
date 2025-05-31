// 경로: src/styles/theme/colors.ts
// 앱에서 사용되는 주요 색상 정의

// 주요 색상 정의 인터페이스
export interface Colors {
  primary: string;
  secondary: string;
  background: string;
  text: string;
  textLight: string;
  textLighter: string;
  placeholder: string;
  error: string;
  success: string;
  warning: string;
  card: string;
  border: string;
  notification?: string; 
  positive: string;
  negative: string;
  gain: string;
  loss: string;
}

// 라이트 테마(기본)
export const lightColors: Colors = {
  primary: '#365BC5', // 토스 메인 파란색
  secondary: '#FF6B35', // 보조 색상
  background: '#F8F9FA', // 배경색
  text: '#1A1A1A', // 텍스트 색상
  textLight: '#AAAAAA', // 텍스트 밝은 색상
  textLighter: '#AAAAAA', // 텍스트 더 밝은 색상
  placeholder: '#AAAAAA', // 플레이스홀더 색상
  error: '#E53935', // 오류 색상
  success: '#4CAF50', // 성공 색상
  warning: '#FF9800', // 경고 색상
  card: '#FFFFFF', // 카드 배경색
  border: '#E8E8E8', // 테두리 색상 추가
  notification: '#FF3B30', // 알림 색상 (선택사항)
  positive: '#FF0000', // 양수(수익) 색상
  negative: '#0022FF', // 음수(손실) 색상
  gain: '#FF0000', // 수익 색상
  loss: '#0022FF', // 손실 색상
};

// 다크 테마
export const darkColors: Colors = {
  primary: '#5A7DD6', // 토스 메인 파란색 (어두운 모드용)
  secondary: '#FF8C5F', // 보조 색상 (어두운 모드용)
  background: '#101013', // 배경색
  text: '#FFFFFF', // 텍스트 색상
  textLight: '#777777', // 텍스트 밝은 색상
  textLighter: '#777777', // 텍스트 더 밝은 색상
  placeholder: '#777777', // 플레이스홀더 색상
  error: '#EF5350', // 오류 색상
  success: '#66BB6A', // 성공 색상
  warning: '#FFB74D', // 경고 색상
  card: '#17171C', // 카드 배경색
  border: '#2C2C2C', // 테두리 색상 추가
  notification: '#FF453A', // 알림 색상 (선택사항)
  positive: '#FF0000', // 양수(수익) 색상
  negative: '#0022FF', // 음수(손실) 색상
  gain: '#FF0000', // 수익 색상
  loss: '#0022FF', // 손실 색상
};

export default { lightColors, darkColors };
