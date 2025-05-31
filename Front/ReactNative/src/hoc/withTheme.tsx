// 경로: src/hoc/withTheme.tsx
import React from 'react';
import { useTheme } from '../styles/theme/ThemeContext';
import { Theme } from '../types/theme';

// withTheme HOC 타입 정의
interface WithThemeProps {
  theme: Theme;
}

// 어떤 컴포넌트든 받을 수 있도록 제네릭 타입 사용
const withTheme = <P extends object>(
  WrappedComponent: React.ComponentType<P & WithThemeProps>
): React.FC<Omit<P, keyof WithThemeProps>> => {
  // 반환되는 함수형 컴포넌트에 표시될 이름 설정
  const displayName = 
    WrappedComponent.displayName || 
    WrappedComponent.name || 
    'Component';

  // 테마를 주입하는 컴포넌트
  const ComponentWithTheme: React.FC<Omit<P, keyof WithThemeProps>> = (props) => {
    // useTheme 훅을 사용하여 현재 테마 가져오기
    const { theme } = useTheme();
    
    // props와 테마를 결합하여 wrapped 컴포넌트에 전달
    return <WrappedComponent {...(props as P)} theme={theme} />;
  };

  // 디버깅을 위한 displayName 설정
  ComponentWithTheme.displayName = `withTheme(${displayName})`;
  
  return ComponentWithTheme;
};

export default withTheme;
