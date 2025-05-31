// 경로: src/styles/pages/signUpPage.styles.ts
import { StyleSheet, ViewStyle, TextStyle } from 'react-native';
import { Dimensions } from 'react-native';
import { Theme } from '../../types/theme';

// 스타일 타입 정의
interface SignUpPageStyles {
  safeArea: ViewStyle;
  container: ViewStyle;
  formContainer: ViewStyle;
  headerTitle: TextStyle;
  inputLabel: TextStyle;
  requiredMark: TextStyle;
  input: TextStyle;
  inputError: TextStyle;
  passwordContainer: ViewStyle;
  passwordInput: TextStyle;
  eyeIcon: ViewStyle;
  phoneContainer: ViewStyle;
  phoneInput: TextStyle;
  carrierLabel: TextStyle;
  signupButton: ViewStyle;
  signupButtonText: TextStyle;
  backButton: ViewStyle;
  backButtonText: TextStyle;
  termsText: TextStyle;
  errorText: TextStyle;
}

export default function createStyles(theme: Theme): SignUpPageStyles {
  const { width, height } = Dimensions.get('window');

  return StyleSheet.create<SignUpPageStyles>({
    safeArea: {
      flex: 1,
      backgroundColor: theme.colors.background,
    },
    container: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
    },
    formContainer: {
      width: width,
      backgroundColor: theme.colors.background,
      padding: 20,
      paddingTop: 30,
      paddingBottom: 30,
    },
    headerTitle: {
      fontSize: 24,
      fontWeight: 'bold',
      color: '#000000',
      marginBottom: 30,
    },
    inputLabel: {
      fontSize: 14,
      fontWeight: '500',
      color: '#000000',
      marginBottom: 10,
    },
    requiredMark: {
      color: '#FF0000',
    },
    input: {
      width: '100%',
      height: 50,
      borderBottomWidth: 1,
      borderBottomColor: '#DDDDDD',
      fontSize: 16,
      color: '#000000',
      marginBottom: 20,
    },
    inputError: {
      borderBottomColor: '#FF0000',
    },
    passwordContainer: {
      flexDirection: 'row',
      alignItems: 'center',
      borderBottomWidth: 1,
      borderBottomColor: '#DDDDDD',
      marginBottom: 20,
    },
    passwordInput: {
      flex: 1,
      height: 50,
      fontSize: 16,
      color: '#000000',
    },
    eyeIcon: {
      padding: 10,
    },
    phoneContainer: {
      flexDirection: 'row',
      alignItems: 'center',
      borderBottomWidth: 1,
      borderBottomColor: '#DDDDDD',
      marginBottom: 20,
    },
    phoneInput: {
      flex: 1,
      height: 50,
      fontSize: 16,
      color: '#000000',
    },
    carrierLabel: {
      fontSize: 14,
      fontWeight: '500',
      color: '#000000',
      marginLeft: 5,
    },
    signupButton: {
      width: '100%',
      height: 50,
      backgroundColor: theme.colors.primary,
      borderRadius: 8,
      justifyContent: 'center',
      alignItems: 'center',
      marginTop: 20,
      marginBottom: 15,
    },
    signupButtonText: {
      color: '#FFFFFF',
      fontSize: 16,
      fontWeight: 'bold',
    },
    backButton: {
      width: '100%',
      height: 50,
      backgroundColor: '#F5F5F5',
      borderRadius: 8,
      justifyContent: 'center',
      alignItems: 'center',
      marginBottom: 20,
    },
    backButtonText: {
      color: '#000000',
      fontSize: 16,
      fontWeight: '500',
    },
    termsText: {
      fontSize: 12,
      color: '#888888',
      textAlign: 'center',
      marginTop: 10,
    },
    errorText: {
      color: '#FF0000',
      fontSize: 12,
      marginTop: -15,
      marginBottom: 15,
    },
  });
}
