// 16-bit carry selected adder 
// series connected by 3 4-bit selectors and 1 4-bit ripple adder
// A,B: input bits
// Sum: output bits
// CO: carry-out bit
module carry_select_adder
(
    input   logic[15:0]     A,
    input   logic[15:0]     B,
    output  logic[15:0]     Sum,
    output  logic           CO
);

    /* TODO
     *
     * Insert code here to implement a carry select.
     * Your code should be completly combinational (don't use always_ff or always_latch).
     * Feel free to create sub-modules or other files. */
    logic  c0,c1,c2;
	 
	 /* The first 4 bits for the adder need not be selected */
	 adder4    FA0 (.A(A[3:0]),   .B(B[3:0]),   .c_in(1'b0), .S(Sum[3:0]),   .c_out(c0));
	 CSA_adder FA1 (.A(A[7:4]),   .B(B[7:4]),   .Cin(c0),    .S(Sum[7:4]),   .Cout(c1));
	 CSA_adder FA2 (.A(A[11:8]),  .B(B[11:8]),  .Cin(c1),    .S(Sum[11:8]),  .Cout(c2));
	 CSA_adder FA3 (.A(A[15:12]), .B(B[15:12]), .Cin(c2),    .S(Sum[15:12]), .Cout(CO));
	  
endmodule
