@echo off
echo ========================================
echo CodeBuddy Demo Video Server
echo ========================================
echo.

echo Step 1: Installing dependencies...
echo.
call npm install
if errorlevel 1 (
    echo ERROR: npm install failed!
    pause
    exit /b 1
)

echo.
echo Step 2: Starting Remotion Studio...
echo.
echo Server will be available at: http://localhost:3000
echo Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

npm start
