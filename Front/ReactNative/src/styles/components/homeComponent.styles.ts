// 경로: src/styles/components/homeComponent.styles.ts
import { StyleSheet, ViewStyle, TextStyle } from 'react-native';
import { Theme } from '../../types/theme';

// 스타일 타입 정의
interface HomeComponentStyles {
  container: ViewStyle;
  contentContainer: ViewStyle;
  sectionHeader: ViewStyle;
  sectionTitle: TextStyle;
  section: ViewStyle;
  linkText: TextStyle;
  dateText: TextStyle;
  card: ViewStyle;
  emptyCard: ViewStyle;
  emptyText: TextStyle;
  accountRow: ViewStyle;
  accountLabel: TextStyle;
  accountValue: TextStyle;
  returnRow: ViewStyle;
  accountShortName: TextStyle;
  recordName: TextStyle;
  returnRatePositive: TextStyle;
  returnRateNegative: TextStyle;
  divider: ViewStyle;
  footerText: TextStyle;
}

export default function createStyles(theme: Theme): HomeComponentStyles {
  return StyleSheet.create<HomeComponentStyles>({
    container: {
      flex: 1,
      backgroundColor: theme.colors.background,
    },
    contentContainer: {
      padding: 16,
      paddingBottom: 30,
    },
    sectionHeader: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: 8,
    },
    section: {
      marginTop: 20,
    },
    sectionTitle: {
      fontSize: 16,
      fontWeight: '600',
      color: theme.colors.text,
    },
    linkText: {
      fontSize: 12,
      color: theme.colors.placeholder,
    },
    dateText: {
      fontSize: 12,
      color: theme.colors.placeholder,
    },
    card: {
      backgroundColor: theme.colors.card,
      borderRadius: 8,
      padding: 16,
      marginBottom: 4,
    },
    emptyCard: {
      alignItems: 'center',
      justifyContent: 'center',
      paddingVertical: 24,
    },
    emptyText: {
      fontSize: 14,
      color: theme.colors.placeholder,
      textAlign: 'center',
    },
    accountRow: {
      flexDirection: 'row',
      alignItems: 'center',
      marginBottom: 4,
    },
    accountLabel: {
      fontSize: 14,
      color: theme.colors.placeholder,
      width: 45,
    },
    accountValue: {
      fontSize: 14,
      color: theme.colors.text,
      fontWeight: '500',
    },
    returnRow: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      paddingVertical: 6,
    },
    accountShortName: {
      fontSize: 14,
      fontWeight: '500',
      color: theme.colors.text,
    },
    recordName: {
      fontSize: 14,
      fontWeight: '500',
      color: theme.colors.text,
    },
    returnRatePositive: {
      fontSize: 14,
      fontWeight: '600',
      color: theme.colors.positive,
    },
    returnRateNegative: {
      fontSize: 14,
      fontWeight: '600',
      color: theme.colors.negative,
    },
    divider: {
      height: 1,
      backgroundColor: theme.colors.border,
      marginVertical: 6,
    },
    footerText: {
      fontSize: 12,
      color: theme.colors.placeholder,
      textAlign: 'center',
      marginTop: 20,
    }
  });
}
