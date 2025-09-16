#!/usr/bin/env python3
"""
Create standardized input files for all Bridge applications
"""

import pandas as pd
import os
from pathlib import Path

def create_comprehensive_bridge_input():
    """Create comprehensive bridge parameters for testing"""
    
    # Comprehensive bridge parameters based on documentation analysis
    data = {
        'Value': [
            100,     # SCALE1 - Main drawing scale
            50,      # SCALE2 - Secondary scale for sections
            15,      # SKEW - Skew angle in degrees (test with non-zero)
            100,     # DATUM - Reference datum level (RL 100.000)
            0,       # TOPRL - Top road level relative reference
            0,       # LEFT - Leftmost chainage (start of bridge)
            100,     # RIGHT - Rightmost chainage (end of bridge)
            10,      # XINCR - Chainage increment for grid
            5,       # YINCR - Elevation increment for grid
            11,      # NOCH - Number of chainages
            3,       # NSPAN - Number of spans
            90,      # LBRIDGE - Total bridge length
            0,       # ABTL - Left abutment chainage
            106.5,   # RTL - Road top level (RL 106.500)
            104.0,   # SOFL - Soffit level (RL 104.000) 
            0.3,     # KERBW - Kerb width
            0.2,     # KERBD - Kerb depth
            7.5,     # CCBR - Clear carriageway width
            0.45,    # SLBTHC - Slab thickness at center
            0.35,    # SLBTHE - Slab thickness at edge
            0.25,    # SLBTHT - Slab thickness at tip
            105.2,   # CAPT - Pier cap top level
            103.8,   # CAPB - Pier cap bottom level
            2.0,     # CAPW - Cap width
            1.2,     # PIERTW - Pier top width
            6,       # BATTR - Pier batter ratio (1:6)
            3.5,     # PIERST - Pier straight length
            2,       # PIERN - Pier number (for multi-pier bridges)
            30,      # SPAN1 - First span length
            95.0,    # FUTRL - Foundation top RL
            1.5,     # FUTD - Foundation depth
            3.0,     # FUTW - Foundation width
            4.0,     # FUTL - Foundation length
            6.0,     # LASLAB - Approach slab length
            8.5,     # APWTH - Approach slab width
            0.2,     # APTHK - Approach slab thickness
            0.05,    # WCTH - Wearing course thickness
            30,      # SPAN2 - Second span length
            30,      # SPAN3 - Third span length
            1.0,     # ABTBAT - Abutment batter
            4.0,     # ABTHT - Abutment height
            2.5,     # ABTW - Abutment width
            3.0,     # ABTWING - Abutment wing wall length
            0.3,     # RAILHT - Railing height
            0.15,    # RAILW - Railing width
            1.5,     # PILEW - Pile width (if applicable)
            12.0,    # PILEL - Pile length
            0.5,     # CUTOFF - Cut-off level below ground
            102.0    # GROUND - Ground level
        ],
        'Variable': [
            'SCALE1', 'SCALE2', 'SKEW', 'DATUM', 'TOPRL', 'LEFT', 'RIGHT', 'XINCR', 'YINCR',
            'NOCH', 'NSPAN', 'LBRIDGE', 'ABTL', 'RTL', 'SOFL', 'KERBW', 'KERBD', 'CCBR',
            'SLBTHC', 'SLBTHE', 'SLBTHT', 'CAPT', 'CAPB', 'CAPW', 'PIERTW', 'BATTR', 'PIERST',
            'PIERN', 'SPAN1', 'FUTRL', 'FUTD', 'FUTW', 'FUTL', 'LASLAB', 'APWTH', 'APTHK', 
            'WCTH', 'SPAN2', 'SPAN3', 'ABTBAT', 'ABTHT', 'ABTW', 'ABTWING', 'RAILHT', 'RAILW',
            'PILEW', 'PILEL', 'CUTOFF', 'GROUND'
        ],
        'Description': [
            'Main drawing scale factor (1:100)',
            'Secondary scale factor for sections (1:50)',
            'Bridge skew angle in degrees',
            'Reference datum level (RL 100.000)',
            'Top road level reference',
            'Leftmost chainage (bridge start)',
            'Rightmost chainage (bridge end)',
            'Chainage increment for grid',
            'Elevation increment for grid',
            'Total number of chainages',
            'Number of spans in bridge',
            'Total length of bridge',
            'Left abutment chainage',
            'Road top level (RL)',
            'Soffit level (RL)',
            'Width of kerb',
            'Depth of kerb',
            'Clear carriageway width',
            'Deck slab thickness at center',
            'Deck slab thickness at edge',
            'Deck slab thickness at tip',
            'Pier cap top level (RL)',
            'Pier cap bottom level (RL)',
            'Pier cap width',
            'Pier top width',
            'Pier batter ratio (1:n)',
            'Pier straight length',
            'Pier number',
            'First span length',
            'Foundation top RL',
            'Foundation depth',
            'Foundation width',
            'Foundation length',
            'Approach slab length',
            'Approach slab width',
            'Approach slab thickness',
            'Wearing course thickness',
            'Second span length',
            'Third span length',
            'Abutment batter',
            'Abutment height',
            'Abutment width',
            'Abutment wing wall length',
            'Railing height',
            'Railing width',
            'Pile width',
            'Pile length',
            'Cut-off level below ground',
            'Ground level (RL)'
        ]
    }
    
    return pd.DataFrame(data)

