#!/bin/bash

echo "🏗️ Setting up BridgeGAD Pro - Enhanced Bridge Design Generator"
echo "============================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or later."
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv bridgegad_env

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source bridgegad_env/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing required packages..."
if [ -f "requirements_enhanced.txt" ]; then
    pip install -r requirements_enhanced.txt
else
    echo "⚠️ requirements_enhanced.txt not found. Installing core packages..."
    pip install streamlit==1.31.0 pandas==2.1.4 ezdxf==1.1.3 openpyxl==3.1.2 numpy==1.26.3 plotly==5.17.0 matplotlib==3.8.2
fi

echo "✅ Installation complete!"
echo ""
echo "🚀 To run the application:"
echo "   1. Activate the environment: source bridgegad_env/bin/activate"
echo "   2. Run the app: streamlit run enhanced_bridge_app.py"
echo ""
echo "🌐 The application will open in your default web browser"
echo "📁 Upload your Excel file with bridge parameters to get started"
