// 경로: src/navigation/AuthNavigator.tsx
import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

// 컴포넌트 임포트
import LoginPage from '../screens/auth/LoginPage';
import SignUpPage from '../screens/auth/SignUpPage';

// 로그인 상태에 따른 네비게이트
import { AuthStackParamList } from '../types/navigation';

const Stack = createNativeStackNavigator<AuthStackParamList>();

// @ts-ignore
const AuthNavigator = () => {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="로그인 페이지" component={LoginPage} />
      <Stack.Screen name="회원가입 페이지" component={SignUpPage} />
    </Stack.Navigator>
  );
};

export default AuthNavigator;
