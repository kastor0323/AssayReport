import { Theme } from './theme';

// 계좌 관련 타입
export interface AccountInfo {
  company: string;
  accountNumber: string;
  returnRate?: number;
}

export interface ApiAccountInfo extends AccountInfo {
  returnRate: number;
}

export interface AccountDetailInfo {
  company: string;
  accountNumber: string;
  name: string;
  number: string;
  principal: number;
  valuation: number;
  dailyProfit: number;
  dailyProfitPercent: number;
  totalProfit: number;
  totalProfitPercent: number;
}

export interface ConnectedAccount {
  accountNumber: string;
  connectedId: string;
}

// 주식 데이터 타입
export interface BaseStockItem {
  name: string;
  price: string;
  amount: string;
  quantity: string;
  availableQuantity: string;
  isForeign: boolean;
  currency: 'KRW' | 'USD';
  originalPrice?: string;
  originalAmount?: string;
}

export interface StockData extends BaseStockItem {
  value?: number;
  krwValue?: number;
}

export interface RebalancingStockItem extends BaseStockItem {
  ticker: string;
  percentChange: number;
  targetPortion: number;
  rebalanceAmount: number;
  market_order?: number;
}

// 현금 아이템 타입
export interface CashItem {
  name: string;
  value: number;
  krwValue: number;
  targetPortion: number;
  rebalanceAmount: number;
}

// 잔고 정보 타입
export interface BalanceInfo {
  accountNumber: string;
  accountName: string;
  totalAmount: string;
  balance: string;
  stocks: BaseStockItem[];
  usdBalance?: string;
}

// 차트 데이터 타입
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

// 차트 색상 타입
export interface ChartColors {
  primary: string;
  secondary: string[];
  cash: {
    krw: string;
    usd: string;
  };
}

// API 요청 파라미터 타입
export interface BalanceRequestParams {
  connectedId: string;
  organization: string;
  account: string;
  account_password: string;
}

// 계좌 비밀번호 관련 타입
export interface SavedAccountInfo {
  account: string;
  account_password: string;
  connectedId: string;
  organization: string;
}

export interface AccountPasswordParams {
  accountNumber: string;
  organization: string;
}

// 컴포넌트 props 타입
export interface StockChartProps {
  theme: Theme;
  data: ChartData[];
}

export interface CircularGraphProps {
  data: ChartData[];
}

export interface MyStockAccountProps {
  theme: Theme;
} 

export type { Theme };
