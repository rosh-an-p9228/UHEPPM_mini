@echo off
title Upload UHE_mini to GitHub
echo ============================================================
echo   Uploading UHE_mini to GitHub: rosh-an-p9228/UHEPPM_mini
echo ============================================================
echo.

cd /d "%~dp0"

echo Pushing code to main branch...
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo   SUCCESS! Project uploaded successfully to:
    echo   https://github.com/rosh-an-p9228/UHEPPM_mini
    echo ============================================================
) else (
    echo.
    echo ============================================================
    echo   Push encountered an error. 
    echo   Please sign in when prompted in the browser.
    echo ============================================================
)

echo.
pause
