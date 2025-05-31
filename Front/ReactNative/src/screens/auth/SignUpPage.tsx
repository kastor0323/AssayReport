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
  KeyboardAvoidingView,
  SafeAreaView
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { useAuth } from '../../context/AuthContext';

// 스타일 임포트
import createStyles from '../../styles/pages/signUpPage.styles';
import withTheme from '../../hoc/withTheme';
import { Theme } from '../../types/theme';
import { LoginPageNavigationProp } from '../../types/navigation';

// 컴포넌트 props 인터페이스 정의
interface SignUpPageProps {
  theme: Theme;
}

const SignUpPage: React.FC<SignUpPageProps> = ({ theme }) => {
  // 폼 상태 관리
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  // UI 상태 관리
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [passwordsMatch, setPasswordsMatch] = useState(true);

  // 단계별 표시 상태
  const [isEmailEntered, setIsEmailEntered] = useState(false);
  const [isNameEntered, setIsNameEntered] = useState(false);
  const [isPasswordEntered, setIsPasswordEntered] = useState(false);
  const [isConfirmPasswordEntered, setIsConfirmPasswordEntered] = useState(false);

  // 애니메이션 값 정의
  const nameAnimation = useState(new Animated.Value(0))[0];
  const pwdAnimation = useState(new Animated.Value(0))[0];
  const confirmPwdAnimation = useState(new Animated.Value(0))[0];
  const signUpBtnAnimation = useState(new Animated.Value(0))[0];

  // AuthContext 사용
  const { signup, loading: authLoading } = useAuth();

  const styles = createStyles(theme);
  const navigation = useNavigation<LoginPageNavigationProp>();

  // 비밀번호 일치 여부 체크
  useEffect(() => {
    if (confirmPassword) {
      setPasswordsMatch(password === confirmPassword);
    } else {
      setPasswordsMatch(true);
    }
  }, [password, confirmPassword]);

  // 이메일 입력 처리
  const handleEmailChange = (text: string) => {
    setEmail(text);
    const newIsEmailEntered = text.length > 0;

    if (newIsEmailEntered !== isEmailEntered) {
      setIsEmailEntered(newIsEmailEntered);

      if (newIsEmailEntered) {
        // 이름 필드 표시 애니메이션
        Animated.timing(nameAnimation, {
          toValue: 1,
          duration: 300,
          delay: 200,
          useNativeDriver: true,
          easing: Easing.out(Easing.ease)
        }).start();
      } else {
        // 이름 필드 숨김 애니메이션
        Animated.timing(nameAnimation, {
          toValue: 0,
          duration: 200,
          useNativeDriver: true,
          easing: Easing.in(Easing.ease)
        }).start();

        // 다른 필드들도 숨김
        setIsNameEntered(false);
        setIsPasswordEntered(false);
        setIsConfirmPasswordEntered(false);

        // 애니메이션 값 초기화
        Animated.parallel([
          Animated.timing(pwdAnimation, {
            toValue: 0,
            duration: 200,
            useNativeDriver: true
          }),
          Animated.timing(confirmPwdAnimation, {
            toValue: 0,
            duration: 200,
            useNativeDriver: true
          }),
          Animated.timing(signUpBtnAnimation, {
            toValue: 0,
            duration: 200,
            useNativeDriver: true
          })
        ]).start();
      }
    }
  };

  // 이름 입력 처리
  const handleNameChange = (text: string) => {
    setName(text);
    const newIsNameEntered = text.length > 0;

    if (newIsNameEntered !== isNameEntered) {
      setIsNameEntered(newIsNameEntered);

      if (newIsNameEntered) {
        // 비밀번호 필드 표시 애니메이션
        Animated.timing(pwdAnimation, {
          toValue: 1,
          duration: 300,
          delay: 200,
          useNativeDriver: true,
          easing: Easing.out(Easing.ease)
        }).start();
      } else {
        // 비밀번호 필드 숨김 애니메이션
        Animated.timing(pwdAnimation, {
          toValue: 0,
          duration: 200,
          useNativeDriver: true,
          easing: Easing.in(Easing.ease)
        }).start();

        // 다음 단계도 초기화
        setIsPasswordEntered(false);
        setIsConfirmPasswordEntered(false);

        // 애니메이션 값 초기화
        Animated.parallel([
          Animated.timing(confirmPwdAnimation, {
            toValue: 0,
            duration: 200,
            useNativeDriver: true
          }),
          Animated.timing(signUpBtnAnimation, {
            toValue: 0,
            duration: 200,
            useNativeDriver: true
          })
        ]).start();
      }
    }
  };

  // 비밀번호 입력 처리
  const handlePasswordChange = (text: string) => {
    setPassword(text);
    const newIsPasswordEntered = text.length > 0;

    if (newIsPasswordEntered !== isPasswordEntered) {
      setIsPasswordEntered(newIsPasswordEntered);

      if (newIsPasswordEntered) {
        // 비밀번호 확인 필드 표시 애니메이션
        Animated.timing(confirmPwdAnimation, {
          toValue: 1,
          duration: 300,
          delay: 200,
          useNativeDriver: true,
          easing: Easing.out(Easing.ease)
        }).start();
      } else {
        // 비밀번호 확인 필드 숨김 애니메이션
        Animated.timing(confirmPwdAnimation, {
          toValue: 0,
          duration: 200,
          useNativeDriver: true,
          easing: Easing.in(Easing.ease)
        }).start();

        // 다음 단계도 초기화
        setIsConfirmPasswordEntered(false);

        // 애니메이션 값 초기화
        Animated.timing(signUpBtnAnimation, {
          toValue: 0,
          duration: 200,
          useNativeDriver: true
        }).start();
      }
    }
  };

  // 비밀번호 확인 입력 처리
  const handleConfirmPasswordChange = (text: string) => {
    setConfirmPassword(text);
    const newIsConfirmPasswordEntered = text.length > 0;

    if (newIsConfirmPasswordEntered !== isConfirmPasswordEntered) {
      setIsConfirmPasswordEntered(newIsConfirmPasswordEntered);

      if (newIsConfirmPasswordEntered) {
        // 가입하기 버튼 표시 애니메이션
        Animated.timing(signUpBtnAnimation, {
          toValue: 1,
          duration: 300,
          delay: 200,
          useNativeDriver: true,
          easing: Easing.out(Easing.ease)
        }).start();
      } else {
        // 가입하기 버튼 숨김 애니메이션
        Animated.timing(signUpBtnAnimation, {
          toValue: 0,
          duration: 200,
          useNativeDriver: true,
          easing: Easing.in(Easing.ease)
        }).start();
      }
    }
  };

  // 회원가입 처리 - 서버 연동 기능
  const handleSignUp = async () => {
    Keyboard.dismiss();

    // 유효성 검사
    if (!email || !name || !password || !confirmPassword) {
      Alert.alert('입력 오류', '모든 필드를 입력해주세요.');
      return;
    }

    if (!passwordsMatch) {
      Alert.alert('입력 오류', '비밀번호가 일치하지 않습니다.');
      return;
    }

    try {
      // AuthContext의 signup 함수 호출
      const result = await signup(email, password, name);
      console.log('회원가입 결과:', result);

      const { success, errorMessage } = result;
      console.log('성공 여부:', success, '오류 메시지:', errorMessage);

      if (success === true) {
        setTimeout(() => {
          Alert.alert(
            '회원가입 성공',
            '회원가입이 성공적으로 완료되었습니다.',
            [{
              text: '확인',
              onPress: () => {
                console.log('네비게이션 실행');
                navigation.navigate('로그인 페이지');
              }
            }],
            { cancelable: false }
          );
        }, 300);
      } else {
        setTimeout(() => {
          Alert.alert(
            '회원가입 실패',
            errorMessage || '회원가입 처리 중 오류가 발생했습니다. 다시 시도해주세요.',
            [{ text: '확인' }],
            { cancelable: false }
          );
          navigation.navigate('회원가입 페이지');
        }, 300);
      }
    } catch (error) {
      console.error('회원가입 중 오류 발생:', error);
      setTimeout(() => {
        Alert.alert(
          '오류 발생',
          '서버 연결 중 오류가 발생했습니다. 네트워크 연결을 확인하고 다시 시도해주세요.',
          [{ text: '확인' }],
          { cancelable: false }
        );
      }, 300);
    }
  };

  // 로그인 페이지로 돌아가기
  const handleBackToLogin = () => {
    navigation.navigate('로그인 페이지');
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
        style={styles.container}
      >
        <View style={styles.formContainer}>
          <Text style={styles.headerTitle}>회원가입</Text>

          {/* 이메일 입력 필드 - 항상 표시 */}
          <Text style={styles.inputLabel}>이메일 <Text style={styles.requiredMark}>*</Text></Text>
          <TextInput
            style={styles.input}
            value={email}
            onChangeText={handleEmailChange}
            autoCapitalize="none"
            keyboardType="email-address"
            placeholder="예) superant@gmail.com"
          />

          {/* 이름 입력 필드 - 애니메이션과 함께 표시 */}
          <Animated.View style={{
            opacity: nameAnimation,
            transform: [{
              translateY: nameAnimation.interpolate({
                inputRange: [0, 1],
                outputRange: [-20, 0],
              })
            }],
          }}>
            <Text style={styles.inputLabel}>이름 <Text style={styles.requiredMark}>*</Text></Text>
            <TextInput
              style={styles.input}
              value={name}
              onChangeText={handleNameChange}
              placeholder="이름을 입력하세요"
            />
          </Animated.View>

          {/* 비밀번호 입력 필드 - 애니메이션과 함께 표시 */}
          <Animated.View style={{
            opacity: pwdAnimation,
            transform: [{
              translateY: pwdAnimation.interpolate({
                inputRange: [0, 1],
                outputRange: [-20, 0],
              })
            }],
          }}>
            <Text style={styles.inputLabel}>비밀번호 <Text style={styles.requiredMark}>*</Text></Text>
            <View style={styles.passwordContainer}>
              <TextInput
                style={styles.passwordInput}
                value={password}
                onChangeText={handlePasswordChange}
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
          </Animated.View>

          {/* 비밀번호 확인 필드 - 애니메이션과 함께 표시 */}
          <Animated.View style={{
            opacity: confirmPwdAnimation,
            transform: [{
              translateY: confirmPwdAnimation.interpolate({
                inputRange: [0, 1],
                outputRange: [-20, 0],
              })
            }],
          }}>
            <Text style={styles.inputLabel}>비밀번호 확인 <Text style={styles.requiredMark}>*</Text></Text>
            <View style={styles.passwordContainer}>
              <TextInput
                style={[
                  styles.passwordInput,
                  !passwordsMatch && confirmPassword ? styles.inputError : null
                ]}
                value={confirmPassword}
                onChangeText={handleConfirmPasswordChange}
                secureTextEntry={!showConfirmPassword}
                placeholder="비밀번호를 다시 입력하세요"
              />
              <TouchableOpacity
                style={styles.eyeIcon}
                onPress={() => setShowConfirmPassword(!showConfirmPassword)}
              >
                <Ionicons
                  name={showConfirmPassword ? "eye" : "eye-off"}
                  size={24}
                  color={theme.colors.text}
                />
              </TouchableOpacity>
            </View>
            {!passwordsMatch && confirmPassword ? (
              <Text style={styles.errorText}>비밀번호가 일치하지 않습니다.</Text>
            ) : null}
          </Animated.View>   

          {/* 가입하기 버튼 - 애니메이션과 함께 표시 */}
          <Animated.View style={{
            opacity: signUpBtnAnimation,
            transform: [{
              translateY: signUpBtnAnimation.interpolate({
                inputRange: [0, 1],
                outputRange: [-20, 0],
              })
            }],
          }}>
            <TouchableOpacity
              style={styles.signupButton}
              onPress={handleSignUp}
              disabled={!email || !name || !password || !confirmPassword || !passwordsMatch || authLoading}
            >
              {authLoading ? (
                <ActivityIndicator size="small" color="#ffffff" />
              ) : (
                <Text style={styles.signupButtonText}>가입하기</Text>
              )}
            </TouchableOpacity>
          </Animated.View>

          {/* 로그인으로 돌아가기 버튼 - 항상 표시 */}
          <TouchableOpacity style={styles.backButton} onPress={handleBackToLogin}>
            <Text style={styles.backButtonText}>로그인으로 돌아가기</Text>
          </TouchableOpacity>

          {/* 약관 안내 - 항상 표시 */}
          <Text style={styles.termsText}>
            가입하면 Superant의 이용약관, 개인정보 처리방침, 쿠키 정책에 동의하게 됩니다.
          </Text>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

export default withTheme(SignUpPage);