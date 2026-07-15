`timescale 1ns/1ps

module lfsr4(

input clk,
input reset,
input shift_en,

output [3:0] q

);

reg [3:0] lfsr;

assign q = lfsr;

always @(posedge clk)

begin

    if(reset)

        lfsr <= 4'b1011;

    else if(shift_en)

    begin

        lfsr[0] <= lfsr[3];
        lfsr[1] <= lfsr[0];
        lfsr[2] <= lfsr[1] ^ lfsr[3];
        lfsr[3] <= lfsr[2];

    end

end

endmodule