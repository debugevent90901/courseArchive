module reg_16 ( input  logic Clk, Reset, Load,
                input  logic [15:0]  In,
                output logic [15:0]  Out);
    always_ff @ (posedge Clk)
    begin
        if (Reset)
            Out <= 16'h0;
        else if (Load)
            Out <= In;
    end
endmodule

module reg_1 (  input  logic Clk, Reset, Load,
                input  logic In,
                output logic Out);
    always_ff @ (posedge Clk)
    begin
        if (Reset)
            Out <= 1'b0;
        else if (Load)
            Out <= In;
    end
endmodule

module reg_12 (  input  logic Clk, Reset, Load,
                input  logic [11:0] In,
                output logic [11:0] Out);
    always_ff @ (posedge Clk)
    begin
        if (Reset)
            Out <= 11'b0;
        else if (Load)
            Out <= In;
    end
endmodule