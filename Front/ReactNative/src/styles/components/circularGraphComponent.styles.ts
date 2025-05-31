// 경로: src/styles/components/circularGraphComponent.styles.js
import { StyleSheet, ViewStyle, TextStyle } from 'react-native';

import { Theme } from '../../types/theme';

// 스타일 타입 정의
interface CircularGraphStyles {
  container: ViewStyle;
  chartContainer: ViewStyle;
  description: TextStyle;
  legendContainer: ViewStyle;
  legendItem: ViewStyle;
  legendColor: ViewStyle;
  legendText: TextStyle;
  chartTitle: TextStyle;
  centerContainer: ViewStyle;
  centerLabel: TextStyle;
  centerValue: TextStyle;
}

export default function createStyles(theme: Theme): CircularGraphStyles {
  return StyleSheet.create<CircularGraphStyles>({
    container: {
      alignItems: 'center',
      padding: 16,
      marginBottom: 16,
    },
    chartContainer: {
      alignItems: 'center',
      justifyContent: 'center',
      width: '100%',
      // paddingVertical: 8,
    },
    description: {
      fontSize: 14,
      color: theme.colors.placeholder,
      marginTop: 16,
      textAlign: 'center',
    },
    legendContainer: {
      flexDirection: 'row',
      flexWrap: 'wrap',
      justifyContent: 'center',
      marginTop: 16,
    },
    legendItem: {
      flexDirection: 'row',
      alignItems: 'center',
      marginRight: 16,
      marginBottom: 8,
    },
    legendColor: {
      width: 12,
      height: 12,
      borderRadius: 6,
      marginRight: 6,
    },
    legendText: {
      fontSize: 12,
      color: theme.colors.text,
    },
    chartTitle: {
      fontSize: 16,
      fontWeight: '500',
      color: theme.colors.text,
      marginBottom: 16,
      alignSelf: 'flex-start',
    },
    centerContainer: {
      position: 'absolute',
      width: 100,
      height: 100,
      borderRadius: 50,
      justifyContent: 'center',
      alignItems: 'center',
    },
    centerLabel: {
      fontSize: 12,
      color: theme.colors.placeholder,
      marginBottom: 4,
    },
    centerValue: {
      fontSize: 14,
      fontWeight: '600',
      color: theme.colors.text,
    }
  });
}
