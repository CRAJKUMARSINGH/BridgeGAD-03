# BridgeGAD Pro - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### Option 1: Automatic Setup (Recommended)

**For Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**For Windows:**
```cmd
setup.bat
```

### Option 2: Manual Setup

1. **Clone or download the repository**
2. **Install Python 3.8+ if not already installed**
3. **Create virtual environment:**
   ```bash
   python -m venv bridgegad_env
   source bridgegad_env/bin/activate  # Linux/Mac
   # or
   bridgegad_env\Scripts\activate  # Windows
   ```
4. **Install requirements:**
   ```bash
   pip install -r requirements_enhanced.txt
   ```

## 🎯 Running the Application

```bash
streamlit run enhanced_bridge_app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## 📊 Sample Data

1. Click "Download Template" to get a sample Excel file
2. Fill in your bridge parameters
3. Upload the file and generate professional DXF drawings

## 🔧 Key Features

- **Professional CAD Output**: Industry-standard DXF files with proper layers
- **Interactive Interface**: Modern web-based UI with real-time editing
- **Multiple Scales**: Support for 1:100, 1:200, 1:500, 1:1000 drawings
- **Title Blocks**: Professional title blocks with project information
- **Error Handling**: Comprehensive validation and helpful error messages

## 📁 File Structure

```
BridgeGAD-Pro/
├── enhanced_bridge_app.py      # Main application
├── cad_utils.py               # CAD utilities
├── requirements_enhanced.txt   # Python dependencies
├── setup.sh                   # Linux/Mac setup script
├── setup.bat                  # Windows setup script
├── README_Enhanced.md         # Detailed documentation
└── samples/                   # Sample files
    ├── bridge_parameters_template.xlsx
    └── sample_output.dxf
```

## 🎨 Excel File Format

Your Excel file should have two sheets:

### Sheet1 - Parameters
| Value | Variable | Description |
|-------|----------|-------------|
| 100   | SCALE1   | Main scale factor |
| 50    | SCALE2   | Secondary scale factor |
| 0     | SKEW     | Skew angle in degrees |
| 3     | NSPAN    | Number of spans |
| 30    | SPAN1    | Individual span length |
| ...   | ...      | ... |

### Sheet2 - Cross Section (Optional)
| Chainage (x) | RL (y) |
|-------------|--------|
| 0.0         | 98.5   |
| 10.0        | 99.2   |
| ...         | ...    |

## 🛠️ Troubleshooting

### Common Issues:

1. **"Module not found" errors**: Make sure virtual environment is activated
2. **Excel file not reading**: Check file format (must be .xlsx)
3. **DXF not generating**: Check all required parameters are present
4. **Browser not opening**: Manually navigate to http://localhost:8501

### Getting Help:

- Check the console for error messages
- Review the comprehensive documentation in README_Enhanced.md
- Open an issue on GitHub with error details

## 🎯 Next Steps

1. **Explore Features**: Try different scales and drawing options
2. **Customize Parameters**: Modify bridge parameters for different designs
3. **Professional Output**: Use generated DXF files in AutoCAD, BricsCAD, etc.
4. **Contribute**: Submit improvements or additional features

---

**Enjoy creating professional bridge drawings with BridgeGAD Pro!** 🏗️
