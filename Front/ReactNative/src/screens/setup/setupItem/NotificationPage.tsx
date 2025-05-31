import React from 'react';
import { View, Text } from 'react-native';
import { Theme } from '../../../types/theme';
import createStyles from '../../../styles/pages/setUpPage.styles';

interface NotificationPageProps {
  theme: Theme;
}

const NotificationPage: React.FC<NotificationPageProps> = ({ theme }) => {
  const styles = createStyles(theme);

  return (
    <View style={styles.pageContainer}>
      <Text style={styles.pageText}>알림 설정 기능 준비 중입니다.</Text>
    </View>
  );
};

export default NotificationPage; 