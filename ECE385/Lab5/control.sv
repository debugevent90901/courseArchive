module control
(
    input   logic Clk, Reset, Run, ClearA_LoadB, M, 
    output  logic SHIFT, LOAD, CLEAR,
    output  logic [1:0] ADD
);

    enum logic [4:0]
    {
        Start, Load,
        Add0, Add1, Add2, Add3, Add4, Add5, Add6, Add7, 
        Shift0, Shift1, Shift2, Shift3, Shift4, Shift5, Shift6, Shift7,
        Halt, Clear, Hold
    }   curr_state, next_state;

    always_ff @(posedge Clk)
    begin
        if (Reset)
            curr_state <= Start;
        else
            curr_state <= next_state;
    end

    always_comb
    begin

        next_state = curr_state;
        unique case (curr_state)

            Start:
                if (ClearA_LoadB)
                        next_state = Load;
                    else if (Run)
                        next_state = Add0;
            Load: next_state = Start;

            Add0: next_state = Shift0;
            Add1: next_state = Shift1;
            Add2: next_state = Shift2;
            Add3: next_state = Shift3;
            Add4: next_state = Shift4;
            Add5: next_state = Shift5;
            Add6: next_state = Shift6;
            Add7: next_state = Shift7;

            Shift0: next_state = Add1;
            Shift1: next_state = Add2;
            Shift2: next_state = Add3;
            Shift3: next_state = Add4;
            Shift4: next_state = Add5;
            Shift5: next_state = Add6;
            Shift6: next_state = Add7;
            Shift7: next_state = Halt;

            Halt:
                if (~Run)
                    next_state = Hold;
            Hold:
                if (Run)
                    next_state = Clear;
                else if (ClearA_LoadB)
                    next_state = Load;
            Clear: next_state = Add0;

        endcase


        case (curr_state)
            Start:
                begin
                    SHIFT <= 1'b0;
                    LOAD <= 1'b0;
                    CLEAR <= 1'b0;
                    ADD <= 2'b00;
                end
            Load:
                begin
                    SHIFT <= 1'b0;
                    LOAD <= 1'b1;
                    CLEAR <= 1'b0;
                    ADD <= 2'b00;
                end
            Add0, Add1, Add2, Add3, Add4, Add5, Add6: 
                begin
                    SHIFT <= 1'b0;
                    LOAD <= 1'b0;
                    CLEAR <= 1'b0;
                    if (M)
                        ADD <= 2'b10;
                    else
                        ADD <= 2'b00;
                end
            Add7:
                begin
                    SHIFT <= 1'b0;
                    LOAD <= 1'b0;
                    CLEAR <= 1'b0;
                    if (M)
                        ADD <= 2'b11;
                    else
                        ADD <= 2'b00;
                end
            Shift0, Shift1, Shift2, Shift3, Shift4, Shift5, Shift6, Shift7:
                begin
                    SHIFT <= 1'b1;
                    LOAD <= 1'b0;
                    CLEAR <= 1'b0;
                    ADD <= 2'b00;
                end
            Halt, Hold:
                begin
                    SHIFT <= 1'b0;
                    LOAD <= 1'b0;
                    CLEAR <= 1'b0;
                    ADD <= 2'b00;
                end
            Clear:
                begin
                    SHIFT <= 1'b0;
                    LOAD <= 1'b0;
                    CLEAR <= 1'b1;
                    ADD <= 2'b00;
                    end
            endcase
    end

endmodule
