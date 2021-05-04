module mux_2(   input logic SELECT,
                input logic [15:0] A,B,
                output logic [15:0] OUT );

    always_comb
    begin
        if (SELECT)
            OUT = B;
        else
            OUT = A;
    end

endmodule

module mux_3(   input  logic [1:0]  SELECT,
                input  logic [15:0] A,B,C,
                output logic [15:0] OUT     );

    always_comb
    begin
        case (SELECT)
            2'b00 : OUT = A;
            2'b01 : OUT = B;
            default : OUT = C;
        endcase
    end 
    
endmodule

module mux_4(   input  logic [1:0]  SELECT,
                input  logic [15:0] A,B,C,D,
                output logic [15:0] OUT     );

    always_comb
    begin
        case (SELECT)
            2'b00 : OUT = A;
            2'b01 : OUT = B;
            2'b10 : OUT = C;
            2'b11 : OUT = D;
        endcase
    end
    
endmodule

module mux_2_3bit(  input logic SELECT,
                            input logic  [2:0] A,B,
                            output logic [2:0] OUT );

    always_comb
    begin
        if (SELECT)
            OUT = B;
        else
            OUT = A;
    end

endmodule