@echo off
setlocal EnableDelayedExpansion

:: ============================================================================
::  NoteWise — Environment Check & Launcher
::  Validates Python, virtual environment, dependencies, API key, then launches
:: ============================================================================

title NoteWise Launcher

:: ── Colors ──────────────────────────────────────────────────────────────────
:: Using ANSI escape codes for Windows 10+ terminals
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "CYAN=[96m"
set "BOLD=[1m"
set "RESET=[0m"

:: ── Banner ──────────────────────────────────────────────────────────────────
echo.
echo %CYAN%%BOLD%=======================================================%RESET%
echo %CYAN%%BOLD%        NoteWise - Smart Study Assistant               %RESET%
echo %CYAN%%BOLD%        Environment Check ^& Launcher v1.0              %RESET%
echo %CYAN%%BOLD%=======================================================%RESET%
echo.

set "PROJECT_DIR=%~dp0"
set "VENV_DIR=%PROJECT_DIR%notewise_env"
set "REQUIREMENTS=%PROJECT_DIR%requirements.txt"
set "ENV_FILE=%PROJECT_DIR%.env"
set "MAIN_FILE=%PROJECT_DIR%main.py"
set "PASS_COUNT=0"
set "FAIL_COUNT=0"

:: ════════════════════════════════════════════════════════════════════════════
::  CHECK 1: Python Installation
:: ════════════════════════════════════════════════════════════════════════════
echo %BOLD%[1/6] Checking Python installation...%RESET%

python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo   %RED%✗ FAIL: Python is not installed or not in PATH.%RESET%
    echo   %YELLOW%  → Download from https://www.python.org/downloads/%RESET%
    echo   %YELLOW%  → Make sure to check "Add Python to PATH" during installation.%RESET%
    set /a FAIL_COUNT+=1
    goto :summary
) else (
    for /f "tokens=2" %%v in ('python --version 2^>^&1') do set "PY_VER=%%v"
    echo   %GREEN%✓ PASS: Python !PY_VER! found%RESET%
    set /a PASS_COUNT+=1
)

:: ── Check minimum version (3.9+) ──
for /f "tokens=1,2 delims=." %%a in ("!PY_VER!") do (
    set "PY_MAJOR=%%a"
    set "PY_MINOR=%%b"
)
if !PY_MAJOR! LSS 3 (
    echo   %RED%✗ FAIL: Python 3.9+ required, found !PY_VER!%RESET%
    set /a FAIL_COUNT+=1
    goto :summary
)
if !PY_MAJOR! EQU 3 if !PY_MINOR! LSS 9 (
    echo   %RED%✗ FAIL: Python 3.9+ required, found !PY_VER!%RESET%
    set /a FAIL_COUNT+=1
    goto :summary
)
echo   %GREEN%✓ PASS: Python version is compatible (3.9+)%RESET%
set /a PASS_COUNT+=1

:: ════════════════════════════════════════════════════════════════════════════
::  CHECK 2: pip
:: ════════════════════════════════════════════════════════════════════════════
echo.
echo %BOLD%[2/6] Checking pip...%RESET%

python -m pip --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo   %RED%✗ FAIL: pip is not available.%RESET%
    echo   %YELLOW%  → Run: python -m ensurepip --upgrade%RESET%
    set /a FAIL_COUNT+=1
    goto :summary
) else (
    for /f "tokens=2" %%v in ('python -m pip --version 2^>^&1') do set "PIP_VER=%%v"
    echo   %GREEN%✓ PASS: pip !PIP_VER! found%RESET%
    set /a PASS_COUNT+=1
)

:: ════════════════════════════════════════════════════════════════════════════
::  CHECK 3: Virtual Environment
:: ════════════════════════════════════════════════════════════════════════════
echo.
echo %BOLD%[3/6] Checking virtual environment...%RESET%

if exist "%VENV_DIR%\Scripts\python.exe" (
    echo   %GREEN%✓ PASS: Virtual environment found at notewise_env\%RESET%
    set /a PASS_COUNT+=1
) else (
    echo   %YELLOW%⚠ Virtual environment not found. Creating...%RESET%
    python -m venv "%VENV_DIR%"
    if %ERRORLEVEL% NEQ 0 (
        echo   %RED%✗ FAIL: Could not create virtual environment.%RESET%
        set /a FAIL_COUNT+=1
        goto :summary
    )
    echo   %GREEN%✓ PASS: Virtual environment created at notewise_env\%RESET%
    set /a PASS_COUNT+=1
)

:: ── Activate venv ──
call "%VENV_DIR%\Scripts\activate.bat"
echo   %GREEN%✓ Virtual environment activated%RESET%

:: ════════════════════════════════════════════════════════════════════════════
::  CHECK 4: Dependencies
:: ════════════════════════════════════════════════════════════════════════════
echo.
echo %BOLD%[4/6] Checking dependencies...%RESET%

if not exist "%REQUIREMENTS%" (
    echo   %RED%✗ FAIL: requirements.txt not found!%RESET%
    set /a FAIL_COUNT+=1
    goto :summary
)

:: Check each critical package
set "MISSING_PKGS=0"
set "PKG_LIST=streamlit google-generativeai pdfplumber python-pptx reportlab Pillow python-dotenv regex"

