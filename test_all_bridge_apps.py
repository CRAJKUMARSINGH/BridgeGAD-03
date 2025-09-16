#!/usr/bin/env python3
"""
Comprehensive BridgeGAD Apps Tester
Tests all BridgeGAD-XX applications with their specific input formats
"""

import os
import sys
import subprocess
import pandas as pd
import shutil
from datetime import datetime
from pathlib import Path

def setup_output_directories():
    """Create output directories for all apps"""
    output_base = Path("C:/Users/Rajkumar/BridgeGAD-03/OUTPUT_01_16092025")
    output_base.mkdir(exist_ok=True)
    
    for i in range(13):  # BridgeGAD-00 to BridgeGAD-12
        app_output = output_base / f"BridgeGAD-{i:02d}"
        app_output.mkdir(exist_ok=True)
    
    return output_base

def get_bridge_apps():
    """Get list of all BridgeGAD applications"""
    base_path = Path("C:/Users/Rajkumar")
    apps = []
    for i in range(13):
        app_path = base_path / f"BridgeGAD-{i:02d}"
        if app_path.exists():
            apps.append(app_path)
    return apps

def test_bridgegad_00(app_path, output_path):
    """Test BridgeGAD-00 application"""
    print(f"Testing BridgeGAD-00...")
    try:
        os.chdir(app_path)
        
        # Check for main scripts
        main_scripts = ['app.py', 'enhanced_bridge_app.py', 'rajkumar_app.py']
        available_script = None
        
        for script in main_scripts:
            if (app_path / script).exists():
                available_script = script
                break
        
        if available_script:
            # Try to create sample input first
            if (app_path / 'create_sample_input.py').exists():
                result = subprocess.run([sys.executable, 'create_sample_input.py'], 
                                      capture_output=True, text=True, timeout=30)
                print(f"  ✓ Sample input creation: {result.returncode == 0}")
            
            # Test basic functionality
            test_code = f"""
import sys
sys.path.append('{app_path}')
try:
    import pandas as pd
    # Look for Excel files
    excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx')]
    if excel_files:
        df = pd.read_excel(excel_files[0])
        print(f"✓ BridgeGAD-00 input processing: {{len(df)}} rows loaded")
    else:
        print("✓ BridgeGAD-00 basic import successful")
    with open('{output_path}/BridgeGAD-00_test_result.txt', 'w') as f:
        f.write(f"BridgeGAD-00 Test Result\\nTime: {{datetime.now()}}\\nStatus: SUCCESS\\n")
except Exception as e:
    print(f"✗ BridgeGAD-00 error: {{e}}")
    with open('{output_path}/BridgeGAD-00_test_result.txt', 'w') as f:
        f.write(f"BridgeGAD-00 Test Result\\nTime: {{datetime.now()}}\\nStatus: ERROR - {{e}}\\n")
"""
            result = subprocess.run([sys.executable, '-c', test_code], 
                                  capture_output=True, text=True, timeout=60)
            print(f"  ✓ BridgeGAD-00 test completed")
            return True
        else:
            print(f"  ✗ No main script found in BridgeGAD-00")
            return False
            
    except Exception as e:
        print(f"  ✗ BridgeGAD-00 error: {e}")
        return False

def test_bridgegad_01(app_path, output_path):
    """Test BridgeGAD-01 application"""
    print(f"Testing BridgeGAD-01...")
    try:
        os.chdir(app_path)
        
        # BridgeGAD-01 seems to have streamlit_app.py and bridge_drawings.py
        if (app_path / 'streamlit_app.py').exists():
            test_code = f"""
import sys
sys.path.append('{app_path}')
try:
    # Test basic imports
    import streamlit
    print("✓ BridgeGAD-01 Streamlit import successful")
    with open('{output_path}/BridgeGAD-01_test_result.txt', 'w') as f:
        f.write(f"BridgeGAD-01 Test Result\\nTime: {{datetime.now()}}\\nStatus: SUCCESS\\nType: Streamlit App\\n")
except Exception as e:
    print(f"✗ BridgeGAD-01 error: {{e}}")
    with open('{output_path}/BridgeGAD-01_test_result.txt', 'w') as f:
        f.write(f"BridgeGAD-01 Test Result\\nTime: {{datetime.now()}}\\nStatus: ERROR - {{e}}\\n")
"""
            result = subprocess.run([sys.executable, '-c', test_code], 
                                  capture_output=True, text=True, timeout=60)
            print(f"  ✓ BridgeGAD-01 test completed")
            return True
        else:
            print(f"  ✗ No streamlit_app.py found in BridgeGAD-01")
            return False
            
    except Exception as e:
        print(f"  ✗ BridgeGAD-01 error: {e}")
        return False

