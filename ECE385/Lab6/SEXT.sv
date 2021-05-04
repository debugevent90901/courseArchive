module SEXT_5 (     input logic [15:0] IR,
                    output logic [15:0] OUT );
    always_comb  
    begin
        if (IR[4])
            OUT = {11'b11111111111, IR[4:0]};
        else 
            OUT = {11'b00000000000, IR[4:0]};
    end
endmodule


module SEXT_6 (     input logic [15:0] IR,
                    output logic [15:0] OUT );
    always_comb  
    begin
        if (IR[5])
            OUT = {10'b1111111111, IR[5:0]};
        else 
            OUT = {10'b0000000000, IR[5:0]};
    end
endmodule


module SEXT_9 (     input logic [15:0] IR,
                    output logic [15:0] OUT );
    always_comb  
    begin
        if (IR[8])
            OUT = {7'b1111111, IR[8:0]};
        else 
            OUT = {7'b0000000, IR[8:0]};
    end
endmodule


module SEXT_11 (     input logic [15:0] IR,
                    output logic [15:0] OUT );
    always_comb  
    begin
        if (IR[10])
            OUT = {5'b11111, IR[10:0]};
        else 
            OUT = {5'b00000, IR[10:0]};
    end
endmodule
