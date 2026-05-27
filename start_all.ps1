# 세 개의 애플리케이션을 동시에 실행하는 PowerShell 스크립트

# 현재 디렉토리 저장
$currentDir = Get-Location

# 1. Spring Boot 애플리케이션 실행 (Gradle 사용)
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$currentDir\Back\Spring\resume'; ./gradlew bootRun"

# 2. Python Flask 애플리케이션 실행 (Back 디렉토리의 스크립트 실행)
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$currentDir'; python Back/03_result_assay.py"

# 3. React 프론트엔드 실행 (Front/blog 디렉토리에서 npm run dev 실행)
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$currentDir\Front\blog'; npm run dev"

Write-Host "모든 애플리케이션이 시작 프로세스에 진입했습니다."
Write-Host "Spring Boot: http://localhost:8082/resume"
Write-Host "Flask API: http://localhost:5000"
Write-Host "Frontend: http://localhost:3000"
