@echo off
chcp 65001 > nul
echo ========================================
echo CodeBuddy Playwright回归测试
echo ========================================
echo.

REM 检查Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到Node.js，请先安装Node.js
    echo 下载地址: https://nodejs.org/
    pause
    exit /b 1
)

echo [步骤 1] 检查依赖...
if not exist "node_modules\" (
    echo 正在安装依赖...
    call npm install
    if %errorlevel% neq 0 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
) else (
    echo 依赖已安装
)

echo.
echo [步骤 2] 检查Playwright浏览器...
if not exist "node_modules\playwright\" (
    echo 正在安装Playwright浏览器...
    call npm run install:browser
    if %errorlevel% neq 0 (
        echo [错误] 浏览器安装失败
        pause
        exit /b 1
    )
) else (
    echo 浏览器已安装
)

echo.
echo [步骤 3] 启动Flask服务器...
cd ..
start /B python app.py > nul 2>&1
timeout /t 3 /nobreak > nul
cd tests

echo.
echo [步骤 4] 运行测试...
echo.
call npx playwright test --reporter=list

echo.
if %errorlevel% equ 0 (
    echo ========================================
    echo 测试通过！✅
    echo ========================================
    echo.
    echo 查看详细报告:
    echo   npm run test:report
    echo.
) else (
    echo ========================================
    echo 测试失败！❌
    echo ========================================
    echo.
    echo 查看详细报告:
    echo   npm run test:report
    echo.
)

echo [步骤 5] 停止Flask服务器...
taskkill /F /IM python.exe > nul 2>&1

pause
