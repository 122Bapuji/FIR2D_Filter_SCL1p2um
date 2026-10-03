import pya
import sys

tech_lef = '/mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/pdk_scl_1p2um/digital_c1d/lef/tech_c1d.lef'
core_lef = '/mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/pdk_scl_1p2um/digital_c1d/lef/core_c1d.lef'
core_gds = '/mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/pdk_scl_1p2um/digital_c1d/gds/core_c1d.gds'
map_file = '/mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/pdk_scl_1p2um/libs.tech/klayout/tech/scl_c1d.map'
def_file = '/mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/routing/fir2d_routed.def'
out_gds  = '/mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/gds/fir2d_core.gds'

print("Configuring KLayout LEF/DEF reader...")
opt = pya.LoadLayoutOptions()
cfg = opt.lefdef_config
cfg.lef_files = [tech_lef, core_lef]
cfg.macro_layout_files = [core_gds]
cfg.map_file = map_file
cfg.read_lef_with_def = True

ly = pya.Layout()
print("Reading routed DEF...")
ly.read(def_file, opt)

top = ly.top_cell()
print(f"Success! Top cell: {top.name}")
print(f"Top cell bbox: ({top.bbox().left*ly.dbu}, {top.bbox().bottom*ly.dbu}) to ({top.bbox().right*ly.dbu}, {top.bbox().top*ly.dbu}) um")
print(f"Total cells in layout: {ly.cells()}")

ly.write(out_gds)
print(f"Core GDS saved successfully to {out_gds}!")
