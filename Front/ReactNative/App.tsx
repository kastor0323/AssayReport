// 경로: App.tsx
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { ActivityIndicator, View } from 'react-native';
import ErrorBoundary from './src/components/common/layout/ErrorBoundary';

// 네비게이터 및 컨텍스트 임포트
import AppNavigator from './src/navigation/AppNavigator';
import AuthNavigator from './src/navigation/AuthNavigator';
import { ThemeProvider } from './src/styles/theme/ThemeContext';
import { AuthProvider, useAuth } from './src/context/AuthContext';
import { AccountsProvider } from './src/context/AccountsContext';

// 조건부 네비게이션을 처리하는 컴포넌트
const RootNavigator: React.FC = () => {
  const { isLoggedIn, loading } = useAuth();
  
  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" />
      </View>
    );
  }
  
  // 로그인 상태에 따라 다른 네비게이터 렌더링
  return isLoggedIn ? <AppNavigator /> : <AuthNavigator />;
};

const App: React.FC = () => {
  return (
    <SafeAreaProvider>
      <ThemeProvider>
        <AccountsProvider>
          <AuthProvider>
            <ErrorBoundary>
              <NavigationContainer>
                <RootNavigator />
              </NavigationContainer>
            </ErrorBoundary>
          </AuthProvider>
        </AccountsProvider>
      </ThemeProvider>
    </SafeAreaProvider>
  );
};

export default App;
