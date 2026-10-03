import pya

ly = pya.Layout()
ly.read('/mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/gds/fir2d_core.gds')
top = ly.top_cell()
dbu = ly.dbu
print(f"Top cell: {top.name}")
for li in ly.layer_indexes():
    info = ly.get_info(li)
    print(f"Layer {info.layer}/{info.datatype}: {top.shapes(li).size()} shapes")
