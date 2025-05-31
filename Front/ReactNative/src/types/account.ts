// 계좌 기본 정보 인터페이스
export interface AccountInfo {
  company: string;
  accountNumber: string;
  returnRate: number;
}

// API에서 가져오는 계좌 정보 인터페이스
export interface ApiAccountInfo extends AccountInfo {
  returnRate: number;
}

// 계좌 상세 정보 인터페이스
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

// 기본 주식 데이터 인터페이스
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
  value?: number;
  krwValue?: number;
}

// 리밸런싱용 주식 데이터 인터페이스
export interface RebalancingStockItem extends BaseStockItem {
  ticker: string;
  percentChange: number;
  targetPortion: number;
  rebalanceAmount: number;
  market_order?: number;
}

// 차트용 주식 데이터 인터페이스
export interface ChartStockItem extends BaseStockItem {
  ratio: number;
  color: string;
  valueUSD?: number;
}

// 잔고 정보 인터페이스
export interface BalanceInfo {
  accountNumber: string;
  accountName: string;
  totalAmount: string;
  balance: string;
  stocks: BaseStockItem[];
  usdBalance?: string;
}

// 계좌 비밀번호 저장 정보
export interface SavedAccountInfo {
  account: string;
  account_password: string;
  organization: string;
  connectedId: string;
}

// 계좌 비밀번호 파라미터
export interface AccountPasswordParams {
  accountNumber: string;
  organization: string;
}

// 차트 색상 유틸리티 타입
export interface ChartColors {
  primary: string;
  secondary: string[];
  cash: {
    krw: string;
    usd: string;
  };
}

export interface ConnectedAccount {
  accountNumber: string;
  connectedId: string;
} 