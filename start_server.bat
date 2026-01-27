@echo off
chcp 65001 >nul
echo ======================================================
echo 任务管理器 - 启动Flask服务
echo ======================================================
echo.
echo 正在启动服务...
echo.
cd /d "%~dp0"
python app.py
pause
