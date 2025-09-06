@echo off
echo 🏗️ Setting up BridgeGAD Pro - Enhanced Bridge Design Generator
echo ============================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or later.
    pause
    exit /b 1
)

echo ✅ Python found

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv bridgegad_env

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call bridgegad_env\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📥 Installing required packages...
if exist requirements_enhanced.txt (
    pip install -r requirements_enhanced.txt
) else (
    echo ⚠️ requirements_enhanced.txt not found. Installing core packages...
    pip install streamlit==1.31.0 pandas==2.1.4 ezdxf==1.1.3 openpyxl==3.1.2 numpy==1.26.3 plotly==5.17.0 matplotlib==3.8.2
)

echo ✅ Installation complete!
echo.
echo 🚀 To run the application:
echo    1. Activate the environment: bridgegad_env\Scripts\activate.bat
echo    2. Run the app: streamlit run enhanced_bridge_app.py
echo.
echo 🌐 The application will open in your default web browser
echo 📁 Upload your Excel file with bridge parameters to get started
pause
