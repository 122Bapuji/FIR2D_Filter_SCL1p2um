import re

def_file = '/mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/routing/fir2d_routed.def'

with open(def_file, 'r') as f:
    text = f.read()

# Look in SPECIALNETS for VDD and VSS rings
for net_name in ['VDD', 'VSS']:
    m = re.search(rf'-\s+{net_name}\s+(.*?);', text, re.DOTALL)
    if m:
        net_def = m.group(1)
        # Search for metal2 vertical segments around X=150-170 um or X=3230-3250 um
        print(f"\n=== SPECIALNET {net_name} ===")
        for line in net_def.split('\n'):
            if 'metal2' in line or 'ROUTED' in line or 'SHAPE RING' in line:
                for match in re.finditer(r'\( (\d+) (\d+) \) \( \* (\d+) \)', line):
                    x, y1, y2 = int(match.group(1))/1000.0, int(match.group(2))/1000.0, int(match.group(3))/1000.0
                    print(f"  {net_name} vertical M2 segment at X={x:.1f} um from Y={y1:.1f} to {y2:.1f} um")
