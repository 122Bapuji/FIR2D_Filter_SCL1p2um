# ==============================================================================
# SDC Timing Constraints for 2D FIR Filter ASIC (SCL 1.2 um CMOS)
# ==============================================================================

set clk_period 20.0
set clk_port   [get_ports clk]

create_clock -name core_clk -period $clk_period $clk_port

set_clock_uncertainty 0.5 [get_clocks core_clk]
set_clock_transition 0.2 [get_clocks core_clk]

# Set I/O Delays explicitly on signal ports (excluding power/ground)
set signal_inputs [get_ports {rst_n valid_in mode* pixel_in*}]
set signal_outputs [get_ports {pixel_out* valid_out line_done frame_done}]

set_input_delay -clock core_clk 4.0 $signal_inputs
set_output_delay -clock core_clk 4.0 $signal_outputs

# Load and driving cell
set_driving_cell -lib_cell INVR02 $signal_inputs
set_load 0.05 $signal_outputs
