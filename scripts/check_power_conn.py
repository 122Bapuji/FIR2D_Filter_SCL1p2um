import pya

ly = pya.Layout()
ly.read('/mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/gds/fir2d_chip_4mmx4mm.gds')
top = ly.top_cell()
dbu = ly.dbu

m1 = ly.layer(8, 0)
m2 = ly.layer(10, 0)

print("Checking instances of PVDD01 and PVSS01 in fir2d_chip_4mmx4mm:")
for inst in top.each_inst():
    c = ly.cell(inst.cell_index)
    if 'PVDD' in c.name or 'PVSS' in c.name:
        bbox = c.bbox().transformed(inst.trans)
        print(f"  {c.name:8s} bbox=({bbox.left*dbu:.1f}, {bbox.bottom*dbu:.1f}) to ({bbox.right*dbu:.1f}, {bbox.top*dbu:.1f}) um")

# Check core cell bounding box
core_cell = None
for inst in top.each_inst():
    c = ly.cell(inst.cell_index)
    if c.name == 'fir2d_top':
        core_cell = c
        bbox = c.bbox().transformed(inst.trans)
        print(f"\nCore cell 'fir2d_top' placed bbox: ({bbox.left*dbu:.1f}, {bbox.bottom*dbu:.1f}) to ({bbox.right*dbu:.1f}, {bbox.top*dbu:.1f}) um")

# Find top-level metal shapes that could be power straps
print("\nTop-level Metal 1 and Metal 2 shapes:")
for li, lname in [(m1, "Metal 1"), (m2, "Metal 2")]:
    shapes = list(top.shapes(li).each())
    print(f"  {lname}: {len(shapes)} shapes in top cell")
    for s in shapes[:15]:
        if s.is_box():
            b = s.box
            print(f"    Box: ({b.left*dbu:.1f}, {b.bottom*dbu:.1f}) to ({b.right*dbu:.1f}, {b.top*dbu:.1f}) width={b.width()*dbu:.1f} height={b.height()*dbu:.1f}")

