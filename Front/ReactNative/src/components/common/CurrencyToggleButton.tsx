import React from 'react';
import { View, TouchableOpacity, Text, StyleSheet } from 'react-native';
import { Theme } from '../../types/theme';
import { CurrencyType } from '../../hooks/useCurrencyToggle';

interface CurrencyToggleButtonProps {
  theme: Theme;
  currencyType: CurrencyType;
  onCurrencyChange: (type: CurrencyType) => void;
}

export const CurrencyToggleButton: React.FC<CurrencyToggleButtonProps> = ({
  theme,
  currencyType,
  onCurrencyChange
}) => {
  return (
    <View style={styles.container}>
      <TouchableOpacity
        style={[
          styles.button,
          currencyType === 'KRW' ? { backgroundColor: theme.colors.primary } : null
        ]}
        onPress={() => onCurrencyChange('KRW')}
      >
        <Text style={[
          styles.text,
          currencyType === 'KRW' ? { color: 'white' } : { color: theme.colors.text }
        ]}>
          원화 (₩)
        </Text>
      </TouchableOpacity>
      
      <TouchableOpacity
        style={[
          styles.button,
          currencyType === 'USD' ? { backgroundColor: theme.colors.primary } : null
        ]}
        onPress={() => onCurrencyChange('USD')}
      >
        <Text style={[
          styles.text,
          currencyType === 'USD' ? { color: 'white' } : { color: theme.colors.text }
        ]}>
          달러 ($)
        </Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    borderRadius: 8,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: '#E5E5E5',
  },
  button: {
    paddingVertical: 8,
    paddingHorizontal: 16,
    justifyContent: 'center',
    alignItems: 'center',
  },
  text: {
    fontSize: 14,
    fontWeight: '500',
  }
}); 