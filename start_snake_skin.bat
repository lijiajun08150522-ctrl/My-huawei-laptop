@echo off
echo ============================================================
echo 贪吃蛇 AI 皮肤生成功能 - 启动脚本
echo ============================================================
echo.

echo [1/2] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python
    pause
    exit /b 1
)
echo Python 环境检查通过
echo.

echo [2/2] 启动 Flask 服务...
echo 服务地址: http://127.0.0.1:5000
echo 游戏地址: http://127.0.0.1:5000/game
echo.
echo 提示: 按 Ctrl+C 停止服务
echo.

python app.py
