// 4-bit selector
// A,B: input bits
// Cin: carry-in bit
// S: output bits
// Cout: carry-out bit
module CSA_adder
(
    input    logic[3:0] A,B,
	 input    logic      Cin,
	 output   logic[3:0] S,
	 output   logic      Cout
);

    logic[3:0] S1,S0;
	 logic      C0,C1;
	 
	 /* compute the result without a carry-in bit */ 
	 adder4    FA0 (.A(A[3:0]),.B(B[3:0]),.c_in(1'b0),.S(S0),.c_out(C0));
	 /* compute the result within a carry-in bit */
	 adder4    FA1 (.A(A[3:0]),.B(B[3:0]),.c_in(1'b1),.S(S1),.c_out(C1));
    /* carry-out biy */
	 assign Cout = (C1&Cin)|C0;
	 
	 /* 2-1 mux */
    always_comb
    begin
        if (Cin) begin
		      S = S1;
		  end else begin
		      S = S0;
		  end
	 end

endmodule
