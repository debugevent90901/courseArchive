module lab5_toplevel
(
    input   logic [7:0] S, 
    input   logic       Clk, Reset, Run, ClearA_LoadB,
    output  logic [6:0] AhexU, AhexL, BhexU, BhexL, 
    output  logic [7:0] Aval, Bval, 
    output  logic       X
    //output logic [8:0] partial
);

    logic       Reset_S, Run_S, ClearA_LoadB_S;
    logic [7:0] S_S;
    logic       SHIFT, LOAD, CLEAR, M, Shift_Out_A;
    logic [8:0] partial_Sum;
    logic [1:0] ADD;

    sync sync_S [7:0] (Clk, S, S_S);
    sync sync_button [2:0] (Clk, {~Reset, ~Run, ~ClearA_LoadB}, {Reset_S, Run_S, ClearA_LoadB_S});
    
    control FSM
                (
                    .*, .Reset(Reset_S), .Run(Run_S), .ClearA_LoadB(ClearA_LoadB_S)
                );

    reg_8 RegisterA
                (  
                    .*, .Reset(Reset_S | LOAD | CLEAR), .Shift_In(X), .Load(ADD[1]), .Shift_En(SHIFT),
                    .D(partial_Sum[7:0]), .Shift_Out(Shift_Out_A), .Data_Out(Aval)
                );

    reg_8 RegisterB
                (  
                    .*, .Load(LOAD), .Reset(Reset_S), .Shift_In(Shift_Out_A), .Shift_En(SHIFT),
                    .D(S_S), .Shift_Out(M), .Data_Out(Bval)
                );
    
    adder_9 adder_9 
                (
                    .SUB(ADD[0]), .A({Aval[7], Aval}), .B({S_S[7], S_S}),
                    .Sum(partial_Sum), .Cout()
                );

    //assign   partial = partial_Sum;

    always_ff @ (posedge Clk)
    begin
        if (Reset_S | LOAD | CLEAR)
            X <= 8'h00;
        else if (ADD[1])
            X <= partial_Sum[8];
    end

    HexDriver hexUA(.In0(Aval[7:4]), .Out0(AhexU));
    HexDriver hexUB(.In0(Bval[7:4]), .Out0(BhexU));
    HexDriver hexLA(.In0(Aval[3:0]), .Out0(AhexL));
    HexDriver hexLB(.In0(Bval[3:0]), .Out0(BhexL));

endmodule