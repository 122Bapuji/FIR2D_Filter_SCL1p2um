import pya
import os

gds_path = "/mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/gds/fir2d_chip_4mmx4mm.gds"
lyp_path = "/mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/pdk_scl_1p2um/libs.tech/klayout/tech/scl_c1d.lyp"
img_dir  = "/mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/plots"

os.makedirs(img_dir, exist_ok=True)

ly = pya.Layout()
ly.read(gds_path)

view = pya.LayoutView()
view.show_layout(ly, True)
if os.path.exists(lyp_path):
    view.load_layer_props(lyp_path)
    print("Loaded SCL 1.2um layer properties (scl_c1d.lyp)")

# Set hierarchy depth to show all details
view.max_hier()

# 1. Full Chip Layout (4mm x 4mm)
view.zoom_fit()
out_full = os.path.join(img_dir, "chip_full_layout.png")
view.save_image(out_full, 2400, 2400)
print(f"Saved: {out_full}")

# 2. Core Layout Detailed (zoom to core area: (300, 300) to (3700, 3700) um)
core_box = pya.DBox(250.0, 250.0, 3750.0, 3750.0)
view.zoom_box(core_box)
out_core = os.path.join(img_dir, "core_layout_detailed.png")
view.save_image(out_core, 2400, 2400)
print(f"Saved: {out_core}")

# 3. Pad Frame Corner (zoom to corner: (0, 0) to (1200, 1200) um)
corner_box = pya.DBox(0.0, 0.0, 1200.0, 1200.0)
view.zoom_box(corner_box)
out_corner = os.path.join(img_dir, "pad_frame_corner.png")
view.save_image(out_corner, 1800, 1800)
print(f"Saved: {out_corner}")

# 4. Core to Pad Interconnect (zoom to right side transition: (3300, 1500) to (3900, 2100) um)
interconnect_box = pya.DBox(3300.0, 1500.0, 3950.0, 2200.0)
view.zoom_box(interconnect_box)
out_inter = os.path.join(img_dir, "core_to_pad_interconnect.png")
view.save_image(out_inter, 1800, 1800)
print(f"Saved: {out_inter}")

print("All layout renders generated successfully!")
