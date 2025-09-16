#!/usr/bin/env python3
"""
BridgeGAD-03 Test Script
Simple test to validate input processing and generate basic output
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

def test_bridgegad03():
    """Test BridgeGAD-03 functionality"""
    print("=" * 50)
    print("Testing BridgeGAD-03 Application")
    print("=" * 50)
    
    try:
        # Load parameters
        df = pd.read_excel('bridge_parameters_template.xlsx', sheet_name=0)
        params = dict(zip(df['Variable'], df['Value']))
        
        print(f"✓ Loaded {len(params)} parameters")
        print(f"✓ Scale factor: {params.get('SCALE1', 100)}")
        print(f"✓ Number of spans: {params.get('NSPAN', 3)}")
        print(f"✓ Span 1 length: {params.get('SPAN1', 30)} m")
        
        # Create simple bridge visualization
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Bridge elevation view
        nspan = int(params.get('NSPAN', 3))
        spans = [params.get(f'SPAN{i+1}', 30) for i in range(nspan)]
        
        # Draw spans
        x_pos = 0
        for i, span_length in enumerate(spans):
            ax1.plot([x_pos, x_pos + span_length], [5, 5], 'b-', linewidth=3, label=f'Span {i+1}' if i == 0 else '')
            ax1.plot([x_pos, x_pos], [0, 5], 'k-', linewidth=2)  # Pier
            x_pos += span_length
        
        ax1.plot([x_pos, x_pos], [0, 5], 'k-', linewidth=2)  # Final pier
        ax1.set_xlim(-5, x_pos + 5)
        ax1.set_ylim(-2, 8)
        ax1.set_title(f'Bridge Elevation - {nspan} Spans', fontsize=14)
        ax1.set_xlabel('Distance (m)')
        ax1.set_ylabel('Height (m)')
        ax1.grid(True, alpha=0.3)
        
        # Bridge plan view
        deck_width = params.get('DECKWD', 10)
        ax2.fill_between([0, x_pos], [0, 0], [deck_width, deck_width], alpha=0.3, color='gray', label='Bridge Deck')
        ax2.set_xlim(-5, x_pos + 5)
        ax2.set_ylim(-2, deck_width + 2)
        ax2.set_title('Bridge Plan View', fontsize=14)
        ax2.set_xlabel('Distance (m)')
        ax2.set_ylabel('Width (m)')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save output
        output_dir = 'OUTPUT_01_16092025'
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = f'{output_dir}/BridgeGAD-03_test_output_{datetime.now().strftime("%H%M%S")}.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Bridge visualization saved: {output_file}")
        
        # Save parameters summary
        summary_file = f'{output_dir}/BridgeGAD-03_parameters_{datetime.now().strftime("%H%M%S")}.txt'
        with open(summary_file, 'w') as f:
            f.write("BridgeGAD-03 Test Results\n")
            f.write("=" * 30 + "\n")
            f.write(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("Bridge Parameters:\n")
            for key, value in params.items():
                f.write(f"  {key}: {value}\n")
        
        print(f"✓ Parameters summary saved: {summary_file}")
        print("✓ BridgeGAD-03 test completed successfully!")
        
        plt.close()
        
        return True
        
    except Exception as e:
        print(f"✗ Error in BridgeGAD-03 test: {e}")
        return False

if __name__ == "__main__":
    test_bridgegad03()
