// 4-bit lookahead unit
// compute all the carry-in bits simultaneously for adders
// P0,P1,P2,P3: propagating signals
// G0,G1,G2,G3: generating signals
// C0: carry-in bit
// C1,C2,C3,Cout: carry-out bits
// P: propagating signal for the whole 4-bit adder
// G: generating signal for the whole 4-bit adder
module CL_unit4
(
    input   logic P0,P1,P2,P3,G0,G1,G2,G3,C0,
	 output  logic C1,C2,C3,Cout,P,G
);

    assign C1 = (C0&P0)|G0;
	 assign C2 = (C0&P0&P1)|(G0&P1)|G1;
	 assign C3 = (C0&P0&P1&P2)|(G0&P1&P2)|(G1&P2)|G2;
    assign Cout = (C0&P0&P1&P2&P3)|(G0&P1&P2&P3)|(G1&P2&P3)|(G2&P3)|G3;
	 assign P = P0&P1&P2&P3;
	 assign G = (G0&P1&P2&P3)|(G1&P2&P3)|(G2&P3)|G3;
	 
endmodule