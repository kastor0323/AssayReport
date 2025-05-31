// 경로: src/styles/rtableComponents.styles.ts
import { StyleSheet, TextStyle, ViewStyle } from 'react-native';
import { Theme } from '../../types/theme';
import { COLUMN_WIDTHS } from '../../constants/tableConfig';

// 공통으로 사용할 스타일 인터페이스 정의
export interface TableComponentStyles {
  container: ViewStyle;
  headerContainer: ViewStyle;
  headerTitle: TextStyle;
  headerAmount: TextStyle;
  categoryTitle: TextStyle;
  tableContainer: ViewStyle;
  fixedColumn: ViewStyle;
  fixedHeader: ViewStyle;
  fixedCell: ViewStyle;
  scrollableHeader: ViewStyle;
  scrollableRow: ViewStyle;
  headerCell: TextStyle;
  nameText: TextStyle;
  subText: TextStyle;
  amountColumn: ViewStyle;
  mainAmount: TextStyle;
  subAmount: TextStyle;
  portionText: TextStyle;
  targetText: TextStyle;
  rebalanceColumn: ViewStyle;
  rebalanceText: TextStyle;
  rebalanceSubText: TextStyle;
  negativeText: TextStyle;
  positiveText: TextStyle;
  percentChange: TextStyle;
  totalContainer: ViewStyle;
  totalAmount: TextStyle;
  changeColumn: ViewStyle;
  changeText: TextStyle;
  valueColumn: ViewStyle;
  cashName: TextStyle;
  stockName: TextStyle;
  stockTicker: TextStyle;
  negativeChange: TextStyle;
  subNegativeChange: TextStyle;
  positiveChange: TextStyle;
  subPositiveChange: TextStyle;
}

// 공통 스타일 생성 함수
export const createTableStyles = (theme: Theme): TableComponentStyles => StyleSheet.create({
  container: {
    backgroundColor: theme.colors.background,
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    // 그림자 효과 (iOS)
    shadowColor: '#000',
    shadowOffset: { width: 2, height: 3 },
    shadowOpacity: 0.2,
    shadowRadius: 2,
    // 안드로이드용 그림자
    elevation: 0.1,
    // 테두리 효과
    borderColor: 'rgba(0,0,0,0.05)',
    borderWidth: 1,
    borderBottomWidth: 2,
    borderRightWidth: 1,
    borderBottomColor: 'rgba(0,0,0,0.2)',
    borderRightColor: 'rgba(0,0,0,0.1)',
  },
  headerContainer: {
    marginBottom: 16,
  },
  headerTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: theme.colors.text,
    marginBottom: 4,
  },
  categoryTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: theme.colors.text,
    marginBottom: 4,
  },
  headerAmount: {
    fontSize: 22,
    fontWeight: '700',
    color: theme.colors.text,
  },
  totalContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  totalAmount: {
    fontSize: 22,
    fontWeight: '700',
    color: theme.colors.text,
    marginRight: 8,
  },
  percentChange: {
    fontSize: 14,
    fontWeight: '600',
    color: theme.colors.text,
  },
  tableContainer: {
    flexDirection: 'row',
  },
  fixedColumn: {
    width: COLUMN_WIDTHS.name,
    borderRightWidth: 1,
    borderRightColor: theme.colors.border,
  },
  fixedHeader: {
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.border,
    justifyContent: 'center',
    alignItems: 'flex-start',
  },
  fixedCell: {
    paddingVertical: 12,
    justifyContent: 'center',
    height: 60,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.border,
    paddingHorizontal: 8,
    alignItems: 'flex-start',
  },
  scrollableHeader: {
    flexDirection: 'row',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.border,
  },
  scrollableRow: {
    flexDirection: 'row',
    height: 60,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.border,
    alignItems: 'center',
  },
  headerCell: {
    fontSize: 12,
    color: theme.colors.placeholder,
    fontWeight: '500',
    padding: 8,
    textAlign: 'right',
  },
  nameText: {
    fontSize: 14,
    fontWeight: '600',
    color: theme.colors.text,
    textAlign: 'left',
  },
  subText: {
    fontSize: 12,
    color: theme.colors.placeholder,
    marginTop: 2,
  },
  // 현금 항목용
  cashName: {
    fontSize: 14,
    fontWeight: '600',
    color: theme.colors.text,
    paddingHorizontal: 8,
    textAlign: 'left',
  },
  // 주식 항목용
  stockName: {
    fontSize: 14,
    fontWeight: '600',
    color: theme.colors.text,
    textAlign: 'left',
  },
  stockTicker: {
    fontSize: 12,
    color: theme.colors.placeholder,
    marginTop: 2,
  },
  amountColumn: {
    justifyContent: 'center',
    alignItems: 'flex-end',
  },
  mainAmount: {
    fontSize: 14,
    fontWeight: '500',
    color: theme.colors.text,
    textAlign: 'right',
  },
  subAmount: {
    fontSize: 12,
    color: theme.colors.placeholder,
    marginTop: 2,
    textAlign: 'right',
  },
  portionText: {
    fontSize: 14,
    fontWeight: '500',
    color: theme.colors.text,
    textAlign: 'right',
  },
  targetText: {
    fontSize: 14,
    fontWeight: '500',
    color: theme.colors.text,
    textAlign: 'right',
  },
  rebalanceColumn: {
    justifyContent: 'center',
    alignItems: 'flex-end',
  },
  rebalanceText: {
    fontSize: 14,
    fontWeight: '600',
    color: theme.colors.text,
    textAlign: 'right',
  },
  rebalanceSubText: {
    fontSize: 12,
    color: theme.colors.placeholder,
    marginTop: 2,
    textAlign: 'right',
  },
  negativeText: {
    color: theme.colors.negative,
  },
  positiveText: {
    color: theme.colors.positive,
  },
  changeColumn: {
    justifyContent: 'center',
    alignItems: 'flex-end',
  },
  changeText: {
    fontSize: 14,
    fontWeight: '600',
    color: theme.colors.text,
    textAlign: 'right',
  },
  valueColumn: {
    justifyContent: 'center',
    alignItems: 'flex-end',
  },
  negativeChange: {
    color: theme.colors.negative,
  },
  subNegativeChange: {
    color: theme.colors.negative+ '99',
  },
  positiveChange: {
    color: theme.colors.positive,
  },
  subPositiveChange: {
    color: theme.colors.positive + '99',
  },
});
