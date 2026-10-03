# ==============================================================================
# Post-Route Static Timing Analysis for 2D FIR Filter ASIC (SCL 1.2 um)
# ==============================================================================

read_lef /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/pdk_scl_1p2um/digital_c1d/lef/tech_c1d.lef
read_lef /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/pdk_scl_1p2um/digital_c1d/lef/core_c1d.lef
read_liberty /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/pdk_scl_1p2um/digital_c1d/lib/c1d_core_typ.lib

read_def /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/routing/fir2d_routed.def
read_spef /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/sta/fir2d.spef

read_sdc /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/constraints/fir2d.sdc

# Generate comprehensive timing reports
report_checks -path_delay min_max -fields {slew cap input nets fanout} -format full_clock_expanded > /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/reports/post_route_timing.rpt
report_wns >> /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/reports/post_route_timing.rpt
report_tns >> /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/reports/post_route_timing.rpt
report_clock_skew >> /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/reports/post_route_timing.rpt
report_check_types -max_slew -max_capacitance -max_fanout >> /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/reports/post_route_timing.rpt

write_sdf /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/sta/fir2d.sdf
report_design_area > /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/reports/physical_area.rpt

puts "INFO: Post-route STA completed successfully."
exit
