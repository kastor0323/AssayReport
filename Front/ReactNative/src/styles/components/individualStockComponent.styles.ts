// 경로: src/styles/components/individualStockComponent.styles.ts
import { StyleSheet, ViewStyle, TextStyle } from 'react-native';

import { Theme } from '../../types/theme';

// 스타일 타입 정의
interface IndividualStockComponentStyles {
  container: ViewStyle;
  colorIndicator: ViewStyle;
  stockInfo: ViewStyle;
  stockName: TextStyle;
  stockValue: TextStyle;
  stockRatio: TextStyle;
}

export default function createStyles(theme: Theme): IndividualStockComponentStyles {
  return StyleSheet.create<IndividualStockComponentStyles>({
    container: {
      flexDirection: 'row',
      alignItems: 'center',
      paddingVertical: 16,
    },
    colorIndicator: {
      width: 12,
      height: 12,
      marginRight: 12,
    },
    stockInfo: {
      flex: 1,
    },
    stockName: {
      fontSize: 16,
      fontWeight: '500',
      color: theme.colors.text,
    },
    stockValue: {
      fontSize: 14,
      color: theme.colors.placeholder,
      marginTop: 4,
    },
    stockRatio: {
      fontSize: 16,
      fontWeight: '600',
      color: theme.colors.text,
    }
  });
}