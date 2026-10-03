// ==============================================================================
// 3x3 Convolution Engine for 2D FIR Filter (Resource-Shared Architecture)
// Single Shared Adder Tree across all 4 Convolution Modes
// ==============================================================================

`timescale 1ns / 1ps

module conv_engine_3x3 #(
    parameter DATA_WIDTH = 8
)(
    input  wire                   clk,
    input  wire                   rst_n,
    input  wire                   valid_in,
    input  wire [1:0]             mode,
    input  wire [DATA_WIDTH-1:0]  p00, p01, p02,
    input  wire [DATA_WIDTH-1:0]  p10, p11, p12,
    input  wire [DATA_WIDTH-1:0]  p20, p21, p22,
    output reg  [DATA_WIDTH-1:0]  pixel_out,
    output reg                    valid_out
);

    // Form signed 12-bit pixel words
    wire signed [11:0] pix00 = {4'b0000, p00};
    wire signed [11:0] pix01 = {4'b0000, p01};
    wire signed [11:0] pix02 = {4'b0000, p02};
    wire signed [11:0] pix10 = {4'b0000, p10};
    wire signed [11:0] pix11 = {4'b0000, p11};
    wire signed [11:0] pix12 = {4'b0000, p12};
    wire signed [11:0] pix20 = {4'b0000, p20};
    wire signed [11:0] pix21 = {4'b0000, p21};
    wire signed [11:0] pix22 = {4'b0000, p22};

    // Shared coefficient multiplication (shift and negate)
    reg signed [12:0] prod00, prod01, prod02;
    reg signed [12:0] prod10, prod11, prod12;
    reg signed [12:0] prod20, prod21, prod22;

    always @(*) begin
        case (mode)
            // 2'b00: Gaussian [1 2 1; 2 4 2; 1 2 1]
            2'b00: begin
                prod00 = pix00;
                prod01 = pix01 <<< 1;
                prod02 = pix02;

                prod10 = pix10 <<< 1;
                prod11 = pix11 <<< 2;
                prod12 = pix12 <<< 1;

                prod20 = pix20;
                prod21 = pix21 <<< 1;
                prod22 = pix22;
            end

            // 2'b01: Sharpening [0 -1 0; -1 5 -1; 0 -1 0]
            2'b01: begin
                prod00 = 13'sd0;
                prod01 = -pix01;
                prod02 = 13'sd0;

                prod10 = -pix10;
                prod11 = (pix11 <<< 2) + pix11;
                prod12 = -pix12;

                prod20 = 13'sd0;
                prod21 = -pix21;
                prod22 = 13'sd0;
            end

            // 2'b10: Sobel X [-1 0 1; -2 0 2; -1 0 1]
            2'b10: begin
                prod00 = -pix00;
                prod01 = 13'sd0;
                prod02 = pix02;

                prod10 = -(pix10 <<< 1);
                prod11 = 13'sd0;
                prod12 = pix12 <<< 1;

                prod20 = -pix20;
                prod21 = 13'sd0;
                prod22 = pix22;
            end

            // 2'b11: Laplacian [-1 -1 -1; -1 8 -1; -1 -1 -1]
            default: begin
                prod00 = -pix00;
                prod01 = -pix01;
                prod02 = -pix02;

                prod10 = -pix10;
                prod11 = pix11 <<< 3;
                prod12 = -pix12;

                prod20 = -pix20;
                prod21 = -pix21;
                prod22 = -pix22;
            end
        endcase
    end

    // Pipeline Stage 1: Registered Row Accumulators
    reg signed [14:0] sum_row0, sum_row1, sum_row2;
    reg [1:0]         pipe_mode;
    reg               pipe_valid;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            sum_row0   <= 15'sd0;
            sum_row1   <= 15'sd0;
            sum_row2   <= 15'sd0;
            pipe_mode  <= 2'b00;
            pipe_valid <= 1'b0;
        end else begin
            sum_row0   <= prod00 + prod01 + prod02;
            sum_row1   <= prod10 + prod11 + prod12;
            sum_row2   <= prod20 + prod21 + prod22;
            pipe_mode  <= mode;
            pipe_valid <= valid_in;
        end
    end

    // Pipeline Stage 2: Normalization, Clamping & Output
    wire signed [15:0] total_sum  = sum_row0 + sum_row1 + sum_row2;
    wire signed [15:0] gauss_norm = total_sum >>> 4;
    wire signed [15:0] abs_total  = (total_sum < 0) ? -total_sum : total_sum;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            pixel_out <= {DATA_WIDTH{1'b0}};
            valid_out <= 1'b0;
        end else begin
            valid_out <= pipe_valid;

            if (pipe_valid) begin
                if (pipe_mode == 2'b00) begin
                    if (gauss_norm < 0)
                        pixel_out <= 8'd0;
                    else if (gauss_norm > 16'sd255)
                        pixel_out <= 8'd255;
                    else
                        pixel_out <= gauss_norm[7:0];
                end else if (pipe_mode == 2'b01) begin
                    if (total_sum < 0)
                        pixel_out <= 8'd0;
                    else if (total_sum > 16'sd255)
                        pixel_out <= 8'd255;
                    else
                        pixel_out <= total_sum[7:0];
                end else begin
                    if (abs_total > 16'sd255)
                        pixel_out <= 8'd255;
                    else
                        pixel_out <= abs_total[7:0];
                end
            end else begin
                pixel_out <= 8'd0;
            end
        end
    end

endmodule