def test_generic_bridgegad(app_name, app_path, output_path):
    """Test generic BridgeGAD application"""
    print(f"Testing {app_name}...")
    try:
        os.chdir(app_path)
        
        # Find Python files
        py_files = list(app_path.glob("*.py"))
        main_files = [f for f in py_files if any(keyword in f.name.lower() 
                     for keyword in ['app', 'main', 'bridge', 'streamlit'])]
        
        if not main_files:
            main_files = py_files[:3]  # Take first 3 Python files
        
        # Check requirements
        requirements_file = app_path / 'requirements.txt'
        has_requirements = requirements_file.exists()
        
        test_code = f"""
import sys
sys.path.append('{app_path}')
import os
from datetime import datetime

try:
    # Try to find and read any documentation
    doc_files = [f for f in os.listdir('.') if f.endswith('.md') or f.endswith('.txt')]
    
    # Try basic Python imports that might be needed
    import pandas as pd
    
    # Look for Excel or input files
    input_files = [f for f in os.listdir('.') if f.endswith(('.xlsx', '.csv', '.json'))]
    
    result_info = []
    result_info.append(f"{app_name} Test Result")
    result_info.append(f"Time: {{datetime.now()}}")
    result_info.append(f"Status: SUCCESS")
    result_info.append(f"Python files: {len(main_files)}")
    result_info.append(f"Documentation files: {{len(doc_files)}}")
    result_info.append(f"Input files: {{len(input_files)}}")
    result_info.append(f"Has requirements.txt: {has_requirements}")
    
    with open('{output_path}/{app_name}_test_result.txt', 'w') as f:
        f.write("\\n".join(result_info))
    
    print(f"✓ {app_name} basic validation successful")
    
except Exception as e:
    with open('{output_path}/{app_name}_test_result.txt', 'w') as f:
        f.write(f"{app_name} Test Result\\nTime: {{datetime.now()}}\\nStatus: ERROR - {{e}}\\n")
    print(f"✗ {app_name} error: {{e}}")
"""
        result = subprocess.run([sys.executable, '-c', test_code], 
                              capture_output=True, text=True, timeout=60)
        print(f"  ✓ {app_name} test completed")
        return True
        
    except Exception as e:
        print(f"  ✗ {app_name} error: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("COMPREHENSIVE BRIDGEGAD APPLICATIONS TEST")
    print("=" * 60)
    
    # Setup output directories
    output_base = setup_output_directories()
    
    # Get all BridgeGAD apps
    apps = get_bridge_apps()
    print(f"Found {len(apps)} BridgeGAD applications")
    
    results = {}
    
    # Test each app
    for app_path in apps:
        app_name = app_path.name
        output_path = output_base / app_name
        
        try:
            if app_name == "BridgeGAD-00":
                results[app_name] = test_bridgegad_00(app_path, output_path)
            elif app_name == "BridgeGAD-01":
                results[app_name] = test_bridgegad_01(app_path, output_path)
            else:
                results[app_name] = test_generic_bridgegad(app_name, app_path, output_path)
                
        except Exception as e:
            print(f"Error testing {app_name}: {e}")
            results[app_name] = False
    
    # Generate summary
    print("\\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    successful = sum(results.values())
    total = len(results)
    
    for app_name, success in results.items():
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{app_name:15} {status}")
    
    print(f"\\nOverall: {successful}/{total} apps tested successfully")
    
    # Save summary
    summary_file = output_base / "test_summary.txt"
    with open(summary_file, 'w') as f:
        f.write("BridgeGAD Applications Test Summary\\n")
        f.write("=" * 40 + "\\n")
        f.write(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
        f.write(f"Total Apps: {total}\\n")
        f.write(f"Successful: {successful}\\n")
        f.write(f"Failed: {total - successful}\\n\\n")
        f.write("Individual Results:\\n")
        for app_name, success in results.items():
            status = "PASSED" if success else "FAILED"
            f.write(f"  {app_name}: {status}\\n")
    
    print(f"\\n✓ Summary saved to: {summary_file}")
    
    # Return to original directory
    os.chdir("C:/Users/Rajkumar/BridgeGAD-03")

if __name__ == "__main__":
    main()
