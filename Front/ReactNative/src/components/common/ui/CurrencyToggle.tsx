import React from 'react';
import { View, TouchableOpacity, Text, StyleSheet } from 'react-native';
import { Theme } from '../../../types/theme';

interface CurrencyToggleProps {
  theme: Theme;
  currencyType: 'won' | 'dollar';
  onCurrencyChange: (type: 'won' | 'dollar') => void;
}

const CurrencyToggle: React.FC<CurrencyToggleProps> = ({
  theme,
  currencyType,
  onCurrencyChange
}) => {
  return (
    <View style={styles.currencyToggleContainer}>
      <TouchableOpacity
        style={[
          styles.currencyButton,
          currencyType === 'dollar' ? [styles.activeCurrency, { backgroundColor: theme.colors.primary }] : null
        ]}
        onPress={() => onCurrencyChange('dollar')}
      >
        <Text style={[
          styles.currencyText,
          currencyType === 'dollar' ? styles.activeCurrencyText : { color: theme.colors.text }
        ]}>$</Text>
      </TouchableOpacity>
      <TouchableOpacity
        style={[
          styles.currencyButton,
          currencyType === 'won' ? [styles.activeCurrency, { backgroundColor: theme.colors.primary }] : null
        ]}
        onPress={() => onCurrencyChange('won')}
      >
        <Text style={[
          styles.currencyText,
          currencyType === 'won' ? styles.activeCurrencyText : { color: theme.colors.text }
        ]}>원</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  currencyToggleContainer: {
    flexDirection: 'row',
    backgroundColor: '#F0F0F0',
    borderRadius: 8,
    padding: 2,
  },
  currencyButton: {
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 6,
  },
  activeCurrency: {
    backgroundColor: '#365BC5',
  },
  currencyText: {
    fontSize: 14,
    fontWeight: '600',
  },
  activeCurrencyText: {
    color: '#FFFFFF',
  },
});

export default CurrencyToggle; 