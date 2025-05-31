import React from 'react';
import { View, Text, ScrollView } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import withTheme from '../../../hoc/withTheme';
import { Theme } from '../../../types/theme';
import createStyles from '../../../styles/pages/setUpPage.styles';

interface PrivacyPageProps {
  theme: Theme;
}

const PrivacyPage: React.FC<PrivacyPageProps> = ({ theme }) => {
  const styles = createStyles(theme);

  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.sectionTitle}>1. 개인정보의 처리 목적</Text>
        <Text style={styles.paragraph}>
          회사는 다음의 목적을 위하여 개인정보를 처리하고 있으며, 다음의 목적 이외의 용도로는 이용하지 않습니다.
        </Text>

        <Text style={styles.sectionTitle}>2. 개인정보의 처리 및 보유 기간</Text>
        <Text style={styles.paragraph}>
          이용자의 개인정보는 원칙적으로 개인정보의 처리목적이 달성되면 지체 없이 파기합니다.
        </Text>

        <Text style={styles.sectionTitle}>3. 개인정보의 제3자 제공</Text>
        <Text style={styles.paragraph}>
          회사는 이용자의 개인정보를 원칙적으로 외부에 제공하지 않습니다.
        </Text>

        <View style={styles.bottomSpacing} />
      </View>
    </ScrollView>
  );
};

export default withTheme(PrivacyPage); 