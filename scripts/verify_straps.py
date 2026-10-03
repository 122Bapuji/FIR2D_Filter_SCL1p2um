import pya

ly = pya.Layout()
ly.read('/mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/gds/fir2d_chip_4mmx4mm.gds')
top = ly.top_cell()
dbu = ly.dbu
m1 = ly.layer(8, 0)
m2 = ly.layer(10, 0)
via1 = ly.layer(9, 0)

print('--- Metal 1 Power Straps in Top Cell ---')
for s in top.shapes(m1).each():
    if s.is_box():
        b = s.box
        w, h = b.width()*dbu, b.height()*dbu
        if (w >= 15 or h >= 15) and w < 3000 and h < 3000:
            print(f'M1 Box: ({b.left*dbu:.1f}, {b.bottom*dbu:.1f}) to ({b.right*dbu:.1f}, {b.top*dbu:.1f}) w={w:.1f}, h={h:.1f}')

print('\n--- Metal 2 Power Straps in Top Cell ---')
for s in top.shapes(m2).each():
    if s.is_box():
        b = s.box
        w, h = b.width()*dbu, b.height()*dbu
        if (w >= 15 or h >= 15) and w < 3000 and h < 3000:
            print(f'M2 Box: ({b.left*dbu:.1f}, {b.bottom*dbu:.1f}) to ({b.right*dbu:.1f}, {b.top*dbu:.1f}) w={w:.1f}, h={h:.1f}')

via_count = sum(1 for _ in top.shapes(via1).each())
print(f'\nTotal VIA1 shapes in top cell: {via_count}')
