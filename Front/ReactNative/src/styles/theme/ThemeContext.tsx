// 경로: src/styles/theme/ThemeContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { lightTheme, darkTheme } from './index';
import { Theme } from '../../types/theme';

type ThemeMode = 'light' | 'dark' | 'system';

// 테마 컨텍스트 인터페이스 정의
interface ThemeContextType {
  theme: Theme;
  isDark: boolean;
  toggleTheme: () => void;
  setTheme: (mode: ThemeMode) => void;
}

// 기본값으로 사용할 컨텍스트 생성
const ThemeContext = createContext<ThemeContextType>({
  theme: lightTheme,
  isDark: false,
  toggleTheme: () => {},
  setTheme: () => {},
});

// ThemeProvider Props 인터페이스
interface ThemeProviderProps {
  children: React.ReactNode;
}

// ThemeProvider 컴포넌트 정의
export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    loadTheme();
  }, []);

  const loadTheme = async () => {
    try {
      const savedTheme = await AsyncStorage.getItem('theme');
      if (savedTheme === 'dark') {
        setIsDark(true);
      }
    } catch (error) {
      console.error('테마 로드 실패:', error);
    }
  };

  const toggleTheme = async () => {
    try {
      const newTheme = !isDark;
      setIsDark(newTheme);
      await AsyncStorage.setItem('theme', newTheme ? 'dark' : 'light');
    } catch (error) {
      console.error('테마 저장 실패:', error);
    }
  };

  const setTheme = async (mode: ThemeMode) => {
    try {
      switch (mode) {
        case 'light':
          setIsDark(false);
          await AsyncStorage.setItem('theme', 'light');
          break;
        case 'dark':
          setIsDark(true);
          await AsyncStorage.setItem('theme', 'dark');
          break;
        case 'system':
          // 시스템 테마 설정 로직 구현 필요
          break;
      }
    } catch (error) {
      console.error('테마 설정 실패:', error);
    }
  };

  return (
    <ThemeContext.Provider
      value={{
        theme: isDark ? darkTheme : lightTheme,
        isDark,
        toggleTheme,
        setTheme,
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
};

// 커스텀 훅으로 테마 사용을 간편하게 제공
export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

export default ThemeContext;
