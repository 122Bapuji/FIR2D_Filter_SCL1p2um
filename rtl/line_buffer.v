// ==============================================================================
// 2D FIR Filter for Real-Time Image Processing
// Target Technology: SCL 1.2 um CMOS (scl_c1d)
// Architecture: Compact Area-Optimized Line Buffer
// ==============================================================================

`timescale 1ns / 1ps

module line_buffer #(
    parameter DATA_WIDTH  = 8,
    parameter LINE_LENGTH = 8
)(
    input  wire                  clk,
    input  wire                  rst_n,
    input  wire                  shift_en,
    input  wire [DATA_WIDTH-1:0] din,
    output wire [DATA_WIDTH-1:0] dout
);

    reg [DATA_WIDTH-1:0] buffer [0:LINE_LENGTH-1];
    integer i;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            for (i = 0; i < LINE_LENGTH; i = i + 1) begin
                buffer[i] <= {DATA_WIDTH{1'b0}};
            end
        end else if (shift_en) begin
            buffer[0] <= din;
            for (i = 1; i < LINE_LENGTH; i = i + 1) begin
                buffer[i] <= buffer[i-1];
            end
        end
    end

    assign dout = buffer[LINE_LENGTH-1];

endmodule
