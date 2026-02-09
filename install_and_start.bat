@echo off
echo ============================================================
echo 安装依赖并启动服务
echo ============================================================
echo.

echo [1/2] 安装依赖...
pip install requests Pillow
if errorlevel 1 (
    echo 安装失败，请检查网络连接
    pause
    exit /b 1
)
echo.
echo 依赖安装完成
echo.

echo [2/2] 启动 Flask 服务...
echo 服务地址: http://127.0.0.1:5000
echo 游戏地址: http://127.0.0.1:5000/game
echo.
echo 提示: 按 Ctrl+C 停止服务
echo.

python app.py
