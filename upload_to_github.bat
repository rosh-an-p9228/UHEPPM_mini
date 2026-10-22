@echo off
title Upload UHE_mini to GitHub
echo ============================================================
echo   Uploading UHE_mini to GitHub: rosh-an-p9228/UHEPPM
echo ============================================================
echo.

cd /d "%~dp0"

echo Checking GitHub repository...
echo If you have not created the repository yet, create it with name: UHEPPM
echo Opening GitHub create page in your browser...
start https://github.com/new?name=UHEPPM

echo.
echo Ready to push to: https://github.com/rosh-an-p9228/UHEPPM.git
echo.
pause

echo Pushing code to main branch...
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo   SUCCESS! Project uploaded successfully to:
    echo   https://github.com/rosh-an-p9228/UHEPPM
    echo ============================================================
) else (
    echo.
    echo ============================================================
    echo   Push encountered an error. 
    echo   Ensure:
    echo   1. The repository 'UHEPPM' is created on GitHub.
    echo   2. You approved the browser sign-in prompt.
    echo ============================================================
)

echo.
pause
