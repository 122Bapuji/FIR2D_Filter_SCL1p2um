import pya

frame_gds = '/mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/padframe/PadFrame_C1D/pad_frame_gds/frame4mmx4mm.gds'
ly = pya.Layout()
ly.read(frame_gds)
top = ly.top_cell()
dbu = ly.dbu

print("Listing all instances in frame4mmx4mm:")
for inst in top.each_inst():
    c = ly.cell(inst.cell_index)
    trans = inst.trans
    bbox = c.bbox().transformed(trans)
    print(f"Cell: {c.name:10s} at ({trans.disp.x*dbu:8.2f}, {trans.disp.y*dbu:8.2f}) center=({bbox.center().x*dbu:8.2f}, {bbox.center().y*dbu:8.2f}) trans={trans.to_s()}")
