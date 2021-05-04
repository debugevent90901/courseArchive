module reg_file
(   input logic Clk, Reset, LD_REG,
    input logic [2:0] DR, SR1, SR2,
    input logic [15:0] BUS_IN,
    output logic [15:0] SR1_OUT, SR2_OUT
);

    logic [7:0][15:0] regs;
    
    always_ff @ (posedge Clk)
    begin
        if (Reset)
            begin
                regs[0] <= 16'h0000;
                regs[1] <= 16'h0000;
                regs[2] <= 16'h0000;
                regs[3] <= 16'h0000;
                regs[4] <= 16'h0000;
                regs[5] <= 16'h0000;    
                regs[6] <= 16'h0000;
                regs[7] <= 16'h0000;
            end

        else
            begin
                if (LD_REG)
                    begin
                        case(DR)
                            3'b000: regs[0] <= BUS_IN;
                            3'b001: regs[1] <= BUS_IN;
                            3'b010: regs[2] <= BUS_IN;
                            3'b011: regs[3] <= BUS_IN;
                            3'b100: regs[4] <= BUS_IN;
                            3'b101: regs[5] <= BUS_IN;
                            3'b110: regs[6] <= BUS_IN;
                            3'b111: regs[7] <= BUS_IN;
                        endcase
                    end
            end
    end
    
    always_comb
    begin
        case (SR1)
            3'b000: SR1_OUT = regs[0];
            3'b001: SR1_OUT = regs[1];
            3'b010: SR1_OUT = regs[2];
            3'b011: SR1_OUT = regs[3];
            3'b100: SR1_OUT = regs[4];
            3'b101: SR1_OUT = regs[5];
            3'b110: SR1_OUT = regs[6];
            3'b111: SR1_OUT = regs[7];
        endcase
        case (SR2)
            3'b000: SR2_OUT = regs[0];
            3'b001: SR2_OUT = regs[1];
            3'b010: SR2_OUT = regs[2];
            3'b011: SR2_OUT = regs[3];
            3'b100: SR2_OUT = regs[4];
            3'b101: SR2_OUT = regs[5];
            3'b110: SR2_OUT = regs[6];
            3'b111: SR2_OUT = regs[7];
        endcase
    end
endmodule
