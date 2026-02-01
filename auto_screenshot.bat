@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ============================================================
echo           CodeBuddy 项目实训证明截图工具
echo ============================================================
echo.

:: 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python
    pause
    exit /b 1
)

:: 检查Playwright是否安装
python -c "import playwright" >nul 2>&1
if errorlevel 1 (
    echo [安装] 正在安装Playwright...
    pip install playwright
    echo [安装] 正在安装Chromium浏览器...
    playwright install chromium
)

:: 检查Flask服务是否运行
curl -s http://localhost:5000 >nul 2>&1
if errorlevel 1 (
    echo [启动] Flask服务未运行，正在启动...
    start /B python app.py
    echo [等待] 等待服务启动...
    timeout /t 3 /nobreak >nul
)

echo.
echo ============================================================
echo 开始自动截图...
echo ============================================================
echo.

:: 运行截图脚本
python screenshot_helper.py

echo.
echo ============================================================
echo 截图完成！
echo ============================================================
echo.
echo 生成的截图文件:
dir /b screenshot-*.png 2>nul
echo.
echo 查看位置: d:\SummerProject\
echo ============================================================
echo.

pause
