module datapath
(
    input logic Clk, Reset,
    input logic LD_MAR, LD_MDR, LD_IR, LD_BEN, LD_CC, LD_REG, LD_PC, LD_LED,
    input logic GatePC, GateMDR, GateALU, GateMARMUX,
    input logic [1:0] PCMUX, ADDR2MUX, ALUK,
    input logic DRMUX, SR1MUX, SR2MUX, ADDR1MUX,
    input logic MIO_EN,
    input logic [15:0] D2CPU,
    output logic  ,
    output logic [11:0] LED,
    output logic [15:0] IR, MAR, MDR, PC
);


logic [15:0]    MDR_In, MDR_Out, MAR_Out, IR_Out, PC_In, PC_Out, PC_Plus, ADDR1_mux_Out, ADDR2_mux_Out, ADDER, 
                SR2_mux_Out, SR1_OUT, SR2_OUT, ALU_Out, BUS, imm5, offset6, PCoffset9, PCoffset11;
logic [2:0]     DR_mux_Out, SR1_mux_Out;
logic           N_In,Z_In,P_In,N_Out,Z_Out,P_Out,BEN_In;

assign PC = PC_Out;
assign IR = IR_Out;
assign MAR = MAR_Out;
assign MDR = MDR_Out;
assign BEN_In = (IR_Out[11] & N_Out) | (IR_Out[10] & Z_Out) | (IR_Out[9] & P_Out);

reg_12 LED_reg(.Clk(Clk), .Reset(Reset), .Load(LD_LED), .In(IR_Out[11:0]), .Out(LED));

reg_16 MDR_reg(.Clk(Clk), .Reset(Reset), .Load(LD_MDR), .In(MDR_In), .Out(MDR_Out));
reg_16 MAR_reg(.Clk(Clk), .Reset(Reset), .Load(LD_MAR), .In(BUS), .Out(MAR_Out));
reg_16 IR_reg(.Clk(Clk), .Reset(Reset), .Load(LD_IR), .In(BUS), .Out(IR_Out));
mux_2 MDR_mux(.SELECT(MIO_EN),.A(BUS),.B(D2CPU),.OUT(MDR_In));

reg_1 N_reg(.Clk(Clk), .Reset(Reset), .Load(LD_CC), .In(N_In), .Out(N_Out));
reg_1 Z_reg(.Clk(Clk), .Reset(Reset), .Load(LD_CC), .In(Z_In), .Out(Z_Out));
reg_1 P_reg(.Clk(Clk), .Reset(Reset), .Load(LD_CC), .In(P_In),  .Out(P_Out));
reg_1 BEN_reg(.Clk(Clk), .Reset(Reset), .Load(LD_BEN), .In(BEN_In), .Out(BEN));

SEXT_5 sext_5(.IR(IR_Out),.OUT(imm5));
SEXT_6 sext_6(.IR(IR_Out),.OUT(offset6));
SEXT_9 sext_9(.IR(IR_Out),.OUT(PCoffset9));
SEXT_11 sext_11(.IR(IR_Out),.OUT(PCoffset11));

reg_16 PC_reg(.Clk(Clk), .Reset(Reset), .Load(LD_PC), .In(PC_In), .Out(PC_Out));
mux_3  PC_mux(.SELECT(PCMUX),.A(PC_Plus),.B(BUS),.C(ADDER),.OUT(PC_In));
ripple_adder PC_adder(.A(PC_Out), .B(16'b1), .Sum(PC_Plus), .CO());

mux_2 ADDR1_mux(.SELECT(ADDR1MUX),.A(PC_Out),.B(SR1_OUT),.OUT(ADDR1_mux_Out));
mux_4 ADDR2_mux(.SELECT(ADDR2MUX),.A(16'b0),.B(offset6),.C(PCoffset9),.D(PCoffset11),.OUT(ADDR2_mux_Out));
ripple_adder ADDR_adder(.A(ADDR1_mux_Out),.B(ADDR2_mux_Out),.Sum(ADDER),.CO());

mux_2_3bit DR_mux(.SELECT(DRMUX),.A(IR_Out[11:9]),.B(3'b111),.OUT(DR_mux_Out));
mux_2_3bit SR1_mux(.SELECT(SR1MUX),.A(IR_Out[11:9]),.B(IR_Out[8:6]),.OUT(SR1_mux_Out));
mux_2 SR2_mux(.SELECT(SR2MUX),.A(SR2_OUT),.B(imm5),.OUT(SR2_mux_Out));

ALU ALU_Unit(.A(SR1_OUT),.B(SR2_mux_Out),.ALUK(ALUK),.Out(ALU_Out));

reg_file REG_FILE(.Clk(Clk), .Reset(Reset), .LD_REG(LD_REG), .DR(DR_mux_Out), .SR1(SR1_mux_Out), .SR2(IR_Out[2:0]), .BUS_IN(BUS), .SR1_OUT(SR1_OUT), .SR2_OUT(SR2_OUT));

    always_comb
    begin
        case ({GatePC, GateMDR, GateALU, GateMARMUX})
            4'b1000 : BUS = PC_Out;
            4'b0100 : BUS = MDR_Out;
            4'b0010 : BUS = ALU_Out;
            4'b0001 : BUS = ADDER;
            default : BUS = 16'hzzzz;
        endcase

        if (BUS == 0)
        begin
            N_In = 1'b0;
            Z_In = 1'b1;
            P_In = 1'b0;
        end
        else if (BUS[15])
        begin
            N_In = 1'b1;
            Z_In = 1'b0;
            P_In = 1'b0;
        end
        else
        begin
            N_In = 1'b0;
            Z_In = 1'b0;
            P_In = 1'b1;
        end
    end

endmodule
