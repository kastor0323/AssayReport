import { StyleSheet, ViewStyle, TextStyle } from 'react-native';
import { Theme } from '../../types/theme';

// MyStockAccountComponent 스타일 타입 정의
export interface MyStockAccountComponentStylesType {
  // 컨테이너 스타일
  container: ViewStyle;
  contentContainer: ViewStyle;
  
  // 계좌 선택 영역 스타일
  accountSelectorContainer: ViewStyle;
  accountButton: ViewStyle;
  selectedAccountButton: ViewStyle;
  accountText: TextStyle;
  selectedAccountText: TextStyle;
  
  // 통화 선택 영역 스타일
  currencySelectorContainer: ViewStyle;
  
  // 요약 정보 영역 스타일
  summaryContainer: ViewStyle;
  smallTitle: TextStyle;
  totalValue: TextStyle;
  
  // 차트 영역 스타일
  chartContainer: ViewStyle;
  
  // 종목 리스트 영역 스타일
  stockListHeader: ViewStyle;
  sectionTitle: TextStyle;
  stockList: ViewStyle;
  stockItemContainer: ViewStyle;
  colorIndicator: ViewStyle;
  stockInfo: ViewStyle;
  stockName: TextStyle;
  stockValue: TextStyle;
  stockRatio: TextStyle;
}

// 스타일 생성 함수
const createStyles = (theme: Theme): MyStockAccountComponentStylesType => StyleSheet.create({
  // 컨테이너 관련 스타일
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  contentContainer: {
    padding: 16,
    paddingBottom: 30, // 하단 여백 추가
  },
  
  // 계좌 선택 영역 스타일
  accountSelectorContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 16,
  },
  accountButton: {
    paddingHorizontal: 12,
    paddingVertical: 8,
    backgroundColor: theme.colors.card,
    borderRadius: 8,
    marginRight: 8,
    marginBottom: 8,
  },
  selectedAccountButton: {
    backgroundColor: theme.colors.primary,
  },
  accountText: {
    color: theme.colors.text,
    fontSize: 14,
  },
  selectedAccountText: {
    color: 'white',
    fontWeight: 'bold',
  },
  
  // 통화 선택 영역 스타일
  currencySelectorContainer: {
    flexDirection: 'row',
    marginBottom: 10,
  },
  
  // 요약 정보 영역 스타일
  summaryContainer: {
    backgroundColor: theme.colors.card,
    borderRadius: 12,
    padding: 16,
    marginBottom: 20,
  },
  smallTitle: {
    fontSize: 14,
    color: theme.colors.text,
    marginBottom: 8,
  },
  totalValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: theme.colors.text,
  },
  
  // 차트 영역 스타일
  chartContainer: {
    marginBottom: 20,
    height: 240,
    alignItems: 'center',
    justifyContent: 'center',
  },
  
  // 종목 리스트 영역 스타일
  stockListHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: theme.colors.text,
  },
  stockList: {
    backgroundColor: theme.colors.card,
    borderRadius: 12,
    padding: 8,
  },
  stockItemContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    paddingHorizontal: 8,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(0,0,0,0.05)',
  },
  colorIndicator: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 10,
  },
  stockInfo: {
    flex: 1,
  },
  stockName: {
    fontSize: 14,
    color: theme.colors.text,
    marginBottom: 4,
  },
  stockValue: {
    fontSize: 14,
    color: theme.colors.text,
    fontWeight: 'bold',
  },
  stockRatio: {
    fontSize: 14,
    color: theme.colors.text,
    fontWeight: 'bold',
  },
});

export default createStyles;
