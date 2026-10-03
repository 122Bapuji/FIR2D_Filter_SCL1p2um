// ==============================================================================
// 2D FIR Filter Core Top-Level Module
// Target Process: SCL 1.2 um CMOS (scl_c1d)
// ==============================================================================

`timescale 1ns / 1ps

module fir2d_top #(
    parameter DATA_WIDTH  = 8,
    parameter LINE_LENGTH = 8,
    parameter TOTAL_LINES = 8
)(
    input  wire                  clk,
    input  wire                  rst_n,
    input  wire                  valid_in,
    input  wire [1:0]            mode,
    input  wire [DATA_WIDTH-1:0] pixel_in,
    output wire [DATA_WIDTH-1:0] pixel_out,
    output wire                  valid_out,
    output reg                   line_done,
    output reg                   frame_done
);

    // -------------------------------------------------------------------------
    // Internal 3x3 Window Signals
    // -------------------------------------------------------------------------
    wire [DATA_WIDTH-1:0] p00, p01, p02;
    wire [DATA_WIDTH-1:0] p10, p11, p12;
    wire [DATA_WIDTH-1:0] p20, p21, p22;

    // Line / Column Counters for boundary and sync management
    reg [4:0] col_cnt;
    reg [4:0] row_cnt;
    reg       window_ready;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            col_cnt      <= 5'd0;
            row_cnt      <= 5'd0;
            window_ready <= 1'b0;
            line_done    <= 1'b0;
            frame_done   <= 1'b0;
        end else if (valid_in) begin
            // Column counting
            if (col_cnt == LINE_LENGTH - 1) begin
                col_cnt   <= 5'd0;
                line_done <= 1'b1;
                // Row counting
                if (row_cnt == TOTAL_LINES - 1) begin
                    row_cnt    <= 5'd0;
                    frame_done <= 1'b1;
                end else begin
                    row_cnt    <= row_cnt + 1'b1;
                    frame_done <= 1'b0;
                end
            end else begin
                col_cnt    <= col_cnt + 1'b1;
                line_done  <= 1'b0;
                frame_done <= 1'b0;
            end

            // 3x3 window is valid once 2 full lines + 2 pixels are received
            if (row_cnt >= 5'd2 && col_cnt >= 5'd2) begin
                window_ready <= 1'b1;
            end
        end else begin
            line_done  <= 1'b0;
            frame_done <= 1'b0;
        end
    end

    // Instantiate 3x3 Sliding Window with Line Buffers
    window_3x3 #(
        .DATA_WIDTH(DATA_WIDTH),
        .LINE_LENGTH(LINE_LENGTH)
    ) u_window (
        .clk(clk),
        .rst_n(rst_n),
        .shift_en(valid_in),
        .din(pixel_in),
        .p00(p00), .p01(p01), .p02(p02),
        .p10(p10), .p11(p11), .p12(p12),
        .p20(p20), .p21(p21), .p22(p22)
    );

    // Gate the valid signal to convolution engine once window is warmed up
    wire conv_valid_in = valid_in & window_ready;

    // Instantiate 3x3 Convolution Engine
    conv_engine_3x3 #(
        .DATA_WIDTH(DATA_WIDTH)
    ) u_conv (
        .clk(clk),
        .rst_n(rst_n),
        .valid_in(conv_valid_in),
        .mode(mode),
        .p00(p00), .p01(p01), .p02(p02),
        .p10(p10), .p11(p11), .p12(p12),
        .p20(p20), .p21(p21), .p22(p22),
        .pixel_out(pixel_out),
        .valid_out(valid_out)
    );

endmodule
