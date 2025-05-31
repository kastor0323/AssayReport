// 파일 경로: src/components/setUoItemComponent.tsx
// 컴포넌트 흐름: 

import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

// 스타일 임포트
import { Theme } from '../../../types/theme';
import createStyles from '../../../styles/components/setUoItemComponent.styles';

// 메뉴 아이템 속성 정의
interface SetUpItemProps {
  itemName: string;
  theme: Theme;
  onPress?: () => void;
  textColor?: string;
}

const SetUoItemComponent: React.FC<SetUpItemProps> = ({ itemName, theme, onPress, textColor }) => {
  const styles = createStyles(theme);

  return (
    <TouchableOpacity style={styles.container} onPress={onPress}>
      <Text style={[styles.itemText, textColor ? { color: textColor } : null]}>{itemName}</Text>
      <View style={styles.iconContainer}>
        <Ionicons 
          name="chevron-forward" 
          size={20} 
          color={theme.colors.placeholder} 
        />
      </View>
    </TouchableOpacity>
  );
};

export default SetUoItemComponent;
