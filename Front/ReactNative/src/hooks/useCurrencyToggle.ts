import { useState } from 'react';

export type CurrencyType = 'KRW' | 'USD';

interface CurrencyToggleResult {
  currencyType: CurrencyType;
  exchangeRate: number;
  handleCurrencyChange: (type: CurrencyType) => void;
  formatCurrency: (value: number) => string;
  convertCurrency: (value: number, fromCurrency: CurrencyType, toCurrency: CurrencyType) => number;
}

export const useCurrencyToggle = (initialRate: number = 1350): CurrencyToggleResult => {
  const [currencyType, setCurrencyType] = useState<CurrencyType>('KRW');
  const exchangeRate = initialRate;

  const handleCurrencyChange = (type: CurrencyType) => {
    setCurrencyType(type);
  };

  const formatCurrency = (value: number): string => {
    if (currencyType === 'USD') {
      return `$${(value / exchangeRate).toFixed(2)}`;
    }
    return `${value.toLocaleString()}원`;
  };

  const convertCurrency = (
    value: number,
    fromCurrency: CurrencyType,
    toCurrency: CurrencyType
  ): number => {
    if (fromCurrency === toCurrency) return value;
    if (fromCurrency === 'USD' && toCurrency === 'KRW') {
      return value * exchangeRate;
    }
    return value / exchangeRate;
  };

  return {
    currencyType,
    exchangeRate,
    handleCurrencyChange,
    formatCurrency,
    convertCurrency
  };
}; 