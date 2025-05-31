// // 파일 경로: src/components/HomeComponent.tsx
// // 컴포넌트 흐름: App.tsx > AppNavigator.tsx > MainPage.tsx > HomeComponent.tsx

// import React, { useState, useEffect } from 'react';
// import { View, Text, TouchableOpacity, ScrollView, Platform } from 'react-native';
// import { useAuth } from '../../../context/AuthContext';
// import { fetchStockAccounts } from '../../../api/homeApi';
// import { findSecuritiesFirmByName } from '../../../data/organizationData';

// // 스타일 임포트
// import withTheme from '../../../hoc/withTheme';
// import createStyles from '../../../styles/components/homeComponent.styles';
// import { Theme } from '../../../types/theme';

// // 계좌 데이터 인터페이스 정의
// interface AccountData {
//   company: string;
//   accountNumber: string;
//   returnRate: number;
// }

// // 리밸런싱 기록 인터페이스 정의
// interface RebalancingRecord {
//   name: string;
//   returnRate: number;
// }

// // 컴포넌트 props 인터페이스 정의
// interface HomeComponentProps {
//   theme: Theme;
// }

// const HomeComponent: React.FC<HomeComponentProps> = ({ theme }) => {
//   const { loggedToken } = useAuth();
//   const { accounts: savedAccounts, addAccount } = useAccounts();

//   // DB에서 불러온 계좌 데이터
//   const [hasAccounts, setHasAccounts] = useState<boolean>(false);
//   const [accounts, setAccounts] = useState<AccountData[]>([]);

//   useEffect(() => {
//     if (!loggedToken) {
//       console.log('토큰 없음, API 호출 안함');
//       return;
//     }

//     // 계좌 정보 가져오기
//     const getAccounts = async () => {
//       console.log('계좌 정보 가져오기 시도...');
//       const result = await fetchStockAccounts(loggedToken);

//       if (result.success && result.data) {
//         console.log('계좌 API 응답:', result.data);
//         setAccounts(result.data);
//         setHasAccounts(result.data.length > 0);

//         // 로컬에 계좌 정보 저장
//         saveAccountsToLocal(result.data);
//       } else {
//         console.log('계좌 정보 가져오기 실패');
//         setAccounts([]);
//         setHasAccounts(false);
//       }
//     };

//     getAccounts();
//   }, [loggedToken]);

//   // 계좌 정보를 로컬에 저장하는 함수
//   const saveAccountsToLocal = async (accountsData: AccountData[]) => {
//     try {
//       console.log('계좌 정보 로컬 저장 시작...');

//       // 이미 저장된 계좌 찾기 (계좌번호로 비교)
//       const alreadySavedAccountNumbers = savedAccounts.map(acc => acc.account);

//       for (const account of accountsData) {
//         // 이미 저장된 계좌는 건너뛰기
//         if (alreadySavedAccountNumbers.includes(account.accountNumber)) {
//           console.log(`계좌 ${account.accountNumber}는 이미 저장되어 있습니다.`);
//           continue;
//         }

//         // 증권사 코드 찾기
//         const firmInfo = findSecuritiesFirmByName(account.company);
//         if (!firmInfo) {
//           console.warn(`증권사 ${account.company}에 대한 코드를 찾을 수 없습니다.`);
//           continue;
//         }

//         // 새 계좌 정보 객체 생성 (비밀번호는 아직 없음)
//         const newAccount = {
//           account: account.accountNumber,
//           account_password: '', // 비밀번호는 비워둠 (사용자가 나중에 입력)
//           connectedId: '', // connectedId도 비워둠 (실제 연결 시 업데이트)
//           organization: firmInfo.code
//         };

//         // AccountsContext에 저장
//         await addAccount(newAccount);
//         console.log(`계좌 ${account.accountNumber} 로컬에 저장됨`);
//       }

//       console.log('모든 계좌 정보 로컬 저장 완료');
//     } catch (error) {
//       console.error('계좌 정보 로컬 저장 중 오류:', error);
//     }
//   };

//   // 리밸런싱 기록 샘플
//   const [hasRecords, setHasRecords] = useState<boolean>(false);
//   const [records, setRecords] = useState<RebalancingRecord[]>([
//     { name: '토스 공격형 투자', returnRate: 1.3 },
//     { name: '토스 안전형 투자', returnRate: 0.5 },
//     { name: '한투 안전형 투자', returnRate: 0.3 }
//   ]);

