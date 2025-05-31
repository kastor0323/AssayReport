import React from 'react';
import { View, Text, ScrollView } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import withTheme from '../../../hoc/withTheme';
import { Theme } from '../../../types/theme';
import createStyles from '../../../styles/pages/termsPage.styles';

interface TermsPageProps {
  theme: Theme;
}

const TermsPage: React.FC<TermsPageProps> = ({ theme }) => {
  const styles = createStyles(theme);

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      <View style={styles.content}>
        <Text style={styles.lastUpdated}>마지막 업데이트: 2024년 3월 21일</Text>
        
        <Text style={styles.sectionTitle}>1. 서비스 이용약관</Text>
        <Text style={styles.paragraph}>
          본 약관은 SMS Project(이하 "회사")가 제공하는 모든 서비스(이하 "서비스")의 이용 조건 및 절차, 회사와 회원 간의 권리, 의무 및 책임사항 등을 규정합니다.
        </Text>

        <Text style={styles.sectionTitle}>2. 용어의 정의</Text>
        <Text style={styles.paragraph}>
          본 약관에서 사용하는 용어의 정의는 다음과 같습니다:{'\n\n'}
          1) "서비스"란 회사가 제공하는 모든 서비스를 의미합니다.{'\n'}
          2) "회원"이란 본 약관에 동의하고 서비스를 이용하는 자를 의미합니다.{'\n'}
          3) "계정"이란 서비스 이용을 위한 회원의 고유 식별 정보를 의미합니다.
        </Text>

        <Text style={styles.sectionTitle}>3. 개인정보 보호</Text>
        <Text style={styles.paragraph}>
          회사는 회원의 개인정보를 보호하기 위해 최선을 다하며, 개인정보 보호정책은 별도로 제공됩니다.
        </Text>

        <Text style={styles.sectionTitle}>4. 서비스 이용</Text>
        <Text style={styles.paragraph}>
          회원은 본 약관 및 관련 법령을 준수하여 서비스를 이용해야 하며, 다음과 같은 행위를 해서는 안 됩니다:{'\n\n'}
          1) 타인의 정보를 도용하거나 허위 정보를 등록하는 행위{'\n'}
          2) 회사의 서비스를 방해하는 행위{'\n'}
          3) 회사의 동의 없이 서비스를 영리 목적으로 이용하는 행위{'\n'}
          4) 기타 불법적이거나 부당한 행위
        </Text>

        <Text style={styles.sectionTitle}>5. 서비스 제공 및 변경</Text>
        <Text style={styles.paragraph}>
          회사는 서비스를 365일, 24시간 제공하기 위해 노력하며, 시스템 점검, 업데이트 등으로 인한 일시적인 중단이 발생할 수 있습니다.
        </Text>

        <View style={styles.bottomSpacing} />
      </View>
    </ScrollView>
  );
};

export default withTheme(TermsPage); 