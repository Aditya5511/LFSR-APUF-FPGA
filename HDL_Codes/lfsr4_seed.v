`timescale 1ns/1ps

module lfsr4_seed(

    input clk,
    input reset,

    input load_seed,
    input [3:0] seed_in,

    input shift_en,

    output [3:0] q

);

reg [3:0] lfsr;

assign q = lfsr;

//----------------------------------------------------
// Maximal-length 4-bit LFSR
// Primitive Polynomial:
// x^4 + x + 1
//----------------------------------------------------

wire feedback;

assign feedback = lfsr[3] ^ lfsr[0];

always @(posedge clk)
begin

    if(reset)

        lfsr <= 4'b0001;      // never start from all zeros

    else if(load_seed)

    begin

        if(seed_in == 4'b0000)
            lfsr <= 4'b0001;
        else
            lfsr <= seed_in;

    end

    else if(shift_en)

    begin

        lfsr <= {lfsr[2:0], feedback};

    end

end

endmodule