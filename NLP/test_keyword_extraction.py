import os
import pandas as pd
import json
from keyword_extraction import KeywordExtractor

def run_tests():
    print("=== [키워드 추출 파이프라인 검증 시작] ===")
    
    # 1. 파일 경로 설정
    base_dir = os.path.dirname(os.path.abspath(__file__))
    company_json_path = os.path.join(base_dir, 'data', 'companies.json')

    # 2. 기업 데이터셋 무결성 검증
    print("\n[검증 1] 기업 데이터셋 정합성 확인")
    assert os.path.exists(company_json_path), f"오류: {company_json_path} 파일이 존재하지 않습니다."

    with open(company_json_path, 'r', encoding='utf-8') as f:
        companies_data = json.load(f)

    total_companies = len(companies_data)
    for co in companies_data:
        assert 'name' in co, "오류: 기업 데이터에 'name' 필드가 누락되었습니다."
        assert 'vision' in co, "오류: 기업 데이터에 'vision' 필드가 누락되었습니다."
        assert 'core_values' in co, f"오류: {co.get('name')} 기업 데이터에 'core_values' 필드가 누락되었습니다."
        assert len(co['core_values']) >= 5, f"오류: {co['name']}의 인재상 키워드 개수가 너무 적습니다. (현재: {len(co['core_values'])}개)"

    print(f"  => 총 기업 수: {total_companies}개")
    print("  => [합격] 기업 데이터 및 인재상 키워드 검증 완수!")

    # 3. 키워드 추출 파이프라인 실행
    print("\n[검증 2] KeywordExtractor 인스턴스화 및 분석 실행")
    extractor = KeywordExtractor()
    assert not extractor.df.empty, "오류: 합격자소서 데이터프레임이 비어 있습니다."
    
    # 파이프라인 작동
    print("  => 분석 실행 중... (시간이 수 초 소요될 수 있습니다)")
    result_df = extractor.analyze_by_job_and_talent()
    
    assert result_df is not None and not result_df.empty, "오류: 분석 결과 데이터프레임이 비어 있습니다."
    print(f"  => [합격] 성공적으로 {len(result_df)}개 직무에 대한 키워드 추출 완료!")
    
    # 4. 출력 결과 파일 구조 및 형식 검증
    print("\n[검증 3] 결과 출력 파일 규격 검사")
    output_csv = os.path.join(base_dir, 'data', 'job_keywords_analysis.csv')
    output_json = os.path.join(base_dir, 'data', 'job_keywords_analysis.json')
    
    assert os.path.exists(output_csv), f"오류: CSV 파일이 생성되지 않았습니다: {output_csv}"
    assert os.path.exists(output_json), f"오류: JSON 파일이 생성되지 않았습니다: {output_json}"
    
    # CSV 로드 테스트
    loaded_df = pd.read_csv(output_csv)
    expected_cols = ['직무', '자소서_개수', '실무_키워드_15', '인재상_키워드_10', '추천_대기업_Top3', '통합_키워드_25']
    for col in expected_cols:
        assert col in loaded_df.columns, f"오류: 결과 CSV 파일에 {col} 컬럼이 없습니다."
        
    print("  => CSV 형식 및 컬럼 규격 완벽 일치 확인!")
    
    # JSON 로드 테스트
    with open(output_json, 'r', encoding='utf-8') as f:
        loaded_json = json.load(f)
        
    assert len(loaded_json) == len(loaded_df), "오류: JSON과 CSV의 행 수가 다릅니다."
    first_job = list(loaded_json.keys())[0]
    for col in expected_cols[1:]:
        assert col in loaded_json[first_job], f"오류: 결과 JSON의 직무 세부항목에 {col} 키가 누락되었습니다."
        
    print("  => JSON 형식 및 컬럼 구조 일치 확인!")
    print("  => [합격] 출력 파일(CSV/JSON) 검증 완수!")
    
    # 5. 상위 5개 직무 키워드 및 추천 기업 결과 시각화
    print("\n=== [상위 5개 주요 직무 키워드 추출 결과 확인] ===")
    top_5_jobs = loaded_df.sort_values(by='자소서_개수', ascending=False).head(5)
    
    for idx, row in top_5_jobs.iterrows():
        print("-" * 70)
        print(f"📌 직무명: {row['직무']} ({row['자소서_개수']}개 자소서 분석)")
        print(f"🚀 실무 키워드 (Top 15):")
        print(f"   {row['실무_키워드_15']}")
        print(f"💡 대기업 인재상 키워드 (Top 10):")
        print(f"   {row['인재상_키워드_10']}")
        print(f"🏢 추천/부합 대기업 (Top 3):")
        print(f"   {row['추천_대기업_Top3']}")
        print("-" * 70)
        
    print("\n=== [모든 검증 완료: 전체 성공!] ===")

if __name__ == "__main__":
    run_tests()
