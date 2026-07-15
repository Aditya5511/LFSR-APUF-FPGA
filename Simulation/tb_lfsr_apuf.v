`timescale 1ns/1ps

module tb_crp_generator;

reg clk;
reg reset;

reg [7:0] challenge_in;

wire [3:0] obfuscated_challenge;
wire response;

integer outfile;
integer i;

lfsr_apuf_paper_top DUT(

    .clk(clk),
    .reset(reset),

    .challenge_in(challenge_in),

    .obfuscated_challenge(obfuscated_challenge),
    .response(response)

);

/////////////////////////////////////////////////////
// Clock
/////////////////////////////////////////////////////

initial
begin
    clk = 0;
    forever #5 clk = ~clk;
end

/////////////////////////////////////////////////////
// Test
/////////////////////////////////////////////////////

initial
begin

    outfile = $fopen("CRP_Output.txt","w");

    if(outfile == 0)
    begin
        $display("ERROR : File could not be opened.");
        $finish;
    end

    $display("File opened successfully.");

    //------------------------------------------------
    // Reset
    //------------------------------------------------

    reset = 1;
    challenge_in = 8'b0;

    repeat(10)
        @(posedge clk);

    reset = 0;

    $display("Reset Released");

    //------------------------------------------------
    // Generate CRPs
    //------------------------------------------------

    for(i=0;i<10000;i=i+1)
    begin

        challenge_in = $random;

        repeat(20)
            @(posedge clk);

        $display("Challenge=%b  LFSR=%b  Response=%b",
                  challenge_in,
                  obfuscated_challenge,
                  response);

        // Write Challenge, LFSR Output and Response
        $fwrite(outfile,"%b %b %b\n",
                challenge_in,
                obfuscated_challenge,
                response);

    end

    $display("Finished Writing.");

    $fclose(outfile);

    $finish;

end

endmodule