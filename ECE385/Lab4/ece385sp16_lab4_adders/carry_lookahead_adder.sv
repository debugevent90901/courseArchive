// 16-bit carry lookahead adder
// connected by 4 4-bit carry lookahead adders and 1 4-bit carry lookahead unit
// A,B: input bits
// Sum: output bits
// CO: carry-out bit
module carry_lookahead_adder
(
    input   logic[15:0]     A,
    input   logic[15:0]     B,
    output  logic[15:0]     Sum,
    output  logic           CO
);

    /* TODO
     *
     * Insert code here to implement a CLA adder.
     * Your code should be completly combinational (don't use always_ff or always_latch).
     * Feel free to create sub-modules or other files. */
	 logic P0,P1,P2,P3,G0,G1,G2,G3,C1,C2,C3;
    CLA_adder4    FA0(.A(A[3:0]),   .B(B[3:0]),   .C0(1'b0), .S(Sum[3:0]),   .P(P0), .G(G0), .Cout());
    CLA_adder4    FA1(.A(A[7:4]),   .B(B[7:4]),   .C0(C1),   .S(Sum[7:4]),   .P(P1), .G(G1), .Cout());
	 CLA_adder4    FA2(.A(A[11:8]),  .B(B[11:8]),  .C0(C2),   .S(Sum[11:8]),  .P(P2), .G(G2), .Cout());
	 CLA_adder4    FA3(.A(A[15:12]), .B(B[15:12]), .C0(C3),   .S(Sum[15:12]), .P(P3), .G(G3), .Cout());
	 
	 //a way to reduce the time cost by carry-out computing 
	 //adder4        FA3 (.A(A[15:12]), .B(B[15:12]), .c_in(c3),   .S(Sum[15:12]), .c_out(CO));
	 
	 // using the same carry unit inside the 4-bit look-ahead adder
	 CL_unit4      Unit(.*,.C0(1'b0),.Cout(CO),.P(),.G());

endmodule
