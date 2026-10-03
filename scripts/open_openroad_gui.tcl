# ==============================================================================
# Tcl script to open the complete 2D FIR Filter in OpenROAD GUI
# ==============================================================================

read_lef /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/pdk_scl_1p2um/digital_c1d/lef/tech_c1d.lef
read_lef /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/pdk_scl_1p2um/digital_c1d/lef/core_c1d.lef
read_lef /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/pdk_scl_1p2um/digital_c1d/lef/io_c1d.lef
read_lef /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/pdk_scl_1p2um/digital_c1d/lef/corner_c1d.lef

read_def /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/database/fir2d_chip_4mmx4mm.def

puts "========================================================================"
puts "SUCCESS: Loaded Complete 4mm x 4mm SCL 1.2um 2D FIR Filter Chip into OpenROAD GUI!"
puts "Includes 40 Peripheral Pads, 4 Corners, Routed Core, and 20um Power Straps"
puts "========================================================================"
