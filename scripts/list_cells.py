import pya

ly = pya.Layout()
ly.read('/mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/padframe/PadFrame_C1D/pad_frame_gds/frame4mmx4mm.gds')
print("All cells in frame4mmx4mm.gds:")
for c in ly.each_cell():
    print(f"  {c.name:20s}")
