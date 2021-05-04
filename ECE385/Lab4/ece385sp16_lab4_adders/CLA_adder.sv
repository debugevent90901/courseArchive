// 1-bit CLA adder
// x,y: input bits
// z: carry-in bit
// s: output bit
// p: propagating signal, indicating whether a carry-out has the possibility of being propagated
// g: generating signal, indicating whether a carry-out is generated
module CLA_adder
(
    input   logic x,y,z,
	 output  logic s,p,g
);
    assign s = x^y^z;
	 assign p = x^y;
	 assign g = x&y;
	 
endmodule