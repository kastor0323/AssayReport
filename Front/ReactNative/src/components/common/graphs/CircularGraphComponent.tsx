// 파일 경로: src/components/common/graphs/CircularGraphComponent.tsx
// 컴포넌트 흐름: App.js > AppNavigator.js > MainPage.jsx > MyStockAccountComponent.jsx > CircularGraphComponent.tsx

import React from 'react';
import { View, Dimensions } from 'react-native';
import { PieChart } from 'react-native-chart-kit';

// 스타일 임포트
import withTheme from '../../../hoc/withTheme';
import createStyles from '../../../styles/components/circularGraphComponent.styles';

// 전역 Theme 타입 가져오기
import { Theme } from '../../../types/theme'; 

// 데이터 아이템 인터페이스 정의
interface DataItem {
  name: string;
  value: number;
  color: string;
}

// 차트 데이터 아이템 인터페이스 정의
interface ChartDataItem extends DataItem {
  legendFontColor: string;
  legendFontSize: number;
}

// 컴포넌트 props 인터페이스 정의
interface CircularGraphComponentProps {
  data: DataItem[];
  theme: Theme; // 공통 Theme 타입 사용
}

const CircularGraphComponent: React.FC<CircularGraphComponentProps> = ({ data, theme }) => {
  const styles = createStyles(theme);

  const chartData: ChartDataItem[] = data.map(item => ({
    name: item.name,
    value: item.value,
    color: item.color,
    legendFontColor: theme.colors.text,
    legendFontSize: 12,
  }));

  const chartConfig = {
    color: (opacity: number = 1) => `rgba(0, 0, 0, ${opacity})`,
  };
  
  const screenWidth: number = Dimensions.get('window').width;

  return (
    <View style={styles.container}>
      <View style={styles.chartContainer}>
        <PieChart
          data={chartData}
          width={Dimensions.get('window').width * 0.85}
          height={250}
          chartConfig={chartConfig}
          accessor="value"
          backgroundColor="transparent"
          paddingLeft="0"
          absolute={false}
          hasLegend={false}
          center={[Dimensions.get('window').width * 0.215, 0]}
          avoidFalseZero
        />
      </View>
    </View>
  );
};

// 디버깅을 위한 displayName 설정
CircularGraphComponent.displayName = 'IndividualStockComponent';

// HOC로 감싸서 내보내기
export default withTheme(CircularGraphComponent);
