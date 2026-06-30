import os
import sys
import subprocess
import threading
import argparse
import time

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

    logger_thread = threading.Thread(target=log_stream, args=(process.stdout, prefix))
    logger_thread.daemon = True
    logger_thread.start()

    return process, logger_thread

def main():
    parser = argparse.ArgumentParser(description="링커리어 합격자소서 스크래핑 & 키워드 분석 파이프라인")
    parser.add_argument("--max-pages", type=int, default=50, help="기업당 최대 검색 페이지 (기본값 50)")
    parser.add_argument("--headless", action="store_true", default=False, help="Selenium 헤드리스 실행 (기본값: False, 브라우저 창 표시)")
    parser.add_argument("--no-headless", dest="headless", action="store_false", help="Selenium GUI 실행 (기본값)")
    args = parser.parse_args()

    print("=================================================================")
    print("         링커리어 합격자소서 스크래핑 & 키워드 분석 파이프라인")
    print("=================================================================\n")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    lk_script = os.path.join(base_dir, "linked_scraper.py")

    lk_cmd = [
        sys.executable, "-u", lk_script,
        "--max-pages", str(args.max_pages)
    ]
    if args.headless:
        lk_cmd.append("--headless")

    start_time = time.time()

    # 1. 링커리어 스크래퍼 실행
    lk_process, lk_thread = run_scraper_process(lk_cmd, "Linkareer")

    print("\n⏳ 링커리어 스크래퍼 실행 중...\n")

    try:
        while lk_process.poll() is None:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n⚠️ 사용자에 의해 파이프라인이 중단되었습니다.")
        lk_process.terminate()
        return

    print("\n=================================================================")
    print(f"📊 스크래핑 완료 (종료 코드: {lk_process.returncode})")
    print("=================================================================\n")

    # 2. 키워드 분석 실행
    print("📝 수집된 합격자소서를 바탕으로 키워드 분석을 시작합니다...\n")

    try:
        from keyword_extraction import KeywordExtractor

        extractor = KeywordExtractor()
        extractor.analyze_data()

        print("\n✅ 키워드 분석 완료!")
        print(f"📁 결과물:")
        print(f"   [자소서 초안용] 직무분야별 키워드 60개 + 추천회사 Top10")
        print(f"   - {os.path.join(base_dir, 'data', 'job_keywords_analysis.csv')}")
        print(f"   - {os.path.join(base_dir, 'data', 'job_keywords_analysis.json')}")
        print(f"   [특정기업 자소서용] 직무명별 × 질문카테고리별 키워드 20개 + 추출회사명")
        print(f"   - {os.path.join(base_dir, 'data', 'job_keywords_by_position.csv')}")
        print(f"   - {os.path.join(base_dir, 'data', 'job_keywords_by_position.json')}")

    except Exception as e:
        print(f"❌ 키워드 분석 오류: {e}")

    duration = time.time() - start_time
    print(f"\n🎉 전체 파이프라인 완료! 총 소요 시간: {duration:.2f}초")

if __name__ == "__main__":
    main()
