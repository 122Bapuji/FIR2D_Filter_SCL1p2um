import pya

ly = pya.Layout()
ly.read('/mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/gds/fir2d_core.gds')
top = ly.top_cell()
dbu = ly.dbu

m1 = ly.layer(8, 0)
m2 = ly.layer(10, 0)

print("Finding long wide power ring shapes in fir2d_core.gds:")
for li, name in [(m1, "M1"), (m2, "M2")]:
    for s in top.shapes(li).each():
        if s.is_box():
            b = s.box
            w = b.width() * dbu
            h = b.height() * dbu
            if w >= 2000 or h >= 2000:
                print(f"  {name}: ({b.left*dbu:.1f}, {b.bottom*dbu:.1f}) to ({b.right*dbu:.1f}, {b.top*dbu:.1f}) w={w:.1f}, h={h:.1f}")
