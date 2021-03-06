/************************************************************************
AES Decryption Core Logic

Dong Kai Wang, Fall 2017

For use with ECE 385 Experiment 9
University of Illinois ECE Department
************************************************************************/

module AES (
	input  logic CLK,
	input  logic RESET,
	input  logic AES_START,
	output logic AES_DONE,
	input  logic [127:0] AES_KEY,
	input  logic [127:0] AES_MSG_ENC,
	output logic [127:0] AES_MSG_DEC
);

logic [127:0] state, newState;
logic [127:0] key;
logic [1407:0] KeySchedule;
logic [127:0] InvShiftRowsOut;
logic [127:0] InvSubBytesOut;
logic [127:0] AddRoundKeyOut;
logic [31:0] InvMixColumnsIn;
logic [31:0] InvMixColumnsOut;


// apply KeyExpansion
KeyExpansion ke(.clk(CLK), .Cipherkey(AES_KEY), .KeySchedule(KeySchedule));

// *************
// * Round 1-9 *
// *************

// apply InvShiftRows
InvShiftRows isr(.data_in(state), .data_out(InvShiftRowsOut));

// apply InvSubBytes
InvSubBytes isb0(.clk(CLK), .in(state[7:0]), .out(InvSubBytesOut[7:0]));
InvSubBytes isb1(.clk(CLK), .in(state[15:8]), .out(InvSubBytesOut[15:8]));
InvSubBytes isb2(.clk(CLK), .in(state[23:16]), .out(InvSubBytesOut[23:16]));
InvSubBytes isb3(.clk(CLK), .in(state[31:24]), .out(InvSubBytesOut[31:24]));
InvSubBytes isb4(.clk(CLK), .in(state[39:32]), .out(InvSubBytesOut[39:32]));
InvSubBytes isb5(.clk(CLK), .in(state[47:40]), .out(InvSubBytesOut[47:40]));
InvSubBytes isb6(.clk(CLK), .in(state[55:48]), .out(InvSubBytesOut[55:48]));
InvSubBytes isb7(.clk(CLK), .in(state[63:56]), .out(InvSubBytesOut[63:56]));
InvSubBytes isb8(.clk(CLK), .in(state[71:64]), .out(InvSubBytesOut[71:64]));
InvSubBytes isb9(.clk(CLK), .in(state[79:72]), .out(InvSubBytesOut[79:72]));
InvSubBytes isb10(.clk(CLK), .in(state[87:80]), .out(InvSubBytesOut[87:80]));
InvSubBytes isb11(.clk(CLK), .in(state[95:88]), .out(InvSubBytesOut[95:88]));
InvSubBytes isb12(.clk(CLK), .in(state[103:96]), .out(InvSubBytesOut[103:96]));
InvSubBytes isb13(.clk(CLK), .in(state[111:104]), .out(InvSubBytesOut[111:104]));
InvSubBytes isb14(.clk(CLK), .in(state[119:112]), .out(InvSubBytesOut[119:112]));
InvSubBytes isb15(.clk(CLK), .in(state[127:120]), .out(InvSubBytesOut[127:120]));

// apply AddRoundKey
AddRoundKey ark(.state(state), .roundKey(key), .out(AddRoundKeyOut));

// apply InvMixColumn
InvMixColumns imc(.in(InvMixColumnsIn), .out(InvMixColumnsOut)); 

// Loop ends
// state machine begins

// round counter
logic [4:0] curr_ctr, next_ctr;

// assign states
enum logic [4:0]
{
		Wait,
		KeyExpansion,
		AddRoundKeyInit,
		AddRoundKeyLoop,
		AddRoundKeyHalt,
		InvShiftRows,
		InvSubBytes,
		InvMixColumn0,
		InvMixColumn1,
		InvMixColumn2,
		InvMixColumn3,
		Done
} curr_state, next_state;

always_ff @(posedge CLK)
	begin
		if (RESET) 
		begin
			curr_state <= Wait;
			curr_ctr <=4'b0;
		end
		
		else 
			curr_state <= next_state;
			curr_ctr <= next_ctr;
			state <= newState;
	end

