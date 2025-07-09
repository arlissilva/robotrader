@echo off
echo Escolha onde rodar:
echo 1 - Localhost
echo 2 - Docker
set /p opt=Escolha: 
if "%opt%"=="1" (python robot_trader/main.py) else (docker compose up --build)