//   // 모달 상태 추가
//   const [isConnectModalVisible, setIsConnectModalVisible] = useState(false);

//   // 모달 열기
//   const openConnectModal = () => {
//     setIsConnectModalVisible(true);
//   };

//   // 모달 닫기
//   const closeConnectModal = () => {
//     setIsConnectModalVisible(false);
//   };

//   const styles = createStyles(theme);

//   return (
//     <ScrollView
//       style={styles.container}
//       contentContainerStyle={styles.contentContainer}
//       showsVerticalScrollIndicator={false}
//     >
//       {/* 계좌 섹션 */}
//       <View style={styles.sectionHeader}>
//         <Text style={styles.sectionTitle}>계좌</Text>
//         <TouchableOpacity onPress={openConnectModal}>
//           <Text style={styles.linkText}>계좌 연동하기 &gt;</Text>
//         </TouchableOpacity>
//       </View>

//       {hasAccounts ? (
//         <View style={styles.card}>
//           {accounts.map((account, index) => (
//             <View key={index}>
//               <View style={styles.accountRow}>
//                 <Text style={styles.accountValue}>{account.company} {account.accountNumber}</Text>
//               </View>
//               {index < accounts.length - 1 && <View style={styles.divider} />}
//             </View>
//           ))}
//         </View>
//       ) : (
//         <View style={[styles.card, styles.emptyCard]}>
//           <Text style={styles.emptyText}>계좌가 아직 없어요</Text>
//         </View>
//       )}

//       {/* 계좌 수익률 섹션 */}
//       <View style={styles.section}>
//         <View style={styles.sectionHeader}>
//           <Text style={styles.sectionTitle}>계좌 수익률</Text>
//           <Text style={styles.dateText}>1월 1일 기준</Text>
//         </View>

//         {hasAccounts ? (
//           <View style={styles.card}>
//             {accounts.map((account, index) => (
//               <View key={index}>
//                 <View style={styles.returnRow}>
//                   <Text style={styles.accountShortName}>
//                     {account.company.includes('증권')
//                       ? account.company.split('증권')[0]
//                       : account.company.substring(0, 2)}
//                     {account.accountNumber.split('-')[0]}
//                   </Text>
//                   <Text
//                     style={account.returnRate > 0 ? styles.returnRatePositive : styles.returnRateNegative}
//                   >
//                     {account.returnRate > 0 ? '+' : ''}{account.returnRate}%
//                   </Text>
//                 </View>
//                 {index < accounts.length - 1 && <View style={styles.divider} />}
//               </View>
//             ))}
//           </View>
//         ) : (
//           <View style={[styles.card, styles.emptyCard]}>
//             <Text style={styles.emptyText}>계좌가 아직 없어요</Text>
//           </View>
//         )}
//       </View>

//       {/* 리밸런싱 기록 수익률 섹션 */}
//       <View style={styles.section}>
//         <View style={styles.sectionHeader}>
//           <Text style={styles.sectionTitle}>리밸런싱 기록 수익률</Text>
//           <Text style={styles.dateText}>1일 전 기준</Text>
//         </View>

//         {hasRecords ? (
//           <View style={styles.card}>
//             {records.map((record, index) => (
//               <View key={index}>
//                 <View style={styles.returnRow}>
//                   <Text style={styles.recordName}>{record.name}</Text>
//                   <Text
//                     style={record.returnRate > 0 ? styles.returnRatePositive : styles.returnRateNegative}
//                   >
//                     {record.returnRate > 0 ? '+' : ''}{record.returnRate}%
//                   </Text>
//                 </View>
//                 {index < records.length - 1 && <View style={styles.divider} />}
//               </View>
//             ))}
//           </View>
//         ) : (
//           <View style={[styles.card, styles.emptyCard]}>
//             <Text style={styles.emptyText}>기록이 아직 없어요</Text>
//           </View>
//         )}
//       </View>
//       <ConnectedAccountComponent
//         isVisible={isConnectModalVisible}
//         onClose={closeConnectModal}
//       />

//     </ScrollView>
//   );
// };

// // React.memo를 사용하여 불필요한 리렌더링 방지
// export default withTheme(HomeComponent);
