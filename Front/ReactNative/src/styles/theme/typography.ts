// 경로: src/styles/theme/typography.ts
// 앱에서 사용되는 텍스트 스타일 정의

import { TextStyle } from 'react-native';

// 타이포그래피 인터페이스 정의
export interface Typography {
  fontSize: {
    small: number;
    medium: number;
    large: number;
    extraLarge: number;
    heading: number;
  };
  fontFamily: {
    regular: string;
    medium: string;
    bold: string;
  };
  styles: {
    title: TextStyle;
    subtitle: TextStyle;
    body: TextStyle;
    caption: TextStyle;
    button: TextStyle;
  };
}


// 기본 타이포그래피 설정
const typography: Typography = {
  fontSize: {
    small: 12,
    medium: 14,
    large: 16,
    extraLarge: 18,
    heading: 24,
  },
  fontFamily: {
    regular: 'Roboto-Regular',
    medium: 'Roboto-Medium',
    bold: 'Roboto-Bold',
  },
  styles: {
    title: {
      fontSize: 24,
      fontWeight: 'bold',
      letterSpacing: 0.15,
    },
    subtitle: {
      fontSize: 18,
      fontWeight: '500',
      letterSpacing: 0.1,
    },
    body: {
      fontSize: 16,
      fontWeight: 'normal',
      letterSpacing: 0.5,
    },
    caption: {
      fontSize: 12,
      fontWeight: 'normal',
      letterSpacing: 0.4,
    },
    button: {
      fontSize: 14,
      fontWeight: '500',
      letterSpacing: 1.25,
      textTransform: 'uppercase',
    },
  },
};

export default typography;
