# 세 개의 애플리케이션을 동시에 실행하는 PowerShell 스크립트

# 현재 디렉토리 저장
$currentDir = Get-Location

# Spring Boot 애플리케이션 실행
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$currentDir\Back\Spring\resume'; ./mvnw spring-boot:run"

# Python Flask 애플리케이션 실행
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$currentDir\NLP'; python 03_result_assay.py"

# npm start 실행 (프론트엔드)
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$currentDir\Front'; npm start"

Write-Host "모든 애플리케이션이 시작되었습니다."
Write-Host "Spring Boot: http://localhost:8082"
Write-Host "Flask API: http://localhost:5000"
Write-Host "Frontend: http://localhost:3000" 