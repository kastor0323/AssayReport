import json
from resume_evaluator import ResumeEvaluator

def run_test():
    # 평가기 초기화
    evaluator = ResumeEvaluator()
    
    # 테스트용 사용자 데이터
    test_user_data = {
        "회사명": "삼성전자",
        "직무": "IT·기술영업",
        "직위": "신입",
        "qa_pairs": [
            {
                "question": "지원동기와 입사 후 포부에 대해 기술해주십시오.",
                "answer": "회사를 선택하는 데 있어서 가장 중요한 기준은, 좋은 동료들과 함께 노력한 결과가 실제 사람들에게 도움이 될 수 있는가입니다. 개발자로서의 꿈이자 목표는 스스로 유명해지거나 돈을 많이 버는 것이 아닙니다. 만든 프로그램으로 인해 시간을 절약하고 편리한 삶을 누리는 것을 지켜본다면 만족하며, 이를 원동력 삼아 새로운 개발에 몰입할 것입니다. DA 사업부는 실생활에 밀접한 가전을 개발해오고 있으며, BESPOKE 브랜드를 통하여 개인화된 디자인을 제공하고 제품군 별로 다양한 편의 기능을 제공함으로써 가전 시장을 선도하고 있습니다. 또한 SmartThings를 통해 사용자들에게 편리한 삶을 제공해오고 있으며, 저 스스로도 그랑데 AI 제품을 통해 그 편리함과 중요성을 느끼고 있습니다. 현직자 선배님들과의 멘토링과 기업탐방, 리서치 연계 프로젝트에 참여함으로써 삼성전자의 인제일 정책에 대해 실감하였고, 지향하는 개발의 가치를 잘 실현할 수 있는 환경이라 확신하였으며, 함께 고객의 편리한 삶 경험을 위해 발전시켜나가고 싶어 지원하였습니다. 입사 후 더 편리한 SmartThings/HCA 사용에 기여하여 만족스러운 경험으로 인한 락인 효과를 이끌고 싶으며, Expert 등급을 취득하여 향상된 알고리즘 능력으로 최적화에 기여하고 싶습니다. 향후 기회가 된다면 SSAFY 멘토링 프로그램에 멘토로써 SW 생태계 순환에 도움을 주고 싶습니다."
            }
        ]
    }
    
    print("\n=== [자소서 평가 시뮬레이션 시작] ===")
    print(f"지원 회사: {test_user_data['회사명']}")
    print(f"지원 직무: {test_user_data['직무']} ({test_user_data['직위']})")
    
    # 평가 실행
    result = evaluator.evaluate_resume(test_user_data)
    
    if result:
        print("\n--- [평가 결과 요약] ---")
        print(f"평균 점수: {result['평균점수']}점")
        print(f"최종 등급: {result['등급']}")
        print(f"산업 분야: {result['산업분야']}")
        
        print("\n--- [상세 문항 평가] ---")
        for detail in result['상세결과']:
            print(f"문항 {detail['질문번호']}: {detail['사용자질문']}")
            print(f"  - 매칭된 합격 키워드: {detail['매칭된합격키워드']}")
            print(f"  - 매칭된 비전 키워드: {detail['매칭된비전키워드']}")
            print(f"  - 합격키워드 점수: {detail['합격키워드점수']}")
            print(f"  - 비전정합성 점수: {detail['비전정합성점수']}")
            print(f"  - 문항 종합 점수: {detail['문항종합점수']}")
    else:
        print("평가 결과 생성 실패")

if __name__ == "__main__":
    run_test()
