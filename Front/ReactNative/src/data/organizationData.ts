// 경로: src/data/organizationData.ts

/**
 * 금융 기관 정보 인터페이스
 */
export interface FinancialOrganization {
    code: string;       // 기관코드
    name: string;       // 기관명
    shortName?: string; // 축약명 (선택적)
  }
  
  /**
   * 증권사 기관코드 목록
   */
  export const SECURITIES_FIRMS: FinancialOrganization[] = [
    { code: '0209', name: '유안타증권' },
    { code: '0218', name: 'KB증권' },
    { code: '0221', name: '골든브릿지투자증권' },
    { code: '0222', name: '한양증권' },
    { code: '0223', name: '리딩투자증권' },
    { code: '0024', name: 'BNK투자증권' },
    { code: '0225', name: 'IBK투자증권' },
    { code: '0227', name: '다올투자증권', shortName: '다올투자' }, // 구 KTB투자증권
    { code: '0238', name: '미래에셋증권', shortName: '미래에셋' }, // 구 미래에셋대우증권
    { code: '0240', name: '삼성증권' },
    { code: '0243', name: '한국투자증권', shortName: '한투' },
    { code: '0247', name: 'NH투자증권', shortName: 'NH투자' },
    { code: '1247', name: 'NH투자증권 모바일증권 나무', shortName: 'NH나무' },
    { code: '0261', name: '교보증권' },
    { code: '0262', name: '하이투자증권' },
    { code: '0263', name: 'HMC투자증권' },
    { code: '0264', name: '키움증권' },
    { code: '0265', name: '이베스트투자증권' },
    { code: '0266', name: 'SK증권' },
    { code: '0267', name: '대신증권' },
    { code: '1267', name: '대신증권 크레온', shortName: '크레온' },
    { code: '0269', name: '한화투자증권' },
    { code: '0270', name: '하나증권', shortName: '하나금투' }, // 구 하나금융투자
    { code: '0278', name: '신한금융투자', shortName: '신한투자' },
    { code: '0279', name: 'DB금융투자' },
    { code: '0280', name: '유진투자증권' },
    { code: '0287', name: '메리츠증권' },
    { code: '0290', name: '부국증권' },
    { code: '0291', name: '신영증권' },
    { code: '0292', name: '케이프투자증권' },
    { code: '0294', name: '한국포스증권' },
    { code: '0295', name: '우리종합금융' }
  ];
  
  /**
   * 코드로 증권사 찾기
   * @param code 찾을 증권사 코드
   * @returns 찾은 증권사 정보 또는 undefined
   */
  export const findSecuritiesFirmByCode = (code: string): FinancialOrganization | undefined => {
    return SECURITIES_FIRMS.find(firm => firm.code === code);
  };
  
  /**
   * 이름으로 증권사 찾기
   * @param name 찾을 증권사 이름
   * @returns 찾은 증권사 정보 또는 undefined
   */
  export const findSecuritiesFirmByName = (name: string): FinancialOrganization | undefined => {
    return SECURITIES_FIRMS.find(firm => 
      firm.name.includes(name) || 
      (firm.shortName && firm.shortName.includes(name))
    );
  };
  
  /**
   * 증권사 코드 목록 반환
   * @returns 모든 증권사 코드 배열
   */
  export const getAllSecuritiesFirmCodes = (): string[] => {
    return SECURITIES_FIRMS.map(firm => firm.code);
  };
  
  /**
   * 증권사 이름 목록 반환
   * @returns 모든 증권사 이름 배열
   */
  export const getAllSecuritiesFirmNames = (): string[] => {
    return SECURITIES_FIRMS.map(firm => firm.name);
  };
  
  export default SECURITIES_FIRMS;
  