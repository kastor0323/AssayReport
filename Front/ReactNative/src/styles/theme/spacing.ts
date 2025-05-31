// 경로: src/styles/theme/spacing.ts
// 앱에서 사용되는 여백 및 간격 정의

// 간격 정의 인터페이스
export interface Spacing {
    tiny: number;
    small: number;
    medium: number;
    large: number;
    extraLarge: number;
    // 기타 필요한 간격 추가
  }
  
  // 기본 간격 정의
  const spacing: Spacing = {
    tiny: 4,
    small: 8,
    medium: 16,
    large: 24,
    extraLarge: 32,
  };
  
  export default spacing;
  