for %%p in (%PKG_LIST%) do (
    pip show %%p >nul 2>&1
    if !ERRORLEVEL! NEQ 0 (
        echo   %YELLOW%  ⚠ Missing: %%p%RESET%
        set /a MISSING_PKGS+=1
    )
)

if !MISSING_PKGS! GTR 0 (
    echo   %YELLOW%  Installing missing dependencies...%RESET%
    pip install -r "%REQUIREMENTS%" --quiet
    if !ERRORLEVEL! NEQ 0 (
        echo   %RED%✗ FAIL: Dependency installation failed.%RESET%
        echo   %YELLOW%  → Try manually: pip install -r requirements.txt%RESET%
        set /a FAIL_COUNT+=1
        goto :summary
    )
    echo   %GREEN%✓ PASS: All dependencies installed successfully%RESET%
    set /a PASS_COUNT+=1
) else (
    echo   %GREEN%✓ PASS: All 8 required packages are installed%RESET%
    set /a PASS_COUNT+=1
)

:: ════════════════════════════════════════════════════════════════════════════
::  CHECK 5: Environment Configuration (.env)
:: ════════════════════════════════════════════════════════════════════════════
echo.
echo %BOLD%[5/6] Checking environment configuration...%RESET%

if not exist "%ENV_FILE%" (
    echo   %RED%✗ FAIL: .env file not found!%RESET%
    echo   %YELLOW%  → Create a .env file with: GEMINI_API_KEY=your_key_here%RESET%
    echo   %YELLOW%  → Get a free key from: https://makersuite.google.com/app/apikey%RESET%
    set /a FAIL_COUNT+=1
    goto :summary
) else (
    echo   %GREEN%✓ PASS: .env file found%RESET%
    set /a PASS_COUNT+=1
)

:: Check if API key is set (not placeholder)
set "API_KEY_OK=0"
for /f "usebackq tokens=1,* delims==" %%a in ("%ENV_FILE%") do (
    set "KEY=%%a"
    set "VAL=%%b"
    if "!KEY!"=="GEMINI_API_KEY" (
        if "!VAL!"=="" (
            set "API_KEY_OK=0"
        ) else if "!VAL!"=="your_gemini_api_key_here" (
            set "API_KEY_OK=0"
        ) else if "!VAL!"=="REPLACE_WITH_YOUR_ACTUAL_GEMINI_API_KEY" (
            set "API_KEY_OK=0"
        ) else (
            set "API_KEY_OK=1"
        )
    )
)

if !API_KEY_OK! EQU 1 (
    echo   %GREEN%✓ PASS: GEMINI_API_KEY is configured%RESET%
    set /a PASS_COUNT+=1
) else (
    echo   %RED%✗ FAIL: GEMINI_API_KEY is missing or is a placeholder!%RESET%
    echo   %YELLOW%  → Edit .env and set: GEMINI_API_KEY=your_actual_key%RESET%
    echo   %YELLOW%  → Get a free key from: https://makersuite.google.com/app/apikey%RESET%
    set /a FAIL_COUNT+=1
    goto :summary
)

:: ════════════════════════════════════════════════════════════════════════════
::  CHECK 6: Project Files
:: ════════════════════════════════════════════════════════════════════════════
echo.
echo %BOLD%[6/6] Checking project files...%RESET%

set "FILES_OK=1"
set "CHECK_FILES=main.py app\dashboard.py core\ocr\gemini_extractor.py core\summarizer\gemini_summarizer.py core\question_gen\gemini_generator.py core\storage\simple_storage.py core\exports\enhanced_exporter.py"

for %%f in (%CHECK_FILES%) do (
    if not exist "%PROJECT_DIR%%%f" (
        echo   %RED%✗ Missing: %%f%RESET%
        set "FILES_OK=0"
    )
)

if "!FILES_OK!"=="1" (
    echo   %GREEN%✓ PASS: All 7 project source files present%RESET%
    set /a PASS_COUNT+=1
) else (
    echo   %RED%✗ FAIL: Some project files are missing!%RESET%
    set /a FAIL_COUNT+=1
    goto :summary
)

:: ════════════════════════════════════════════════════════════════════════════
::  SUMMARY & LAUNCH
:: ════════════════════════════════════════════════════════════════════════════
:summary
echo.
echo %CYAN%%BOLD%=======================================================%RESET%
echo %BOLD%  Summary: !PASS_COUNT! passed, !FAIL_COUNT! failed%RESET%
echo %CYAN%%BOLD%=======================================================%RESET%

if !FAIL_COUNT! GTR 0 (
    echo.
    echo %RED%%BOLD%  ✗ Environment check failed. Fix the issues above and try again.%RESET%
    echo.
    pause
    exit /b 1
)

echo.
echo %GREEN%%BOLD%  ✓ All checks passed! Launching NoteWise...%RESET%
echo.
echo %CYAN%  → App will open at: http://localhost:8501%RESET%
echo %CYAN%  → Press Ctrl+C in this window to stop the server%RESET%
echo.

:: ── Launch Streamlit ──
streamlit run "%MAIN_FILE%" --server.headless true --browser.gatherUsageStats false
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo %RED%✗ Streamlit exited with an error.%RESET%
    echo %YELLOW%  → Try running manually: streamlit run main.py%RESET%
    pause
    exit /b 1
)

endlocal