def create_cross_section_data():
    """Create realistic cross-section data for bridge"""
    import numpy as np
    
    # Create realistic river bed profile
    chainages = [0, 10, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 90, 100]
    
    # River bed levels with realistic profile
    bed_levels = [
        102.0,  # Left bank
        101.5,  # Approach
        101.0,  # Bank slope
        99.5,   # Mid slope
        97.0,   # River bed start
        95.5,   # Deep section
        94.0,   # Deepest point
        94.5,   # River bed
        95.0,   # Rising
        97.0,   # River bed end
        99.5,   # Mid slope
        101.0,  # Bank slope
        101.5,  # Approach
        102.0,  # Right bank
        102.5,  # Approach
        103.0,  # High ground
        103.5   # Right end
    ]
    
    return pd.DataFrame({
        'Chainage': chainages,
        'RL': bed_levels,
        'Description': [f'Cross-section at Ch {ch}' for ch in chainages]
    })

def create_span_configuration():
    """Create span configuration data"""
    return pd.DataFrame({
        'Span_No': [1, 2, 3],
        'Length': [30.0, 30.0, 30.0],
        'Type': ['Simply Supported', 'Simply Supported', 'Simply Supported'],
        'Material': ['RCC', 'RCC', 'RCC'],
        'Start_Chainage': [0, 30, 60],
        'End_Chainage': [30, 60, 90]
    })

def save_standard_inputs(base_path):
    """Save all standard input files"""
    
    # Create main parameters file
    df_params = create_comprehensive_bridge_input()
    df_cross = create_cross_section_data()
    df_spans = create_span_configuration()
    
    # Save comprehensive input file
    comprehensive_file = base_path / 'bridge_parameters_comprehensive.xlsx'
    with pd.ExcelWriter(comprehensive_file, engine='openpyxl') as writer:
        df_params.to_excel(writer, sheet_name='Sheet1', index=False)
        df_cross.to_excel(writer, sheet_name='Sheet2', index=False)
        df_spans.to_excel(writer, sheet_name='Spans', index=False)
    
    # Save simple input file
    simple_file = base_path / 'bridge_parameters_simple.xlsx'
    df_simple = df_params.head(20)  # First 20 essential parameters
    with pd.ExcelWriter(simple_file, engine='openpyxl') as writer:
        df_simple.to_excel(writer, sheet_name='Sheet1', index=False)
        df_cross.to_excel(writer, sheet_name='Sheet2', index=False)
    
    # Save spans-only file (for span-specific apps)
    spans_file = base_path / 'spans_only.xlsx'
    with pd.ExcelWriter(spans_file, engine='openpyxl') as writer:
        df_spans.to_excel(writer, sheet_name='Sheet1', index=False)
    
    # Save input.xlsx (common name used by many apps)
    input_file = base_path / 'input.xlsx'
    with pd.ExcelWriter(input_file, engine='openpyxl') as writer:
        df_params.to_excel(writer, sheet_name='Sheet1', index=False)
        df_cross.to_excel(writer, sheet_name='Sheet2', index=False)
    
    print(f"Created input files in {base_path}:")
    print(f"  - {comprehensive_file.name}")
    print(f"  - {simple_file.name}")
    print(f"  - {spans_file.name}")
    print(f"  - {input_file.name}")

def main():
    """Create standardized input files for all Bridge applications"""
    print("========================================")
    print("CREATING STANDARDIZED INPUT FILES")
    print("========================================")
    
    base_dir = Path("C:/Users/Rajkumar")
    
    # List of Bridge applications
    bridge_apps = [
        "BridgeGAD-00", "BridgeGAD-01", "BridgeGAD-02", "BridgeGAD-03",
        "BridgeGAD-04", "BridgeGAD-05", "BridgeGAD-06", "BridgeGAD-07",
        "BridgeGAD-08", "BridgeGAD-09", "BridgeGAD-10", "BridgeGAD-11",
        "BridgeGAD-12", "Bridge-Causeway-Design", "BridgeDraw", "Bridge_Slab_Design"
    ]
    
    for app_name in bridge_apps:
        app_path = base_dir / app_name
        
        if app_path.exists():
            print(f"\nProcessing {app_name}...")
            
            # Create SAMPLE_INPUT_FILES directory
            sample_dir = app_path / "SAMPLE_INPUT_FILES"
            sample_dir.mkdir(exist_ok=True)
            
            # Create OUTPUT directory
            output_dir = app_path / "OUTPUT_01_16092025"
            output_dir.mkdir(exist_ok=True)
            
            # Save input files
            save_standard_inputs(sample_dir)
            
        else:
            print(f"App not found: {app_name}")
    
    print("\n========================================")
    print("INPUT FILE CREATION COMPLETE")
    print("All Bridge apps now have standardized input files")
    print("========================================")

if __name__ == "__main__":
    main()