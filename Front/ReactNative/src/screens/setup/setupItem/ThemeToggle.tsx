// 경로: src/components/common/ui/ThemeToggle.tsx
import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { useTheme } from '../../../styles/theme/ThemeContext';
import { Theme } from '../../../types/theme';
import createStyles from '../../../styles/pages/setUpPage.styles';

interface ThemeToggleProps {
  theme: Theme;
}

const ThemeToggle: React.FC<ThemeToggleProps> = ({ theme }) => {
  const { isDark, setTheme } = useTheme();
  const styles = createStyles(theme);

  return (
    <View style={styles.container}>
      <TouchableOpacity 
        style={styles.themeOptionContainer} 
        onPress={() => setTheme('light')}
      >
        <Text style={styles.themeOptionText}>라이트 모드</Text>
        <View style={!isDark ? styles.themeSelectedIndicator : styles.themeUnselectedIndicator} />
      </TouchableOpacity>

      <TouchableOpacity 
        style={styles.themeOptionContainer} 
        onPress={() => setTheme('dark')}
      >
        <Text style={styles.themeOptionText}>다크 모드</Text>
        <View style={isDark ? styles.themeSelectedIndicator : styles.themeUnselectedIndicator} />
      </TouchableOpacity>
    </View>
  );
};

export default ThemeToggle;
