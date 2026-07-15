`timescale 1ns/1ps

module obfuscator4(

input [3:0] ext_challenge,
input [3:0] lfsr_challenge,

output [3:0] obf_challenge

);

assign obf_challenge = ext_challenge ^ lfsr_challenge;

endmodule