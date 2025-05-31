import AsyncStorage from '@react-native-async-storage/async-storage';
import { useState, useCallback } from 'react';

// 암호화된 저장소를 위한 훅
// 참고: 실제 암호화를 위해서는 react-native-encrypted-storage 라이브러리 설치 필요
export const useSecureStore = <T>(storageKey: string, initialValue: T) => {
  const [storedValue, setStoredValue] = useState<T>(initialValue);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  // 값 로드
  const loadValue = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      // AsyncStorage에서 데이터 가져오기
      const item = await AsyncStorage.getItem(storageKey);
      
      // 값이 존재하면 파싱하여 상태 업데이트
      if (item !== null) {
        setStoredValue(JSON.parse(item));
      }
    } catch (e) {
      setError(e instanceof Error ? e : new Error('알 수 없는 오류가 발생했습니다'));
      console.error(`${storageKey} 로드 오류:`, e);
    } finally {
      setLoading(false);
    }
  }, [storageKey]);

  // 값 저장
  const saveValue = useCallback(async (value: T) => {
    try {
      setLoading(true);
      setError(null);
      // 값을 JSON 문자열로 변환하여 저장
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      await AsyncStorage.setItem(storageKey, JSON.stringify(valueToStore));
      return true;
    } catch (e) {
      setError(e instanceof Error ? e : new Error('알 수 없는 오류가 발생했습니다'));
      console.error(`${storageKey} 저장 오류:`, e);
      return false;
    } finally {
      setLoading(false);
    }
  }, [storageKey, storedValue]);

  // 값 삭제
  const removeValue = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      await AsyncStorage.removeItem(storageKey);
      setStoredValue(initialValue);
      return true;
    } catch (e) {
      setError(e instanceof Error ? e : new Error('알 수 없는 오류가 발생했습니다'));
      console.error(`${storageKey} 삭제 오류:`, e);
      return false;
    } finally {
      setLoading(false);
    }
  }, [storageKey, initialValue]);

  return { 
    value: storedValue, 
    loading, 
    error, 
    loadValue, 
    saveValue, 
    removeValue 
  };
}; 