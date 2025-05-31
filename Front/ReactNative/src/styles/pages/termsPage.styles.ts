import { StyleSheet, ViewStyle, TextStyle } from 'react-native';
import { Theme } from '../../types/theme';

interface TermsPageStyles {
  container: ViewStyle;
  header: ViewStyle;
  headerTitle: TextStyle;
  content: ViewStyle;
  lastUpdated: TextStyle;
  sectionTitle: TextStyle;
  paragraph: TextStyle;
  bottomSpacing: ViewStyle;
}

export default function createStyles(theme: Theme): TermsPageStyles {
  return StyleSheet.create<TermsPageStyles>({
    container: {
      flex: 1,
      backgroundColor: theme.colors.background,
    },
    header: {
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'space-between',
      paddingHorizontal: 16,
      height: 56,
      borderBottomWidth: 1,
      borderBottomColor: theme.colors.border,
    },
    headerTitle: {
      fontSize: 18,
      fontWeight: '600',
      color: theme.colors.text,
    },
    content: {
      flex: 1,
      padding: 16,
    },
    lastUpdated: {
      fontSize: 12,
      color: theme.colors.textLight,
      marginBottom: 24,
    },
    sectionTitle: {
      fontSize: 16,
      fontWeight: '600',
      color: theme.colors.text,
      marginTop: 24,
      marginBottom: 12,
    },
    paragraph: {
      fontSize: 14,
      lineHeight: 20,
      color: theme.colors.text,
      marginBottom: 16,
    },
    bottomSpacing: {
      height: 40,
    },
  });
} 