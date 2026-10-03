import pya

ly = pya.Layout()
ly.read('/mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/gds/fir2d_chip_4mmx4mm.gds')
top = ly.top_cell()
dbu = ly.dbu

print(f"Top cell: {top.name}")
print(f"BBox: ({top.bbox().left*dbu}, {top.bbox().bottom*dbu}) to ({top.bbox().right*dbu}, {top.bbox().top*dbu})")

for inst in top.each_inst():
    c = ly.cell(inst.cell_index)
    t = inst.trans
    print(f"Inst cell={c.name:10s} pos=({t.disp.x*dbu:.1f}, {t.disp.y*dbu:.1f}) rot={t.angle} mir={t.is_mirror()}")
