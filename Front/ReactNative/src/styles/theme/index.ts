// 경로: src/styles/theme/index.ts
// 테마 관련 파일 통합 인덱스
import { lightColors, darkColors, Colors } from './colors';
import spacing, { Spacing } from './spacing';
import typography, { Typography } from './typography';
import shadows, { Shadows } from './shadows';
import { Theme } from '../../types/theme';

// 라이트 테마 (기본)
export const lightTheme: Theme = {
  colors: lightColors,
  spacing: spacing,
  fonts: typography,
  shadows: shadows,
  mode: 'light',
};

// 다크 테마
export const darkTheme: Theme = {
  colors: darkColors,
  spacing: spacing,
  fonts: typography,
  shadows: shadows,
  mode: 'dark',
};

export type { Colors, Spacing, Typography, Shadows };
export { lightColors, darkColors, spacing, typography, shadows };

// 객체 리터럴 대신 변수로 선언하고 내보내기
const themes = { lightTheme, darkTheme };
export default themes;
