// 파일 경로: src/components/IndividualStockComponent.tsx
// 컴포넌트 흐름: App.js > AppNavigator.js > MainPage.jsx > MyStockAccountComponent.jsx > IndividualStockComponent.tsx

import React from 'react';
import { View, Text } from 'react-native';

// HOC 임포트
import withTheme from '../../hoc/withTheme';
import createStyles from '../../styles/components/individualStockComponent.styles';

// 공통 Theme 타입
import { Theme } from '../../types/theme';

// 주식 데이터 인터페이스 정의
interface Stock {
  color: string;
  name: string;
  value: number;
  ratio: number;
}

// 컴포넌트 props 인터페이스 정의
interface IndividualStockComponentProps {
  stock: Stock;
  theme: Theme;
}

// React.memo를 사용하여 불필요한 리렌더링 방지
const IndividualStockComponent: React.FC<IndividualStockComponentProps> = React.memo(({ stock, theme }) => {
  const styles = createStyles(theme);
  
  return (
    <View style={styles.container}>
      <View style={[styles.colorIndicator, { backgroundColor: stock.color }]} />
      <View style={styles.stockInfo}>
        <Text style={styles.stockName}>{stock.name}</Text>
        <Text style={styles.stockValue}>{stock.value.toLocaleString()}원</Text>
      </View>
      <Text style={styles.stockRatio}>{stock.ratio}%</Text>
    </View>
  );
});

// 디버깅을 위한 displayName 설정
IndividualStockComponent.displayName = 'IndividualStockComponent';

// withTheme HOC로 감싸서 내보내기
export default withTheme(IndividualStockComponent);
