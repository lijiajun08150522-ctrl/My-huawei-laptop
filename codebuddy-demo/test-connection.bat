@echo off
echo ========================================
echo CodeBuddy Demo - Connection Test
echo ========================================
echo.

echo [1/5] Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Node.js is not installed!
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)
echo [OK] Node.js is installed
node --version
echo.

echo [2/5] Checking npm...
npm --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] npm is not installed!
    pause
    exit /b 1
)
echo [OK] npm is installed
npm --version
echo.

echo [3/5] Checking project files...
if not exist "package.json" (
    echo [FAIL] package.json not found!
    echo Current directory: %CD%
    pause
    exit /b 1
)
echo [OK] package.json exists
if not exist "remotion.config.ts" (
    echo [WARN] remotion.config.ts not found
) else (
    echo [OK] remotion.config.ts exists
)
if not exist "tsconfig.json" (
    echo [WARN] tsconfig.json not found
) else (
    echo [OK] tsconfig.json exists
)
if not exist "src\Root.tsx" (
    echo [WARN] src\Root.tsx not found
) else (
    echo [OK] src\Root.tsx exists
)
if not exist "src\CodeBuddyIntro.tsx" (
    echo [WARN] src\CodeBuddyIntro.tsx not found
) else (
    echo [OK] src\CodeBuddyIntro.tsx exists
)
echo.

echo [4/5] Checking dependencies...
if not exist "node_modules" (
    echo [INFO] Dependencies not installed yet
    echo Installing now...
    echo.
    call npm install
    if errorlevel 1 (
        echo [FAIL] npm install failed!
        echo Please check your internet connection
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies already installed
)
echo.

echo [5/5] Checking port 3000...
netstat -ano | findstr ":3000" | findstr "LISTENING" >nul 2>&1
if errorlevel 1 (
    echo [OK] Port 3000 is available
) else (
    echo [WARN] Port 3000 is already in use
    echo Please close other applications or kill the process
)
echo.

echo ========================================
echo All checks passed!
echo ========================================
echo.
echo Starting Remotion Studio...
echo Server will be available at: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

npm start

if errorlevel 1 (
    echo.
    echo ========================================
    echo [FAIL] Server failed to start
    echo ========================================
    echo.
    echo Possible reasons:
    echo 1. Dependencies not installed correctly
    echo 2. Port 3000 is in use by another application
    echo 3. Missing files in the project
    echo.
    echo Please see TROUBLESHOOTING.md for more help
    pause
)
