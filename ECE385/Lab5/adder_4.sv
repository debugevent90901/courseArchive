module adder_4
(
    input   logic [3:0] A, B,
    input   logic       Cin,
    output  logic [3:0] Sum,
    output  logic       Cout
);

    logic C0, C1, C2;
    
    full_adder  FA0(.*, .A(A[0]), .B(B[0]), .Sum(Sum[0]), .Cout(C0));
    full_adder  FA1(    .A(A[1]), .B(B[1]), .Cin(C0), .Sum(Sum[1]), .Cout(C1));
    full_adder  FA2(    .A(A[2]), .B(B[2]), .Cin(C1), .Sum(Sum[2]), .Cout(C2));
    full_adder  FA3(.*, .A(A[3]), .B(B[3]), .Cin(C2), .Sum(Sum[3]));
    
endmodule