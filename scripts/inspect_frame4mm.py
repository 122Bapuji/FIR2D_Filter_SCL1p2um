import pya

frame_gds = '/mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/padframe/PadFrame_C1D/pad_frame_gds/frame4mmx4mm.gds'
ly = pya.Layout()
ly.read(frame_gds)
top = ly.top_cell()
dbu = ly.dbu
print(f"Top cell: {top.name}")
print(f"Die BBox: ({top.bbox().left*dbu}, {top.bbox().bottom*dbu}) to ({top.bbox().right*dbu}, {top.bbox().top*dbu}) um")

labels = {}
m2_lbl = ly.layer(10, 7)
for s in top.shapes(m2_lbl).each():
    if s.is_text():
        t = s.text
        if t.string.startswith('PAD') and not t.string.endswith('_OUT'):
            labels[t.string] = (t.x*dbu, t.y*dbu)

print(f"Found {len(labels)} PAD labels:")
for k, v in sorted(labels.items(), key=lambda x: int(x[0][3:])):
    print(f"  {k}: ({v[0]:.2f}, {v[1]:.2f}) um")
