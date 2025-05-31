// // 파일 경로: src/pages/MainPage.tsx
// // 컴포넌트 흐름: App.js > AppNavigator.tsx > MainPage.tsx

// import React, { useState } from 'react';
// import { View, Text, TouchableOpacity, Image } from 'react-native';
// import { FontAwesome5, Ionicons } from '@expo/vector-icons';
// import { useSafeAreaInsets } from 'react-native-safe-area-context';
// import { useNavigation } from '@react-navigation/native';


// // 네비게이트 타입 임포트
// import { MainPageNavigationProp } from '../../types/navigation';

// // 스타일 임포트
// import createStyles from '../../styles/pages/mainPage.styles';
// import withTheme from '../../hoc/withTheme';
// import { Theme } from '../../types/theme';

// // 탭 타입 정의
// type TabType = '홈' | '자산' | '리밸런싱' | '기록';

// // 컴포넌트 props 인터페이스 정의
// interface MainPageProps {
//   theme: Theme;
// }

// const MainPage: React.FC<MainPageProps> = ({ theme }) => {
//   const [activeTab, setActiveTab] = useState<TabType>('홈');
//   const insets = useSafeAreaInsets(); 
//   const styles = createStyles(theme);
//   const navigation = useNavigation<MainPageNavigationProp>();
  
//   // 현재 탭에 따른 컴포넌트 렌더링
//   const renderComponent = (): React.ReactNode => {
//     switch(activeTab) {
//       case '홈':
//         return <HomeComponent/>;
//       case '자산':
//         return <MyStockAccountComponent />;
//       case '리밸런싱':
//         return <RebalancingComponent />;
//       case '기록':
//         return <RecordComponent />;
//       default:
//         return <MyStockAccountComponent />;
//     }
//   };
  
//   return (
//     <View style={[styles.container, { paddingTop: insets.top }]}>
      
//       {/* 서브 헤더 */}
//       <View style={styles.subHeader}>
//         <TouchableOpacity 
//           style={styles.button}
//           onPress={() => setActiveTab('홈')}
//         >
//           <Image source={require('../../../assets/ant_head.png')} style={styles.logoImage} resizeMode="contain" />
//         </TouchableOpacity>
        
//         <Text style={styles.pageName}>{activeTab}</Text>
        
//         <TouchableOpacity 
//           style={styles.button}
//           onPress={() => navigation.navigate('설정 페이지')}
//         >
//           <Text style={{ color: theme.colors.text }}>설정</Text>
//         </TouchableOpacity>
//       </View>
      
//       {/* 메인 콘텐츠 영역 */}
//       <View style={styles.content}>
//         {renderComponent()}
//       </View>
      
//       {/* 하단 네비게이션 바 */}
//       <View style={styles.bottomNav}>
//         {/* 홈 탭 */}
//         <TouchableOpacity 
//           style={styles.navItem} 
//           onPress={() => setActiveTab('홈')}
//         >
//           <FontAwesome5 
//             name="home" 
//             size={24} 
//             color={activeTab === '홈' ? theme.colors.primary : theme.colors.placeholder} 
//           />
//           <Text style={[styles.navText, activeTab === '홈' && styles.activeNavText]}>
//             홈
//           </Text>
//         </TouchableOpacity>
        
//         {/* 자산 탭 */}
//         <TouchableOpacity 
//           style={styles.navItem} 
//           onPress={() => setActiveTab('자산')}
//         >
//           <FontAwesome5 
//             name="wallet" 
//             size={24} 
//             color={activeTab === '자산' ? theme.colors.primary : theme.colors.placeholder} 
//           />
//           <Text style={[styles.navText, activeTab === '자산' && styles.activeNavText]}>
//             자산
//           </Text>
//         </TouchableOpacity>
        
//         {/* 리밸런싱 탭 */}
//         <TouchableOpacity 
//           style={styles.navItem} 
//           onPress={() => setActiveTab('리밸런싱')}
//         >
//           <Ionicons 
//             name="sync" 
//             size={24} 
//             color={activeTab === '리밸런싱' ? theme.colors.primary : theme.colors.placeholder} 
//           />
//           <Text style={[styles.navText, activeTab === '리밸런싱' && styles.activeNavText]}>
//             리밸런싱
//           </Text>
//         </TouchableOpacity>
        
//         {/* 기록 탭 */}
//         <TouchableOpacity 
//           style={styles.navItem} 
//           onPress={() => setActiveTab('기록')}
//         >
//           <Ionicons 
//             name="document-text-outline" 
//             size={24} 
//             color={activeTab === '기록' ? theme.colors.primary : theme.colors.placeholder} 
//           />
//           <Text style={[styles.navText, activeTab === '기록' && styles.activeNavText]}>
//             기록
//           </Text>
//         </TouchableOpacity>
//       </View>
//     </View>
//   );
// };

// export default withTheme(MainPage);
