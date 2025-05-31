// 경로: src/styles/pages/loginPage.styles.ts
import { Dimensions, StyleSheet, ViewStyle, TextStyle, ImageStyle } from 'react-native';
import { Theme } from '../../types/theme';

// 스타일 타입 정의
interface LoginPage {
  container: ViewStyle;
  loadingContainer: ViewStyle;
  logoContainer: ViewStyle;
  logo: TextStyle;
  logoImage: ImageStyle;
  formContainer: ViewStyle;
  inputLabel: TextStyle;
  input: TextStyle;
  passwordContainer: ViewStyle;
  passwordInput: TextStyle;
  eyeIcon: ViewStyle;
  forgotPasswordText: TextStyle;
  dividerContainer: ViewStyle;
  dividerLine: ViewStyle;
  dividerText: TextStyle;
  startButton: ViewStyle;
  startButtonText: TextStyle;
  loginButton: ViewStyle;
  loginButtonText: TextStyle;
  kakaoButton: ViewStyle;
  kakaoButtonText: TextStyle;
  createAccountContainer: ViewStyle;
  createAccountText: TextStyle;
  signupButton: ViewStyle;
  signupButtonText: TextStyle;
  termsText: TextStyle;
  // 추가된 로컬 스타일
  fixedContainer: ViewStyle;
  dynamicContainer: ViewStyle;
}

export default function createStyles(theme: Theme): LoginPage {
  const { height } = Dimensions.get('window');

  return StyleSheet.create<LoginPage>({
    container: {
      flex: 1,
      backgroundColor: theme.colors.background,
      paddingHorizontal: 20,
      justifyContent: 'center',
    },
    loadingContainer: {
      justifyContent: 'center',
      alignItems: 'center',
    },
    logoContainer: {
      alignItems: 'center',
      marginBottom: 50,
    },
    logo: {
      fontSize: 20,
      fontWeight: 'bold',
      color: theme.colors.text,
    },
    logoImage: {
      width: 150,
      height: 150,
      alignSelf: 'center',
    },
    formContainer: {
      width: '100%',
      marginBottom: 20,
    },
    inputLabel: {
      fontSize: 14,
      fontWeight: '500',
      color: theme.colors.text,
      marginBottom: 10,
    },
    input: {
      width: '100%',
      height: 50,
      borderBottomWidth: 1,
      borderBottomColor: theme.colors.border,
      fontSize: 16,
      color: theme.colors.text,
      marginBottom: 20,
    },
    passwordContainer: {
      flexDirection: 'row',
      alignItems: 'center',
      borderBottomWidth: 1,
      borderBottomColor: theme.colors.border,
      marginBottom: 10,
    },
    passwordInput: {
      flex: 1,
      height: 50,
      fontSize: 16,
      color: theme.colors.text,
    },
    eyeIcon: {
      padding: 10,
    },
    forgotPasswordText: {
      fontSize: 14,
      color: theme.colors.text,
      textDecorationLine: 'underline',
      marginTop: 10,
      marginBottom: 20,
    },
    dividerContainer: {
      flexDirection: 'row',
      alignItems: 'center',
      marginVertical: 15,
    },
    dividerLine: {
      flex: 1,
      height: 1,
      backgroundColor: theme.colors.border,
    },
    dividerText: {
      paddingHorizontal: 10,
      color: theme.colors.text,
    },
    startButton: {
      width: '100%',
      height: 50,
      backgroundColor: theme.colors.primary,
      borderRadius: 25,
      justifyContent: 'center',
      alignItems: 'center',
      marginVertical: 20,
    },
    startButtonText: {
      color: '#FFFFFF',
      fontSize: 16,
      fontWeight: 'bold',
    },
    loginButton: {
      width: '100%',
      height: 50,
      backgroundColor: theme.colors.primary,
      borderRadius: 25,
      justifyContent: 'center',
      alignItems: 'center',
      marginBottom: 20,
    },
    loginButtonText: {
      color: '#FFFFFF',
      fontSize: 16,
      fontWeight: 'bold',
    },
    kakaoButton: {
      width: '100%',
      height: 50,
      backgroundColor: '#FFE500', // 카카오 색상
      borderRadius: 25,
      justifyContent: 'center',
      alignItems: 'center',
      marginBottom: 20,
    },
    kakaoButtonText: {
      color: '#000000',
      fontSize: 16,
      fontWeight: 'bold',
    },
    createAccountContainer: {
      alignItems: 'center',
      marginBottom: 15,
    },
    createAccountText: {
      fontSize: 14,
      color: theme.colors.text,
    },
    signupButton: {
      width: '100%',
      height: 50,
      backgroundColor: '#DDDDDD', // 회색
      borderRadius: 25,
      justifyContent: 'center',
      alignItems: 'center',
      marginBottom: 20,
    },
    signupButtonText: {
      color: '#000000',
      fontSize: 16,
      fontWeight: 'bold',
    },
    termsText: {
      fontSize: 12,
      color: theme.colors.placeholder,
      textAlign: 'center',
      marginTop: 15,
    },
    fixedContainer: {
      width: '100%',
      backgroundColor: 'transparent',
      zIndex: 10,
      marginTop: height / 6,
    },
    dynamicContainer: {
      flex: 1,
      width: '100%',
      marginTop: 10,
    }
  });
}
