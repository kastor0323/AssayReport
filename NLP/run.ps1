# NLP 디렉토리 기준으로 실행
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# 가상환경 활성화
$venvActivate = Join-Path $scriptDir ".venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    & $venvActivate
} else {
    Write-Warning "가상환경을 찾을 수 없습니다: $venvActivate"
}

# 파이프라인 실행 (전달된 모든 인자 그대로 통과)
# 예시: .\run.ps1 --max-pages 5 --no-headless
python pipeline.py @args
