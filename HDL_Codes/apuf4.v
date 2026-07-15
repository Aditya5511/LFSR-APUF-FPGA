`timescale 1ns/1ps

module apuf4(

    input  [3:0] challenge,

    input  top_in,
    input  bottom_in,

    output top_out,
    output bottom_out

);

(* KEEP = "TRUE" *) wire t1,b1;
(* KEEP = "TRUE" *) wire t2,b2;
(* KEEP = "TRUE" *) wire t3,b3;

(* DONT_TOUCH = "TRUE" *)
switch_block s1(

    .challenge(challenge[3]),
    .top_in(top_in),
    .bottom_in(bottom_in),
    .top_out(t1),
    .bottom_out(b1)

);

(* DONT_TOUCH = "TRUE" *)
switch_block s2(

    .challenge(challenge[2]),
    .top_in(t1),
    .bottom_in(b1),
    .top_out(t2),
    .bottom_out(b2)

);

(* DONT_TOUCH = "TRUE" *)
switch_block s3(

    .challenge(challenge[1]),
    .top_in(t2),
    .bottom_in(b2),
    .top_out(t3),
    .bottom_out(b3)

);

(* DONT_TOUCH = "TRUE" *)
switch_block s4(

    .challenge(challenge[0]),
    .top_in(t3),
    .bottom_in(b3),
    .top_out(top_out),
    .bottom_out(bottom_out)

);

endmodule