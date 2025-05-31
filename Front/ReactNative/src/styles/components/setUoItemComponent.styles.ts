// 경로: src/styles/components/setUoItemComponent.styles.ts
import { StyleSheet, ViewStyle, TextStyle } from 'react-native';
import { Theme } from '../../types/theme';

// 스타일 타입 정의
interface SetUpItemStyles {
  container: ViewStyle;
  itemText: TextStyle;
  iconContainer: ViewStyle;
}

export default function createStyles(theme: Theme): SetUpItemStyles {
  return StyleSheet.create<SetUpItemStyles>({
    container: {
      width: '100%',
      height: 56,
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'space-between',
      paddingHorizontal: 20,
      backgroundColor: theme.colors.background,
      borderBottomWidth: 1,
      borderBottomColor: theme.colors.border,
    },
    itemText: {
      fontSize: 16,
      fontWeight: '400',
      color: theme.colors.text,
      flex: 1,
    },
    iconContainer: {
      width: 24,
      height: 24,
      alignItems: 'center',
      justifyContent: 'center',
      marginLeft: 8,
    }
  });
}
