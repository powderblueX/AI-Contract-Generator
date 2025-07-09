@echo off
setlocal enabledelayedexpansion

REM ========================================
REM   Contract Generator - Fixed Version
REM   Resolved batch recursion issue
REM ========================================

REM Change to script directory
cd /d "%~dp0"
echo Current directory: %CD%
echo.

REM Stage 1: Direct Conda path detection
echo [1/5] Locating Conda installation...
set "CONDA_BASE="

REM Check common Conda installation paths
for %%d in (C D E F) do (
    if exist "%%d:\Anaconda3\Scripts\conda.exe" set "CONDA_BASE=%%d:\Anaconda3"
    if exist "%%d:\Miniconda3\Scripts\conda.exe" set "CONDA_BASE=%%d:\Miniconda3"
    if exist "%%d:\Anaconda\Scripts\conda.exe" set "CONDA_BASE=%%d:\Anaconda"
)

if not defined CONDA_BASE (
    echo [ERROR] Conda not found in default locations. Please:
    echo   1. Run in Anaconda Prompt, OR
    echo   2. Set CONDA_BASE manually in this script
    pause
    exit /b 1
)

echo [SUCCESS] Using Conda at: %CONDA_BASE%
echo.

REM Stage 2: Safe environment setup
echo [2/5] Setting up base environment...
call "%CONDA_BASE%\Scripts\activate.bat" base || (
    echo [ERROR] Base activation failed
    echo Try manual activation: call "%CONDA_BASE%\Scripts\activate.bat" base
    pause
    exit /b 1
)

REM Stage 3: Environment creation
echo [3/5] Processing environment...
if not exist environment.yml (
    echo [ERROR] environment.yml not found
    dir /b
    pause
    exit /b 1
)

echo Checking existing environments...
conda env list | findstr /rc:"^ *contract_generation " >nul
if errorlevel 1 (
    echo Creating new environment...
    conda env create -f environment.yml --quiet
) else (
    echo Updating existing environment...
    conda env update -f environment.yml --quiet
)

if errorlevel 1 (
    echo [ERROR] Environment setup failed
    echo Try manual command: conda env create -f environment.yml
    pause
    exit /b 1
)

REM Stage 4: Safe environment activation
echo [4/5] Activating environment...
call "%CONDA_BASE%\Scripts\activate.bat" contract_generation || (
    echo [ERROR] Activation failed
    echo Try manual activation: conda activate contract_generation
    pause
    exit /b 1
)

REM Stage 5: Run application
echo [5/5] Starting application...
set "PYTHONPATH=%CD%"
echo PYTHONPATH set to: %PYTHONPATH%
echo Launching demo.py...
echo ========================================
python demo.py
echo ========================================
echo.

REM Cleanup
echo [INFO] Deactivating environment...
conda deactivate

echo ========================================
echo    Operation completed successfully
echo ========================================
pause
exit /b 0