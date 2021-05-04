// 4-bit carry lookahead adder
// A,B: input bits
// c0: carry-in bit
// S: output bits
// P: propagating signal, indicating whether a carry-out has the possibility of being propagated
// G: generating signal, indicating whether a carry-out is generated
// Cout: carry-out bit
module CLA_adder4
(
    input   logic[3:0] A,B,
	 input   logic      C0,
	 output  logic[3:0] S,
	 output  logic      P,G,Cout
);

    logic C1,C2,C3,P0,P1,P2,P3,G0,G1,G2,G3;
    
	 CLA_adder    FA0(.x(A[0]),.y(B[0]),.z(C0),.s(S[0]),.p(P0),.g(G0));
    CLA_adder    FA1(.x(A[1]),.y(B[1]),.z(C1),.s(S[1]),.p(P1),.g(G1));
	 CLA_adder    FA2(.x(A[2]),.y(B[2]),.z(C2),.s(S[2]),.p(P2),.g(G2));
	 CLA_adder    FA3(.x(A[3]),.y(B[3]),.z(C3),.s(S[3]),.p(P3),.g(G3));
	 CL_unit4     Unit(.*);
	 
endmodule
