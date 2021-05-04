// 16-bit ripple adder series connected by 4 4-bit ripple adders
// A,B: input bits
// Sum: output bits
// CO: carry-out bit
module ripple_adder
(
    input   logic[15:0]     A,
    input   logic[15:0]     B,
    output  logic[15:0]     Sum,
    output  logic           CO
);

    /* TODO
     *
     * Insert code here to implement a ripple adder.
     * Your code should be completly combinational (don't use always_ff or always_latch).
     * Feel free to create sub-modules or other files. */
	  logic  c0,c1,c2;
	  
	 adder4    FA0 (.A(A[3:0]),   .B(B[3:0]),   .c_in(1'b0), .S(Sum[3:0]),   .c_out(c0));
	 adder4    FA1 (.A(A[7:4]),   .B(B[7:4]),   .c_in(c0),   .S(Sum[7:4]),   .c_out(c1));
	 adder4    FA2 (.A(A[11:8]),  .B(B[11:8]),  .c_in(c1),   .S(Sum[11:8]),  .c_out(c2));
	 adder4    FA3 (.A(A[15:12]), .B(B[15:12]), .c_in(c2),   .S(Sum[15:12]), .c_out(CO));

endmodule
