import pya

ly = pya.Layout()
ly.read('/mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/gds/fir2d_chip_4mmx4mm.gds')
top = ly.top_cell()
dbu = ly.dbu

pad_insts = []
for inst in top.each_inst():
    c = ly.cell(inst.cell_index)
    if any(p in c.name for p in ['IPAD', 'OPAD', 'PVDD', 'PVSS']):
        t = inst.trans
        bbox = c.bbox().transformed(t)
        pad_insts.append((c.name, t.disp.x*dbu, t.disp.y*dbu, t.angle, t.is_mirror(), bbox.left*dbu, bbox.bottom*dbu, bbox.right*dbu, bbox.top*dbu))

print(f'Total pad instances found: {len(pad_insts)}')
for p in pad_insts:
    print(f"cell={p[0]:8s} pos=({p[1]:6.1f}, {p[2]:6.1f}) angle={p[3]} mir={str(p[4]):5s} bbox=({p[5]:6.1f}, {p[6]:6.1f}) to ({p[7]:6.1f}, {p[8]:6.1f})")
