import { StyleSheet } from 'react-native';
import { Theme } from '../../types/theme';

const createStyles = (theme: Theme) => {
  return StyleSheet.create({
    container: {
      width: '100%',
      marginVertical: 8,
      zIndex: 100, // 다른 요소보다 위에 표시
    },
    
    // 선택된 계좌 영역 스타일
    selectedAccountContainer: {
      width: '100%',
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'space-between',
      backgroundColor: theme.colors.primary,
      borderRadius: 8,
      paddingHorizontal: 16,
      paddingVertical: 12,
      marginBottom: 4,
      minHeight: 50, // 최소 높이 설정
    },
    selectedAccountTextContainer: {
      flex: 1,
    },
    selectedAccountText: {
      color: 'white',
      fontWeight: '600',
      fontSize: 16,
    },
    noAccountText: {
      color: 'white',
      fontStyle: 'italic',
      textAlign: 'center',
      width: '100%',
    },

    // 드롭다운 모달 스타일
    modalOverlay: {
      flex: 1,
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
      justifyContent: 'flex-start',
      alignItems: 'center',
      paddingTop: 80, // 상단에서 약간 떨어진 위치에 표시
    },
    dropdown: {
      width: '90%',
      maxHeight: 300,
      borderRadius: 8,
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.25,
      shadowRadius: 3.84,
      elevation: 5,
    },
    accountList: {
      borderRadius: 8,
    },

    // 계좌 항목 스타일
    accountItem: {
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'space-between',
      paddingVertical: 12,
      paddingHorizontal: 16,
      height: 50, // 높이 고정
    },
    selectedAccountItem: {
      backgroundColor: theme.colors.primary,
    },
    accountItemText: {
      fontSize: 16,
      color: theme.colors.text,
    },
    selectedAccountItemText: {
      color: 'white',
      fontWeight: '600',
    },
    separator: {
      height: 1,
      backgroundColor: theme.colors.border,
      marginHorizontal: 8,
    },
  });
};

export default createStyles; 