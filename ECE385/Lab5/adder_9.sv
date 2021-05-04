module adder_9
(
    input   SUB,
    input   logic [8:0] A,
    input   logic [8:0] B,
    output  logic [8:0] Sum,
    output  logic       Cout
);

    logic       C0, C1;
    logic [8:0] MUX;
    
    always_comb 
    begin
        if (SUB)
            MUX = ~B;
        else
            MUX = B;
    end
    
    adder_4     A40 (.A(A[3:0]), .B(MUX[3:0]), .Cin(SUB), .Sum(Sum[3:0]), .Cout(C0));
    adder_4     A41 (.A(A[7:4]), .B(MUX[7:4]), .Cin(C0),  .Sum(Sum[7:4]), .Cout(C1));
    full_adder  FA1 (.A(A[8]),   .B(MUX[8]),   .Cin(C1),  .Sum(Sum[8]),   .Cout(Cout));

endmodule

