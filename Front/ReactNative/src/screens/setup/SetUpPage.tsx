// 파일 경로: src/screens/setup/SetUpPage.tsx
// 컴포넌트 흐름: App.js > AuthNavigator.tsx > SetUpPage.tsx

import React from 'react';
import { View, Text, ScrollView, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

// 컴포넌트 임포트
import { useAuth } from '../../context/AuthContext';
import ThemeToggle from './setupItem/ThemeToggle';
import TermsPage from './setupItem/TermsPage';
import PrivacyPage from './setupItem/PrivacyPage';
import NotificationPage from './setupItem/NotificationPage';
import ProfilePage from './setupItem/ProfilePage';

// 스타일 임포트
import createStyles from '../../styles/pages/setUpPage.styles';
import withTheme from '../../hoc/withTheme';
import { Theme } from '../../types/theme';

// 설정 스택 네비게이터 타입 정의
type SetUpStackParamList = {
  설정: undefined;
  프로필관리: undefined;
  알림설정: undefined;
  테마: undefined;
  이용약관: undefined;
  개인정보처리방침: undefined;
};

const SetUpStack = createNativeStackNavigator<SetUpStackParamList>();

// 공통 헤더 컴포넌트
interface SetUpHeaderProps {
  title: string;
  theme: Theme;
}

const SetUpHeader: React.FC<SetUpHeaderProps> = ({ title, theme }) => {
  const navigation = useNavigation();
  const insets = useSafeAreaInsets();
  const styles = createStyles(theme);

  return (
    <View style={[styles.header, { marginTop: insets.top }]}>
      <TouchableOpacity onPress={() => navigation.goBack()}>
        <Ionicons name="arrow-back" size={24} color={theme.colors.text} />
      </TouchableOpacity>
      <Text style={styles.headerTitle}>{title}</Text>
      <View style={{ width: 24 }} />
    </View>
  );
};

interface MenuItemType {
  id: string;
  name: string;
  navigationTarget?: string;
  isRed?: boolean;
}

interface MenuSection {
  items: MenuItemType[];
}

const MenuItem: React.FC<{
  name: string;
  onPress: () => void;
  theme: Theme;
  isRed?: boolean;
}> = ({ name, onPress, theme, isRed }) => {
  const styles = createStyles(theme);
  
  return (
    <TouchableOpacity style={styles.menuItem} onPress={onPress}>
      <Text style={[
        styles.menuItemText,
        isRed && { color: theme.colors.error }
      ]}>{name}</Text>
      <Ionicons 
        name="chevron-forward" 
        size={20} 
        color={theme.colors.textLight}
      />
    </TouchableOpacity>
  );
};

// 메인 설정 화면 컴포넌트
const SetUpMain: React.FC<{ theme: Theme }> = ({ theme }) => {
  const navigation = useNavigation();
  const styles = createStyles(theme);
  const { logout } = useAuth();
  
  const menuSections: MenuSection[] = [
    {
      items: [
        { id: 'profile', name: '프로필 관리', navigationTarget: '프로필관리' },
        { id: 'notification', name: '알림 설정', navigationTarget: '알림설정' },
        { id: 'theme', name: '테마', navigationTarget: '테마' },
      ]
    },
    {
      items: [
        { id: 'privacy', name: '개인정보 처리방침', navigationTarget: '개인정보처리방침' },
        { id: 'terms', name: '이용약관', navigationTarget: '이용약관' },
      ]
    },
    {
      items: [
        { id: 'logout', name: '로그아웃', isRed: true },
      ]
    }
  ];

  const handleItemPress = (item: MenuItemType) => {
    if (item.id === 'logout') {
      logout();
    } else if (item.navigationTarget) {
      navigation.navigate(item.navigationTarget as never);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        {menuSections.map((section, sectionIndex) => (
          <View key={`section-${sectionIndex}`} style={styles.menuSection}>
            {section.items.map((item, itemIndex) => (
              <React.Fragment key={item.id}>
                <MenuItem
                  name={item.name}
                  onPress={() => handleItemPress(item)}
                  theme={theme}
                  isRed={item.isRed}
                />
                {itemIndex < section.items.length - 1 && (
                  <View style={styles.divider} />
                )}
              </React.Fragment>
            ))}
          </View>
        ))}
      </View>
    </ScrollView>
  );
};

interface SetUpPageProps {
  theme: Theme;
}

const SetUpPage: React.FC<SetUpPageProps> = ({ theme }) => {
  const ThemedSetUpMain = withTheme(SetUpMain);
  const ThemedProfilePage = withTheme(ProfilePage);
  const ThemedNotificationPage = withTheme(NotificationPage);
  const ThemedThemeToggle = withTheme(ThemeToggle);
  const ThemedTermsPage = withTheme(TermsPage);
  const ThemedPrivacyPage = withTheme(PrivacyPage);

  return (
    <SetUpStack.Navigator 
      screenOptions={{
        header: ({ route }) => {
          const ThemedHeader = withTheme(SetUpHeader);
          return <ThemedHeader title={route.name} />;
        },
        contentStyle: {
          backgroundColor: theme.colors.card
        }
      }}
    >
      <SetUpStack.Screen name="설정" component={ThemedSetUpMain} />
      <SetUpStack.Screen name="프로필관리" component={ThemedProfilePage} />
      <SetUpStack.Screen name="알림설정" component={ThemedNotificationPage} />
      <SetUpStack.Screen name="테마" component={ThemedThemeToggle} />
      <SetUpStack.Screen name="이용약관" component={ThemedTermsPage} />
      <SetUpStack.Screen name="개인정보처리방침" component={ThemedPrivacyPage} />
    </SetUpStack.Navigator>
  );
};

export default withTheme(SetUpPage);
