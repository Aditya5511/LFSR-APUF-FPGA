`timescale 1ns/1ps

module control_unit(

    input clk,
    input reset,

    input [3:0] C2,

    output reg shift_en,
    output reg start_apuf

);

reg [1:0] state;
reg [3:0] count;

parameter IDLE      = 2'b00;
parameter SHIFTING  = 2'b01;
parameter START_PUF = 2'b10;

always @(posedge clk)
begin

    if(reset)
    begin

        state <= IDLE;
        count <= 0;

        shift_en <= 0;
        start_apuf <= 0;

    end

    else
    begin

        case(state)

        IDLE:
        begin

            count <= 0;

            shift_en <= 0;
            start_apuf <= 0;

            state <= SHIFTING;

        end

        SHIFTING:
        begin

            shift_en <= 1;
            start_apuf <= 0;

            if(count == C2-1)
            begin

                count <= 0;
                state <= START_PUF;

            end

            else
            begin

                count <= count + 1;

            end

        end

        START_PUF:
        begin

            shift_en <= 0;

            start_apuf <= 1;

            state <= IDLE;

        end

        default:
        begin

            state <= IDLE;

        end

        endcase

    end

end

endmodule