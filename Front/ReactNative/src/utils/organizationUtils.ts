import { findSecuritiesFirmByName } from '../data/organizationData';

export const getOrganizationCode = (companyName: string): string => {
  const firm = findSecuritiesFirmByName(companyName);
  if (firm) {
    console.log(`증권사 ${companyName} -> 코드 ${firm.code} 변환 성공`);
    return firm.code;
  } else {
    console.warn(`증권사 코드를 찾을 수 없음: ${companyName}`);
    // 기본 코드 반환 (삼성증권)
    return '0240';
  }
};

export const getShortCompanyName = (companyName: string): string => {
  if (companyName.includes('증권')) {
    return companyName.split('증권')[0];
  }
  return companyName.substring(0, 2);
}; 