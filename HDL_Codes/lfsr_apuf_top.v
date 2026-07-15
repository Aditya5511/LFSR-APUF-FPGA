`timescale 1ns/1ps

module lfsr_apuf_top(

input clk,
input reset,

output [3:0] challenge,
output response

);

wire top_out;
wire bottom_out;

wire shift_en;
wire start_apuf;

control_unit CU(

.clk(clk),
.reset(reset),
.C2(4'd6),
.shift_en(shift_en),
.start_apuf(start_apuf)

);

lfsr4 L1(

.clk(clk),
.reset(reset),
.shift_en(shift_en),
.q(challenge)

);

apuf4 P1(

.challenge(challenge),
.top_in(1'b1),
.bottom_in(1'b0),
.top_out(top_out),
.bottom_out(bottom_out)

);

arbiter A1(

.top(top_out),
.bottom(bottom_out),
.response(response)

);

endmodule