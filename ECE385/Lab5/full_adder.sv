module full_adder(  input logic A, B, Cin,
                    output logic Sum, Cout);

    assign Sum = A ^ B ^ Cin;
    assign Cout = (A & B ) | (B & Cin) | (A & Cin);

endmodule
