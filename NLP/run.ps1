# 잡코리아 & 링커리어 파이프라인 실행 스크립트
# 사용법: .\run.ps1 [옵션]
# 예시:   .\run.ps1 --jk-start 1 --jk-end 3

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvActivate = Join-Path $ScriptDir ".venv\Scripts\Activate.ps1"

if (-not (Test-Path $VenvActivate)) {
    Write-Error "venv를 찾을 수 없습니다: $VenvActivate"
    Write-Host "먼저 venv를 생성하세요: python -m venv .venv"
    exit 1
}

& $VenvActivate
python "$ScriptDir\pipeline.py" @args
