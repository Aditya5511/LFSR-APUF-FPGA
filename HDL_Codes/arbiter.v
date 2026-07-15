`timescale 1ns/1ps

(* DONT_TOUCH = "TRUE" *)
module arbiter(

    input top,
    input bottom,

    output response

);

assign response = top;

endmodule