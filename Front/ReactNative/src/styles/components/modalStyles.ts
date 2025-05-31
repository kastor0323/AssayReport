import { StyleSheet, TextStyle, ViewStyle } from 'react-native';
import { Theme } from '../../types/theme';

// 모달 스타일 타입 정의
export interface ModalStylesType {
  modalBackground: ViewStyle;
  modalContainer: ViewStyle;
  modalTitle: TextStyle;
  modalSubtitle: TextStyle;
  passwordInput: ViewStyle & TextStyle;
  errorText: TextStyle;
  buttonContainer: ViewStyle;
  button: ViewStyle;
  cancelButton: ViewStyle;
  confirmButton: ViewStyle;
  cancelButtonText: TextStyle;
  confirmButtonText: TextStyle;
}

// 기본 모달 스타일
export const createModalStyles = (theme: Theme): ModalStylesType => StyleSheet.create({
  modalBackground: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000,
  },
  modalContainer: {
    width: '80%',
    backgroundColor: theme.colors.background,
    borderRadius: 10,
    padding: 20,
    alignItems: 'center',
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
    color: theme.colors.text,
  },
  modalSubtitle: {
    fontSize: 14,
    color: theme.colors.placeholder,
    marginBottom: 20,
  },
  passwordInput: {
    width: '100%',
    height: 50,
    borderWidth: 1,
    borderColor: theme.colors.border,
    borderRadius: 8,
    paddingHorizontal: 15,
    fontSize: 16,
    marginBottom: 15,
    color: theme.colors.text,
  },
  errorText: {
    color: 'red',
    marginBottom: 15,
    fontSize: 14,
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: '100%',
  },
  button: {
    width: '48%',
    height: 45,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
  },
  cancelButton: {
    backgroundColor: '#f0f0f0',
  },
  confirmButton: {
    backgroundColor: theme.colors.primary,
  },
  cancelButtonText: {
    color: theme.colors.text,
    fontSize: 16,
  },
  confirmButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  }
});

// 계좌 비밀번호 모달 스타일 타입 정의 (기본 모달 스타일과 동일)
export type AccountPasswordModalStylesType = ModalStylesType;

// 계좌 비밀번호 모달 스타일 (기본 모달 스타일 확장)
export const createAccountPasswordModalStyles = (theme: Theme): AccountPasswordModalStylesType => createModalStyles(theme); 