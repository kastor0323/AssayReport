// 파일 경로: src/screens/auth/LoginPage.tsx
// 컴포넌트 흐름: App.js > AuthNavigator.tsx > LoginPage.tsx

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  TextInput,
  ActivityIndicator,
  Alert,
  Animated,
  Easing,
  Platform,
  UIManager,
  Keyboard,
  Image,
  StyleSheet
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';

// 컴포넌트 임포트
import { LoginPageNavigationProp } from '../../types/navigation';
import { useAuth } from '../../context/AuthContext';

// 스타일 임포트
import createStyles from '../../styles/pages/loginPage.styles';
import withTheme from '../../hoc/withTheme';
import { Theme } from '../../types/theme';

// 컴포넌트 props 인터페이스 정의
interface LoginPageProps {
  theme: Theme;
}

const LoginPage: React.FC<LoginPageProps> = ({ theme }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isEmailEntered, setIsEmailEntered] = useState(false);

  // 애니메이션 값 정의
  const fadeOutAnim = useState(new Animated.Value(1))[0];
  const slideUpAnim = useState(new Animated.Value(0))[0];

  const styles = createStyles(theme);
  const { login, loginWithKakao, loading } = useAuth();
  const navigation = useNavigation<LoginPageNavigationProp>();

  // 이메일 입력 상태를 감지하는 함수
  const handleEmailChange = (text: string) => {
    setEmail(text);
    const newIsEmailEntered = text.length > 0;

    // 상태가 변경될 때만 애니메이션 적용
    if (newIsEmailEntered !== isEmailEntered) {
      if (newIsEmailEntered) {
        // 이메일이 입력되었을 때
        Animated.timing(fadeOutAnim, {
          toValue: 0,
          duration: 250,
          useNativeDriver: true,
          easing: Easing.ease
        }).start();

        Animated.timing(slideUpAnim, {
          toValue: 1,
          duration: 300,
          delay: 100,
          useNativeDriver: true,
          easing: Easing.out(Easing.ease)
        }).start();
      } else {
        // 이메일이 삭제되었을 때
        Animated.timing(fadeOutAnim, {
          toValue: 1,
          duration: 250,
          useNativeDriver: true,
          easing: Easing.ease
        }).start();

        Animated.timing(slideUpAnim, {
          toValue: 0,
          duration: 200,
          useNativeDriver: true,
          easing: Easing.in(Easing.ease)
        }).start();
      }

      setIsEmailEntered(newIsEmailEntered);
    }
  };

  // 로그인 처리 함수
  const handleLogin = async () => {
    Keyboard.dismiss(); // 키보드 닫기

    if (!email || !password) {
      Alert.alert('입력 오류', '이메일과 비밀번호를 모두 입력해주세요.');
      return;
    }

    console.log('로그인 시도 (LoginPage):', email);
    // 로그인 처리 로직
    const success = await login(email, password);
    console.log('로그인 결과 (LoginPage):', success);
    if (!success) {
      Alert.alert('로그인 실패', '이메일 또는 비밀번호가 올바르지 않습니다.');
    }
  };

  // 카카오 로그인 처리
  const handleKakaoLogin = async () => {
    const success = await loginWithKakao();
    if (!success) {
      Alert.alert('카카오 로그인 실패', '카카오 로그인 과정에서 오류가 발생했습니다.');
    }
  };
  // 회원가입 네비게이트
  const handleCreateAccount = () => {
    navigation.navigate('회원가입 페이지');
  };

  // 비밀번호 찾기 기능
  const handleForgotPassword = () => {
    Alert.alert('안내', '비밀번호 찾기 기능은 현재 개발 중입니다.');
  };

  if (loading) {
    return (
      <View style={[styles.container, styles.loadingContainer]}>
        <ActivityIndicator size="large" color={theme.colors.primary} />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* 고정된 상단 컨테이너 */}
      <View style={styles.fixedContainer}>
        {/* 로고 */}
        <View style={styles.logoContainer}>
        <Text style={styles.logo}>SMS</Text>
          <Image source={require('../../../assets/super_ant.png')} style={styles.logoImage} resizeMode="contain" />
        </View>

        {/* 이메일 입력 필드 - 항상 고정 위치 */}
        <View>
          <Text style={styles.inputLabel}>이메일 *</Text>
          <TextInput
            style={styles.input}
            value={email}
            onChangeText={handleEmailChange}
            autoCapitalize="none"
            keyboardType="email-address"
            placeholder="이메일을 입력하세요"
          />
        </View>
      </View>

      {/* 동적 컨텐츠 영역 */}
      <View style={styles.dynamicContainer}>
        {/* 비밀번호 입력 - 애니메이션 효과와 함께 표시 */}
        {isEmailEntered && (
          <Animated.View
            style={{
              opacity: slideUpAnim,
              transform: [
                {
                  translateY: slideUpAnim.interpolate({
                    inputRange: [0, 1],
                    outputRange: [-20, 0], // 20px 위로 슬라이드
                  }),
                },
              ],
            }}
          >
            <Text style={styles.inputLabel}>비밀번호 *</Text>
            <View style={styles.passwordContainer}>
              <TextInput
                style={styles.passwordInput}
                value={password}
                onChangeText={setPassword}
                secureTextEntry={!showPassword}
                placeholder="비밀번호를 입력하세요"
              />
              <TouchableOpacity
                style={styles.eyeIcon}
                onPress={() => setShowPassword(!showPassword)}
              >
                <Ionicons
                  name={showPassword ? "eye" : "eye-off"}
                  size={24}
                  color={theme.colors.text}
                />
              </TouchableOpacity>
            </View>

            {/* 비밀번호 찾기 링크 */}
            <TouchableOpacity onPress={handleForgotPassword}>
              <Text style={styles.forgotPasswordText}>비밀번호를 잊으셨나요?</Text>
            </TouchableOpacity>

            {/* 로그인 버튼 */}
            <TouchableOpacity style={styles.loginButton} onPress={handleLogin}>
              <Text style={styles.loginButtonText}>로그인</Text>
            </TouchableOpacity>
          </Animated.View>
        )}

        {/* "또는" 구분선과 그 아래 내용 - 애니메이션과 함께 숨김 */}
        {!isEmailEntered && (
          <Animated.View
            style={{
              opacity: fadeOutAnim,
              transform: [
                {
                  translateY: fadeOutAnim.interpolate({
                    inputRange: [0, 1],
                    outputRange: [20, 0], // translateY로 애니메이션
                  }),
                },
              ],
              marginTop: 10,
            }}
          >
            {/* 또는 구분선 */}
            <View style={styles.dividerContainer}>
              <View style={styles.dividerLine} />
              <Text style={styles.dividerText}>또는</Text>
              <View style={styles.dividerLine} />
            </View>

            {/* 카카오 로그인 버튼 */}
            <TouchableOpacity style={styles.kakaoButton} onPress={handleKakaoLogin}>
              <Text style={styles.kakaoButtonText}>카카오로 계정으로 계속하기</Text>
            </TouchableOpacity>

            {/* 계정 생성 링크 */}
            <View style={styles.createAccountContainer}>
              <Text style={styles.createAccountText}>계정이 없으신가요?</Text>
            </View>

            {/* 계정 생성 버튼 */}
            <TouchableOpacity style={styles.signupButton} onPress={handleCreateAccount}>
              <Text style={styles.signupButtonText}>계정 만들기</Text>
            </TouchableOpacity>

            {/* 약관 안내 - 이메일 입력 시 숨김 */}
            <Text style={styles.termsText}>
              가입하면 Superant의 이용약관, 개인정보 처리방침, 쿠키 정책에 동의하게 됩니다.
            </Text>
          </Animated.View>
        )}
      </View>
    </View>
  );
};

export default withTheme(LoginPage);
