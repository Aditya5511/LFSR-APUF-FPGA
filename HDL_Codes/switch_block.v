`timescale 1ns/1ps

(* DONT_TOUCH = "TRUE" *)
module switch_block(

    input  wire challenge,
    input  wire top_in,
    input  wire bottom_in,

    output wire top_out,
    output wire bottom_out

);

assign top_out    = challenge ? bottom_in : top_in;
assign bottom_out = challenge ? top_in    : bottom_in;

endmodule