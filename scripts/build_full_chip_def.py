#!/usr/bin/env python3
"""
build_full_chip_def.py
Generates the complete 4.0 mm x 4.0 mm full chip DEF file for OpenROAD GUI viewing.
Includes:
- Die area (0 0) (4000000 4000000)
- 4 CORNER cells
- 40 Peripheral Pads (IPAD20, OPAD02, IPAD00, PVDD01, PVSS01)
- Centered 3400 um x 3400 um core with all 67,226 standard cells shifted by (+300000, +300000)
- Dual concentric power rings & followpins shifted by (+300000, +300000)
- 8 Wide 20 um power straps connecting power pads to core rings
- All 1,687 routed signal nets shifted by (+300000, +300000)
"""

import re
import os

CORE_DEF = "/mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/routing/fir2d_routed.def"
FULL_DEF = "/mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/database/fir2d_chip_4mmx4mm.def"
ROUTING_DEF = "/mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/routing/fir2d_chip_4mmx4mm.def"
DX = 300000
DY = 300000

print(f"Reading {CORE_DEF}...")

# Pad definitions (cell_name, x_nm, y_nm, orient)
# Exact coordinates from SCL frame4mmx4mm
pads = [
    # Bottom Edge (y = 304.9 um = 304900 nm, orient = FS)
    ("PAD_B01", "IPAD20", 350900, 304900, "FS"),
    ("PAD_B02", "IPAD20", 701000, 304900, "FS"),
    ("PAD_B03", "IPAD20", 1051000, 304900, "FS"),
    ("PAD_B04_PVSS", "PVSS01", 1400000, 304900, "FS"),
    ("PAD_B05", "IPAD20", 1751000, 304900, "FS"),
    ("PAD_B06", "IPAD20", 2100900, 304900, "FS"),
    ("PAD_B07_PVDD", "PVDD01", 2450000, 304900, "FS"),
    ("PAD_B08", "IPAD20", 2801000, 304900, "FS"),
    ("PAD_B09", "IPAD20", 3151000, 304900, "FS"),
    ("PAD_B10", "IPAD20", 3501000, 304900, "FS"),

    # Left Edge (x = 304.9 um = 304900 nm, orient = W)
    ("PAD_L01", "IPAD00", 304900, 350900, "W"),
    ("PAD_L02", "IPAD00", 304900, 701000, "W"),
    ("PAD_L03", "IPAD00", 304900, 1051000, "W"),
    ("PAD_L04_PVDD", "PVDD01", 304900, 1400000, "W"),
    ("PAD_L05", "IPAD00", 304900, 1751000, "W"),
    ("PAD_L06", "IPAD00", 304900, 2100900, "W"),
    ("PAD_L07_PVSS", "PVSS01", 304900, 2450000, "W"),
    ("PAD_L08", "IPAD00", 304900, 2801000, "W"),
    ("PAD_L09", "IPAD00", 304900, 3151000, "W"),
    ("PAD_L10", "IPAD00", 304900, 3501000, "W"),

    # Right Edge (x = 3695.1 um = 3695100 nm, orient = FW)
    ("PAD_R01", "IPAD20", 3695100, 350900, "FW"),
    ("PAD_R02", "IPAD20", 3695100, 701000, "FW"),
    ("PAD_R03", "IPAD20", 3695100, 1051000, "FW"),
    ("PAD_R04_PVSS", "PVSS01", 3695100, 1400000, "FW"),
    ("PAD_R05", "IPAD20", 3695100, 1751000, "FW"),
    ("PAD_R06", "IPAD20", 3695100, 2100900, "FW"),
    ("PAD_R07_PVDD", "PVDD01", 3695100, 2450000, "FW"),
    ("PAD_R08", "OPAD02", 3695100, 2801000, "FW"),
    ("PAD_R09", "OPAD02", 3695100, 3151000, "FW"),
    ("PAD_R10", "OPAD02", 3695100, 3501000, "FW"),

    # Top Edge (y = 3695.1 um = 3695100 nm, orient = N)
    ("PAD_T01", "OPAD02", 350900, 3695100, "N"),
    ("PAD_T02", "OPAD02", 701000, 3695100, "N"),
    ("PAD_T03", "OPAD02", 1051000, 3695100, "N"),
    ("PAD_T04_PVDD", "PVDD01", 1400000, 3695100, "N"),
    ("PAD_T05", "OPAD02", 1751000, 3695100, "N"),
    ("PAD_T06", "OPAD02", 2100900, 3695100, "N"),
    ("PAD_T07_PVSS", "PVSS01", 2450000, 3695100, "N"),
    ("PAD_T08", "OPAD02", 2801000, 3695100, "N"),
    ("PAD_T09", "OPAD02", 3151000, 3695100, "N"),
    ("PAD_T10", "OPAD02", 3501000, 3695100, "N"),
]

# Corners
corners = [
    ("CORNER_SW", "CORNER", 0, 0, "N"),
    ("CORNER_SE", "CORNER", 3695100, 0, "FN"),
    ("CORNER_NE", "CORNER", 3695100, 3695100, "S"),
    ("CORNER_NW", "CORNER", 0, 3695100, "FS"),
]

coord_pair_pattern = re.compile(r'\(\s*(\d+|\*)\s+(\d+|\*)\s*\)')

