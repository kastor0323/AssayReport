import os
import sys
import subprocess
import threading
import argparse
import pandas as pd
import time
import getpass

# Windows에서 venv 실행 시 stdout 인코딩이 cp949로 설정되는 문제 해결
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def log_stream(stream, prefix):
    """실시간으로 프로세스의 출력을 콘솔에 로깅합니다."""
    try:
        for line in iter(stream.readline, ''):
            if line:
                sys.stdout.write(f"[{prefix}] {line}")
                sys.stdout.flush()
    except Exception as e:
        sys.stdout.write(f"[{prefix}] 로깅 에러: {e}\n")
        sys.stdout.flush()

def run_scraper_process(cmd, prefix):
    """자식 프로세스를 실행하고 출력을 로깅 스레드로 연결합니다."""
    print(f"\n🚀 {prefix} 프로세스 시작: {' '.join(cmd)}")
    
    # PYTHONUTF8=1로 자식 프로세스도 UTF-8로 출력하게 강제합니다.
    child_env = {**os.environ, 'PYTHONUTF8': '1'}
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf-8',
        errors='replace',
        bufsize=1,
        env=child_env
    )
    
    # 실시간 로깅을 위한 데몬 스레드 시작
    logger_thread = threading.Thread(target=log_stream, args=(process.stdout, prefix))
    logger_thread.daemon = True
    logger_thread.start()
    
    return process, logger_thread

def main():
    parser = argparse.ArgumentParser(description="잡코리아 & 링커리어 병렬 합격자소서 스크래핑 & 키워드 분석 파이프라인")
    parser.add_argument("--id", help="잡코리아 아이디")
    parser.add_argument("--password", help="잡코리아 비밀번호")
    parser.add_argument("--jk-start", type=int, default=1, help="잡코리아 시작 페이지")
    parser.add_argument("--jk-end", type=int, default=2, help="잡코리아 끝 페이지")
    parser.add_argument("--lk-start", type=int, default=1, help="링커리어 시작 페이지")
    parser.add_argument("--lk-end", type=int, default=2, help="링커리어 끝 페이지")
    parser.add_argument("--headless", action="store_true", default=True, help="링커리어 Selenium 브라우저 헤드리스 실행 여부 (기본값: True)")
    parser.add_argument("--no-headless", dest="headless", action="store_false", help="링커리어 Selenium 브라우저 GUI 실행")
    
    args = parser.parse_args()
    
    print("=================================================================")
    print("      잡코리아 & 링커리어 합격자소서 병렬 스크래핑 파이프라인")
    print("=================================================================\n")
    
    user_id = args.id
    password = args.password
    
    # 잡코리아 ID/PW 확인 및 대화형 입력 처리
    if not user_id:
        user_id = input("🔑 잡코리아 아이디 입력: ").strip()
    if not password:
        password = getpass.getpass("🔑 잡코리아 비밀번호 입력: ").strip()
        
    if not user_id or not password:
        print("❌ 잡코리아 로그인 아이디와 비밀번호가 필요합니다. 종료합니다.")
        return
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 스크래퍼 스크립트 경로 설정
    jk_script = os.path.join(base_dir, "jobkorea_scraper.py")
    lk_script = os.path.join(base_dir, "linked_scraper.py")
    
    # 실행 명령어 빌드 (동일한 Python 인터프리터 사용, 실시간 병렬 출력을 위해 -u 플래그 사용)
    jk_cmd = [
        sys.executable, "-u", jk_script,
        "--id", user_id,
        "--password", password,
        "--start", str(args.jk_start),
        "--end", str(args.jk_end)
    ]
    
    lk_cmd = [
        sys.executable, "-u", lk_script,
        "--start", str(args.lk_start),
        "--end", str(args.lk_end)
    ]
    if args.headless:
        lk_cmd.append("--headless")
        
    start_time = time.time()
    
    # 1. 두 스크래퍼 병렬 실행 (서로 다른 프로세스/메모리 영역)
    jk_process, jk_thread = run_scraper_process(jk_cmd, "JobKorea")
    lk_process, lk_thread = run_scraper_process(lk_cmd, "Linkareer")
    
    print("\n⏳ 두 스크래퍼가 백그라운드에서 실행 중입니다. 실시간 로깅을 모니터링합니다...\n")
    
    # 프로세스 종료 대기
    try:
        while True:
            jk_poll = jk_process.poll()
            lk_poll = lk_process.poll()
            
            if jk_poll is not None and lk_poll is not None:
                break
                
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n⚠️ 사용자에 의해 파이프라인이 중단되었습니다. 하위 프로세스를 강제 종료합니다.")
        jk_process.terminate()
        lk_process.terminate()
        return
        
    # 종료 코드 확인
    print("\n=================================================================")
    print(f"📊 스크래핑 프로세스 완료 (JobKorea: {jk_process.returncode}, Linkareer: {lk_process.returncode})")
    print("=================================================================\n")
    
    # 2. 키워드 분석 프로세스 실행
    print("📝 수집된 합격자소서를 바탕으로 키워드 및 비전 매칭 분석을 시작합니다...\n")
    
    try:
        # keyword_extraction 모듈의 KeywordExtractor 임포트 및 실행
        from keyword_extraction import KeywordExtractor
        
        extractor = KeywordExtractor()
        # analyze_jobkorea_data() 내부에서 analyze_by_job_and_talent()가 호출되며 JSON 파일이 저장됩니다.
        extractor.analyze_jobkorea_data()
        
        print("\n✅ 키워드 분석 및 매칭 프로세스 완료!")
        
        output_csv = os.path.join(base_dir, "data", "job_keywords_analysis.csv")
        output_json = os.path.join(base_dir, "data", "job_keywords_analysis.json")
        
        print(f"📁 결과물 경로:")
        print(f"   - CSV 결과: {output_csv}")
        print(f"   - JSON 결과: {output_json}")
        
    except Exception as e:
        print(f"❌ 키워드 분석 과정에서 오류가 발생했습니다: {e}")
        
    end_time = time.time()
    duration = end_time - start_time
    print(f"\n🎉 전체 파이프라인 완료! 총 소요 시간: {duration:.2f}초")

if __name__ == "__main__":
    main()
