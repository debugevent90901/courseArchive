module ALU( input logic [15:0] A, B,
            input logic [1:0] ALUK,
            output logic [15:0] Out );

    logic [15:0] AB_Sum;
    ripple_adder adder(.A(A),.B(B),.Sum(AB_Sum),.CO());
    
    // { 00: pass A, 01: A+B, 10: A&B, 11: ~A }
    always_comb
    begin
        case (ALUK)
            2'b00: Out = AB_Sum;
            2'b01: Out = A & B;
            2'b10: Out = ~A;
            2'b11: Out = A;
        endcase
    end

endmodule
