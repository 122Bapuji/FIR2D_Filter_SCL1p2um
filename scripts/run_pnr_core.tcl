# ==============================================================================
# SCL 1.2 um Physical Design Script for 2D FIR Image Filter Core
# Floorplan Size: 3400 x 3400 um (Matched to SCL 4mm x 4mm Standard Pad Frame)
# ==============================================================================

# 1. Read Technology and Standard Cell LEF
read_lef /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/pdk_scl_1p2um/digital_c1d/lef/tech_c1d.lef
read_lef /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/pdk_scl_1p2um/digital_c1d/lef/core_c1d.lef

# 2. Read Timing Liberty
read_liberty /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/pdk_scl_1p2um/digital_c1d/lib/c1d_core_typ.lib

# 3. Read Gate-Level Netlist
read_verilog /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/synthesis/fir2d_gate.v
link_design fir2d_top

# 4. Read SDC Timing Constraints
read_sdc /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/constraints/fir2d.sdc

# 5. Floorplan: 3400 x 3400 um block cavity (fits inside 3390 x 3390 um 4mm die core)
initialize_floorplan -site CORE -die_area "0 0 3400 3400" -core_area "200 200 3200 3200"

# Remove alternating rows (SCL 1.2 um PDK rule to prevent well/diffusion overlaps)
set block [[ord::get_db_block] getRows]
set count 0
foreach row $block {
    if { [expr $count % 2] != 0 } {
        odb::dbRow_destroy $row
    }
    incr count
}
puts "INFO: Initialized floorplan with alternating rows removed ($count total rows evaluated)"
write_def /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/floorplan/fir2d_fp.def

# 6. Power Distribution Network (PDN)
add_global_connection -net VDD -pin_pattern VDD -power
add_global_connection -net VSS -pin_pattern VSS -ground
global_connect

set_voltage_domain -name CORE -power VDD -ground VSS
define_pdn_grid -name "Core_1" -voltage_domain CORE -pins "metal2"
set_pdnsim_net_voltage -net VDD -voltage 5.0
set_pdnsim_net_voltage -net VSS -voltage 0.0

add_pdn_stripe -grid "Core_1" -layer metal1 -width 9.0 -followpins -extend_to_core_ring
add_pdn_ring -grid "Core_1" -layer {"metal1" "metal2"} -widths "7 7" -spacings "5 5" -core_offsets "30 30"
add_pdn_connect -grid "Core_1" -layers {"metal1" "metal2"}

pdngen
write_def /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/power/fir2d_pdn.def
puts "INFO: PDN generated successfully."

# 7. Track generation and Pin placement matching padframe sides
make_tracks metal1 -x_offset 0.0 -x_pitch 4.0 -y_offset 0.0 -y_pitch 4.0
make_tracks metal2 -x_offset 0.0 -x_pitch 4.2 -y_offset 0.0 -y_pitch 4.2

set_io_pin_constraint -direction bottom -pin_names {clk rst_n valid_in {mode[0]} {mode[1]} {pixel_in[0]} {pixel_in[1]}}
set_io_pin_constraint -direction right  -pin_names {{pixel_in[2]} {pixel_in[3]} {pixel_in[4]} {pixel_in[5]} {pixel_in[6]}}
set_io_pin_constraint -direction top    -pin_names {{pixel_in[7]} {pixel_out[0]} {pixel_out[1]} {pixel_out[2]} {pixel_out[3]} {pixel_out[4]} {pixel_out[5]}}
set_io_pin_constraint -direction left   -pin_names {{pixel_out[6]} {pixel_out[7]} valid_out line_done frame_done}

place_pins -hor_layers {metal1} -ver_layers {metal2}
puts "INFO: IO pins placed according to pad assignments."

# 8. Placement
global_placement -density 0.65
puts "INFO: Global placement completed."

detailed_placement -max_displacement {1000 500}
puts "INFO: Detailed placement completed."
check_placement -verbose

write_def /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/placement/fir2d_placed.def
write_db /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/placement/fir2d_placed.odb

# 9. Clock Tree Synthesis (CTS)
set_cmd_units -time ns -capacitance pF -resistance kOhm -voltage V -current mA
create_clock -name clk -period 20.0 [get_ports clk]
set_propagated_clock [all_clocks]

clock_tree_synthesis -root_buf CDRI01 -buf_list "CDRI01" -sink_clustering_enable
repair_clock_nets
detailed_placement -max_displacement {1000 500}

report_cts -out_file /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/reports/cts.rpt
write_def /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/cts/fir2d_cts.def
write_db /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/cts/fir2d_cts.odb
puts "INFO: CTS completed."

# 10. Routing
set_global_routing_layer_adjustment metal1 0
set_global_routing_layer_adjustment metal2 0
set_routing_layers -signal metal1-metal2 -clock metal1-metal2

global_route -allow_congestion -verbose

detailed_route \
    -top_routing_layer metal2 \
    -via_in_pin_bottom_layer metal1 \
    -via_in_pin_top_layer metal2 \
    -verbose 1
puts "INFO: Detailed routing completed."

# 11. Filler placement
filler_placement -prefix FILLER [list "FILLER1" "FILLER2" "FILLER3" "FILLER4" "FILLER5"]
check_placement -verbose

write_def /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/routing/fir2d_routed.def
write_verilog -include_pwr_gnd /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/routing/fir2d_routed_pwr.v
write_verilog -remove_cells {FILLER1 FILLER2 FILLER3 FILLER4 FILLER5} /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/routing/fir2d_routed_sim.v

# 12. Extraction
define_process_corner -ext_model_index 0 /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/pdk_scl_1p2um/libs.tech/openrcx/scl_c1d.rcx.lib
extract_parasitics -ext_model_file /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/pdk_scl_1p2um/libs.tech/openrcx/scl_c1d.rcx.lib
write_spef /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/sta/fir2d.spef
puts "INFO: Parasitic extraction completed."

# 13. Post-layout Static Timing Analysis (STA)
read_sdc /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/constraints/fir2d.sdc
report_checks -path_delay min_max -fields {slew cap input nets fanout} -format full_clock_expanded > /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/reports/post_route_timing.rpt
report_wns >> /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/reports/post_route_timing.rpt
report_tns >> /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/reports/post_route_timing.rpt
report_clock_skew >> /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/reports/post_route_timing.rpt
report_check_types -max_slew -max_capacitance -max_fanout >> /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/reports/post_route_timing.rpt

write_sdf /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/sta/fir2d.sdf
puts "INFO: Post-route STA completed successfully."

# 14. Report Design Metrics
report_design_area > /mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/reports/physical_area.rpt
puts "INFO: Physical design core flow finished successfully."
exit