always_comb 
begin
	next_state = curr_state;
	next_ctr = curr_ctr;
	newState = state;
	key = 128'b0;
	InvMixColumnsIn = 32'b0;
	
	AES_DONE = 1'b0;
	AES_MSG_DEC = 128'b0;

	unique case (curr_state)
    
	Wait:
		begin
			if (AES_START == 1'b1)
			begin
				next_ctr = 4'b0;
				next_state = KeyExpansion;
			end 

			else
				next_state = Wait;
		end
	
	KeyExpansion:
		begin
			if (curr_ctr == 10) 
			begin
				next_state = AddRoundKeyInit;
				next_ctr = 0;
			end

			else 
			begin
				next_state = KeyExpansion;
				next_ctr = curr_ctr + 4'b1;
			end
		end
	
	AddRoundKeyInit: 
		begin
			next_state = InvShiftRows;
		end
    
	InvShiftRows:
		begin
			next_state = InvSubBytes;
		end
	
	InvSubBytes:
		begin
			if (curr_ctr == 9)
			begin
				next_state = AddRoundKeyHalt;
				next_ctr = 0;
			end

			else
				next_state = AddRoundKeyLoop;
		end
    
    AddRoundKeyLoop:
		begin
			next_state = InvMixColumn0;
		end
	
	InvMixColumn0:
		begin
			next_state = InvMixColumn1;
		end
	
	InvMixColumn1:
		begin
			next_state = InvMixColumn2;
		end

	InvMixColumn2:
		begin
			next_state = InvMixColumn3;
		end
	
	InvMixColumn3:
		begin
			next_state = InvShiftRows;
			next_ctr = curr_ctr + 4'b1;
		end
	
	AddRoundKeyHalt:
		begin
			next_state = Done; 
		end
	
	Done:
		begin
			if (AES_START == 0)
				next_state = Wait;
			else
				next_state = Done;
		end
	default: next_state = Wait;
	endcase

	case (curr_state)
    
    Wait:
		begin
			// do nothing	
		end
	
	KeyExpansion:
		begin
			newState = AES_MSG_ENC; 
		end
	
	AddRoundKeyInit:
		begin
			newState = AddRoundKeyOut;
			key = KeySchedule[127:0];
		end
    
    InvShiftRows:
		begin
			newState = InvShiftRowsOut;
		end
    
	InvSubBytes:
		begin
			newState = InvSubBytesOut;
		end
    
    AddRoundKeyLoop:
		begin
			newState = AddRoundKeyOut;
			case (curr_ctr)
				4'd8: key = KeySchedule[1279:1152];
				4'd7: key = KeySchedule[1151:1024];
				4'd6: key = KeySchedule[1023:896];
				4'd5: key = KeySchedule[895:768];
				4'd4: key = KeySchedule[767:640];
				4'd3: key = KeySchedule[639:512];
				4'd2: key = KeySchedule[511:384];
				4'd1: key = KeySchedule[383:256];
				4'd0: key = KeySchedule[255:128];
				default: key = 128'b0;
			endcase
		end
    
	InvMixColumn0:
		begin
			InvMixColumnsIn = state[31:0];
			newState[31:0] = InvMixColumnsOut;
		end

	InvMixColumn1:
		begin
			InvMixColumnsIn = state[63:32];
			newState[63:32] = InvMixColumnsOut;
		end
	
	InvMixColumn2:
		begin
			InvMixColumnsIn = state[95:64];
			newState[95:64] = InvMixColumnsOut;
		end
	
	InvMixColumn3:
		begin
			InvMixColumnsIn = state[127:96];
			newState[127:96] = InvMixColumnsOut;
		end

    AddRoundKeyHalt:
		begin
			newState = AddRoundKeyOut;
			key = KeySchedule[1407:1280];
		end
	
	Done:
		begin
			AES_MSG_DEC = AddRoundKeyOut;
			AES_DONE = 1'b1;
		end
	endcase
end
endmodule