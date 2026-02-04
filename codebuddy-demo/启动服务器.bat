@echo off
chcp 65001 > nul
echo ========================================
echo CodeBuddy Demo Video Server
echo ========================================
echo.
echo 正在启动 Remotion Studio...
echo.
echo 服务器将在浏览器中自动打开
echo 地址: http://localhost:3000
echo.
echo 按 Ctrl+C 可停止服务器
echo.
echo ========================================
echo.

d:
cd d:\SummerProject\codebuddy-demo

npm start

pause
