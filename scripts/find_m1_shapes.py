import pya

ly = pya.Layout()
ly.read('/mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/gds/fir2d_core.gds')
top = ly.top_cell()
dbu = ly.dbu
m1 = ly.layer(8, 0)

print("Horizontal M1 shapes with width >= 500 um:")
for s in top.shapes(m1).each():
    if s.is_box():
        b = s.box
        w = b.width() * dbu
        h = b.height() * dbu
        if w >= 500:
            print(f"  M1 Box: ({b.left*dbu:.1f}, {b.bottom*dbu:.1f}) to ({b.right*dbu:.1f}, {b.top*dbu:.1f}) w={w:.1f}, h={h:.1f}")
