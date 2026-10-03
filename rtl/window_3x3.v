// ==============================================================================
// 3x3 Sliding Window Generator for 2D FIR Filter
// ==============================================================================

`timescale 1ns / 1ps

module window_3x3 #(
    parameter DATA_WIDTH  = 8,
    parameter LINE_LENGTH = 8
)(
    input  wire                  clk,
    input  wire                  rst_n,
    input  wire                  shift_en,
    input  wire [DATA_WIDTH-1:0] din,
    output reg  [DATA_WIDTH-1:0] p00, p01, p02,
    output reg  [DATA_WIDTH-1:0] p10, p11, p12,
    output reg  [DATA_WIDTH-1:0] p20, p21, p22
);

    wire [DATA_WIDTH-1:0] line0_dout;
    wire [DATA_WIDTH-1:0] line1_dout;

    // Line Buffer 1: delays current line by LINE_LENGTH pixels
    line_buffer #(
        .DATA_WIDTH(DATA_WIDTH),
        .LINE_LENGTH(LINE_LENGTH)
    ) lb1 (
        .clk(clk),
        .rst_n(rst_n),
        .shift_en(shift_en),
        .din(din),
        .dout(line1_dout)
    );

    // Line Buffer 2: delays previous line by LINE_LENGTH pixels
    line_buffer #(
        .DATA_WIDTH(DATA_WIDTH),
        .LINE_LENGTH(LINE_LENGTH)
    ) lb0 (
        .clk(clk),
        .rst_n(rst_n),
        .shift_en(shift_en),
        .din(line1_dout),
        .dout(line0_dout)
    );

    // Shift 3x3 window registers
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            p00 <= {DATA_WIDTH{1'b0}};
            p01 <= {DATA_WIDTH{1'b0}};
            p02 <= {DATA_WIDTH{1'b0}};

            p10 <= {DATA_WIDTH{1'b0}};
            p11 <= {DATA_WIDTH{1'b0}};
            p12 <= {DATA_WIDTH{1'b0}};

            p20 <= {DATA_WIDTH{1'b0}};
            p21 <= {DATA_WIDTH{1'b0}};
            p22 <= {DATA_WIDTH{1'b0}};
        end else if (shift_en) begin
            // Row 0 (Oldest line)
            p00 <= p01;
            p01 <= p02;
            p02 <= line0_dout;

            // Row 1 (Middle line)
            p10 <= p11;
            p11 <= p12;
            p12 <= line1_dout;

            // Row 2 (Current line)
            p20 <= p21;
            p21 <= p22;
            p22 <= din;
        end
    end

endmodule
