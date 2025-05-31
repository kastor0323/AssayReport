// 경로: src/styles/components/rebalancingComponent.styles.js
import { StyleSheet, Dimensions } from 'react-native';
import { Theme } from '../../types/theme';

export default function createStyles(theme: Theme, cardWidth?: number) {
  return StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: theme.colors.background,
    },
    contentContainer: {
      padding: 16,
    },
    accountSelectorContainer: {
      flexDirection: 'row',
      marginBottom: 15,
      flexWrap: 'wrap',
    },
    accountButton: {
      paddingVertical: 8,
      paddingHorizontal: 15,
      marginRight: 10,
      marginBottom: 8,
      borderRadius: 25,
      backgroundColor: theme.colors.card,
    },
    selectedAccountButton: {
      backgroundColor: theme.colors.primary,
      // 테두리 효과
      borderColor: 'rgba(0,0,0,0.05)',
      borderWidth: 1,
      borderBottomWidth: 2,
      borderRightWidth: 1,
      borderBottomColor: 'rgba(0,0,0,0.2)',
      borderRightColor: 'rgba(0,0,0,0.1)',
      ...theme.shadows.default,
      // 위치 및 크기 효과
      marginBottom: 10,
      marginTop: 0,
      marginRight: 2,
      transform: [{ scale: 1.02 }],
    },
    accountText: {
      fontSize: 14,
      color: theme.colors.text,
    },
    selectedAccountText: {
      fontSize: 14,
      color: '#FFF',
      fontWeight: 'bold',
    },
    // 계좌 정보 스타일
    accountContainer: {
      backgroundColor: theme.colors.background,
      borderRadius: 12,
      padding: 16,
      marginBottom: 12,
      ...theme.shadows.default,
      // 테두리 효과
      borderColor: 'rgba(0,0,0,0.05)',
      borderWidth: 1,
      borderBottomWidth: 2,
      borderRightWidth: 1,
      borderBottomColor: 'rgba(0,0,0,0.2)',
      borderRightColor: 'rgba(0,0,0,0.1)',
    },
    // 리밸런싱 가로 스와이프 스타일
    recordSwipeContainer: {
      marginBottom: 20,
      paddingVertical: 15,
      alignItems: 'flex-start',
      justifyContent: 'flex-start',
      overflow: 'visible',
    },
    recordItemContainer: {
      padding: 16,
      width: '100%',
      borderRadius: 12,
      backgroundColor: theme.colors.background,
      ...theme.shadows.default,
      // 테두리 효과
      borderColor: 'rgba(0,0,0,0.05)',
      borderWidth: 1,
      borderBottomWidth: 1,
      borderRightWidth: 1,
      borderBottomColor: 'rgba(0,0,0,0.1)',
      borderRightColor: 'rgba(0,0,0,0.05)',
      // 내부 패딩 설정
      paddingHorizontal: 16,
      paddingVertical: 16,
      marginVertical: 5,
      overflow: 'visible',
    },
    addRecordContainer: {
      padding: 16,
      width: '100%',
      borderRadius: 12,
      backgroundColor: theme.colors.primary,
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: 150,
      ...theme.shadows.default,
      overflow: 'visible',
      marginVertical: 5,
    },
    loadPortfolioContainer: {
      padding: 16,
      width: '100%',
      borderRadius: 12,
      backgroundColor: theme.colors.primary,
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: 150,
      ...theme.shadows.default,
      overflow: 'visible',
      marginVertical: 5,
    },
    loadPortfolioIcon: {
      fontSize: 48,
      color: '#FFF',
      marginBottom: 12,
    },
    addRecordIcon: {
      fontSize: 48,
      color: '#FFF',
      marginBottom: 12,
    },
    addRecordText: {
      fontSize: 16,
      fontWeight: '600',
      color: '#FFF',
    },
    recordPaginationContainer: {
      flexDirection: 'row',
      justifyContent: 'center',
      marginTop: 8,
    },
    paginationDot: {
      width: 6,
      height: 6,
      borderRadius: 3,
      marginHorizontal: 3,
      backgroundColor: '#DDDDDD',
    },
    activePaginationDot: {
      backgroundColor: '#2F80ED',
      width: 12,
    },
    // 리밸런싱 기록명 토글
    recordToggleContainer: {
      marginBottom: 10,
    },
    recordToggleButton: {
      paddingBottom: 8,
      borderRadius: 16,
    },
    recordToggleText: {
      fontSize: 18,
      color: theme.colors.text,
    },
    recordToggleRow: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
    },
    recordEditButton: {
      marginLeft: 8,
      paddingVertical: 4,
      paddingHorizontal: 10,
      borderRadius: 8,
      backgroundColor: theme.colors.background,
      alignSelf: 'center',
    },
    recordEditText: {
      fontSize: 14,
      color: theme.colors.primary,
      fontWeight: 'bold',
    },
    modalBackground: {
      flex: 1,
      backgroundColor: 'rgba(0,0,0,0.3)',
      justifyContent: 'center',
      alignItems: 'center',
    },
    modalContent: {
      width: '80%',
      backgroundColor: theme.colors.background,
      borderRadius: 10,
      padding: 16,
      maxHeight: 300,
      ...theme.shadows.default,
      // 테두리 효과
      borderColor: 'rgba(0,0,0,0.05)',
      borderWidth: 1,
      borderBottomWidth: 2,
      borderRightWidth: 1,
      borderBottomColor: 'rgba(0,0,0,0.2)',
      borderRightColor: 'rgba(0,0,0,0.1)',
    },
    recordOption: {
      paddingVertical: 12,
      borderBottomWidth: 1,
      borderBottomColor: theme.colors.border,
    },
    recordOptionText: {
      fontSize: 15,
      color: theme.colors.text,
    },
    accountTitle: {
      fontSize: 18,
      fontWeight: '600',
      color: theme.colors.text,
      marginBottom: 12,
    },
    accountInfoRow: {
      marginBottom: 12,
      flexWrap: 'wrap',
    },
    accountInfoItem: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      flex: 1,
      minWidth: 80,
      marginHorizontal: 2,
    },
    infoLabel: {
      fontSize: 15,
      color: theme.colors.placeholder,
      marginBottom: 0,
    },
    infoValue: {
      fontSize: 16,
      fontWeight: '500',
      color: theme.colors.text,
      textAlign: 'right',
    },
    // 수익 색상
    profitPositive: {
      fontSize: 16,
      fontWeight: 'bold',
      color: '#FF3B30',
      textAlign: 'right',
    },
    profitNegative: {
      fontSize: 16,
      fontWeight: 'bold',
      color: theme.colors.negative,
      textAlign: 'right',
    },
    // 통화 토글
    currencyToggleContainer: {
      flexDirection: 'row',
      backgroundColor: theme.colors.card,
      borderRadius: 16,
      overflow: 'hidden',
      ...theme.shadows.default,
      // 테두리 효과
      borderColor: 'rgba(0,0,0,0.05)',
      borderWidth: 1,
      borderBottomWidth: 2,
      borderRightWidth: 1,
      borderBottomColor: 'rgba(0,0,0,0.2)',
      borderRightColor: 'rgba(0,0,0,0.1)',
    },
    rotateButton: {
      flexDirection: 'row',
      justifyContent: 'center',
      alignItems: 'center',
      paddingVertical: 6,
      paddingHorizontal: 10,
      borderRadius: 16,
      backgroundColor: theme.colors.card,
      marginRight: 8,
      ...theme.shadows.default,
      // 테두리 효과
      borderColor: 'rgba(0,0,0,0.05)',
      borderWidth: 1,
      borderBottomWidth: 2,
      borderRightWidth: 1,
      borderBottomColor: 'rgba(0,0,0,0.2)',
      borderRightColor: 'rgba(0,0,0,0.1)',
    },
    rotateButtonText: {
      fontSize: 14,
      fontWeight: '600',
      color: theme.colors.text,
    },
    currencyButton: {
      paddingVertical: 6,
      paddingHorizontal: 14,
    },
    activeCurrency: {
      backgroundColor: theme.colors.primary,
    },
    currencyText: {
      fontSize: 14,
      fontWeight: '600',
      color: theme.colors.text,
    },
    activeCurrencyText: {
      color: '#fff',
    },
    card: {
      width: cardWidth || Dimensions.get('window').width - 32,
      padding: 20,
      backgroundColor: theme.colors.card,
      borderRadius: 12,
      ...theme.shadows.default,
    },
  });
}
