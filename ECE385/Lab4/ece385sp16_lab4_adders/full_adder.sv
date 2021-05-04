// 1-bit full-adder
// x,y: input bits
// z: carry-in bit
// s: output bit
// c: carry-out bit
module full_adder
(
    input   logic x, y, z,
	 output  logic s, c
);

    assign s = x^y^z;
	 assign c = (x&y)|(y&z)|(x&z);
	 
endmodule