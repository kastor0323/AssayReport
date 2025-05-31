// 참고: 실제 앱에서는 react-native-encrypted-storage, expo-secure-store 등 보안 라이브러리를 사용해야 합니다.
// 이 코드는 간단한 마스킹 처리 예시입니다.

/**
 * 계좌 비밀번호와 같은 민감한 정보를 마스킹 처리
 * @param text 원본 텍스트
 * @param visibleChars 보여줄 글자 수 (기본값: 2)
 * @returns 마스킹된 텍스트
 */
export const maskSensitiveInfo = (text: string, visibleChars: number = 2): string => {
  if (!text) return '';
  
  // 텍스트가 visibleChars보다 짧으면 전체 마스킹
  if (text.length <= visibleChars) {
    return '*'.repeat(text.length);
  }
  
  // 앞의 visibleChars 글자만 표시하고 나머지는 *로 마스킹
  const visible = text.substring(0, visibleChars);
  const masked = '*'.repeat(text.length - visibleChars);
  
  return visible + masked;
};

/**
 * 계좌번호 마스킹 처리 (중간 부분을 *로 변경)
 * @param accountNumber 계좌번호
 * @returns 마스킹된 계좌번호
 */
export const maskAccountNumber = (accountNumber: string): string => {
  if (!accountNumber) return '';
  
  // 계좌번호 길이에 따라 다르게 처리
  if (accountNumber.length <= 4) {
    return accountNumber; // 너무 짧으면 그대로 반환
  }
  
  // 앞 2자리와 뒤 4자리만 보이게 마스킹
  const prefix = accountNumber.substring(0, 2);
  const suffix = accountNumber.substring(accountNumber.length - 4);
  const maskedLength = accountNumber.length - 6;
  const masked = '*'.repeat(maskedLength > 0 ? maskedLength : 0);
  
  return `${prefix}${masked}${suffix}`;
};

/**
 * 저장용 계좌 정보 마스킹 처리
 * 화면에 표시하기 위한 용도로 비밀번호를 마스킹 처리하며
 * 실제 저장은 암호화된 형태로 해야 합니다.
 */
export const maskAccountInfoForDisplay = (accountInfo: any) => {
  if (!accountInfo) return null;
  
  return {
    ...accountInfo,
    account: maskAccountNumber(accountInfo.account),
    account_password: accountInfo.account_password ? '******' : '',
  };
};

/**
 * 마스킹된 계좌 목록 생성
 * 화면에 표시하기 위한 용도
 */
export const getMaskedAccountList = (accounts: any[]): any[] => {
  if (!accounts || !Array.isArray(accounts)) return [];
  
  return accounts.map(account => maskAccountInfoForDisplay(account));
}; 