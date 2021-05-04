// 4-bits ripple adder series connected by 4 full-adder
// A,B: input bits
// c_in: carry-in bit
// S: output bits
// c_out: carry-out bit
module adder4 
(
    input   logic[3:0] A,B,
	 input   logic      c_in,
	 output  logic[3:0] S,
	 output  logic      c_out
);

    logic c0,c1,c2;
	 
	 full_adder    FA0 (.x(A[0]), .y(B[0]), .z(c_in), .s(S[0]), .c(c0));
	 full_adder    FA1 (.x(A[1]), .y(B[1]), .z(c0),   .s(S[1]), .c(c1));
	 full_adder    FA2 (.x(A[2]), .y(B[2]), .z(c1),   .s(S[2]), .c(c2));
	 full_adder    FA3 (.x(A[3]), .y(B[3]), .z(c2),   .s(S[3]), .c(c_out));
	 
endmodule
