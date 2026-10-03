import pya

ly = pya.Layout()
ly.read('/mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/padframe/PadFrame_C1D/klayout/gds/io_pad_c1d.gds')
dbu = ly.dbu

m1 = ly.layer(8, 0)
m2 = ly.layer(10, 0)

for name in ['PVDD01', 'PVSS01', 'IPAD20', 'OPAD02']:
    c = ly.cell(name)
    print(f"\nCell {name} (BBox: {c.bbox().left*dbu:.1f}, {c.bbox().bottom*dbu:.1f} to {c.bbox().right*dbu:.1f}, {c.bbox().top*dbu:.1f}):")
    for li, lname in [(m1, "M1"), (m2, "M2")]:
        boxes = []
        for s in c.shapes(li).each():
            if s.is_box():
                boxes.append(s.box)
        print(f"  {lname}: {len(boxes)} boxes. Bounding box: {c.bbox_per_layer(li).left*dbu:.1f}, {c.bbox_per_layer(li).bottom*dbu:.1f} to {c.bbox_per_layer(li).right*dbu:.1f}, {c.bbox_per_layer(li).top*dbu:.1f}")