def shift_coords(match):
    x_str, y_str = match.group(1), match.group(2)
    if x_str == '*':
        new_x = '*'
    else:
        new_x = str(int(x_str) + DX)
    if y_str == '*':
        new_y = '*'
    else:
        new_y = str(int(y_str) + DY)
    return f"( {new_x} {new_y} )"

current_specialnet = None

with open(CORE_DEF, 'r') as fin, open(FULL_DEF, 'w') as fout:
    section = None
    
    for line in fin:
        # Header modifications
        if line.startswith("DESIGN"):
            fout.write("DESIGN fir2d_chip_4mmx4mm ;\n")
            continue
        if line.startswith("DIEAREA"):
            fout.write("DIEAREA ( 0 0 ) ( 4000000 4000000 ) ;\n")
            continue
        if line.startswith("ROW "):
            parts = line.split()
            parts[3] = str(int(parts[3]) + DX)
            parts[4] = str(int(parts[4]) + DY)
            fout.write(" ".join(parts) + "\n")
            continue
        if line.startswith("TRACKS "):
            parts = line.split()
            parts[2] = str(int(parts[2]) + (DX if parts[1] == 'X' else DY))
            fout.write(" ".join(parts) + "\n")
            continue
        if line.startswith("GCELLGRID "):
            parts = line.split()
            parts[2] = str(int(parts[2]) + (DX if parts[1] == 'X' else DY))
            fout.write(" ".join(parts) + "\n")
            continue
            
        if line.startswith("COMPONENTS"):
            count = int(line.split()[1])
            new_count = count + len(pads) + len(corners)
            fout.write(f"COMPONENTS {new_count} ;\n")
            # Write pads & corners first
            for inst_name, macro, x, y, ori in corners:
                fout.write(f"    - {inst_name} {macro} + PLACED ( {x} {y} ) {ori} ;\n")
            for inst_name, macro, x, y, ori in pads:
                fout.write(f"    - {inst_name} {macro} + PLACED ( {x} {y} ) {ori} ;\n")
            section = "COMPONENTS"
            continue
            
        if section == "COMPONENTS":
            if line.strip() == "END COMPONENTS":
                fout.write("END COMPONENTS\n")
                section = None
                continue
            shifted_line = coord_pair_pattern.sub(shift_coords, line)
            fout.write(shifted_line)
            continue

        if line.startswith("PINS"):
            fout.write(line)
            section = "PINS"
            continue

        if section == "PINS":
            if line.strip() == "END PINS":
                fout.write("END PINS\n")
                section = None
                continue
            shifted_line = coord_pair_pattern.sub(shift_coords, line)
            fout.write(shifted_line)
            continue

        if line.startswith("SPECIALNETS"):
            fout.write(line)
            section = "SPECIALNETS"
            continue

        if section == "SPECIALNETS":
            if line.strip().startswith("- VDD "):
                current_specialnet = "VDD"
            elif line.strip().startswith("- VSS "):
                current_specialnet = "VSS"

            if line.strip() == "END SPECIALNETS":
                fout.write("END SPECIALNETS\n")
                section = None
                current_specialnet = None
                continue

            # If this line ends a specialnet statement with ';'
            if line.rstrip().endswith(";") and current_specialnet in ("VDD", "VSS"):
                line_without_semi = line.rstrip()[:-1].rstrip()
                shifted_line = coord_pair_pattern.sub(shift_coords, line_without_semi)
                fout.write(shifted_line + "\n")
                
                if current_specialnet == "VDD":
                    fout.write("      NEW metal2 20000 + SHAPE STRIPE ( 2525600 304900 ) ( 2525600 501500 )\n")
                    fout.write("      NEW metal2 20000 + SHAPE STRIPE ( 1475600 3458800 ) ( 1475600 3695100 )\n")
                    fout.write("      NEW metal1 20000 + SHAPE STRIPE ( 304900 1475600 ) ( 458000 1475600 )\n")
                    fout.write("      NEW metal1 20000 + SHAPE STRIPE ( 3542000 2525600 ) ( 3695100 2525600 ) ;\n")
                elif current_specialnet == "VSS":
                    fout.write("      NEW metal2 20000 + SHAPE STRIPE ( 1475600 304900 ) ( 1475600 513500 )\n")
                    fout.write("      NEW metal2 20000 + SHAPE STRIPE ( 2525600 3446800 ) ( 2525600 3695100 )\n")
                    fout.write("      NEW metal1 20000 + SHAPE STRIPE ( 304900 2525600 ) ( 470000 2525600 )\n")
                    fout.write("      NEW metal1 20000 + SHAPE STRIPE ( 3530000 1475600 ) ( 3695100 1475600 ) ;\n")
                current_specialnet = None
                continue

            shifted_line = coord_pair_pattern.sub(shift_coords, line)
            fout.write(shifted_line)
            continue

        if line.startswith("NETS"):
            fout.write(line)
            section = "NETS"
            continue

        if section == "NETS":
            shifted_line = coord_pair_pattern.sub(shift_coords, line)
            fout.write(shifted_line)
            continue

        fout.write(line)

import shutil
shutil.copyfile(FULL_DEF, ROUTING_DEF)

print(f"[SUCCESS] Generated Full Chip DEF: {FULL_DEF}")
file_size = os.path.getsize(FULL_DEF)
print(f"File size: {file_size:,} bytes")
