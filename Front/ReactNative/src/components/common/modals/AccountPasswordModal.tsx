import React from 'react';
import { View, Text, Modal, TouchableOpacity, TextInput, StyleSheet } from 'react-native';
import { Theme } from '../../../types/theme';

// 계좌 비밀번호 모달 props 인터페이스
interface AccountPasswordModalProps {
  theme: Theme;
  visible: boolean;
  account: {
    company: string;
    accountNumber: string;
  } | null;
  password: string;
  onChangePassword: (text: string) => void;
  onConfirm: () => void;
  onCancel: () => void;
  isLoading: boolean;
  errorMessage?: string;
}

const AccountPasswordModal: React.FC<AccountPasswordModalProps> = ({
  theme,
  visible,
  account,
  password,
  onChangePassword,
  onConfirm,
  onCancel,
  isLoading,
  errorMessage
}) => {
  return (
    <Modal
      visible={visible}
      transparent
      animationType="fade"
      onRequestClose={onCancel}
    >
      <TouchableOpacity
        style={styles.modalBackground}
        activeOpacity={1}
        onPressOut={() => !isLoading && onCancel()}
      >
        <View style={[styles.modalContent, { borderColor: theme.colors.border, backgroundColor: theme.colors.background }]}>
          <Text style={[styles.modalTitle, { color: theme.colors.text }]}>
            계좌 비밀번호 입력
          </Text>
          
          {account && (
            <Text style={[styles.modalSubtitle, { color: theme.colors.secondary }]}>
              {account.company} ({account.accountNumber.slice(-4)})
            </Text>
          )}
          
          <TextInput
            style={[styles.passwordInput, { borderColor: theme.colors.border }]}
            value={password}
            onChangeText={onChangePassword}
            placeholder="계좌 비밀번호"
            placeholderTextColor={theme.colors.placeholder}
            secureTextEntry={true}
            keyboardType="number-pad"
            maxLength={10}
            editable={!isLoading}
          />
          
          {errorMessage ? (
            <Text style={styles.errorText}>
              {errorMessage}
            </Text>
          ) : null}
          
          <View style={styles.buttonContainer}>
            <TouchableOpacity
              style={[styles.button, styles.cancelButton]}
              onPress={onCancel}
              disabled={isLoading}
            >
              <Text style={[styles.cancelButtonText, { color: theme.colors.text }]}>
                취소
              </Text>
            </TouchableOpacity>
            
            <TouchableOpacity
              style={[styles.button, styles.confirmButton]}
              onPress={onConfirm}
              disabled={isLoading}
            >
              <Text style={styles.confirmButtonText}>
                {isLoading ? '처리 중...' : '확인'}
              </Text>
            </TouchableOpacity>
          </View>
        </View>
      </TouchableOpacity>
    </Modal>
  );
};

const styles = StyleSheet.create({
  modalBackground: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    width: '80%',
    padding: 20,
    backgroundColor: 'white',
    borderRadius: 16,
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 8,
    textAlign: 'center',
  },
  modalSubtitle: {
    marginBottom: 20,
    textAlign: 'center',
  },
  passwordInput: {
    borderWidth: 1,
    borderRadius: 8,
    padding: 12,
    marginBottom: 15,
    width: '100%',
  },
  errorText: {
    color: 'red',
    marginBottom: 15,
    textAlign: 'center',
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  button: {
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
    flex: 1,
  },
  cancelButton: {
    backgroundColor: '#f0f0f0',
    marginRight: 10,
  },
  confirmButton: {
    backgroundColor: '#3473E7',
  },
  cancelButtonText: {
    fontWeight: '500',
  },
  confirmButtonText: {
    color: '#FFF',
    fontWeight: 'bold',
  }
});

export default AccountPasswordModal; 