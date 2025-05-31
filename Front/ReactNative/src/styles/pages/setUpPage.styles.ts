// 경로: src/styles/pages/setUpPage.styles.ts
import { StyleSheet, ViewStyle, TextStyle } from 'react-native';
import { Theme } from '../../types/theme';

// 스타일 타입 정의
interface SetUpPageStyles {
  container: ViewStyle;
  contentStyle: ViewStyle;
  header: ViewStyle;
  headerTitle: TextStyle;
  content: ViewStyle;
  menuSection: ViewStyle;
  menuItem: ViewStyle;
  menuItemText: TextStyle;
  menuItemArrow: TextStyle;
  divider: ViewStyle;
  sectionDivider: ViewStyle;
  // 테마 토글 스타일
  themeOptionContainer: ViewStyle;
  themeOptionText: TextStyle;
  themeSelectedIndicator: ViewStyle;
  themeUnselectedIndicator: ViewStyle;
  // 프로필/알림 페이지 스타일
  pageContainer: ViewStyle;
  pageText: TextStyle;
}

export default function createStyles(theme: Theme): SetUpPageStyles {
  return StyleSheet.create<SetUpPageStyles>({
    container: {
      flex: 1,
      backgroundColor: theme.colors.background,
    },
    contentStyle: {
      backgroundColor: theme.colors.background,
    },
    header: {
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'space-between',
      paddingHorizontal: 16,
      height: 56,
      backgroundColor: theme.colors.card,
    },
    headerTitle: {
      fontSize: 18,
      fontWeight: '600',
      color: theme.colors.text,
    },
    content: {
      flex: 1,
    },
    menuSection: {
      backgroundColor: theme.colors.card,
      marginVertical: 10,
    },
    menuItem: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      paddingVertical: 16,
      paddingHorizontal: 16,
      backgroundColor: theme.colors.card,
    },
    menuItemText: {
      fontSize: 16,
      color: theme.colors.text,
    },
    menuItemArrow: {
      fontSize: 20,
      color: theme.colors.textLight,
    },
    divider: {
      height: 2,
      backgroundColor: theme.colors.background,
    },
    sectionDivider: {
      height: 8,
      backgroundColor: theme.colors.background,
    },
    // 테마 토글 스타일
    themeOptionContainer: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      paddingVertical: 16,
      paddingHorizontal: 16,
      backgroundColor: theme.colors.card,
      marginBottom: 8,
    },
    themeOptionText: {
      fontSize: 16,
      color: theme.colors.text,
    },
    themeSelectedIndicator: {
      width: 24,
      height: 24,
      borderRadius: 12,
      backgroundColor: theme.colors.primary,
    },
    themeUnselectedIndicator: {
      width: 24,
      height: 24,
      borderRadius: 12,
      borderWidth: 2,
      borderColor: theme.colors.border,
    },
    // 프로필/알림 페이지 스타일
    pageContainer: {
      flex: 1,
      backgroundColor: theme.colors.background,
      justifyContent: 'center',
      alignItems: 'center',
      padding: 16,
    },
    pageText: {
      fontSize: 16,
      color: theme.colors.textLight,
      textAlign: 'center',
    },
  });
}
