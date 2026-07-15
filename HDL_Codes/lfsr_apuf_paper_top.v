`timescale 1ns/1ps

module lfsr_apuf_paper_top(

    input clk,
    input reset,

    input [7:0] challenge_in,

    output [3:0] obfuscated_challenge,
    output response,

    // Debug outputs
    output shift_en_debug,
    output start_apuf_debug

);

wire [3:0] C1;
wire [3:0] C2;

wire shift_en;
wire start_apuf;

wire top_out;
wire bottom_out;

reg load_seed;
reg seed_loaded;

reg response_reg;
wire response_wire;

//
// Challenge Splitter
//
challenge_splitter CS(

    .challenge(challenge_in),
    .C1(C1),
    .C2(C2)

);

//
// Control Unit
//
control_unit CU(

    .clk(clk),
    .reset(reset),
    .C2(C2),

    .shift_en(shift_en),
    .start_apuf(start_apuf)

);

//
// Export debug signals
//
assign shift_en_debug   = shift_en;
assign start_apuf_debug = start_apuf;

//
// Generate one-clock load_seed pulse
//
always @(posedge clk)
begin

    if(reset)
    begin
        load_seed   <= 1'b0;
        seed_loaded <= 1'b0;
    end

    else if(!seed_loaded)
    begin
        load_seed   <= 1'b1;
        seed_loaded <= 1'b1;
    end

    else
    begin
        load_seed <= 1'b0;
    end

end

//
// LFSR
//
lfsr4_seed LFSR(

    .clk(clk),
    .reset(reset),

    .load_seed(load_seed),
    .seed_in(C1),

    .shift_en(shift_en),

    .q(obfuscated_challenge)

);

//
// APUF
//
apuf4 PUF(

    .challenge(obfuscated_challenge),

    .top_in(1'b1),
    .bottom_in(1'b0),

    .top_out(top_out),
    .bottom_out(bottom_out)

);

//
// Arbiter
//
arbiter A1(

    .top(top_out),
    .bottom(bottom_out),

    .response(response_wire)

);

//
// Response Register
//
always @(posedge clk)
begin

    if(reset)
        response_reg <= 1'b0;

    else if(start_apuf)
        response_reg <= response_wire;

end

assign response = response_reg;

endmodule