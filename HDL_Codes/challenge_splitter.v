`timescale 1ns/1ps

module challenge_splitter(

    input  [7:0] challenge,
    output [3:0] C1,
    output [3:0] C2

);

assign C1 = challenge[7:4];
assign C2 = challenge[3:0];

endmodule