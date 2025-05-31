import React from 'react';
import { View, Text } from 'react-native';
import { Theme } from '../../../types/theme';
import createStyles from '../../../styles/pages/setUpPage.styles';

interface ProfilePageProps {
  theme: Theme;
}

const ProfilePage: React.FC<ProfilePageProps> = ({ theme }) => {
  const styles = createStyles(theme);

  return (
    <View style={styles.pageContainer}>
      <Text style={styles.pageText}>프로필 관리 기능 준비 중입니다.</Text>
    </View>
  );
};

export default ProfilePage; 