// 차트 데이터 인터페이스
export interface ChartData {
  name: string;
  value: number;
  ratio: number;
  color: string;
  valueUSD?: number;
  krwValue: number;
  currency: 'KRW' | 'USD';
  isForeign: boolean;
  amount: string;
  originalAmount?: string;
}

// 차트 색상 인터페이스
export interface ChartColors {
  primary: string;
  secondary: string[];
  cash: {
    krw: string;
    usd: string;
  };
}

// 차트 색상 가져오기 함수
export const getChartColor = (colors: ChartColors, index: number, name?: string): string => {
  if (name === '원화 현금 (예수금)') return colors.cash.krw;
  if (name === '달러 현금 (USD)') return colors.cash.usd;
  if (index === 0) return colors.primary;
  const secondaryIndex = (index - 1) % colors.secondary.length;
  return colors.secondary[secondaryIndex];
}; 