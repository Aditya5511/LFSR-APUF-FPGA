`timescale 1ns/1ps

module top(

input [3:0] challenge,

input top_in,
input bottom_in,

output response

);

wire top_out;
wire bottom_out;

apuf4 puf(

.challenge(challenge),
.top_in(top_in),
.bottom_in(bottom_in),
.top_out(top_out),
.bottom_out(bottom_out)

);

arbiter arb(

.top(top_out),
.bottom(bottom_out),
.response(response)

);

endmodule