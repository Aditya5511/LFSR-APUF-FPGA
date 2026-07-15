`timescale 1ns/1ps

module lfsr_apuf_boolean_top(

    input         clk,
    input  [15:0] sw,
    input  [3:0]  btn,

    output [15:0] led

);

//--------------------------------------------------
// Internal Signals
//--------------------------------------------------

wire [3:0] obfuscated_challenge;

wire response;

wire shift_en_debug;
wire start_apuf_debug;

//--------------------------------------------------
// Instantiate Core Design
//--------------------------------------------------

lfsr_apuf_paper_top DUT(

    .clk(clk),
    .reset(btn[0]),

    .challenge_in(sw[7:0]),

    .obfuscated_challenge(obfuscated_challenge),
    .response(response),

    .shift_en_debug(shift_en_debug),
    .start_apuf_debug(start_apuf_debug)

);

//--------------------------------------------------
// LED Mapping
//--------------------------------------------------

// LED0-LED3 : Obfuscated Challenge
assign led[3:0] = obfuscated_challenge;

// LED4-LED7 : Original Challenge (Lower 4 bits)
assign led[7:4] = sw[3:0];

// LED8 : LFSR shifting
assign led[8] = shift_en_debug;

// LED9 : PUF Trigger
assign led[9] = start_apuf_debug;

// LED10-LED14 : OFF
assign led[14:10] = 5'b00000;

// LED15 : Final Response
assign led[15] = response;

endmodule