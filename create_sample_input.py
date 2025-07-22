import pandas as pd
import numpy as np

# Create sample bridge parameters
data = {
    'Value': [
        100,    # SCALE1
        50,     # SCALE2
        0,      # SKEW
        100,    # DATUM
        0,      # TOPRL
        0,      # LEFT
        100,    # RIGHT
        10,     # XINCR
        1,      # YINCR
        11,     # NOCH
        3,      # NSPAN
        30,     # LBRIDGE
        0,      # ABTL
        105,    # RTL
        103,    # SOFL
        0.3,    # KERBW
        0.2,    # KERBD
        7.5,    # CCBR
        0.2,    # SLBTHC
        0.3,    # SLBTHE
        0.25,   # SLBTHT
        104,    # CAPT
        102,    # CAPB
        1.2,    # CAPW
        0.8,    # PIERTW
        6,      # BATTR
        2,      # PIERST
        1,      # PIERN
        10,     # SPAN1
        98,     # FUTRL
        1,      # FUTD
        2.5,    # FUTW
        3,      # FUTL
        3,      # LASLAB
        8.5,    # APWTH
        0.2,    # APTHK
        0.05    # WCTH
    ],
    'Variable': [
        'SCALE1', 'SCALE2', 'SKEW', 'DATUM', 'TOPRL', 'LEFT', 'RIGHT', 'XINCR', 'YINCR',
        'NOCH', 'NSPAN', 'LBRIDGE', 'ABTL', 'RTL', 'SOFL', 'KERBW', 'KERBD', 'CCBR',
        'SLBTHC', 'SLBTHE', 'SLBTHT', 'CAPT', 'CAPB', 'CAPW', 'PIERTW', 'BATTR', 'PIERST',
        'PIERN', 'SPAN1', 'FUTRL', 'FUTD', 'FUTW', 'FUTL', 'LASLAB', 'APWTH', 'APTHK', 'WCTH'
    ],
    'Description': [
        'Main scale factor',
        'Secondary scale factor',
        'Skew angle in degrees',
        'Reference datum level',
        'Top road level',
        'Leftmost chainage',
        'Rightmost chainage',
        'Chainage increment in X direction',
        'Elevation increment in Y direction',
        'Total number of chainages',
        'Number of spans',
        'Length of bridge',
        'Chainage of left abutment',
        'Road top level',
        'Soffit level',
        'Width of kerb',
        'Depth of kerb',
        'Clear carriageway width',
        'Thickness of slab at center',
        'Thickness of slab at edge',
        'Thickness of slab at tip',
        'Pier cap top RL',
        'Pier cap bottom RL',
        'Cap width',
        'Pier top width',
        'Pier batter',
        'Straight length of pier',
        'Pier number',
        'Individual span length',
        'Founding RL',
        'Depth of footing',
        'Width of footing',
        'Length of footing',
        'Length of approach slab',
        'Width of approach slab',
        'Thickness of approach slab',
        'Thickness of wearing course'
    ]
}

# Create cross-section data (Sheet2)
chainages = np.linspace(0, 100, 20)  # 20 points from 0 to 100
rls = 100 + np.sin(chainages/10) * 2  # Simple sine wave for RL values

# Create a Pandas Excel writer
with pd.ExcelWriter('bridge_parameters_template.xlsx', engine='openpyxl') as writer:
    # Write parameters to Sheet1
    pd.DataFrame(data).to_excel(writer, sheet_name='Sheet1', index=False)
    
    # Write cross-section data to Sheet2
    cross_section = pd.DataFrame({
        'Chainage (x)': chainages,
        'RL (y)': rls
    })
    cross_section.to_excel(writer, sheet_name='Sheet2', index=False)

print("Sample input file 'bridge_parameters_template.xlsx' has been created.")
