module testbench();

timeunit 10ns;
timeprecision 1ns;

logic CLK;
logic RESET;
logic AES_START;
logic AES_DONE;
logic [127:0] AES_KEY;
logic [127:0] AES_MSG_ENC;
logic [127:0] AES_MSG_DEC;

logic [127:0] state, newState;
logic [127:0] key;
logic [1407:0] KeySchedule;
logic [127:0] InvShiftRowsOut;
logic [127:0] InvSubBytesOut;
logic [127:0] AddRoundKeyOut;
logic [31:0] InvMixColumnsIn;
logic [31:0] InvMixColumnsOut;

logic [4:0] curr_ctr, next_ctr;
logic [4:0] curr_state, next_state;

AES aes(.*);

assign state = aes.state;
assign newState = aes.newState;
assign key = aes.key;
assign KeySchedule = aes.KeySchedule;
assign InvShiftRowsOut = aes.InvShiftRowsOut;
assign InvSubBytesOut = aes.InvSubBytesOut;
assign AddRoundKeyOut = aes.AddRoundKeyOut;
assign InvMixColumnsIn = aes.InvMixColumnsIn;
assign InvMixColumnsOut = aes.InvMixColumnsOut;
assign curr_ctr = aes.curr_ctr;
assign next_ctr = aes.next_ctr;
assign curr_state = aes.curr_state;
assign next_state = aes.next_state;

always begin : CLOCK_GENERATION
#1 CLK = ~CLK;
end

initial begin: CLOCK_INITIALIZATION
    CLK = 0;
end 

initial begin: TEST_VECTORS
RESET = 1;
AES_START = 0;
AES_MSG_ENC = 128'hdaec3055df058e1c39e814ea76f6747e;
AES_KEY = 128'h000102030405060708090a0b0c0d0e0f;
#5 RESET = 0;
#5 AES_START = 1;
#1000;
end

endmodule