/************************************************************************
Lab 9 Nios Software

Dong Kai Wang, Fall 2017
Christine Chen, Fall 2013

For use with ECE 385 Experiment 9
University of Illinois ECE Department
************************************************************************/

#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include "aes.h"

#define Nb 4
#define Nk 4 
#define Nr 10

// Pointer to base address of AES module, make sure it matches Qsys
volatile unsigned int * AES_PTR = (unsigned int *) 0x00000100;

// Execution mode: 0 for testing, 1 for benchmarking
int run_mode = 0;

/** charToHex
 *  Convert a single character to the 4-bit value it represents.
 *  
 *  Input: a character c (e.g. 'A')
 *  Output: converted 4-bit value (e.g. 0xA)
 */
char charToHex(char c)
{
	char hex = c;

	if (hex >= '0' && hex <= '9')
		hex -= '0';
	else if (hex >= 'A' && hex <= 'F')
	{
		hex -= 'A';
		hex += 10;
	}
	else if (hex >= 'a' && hex <= 'f')
	{
		hex -= 'a';
		hex += 10;
	}
	return hex;
}

/** charsToHex
 *  Convert two characters to byte value it represents.
 *  Inputs must be 0-9, A-F, or a-f.
 *  
 *  Input: two characters c1 and c2 (e.g. 'A' and '7')
 *  Output: converted byte value (e.g. 0xA7)
 */
char charsToHex(char c1, char c2)
{
	char hex1 = charToHex(c1);
	char hex2 = charToHex(c2);
	return (hex1 << 4) + hex2;
}

// The following 8 functions are axuiliary functions in aes encryption
// key expansion algorithm implementation
// keySchedule 4x11, every 32 bit
unsigned int RotWord(unsigned int word)
{
    return ((word & 0x00FFFFFF) << 8) | ((word & 0xFF000000) >> 24);
}

unsigned int SubWord(unsigned int word)
{
	return (aes_sbox[(word & 0xFF000000) >> 24] << 24) | (aes_sbox[(word & 0x00FF0000) >> 16] << 16) | (aes_sbox[(word & 0x0000FF00) >> 8] << 8) | (aes_sbox[word & 0x000000FF]);
}

void KeyExpansion(unsigned char * key, unsigned int * keySchedule, unsigned int numWords)
{
	for (int i = 0 ; i < numWords ; i++)
		keySchedule[i] = (key[i]<<24 | key[i+4]<<16 | key[i+8]<<8 | key[i+12]);
	
	for (int j = numWords ; j < Nb*(Nr+1) ; j++)
	{
		unsigned int tmp = keySchedule[j-1];
		if (j % numWords == 0)
			tmp = SubWord(RotWord(tmp)) ^ Rcon[j/numWords];
		keySchedule[j] = keySchedule[j-numWords] ^ tmp;	
	}
}

//add round key
void AddRoundKey(unsigned char * state, unsigned int * keySchedule)
{
    for (int i = 0 ; i <= 3 ; i++)
    {
        for (int j = 0 ; j <= 3 ; j++)
            state[i*4+j] ^= (keySchedule[j] >> (8*(3-i))) & 0xFF;
    }
}

// subBytes
void SubBytes(unsigned char * state)
{
	for (int i = 0 ; i <= 15 ; i++)
		state[i] = aes_sbox[state[i]];
}

//shiftRows
void shift (unsigned char * state, int n)
{
	for (int i = 1 ; i <= n ; i++)
	{
		unsigned char tmp = state[4*n];
		for (int j = 0 ; j <= 2 ; j++)
			state[4*n+j] = state[4*n+j+1];
		state[4*n+3] = tmp;
	}
}

void ShiftRows(unsigned char * state)
{
    shift(state, 1);
    shift(state, 2);
    shift(state, 3);
}

// mixColumns
void MixColumns(unsigned char * state)
{
	unsigned char b0, b1, b2, b3;

	for (int i = 0 ; i <= 3 ; i++)
	{
		b0 = gf_mul[state[0*4+i]][0] ^ gf_mul[state[1*4+i]][1] ^ state[2*4+i] ^ state[3*4+i];
		b1 = state[0*4+i] ^ gf_mul[state[1*4+i]][0] ^ gf_mul[state[2*4+i]][1] ^ state[3*4+i];
		b2 = state[0*4+i] ^ state[1*4+i] ^ gf_mul[state[2*4+i]][0] ^ gf_mul[state[3*4+i]][1];
		b3 = gf_mul[state[0*4+i]][1] ^ state[1*4+i] ^ state[2*4+i] ^ gf_mul[state[3*4+i]][0];
        
		state[0*4+i] = b0;
		state[1*4+i] = b1;
		state[2*4+i] = b2;
		state[3*4+i] = b3;
	}
}

/** encrypt
 *  Perform AES encryption in software.
 *
 *  Input: msg_ascii - Pointer to 32x 8-bit char array that contains the input message in ASCII format
 *         key_ascii - Pointer to 32x 8-bit char array that contains the input key in ASCII format
 *  Output:  msg_enc - Pointer to 4x 32-bit int array that contains the encrypted message
 *               key - Pointer to 4x 32-bit int array that contains the input key
 */
void encrypt(unsigned char * msg_ascii, unsigned char * key_ascii, unsigned int * msg_enc, unsigned int * key)
{
	// Implement this function
	unsigned char state[4*Nb];
	unsigned char keyOrig[4*Nk];
	
	for (int i = 0 ; i <= 15 ; i++)
	{
		// 2 x 8-bit char(16-bit in total)--> 1 x 8 bit hex
		// 32 x 8-bit(input) --> 32x8/2=128-bit (a block)
		// 4x4 matrix, each position 8-bit(a byte)
		state[i%4*4+i/4] = charsToHex(msg_ascii[2*i], msg_ascii[2*i+1]);
		// key is also 128 bit
		// same as above
		keyOrig[i%4*4+i/4] = charsToHex(key_ascii[2*i], key_ascii[2*i+1]);
	}
    
	// 4 word for 11 cycle, each word 32-bit, 4x11x32=1408-bit=176byte
	// len(keySchedule) = 44
    unsigned int keySchedule[Nb*(Nr+1)];
    KeyExpansion(keyOrig, keySchedule, Nk);
    
	AddRoundKey(state, keySchedule);
    
	// round 1-9
	for (int round = 1 ; round <= Nr-1 ; round++)
	{
		SubBytes(state);
		ShiftRows(state);
		MixColumns(state);
		AddRoundKey(state, keySchedule+round*4);
	}
    
	// round 10
	SubBytes(state);
	ShiftRows(state);
	AddRoundKey(state, keySchedule+40);
	
	for (int i = 0 ; i <= 3 ; i++)
	{
		// len(key)=4, 4 words, each 32-bit
		key[i] = keyOrig[i]<<24 | keyOrig[i+4]<<16 | keyOrig[i+8]<<8 | keyOrig[i+12];
		msg_enc[i] = state[i]<<24 | state[i+4]<<16 | state[i+8]<<8 | state[i+12];
	}

	// for debug purposes
	/*
    for (int i = 0 ; i <= 15 ; i++)
    {
        printf("%x\n", state[i]);
    }
	*/
}

/** decrypt
 *  Perform AES decryption in hardware.
 *
 *  Input:  msg_enc - Pointer to 4x 32-bit int array that contains the encrypted message
 *              key - Pointer to 4x 32-bit int array that contains the input key
 *  Output: msg_dec - Pointer to 4x 32-bit int array that contains the decrypted message
 */
void decrypt(unsigned int * msg_enc, unsigned int * msg_dec, unsigned int * key)
{
	// Implement this function

	AES_PTR[14] = 0;
	AES_PTR[15] = 0;

	/*
	for(int i = 0; i < 4; i++){
		AES_PTR[i] = key[3-i];
		AES_PTR[i+4] = msg_enc[3-i];
	}
	*/

	AES_PTR[0] = key[3];
	AES_PTR[4] = msg_enc[3];
	AES_PTR[1] = key[2];
	AES_PTR[5] = msg_enc[2];
	AES_PTR[2] = key[1];
	AES_PTR[6] = msg_enc[1];
	AES_PTR[3] = key[0];
	AES_PTR[7] = msg_enc[0];

	AES_PTR[14] = 1;
	while(!AES_PTR[15]){}

	/*
	for(int i = 0; i < 4; i++){
		msg_dec[i] = AES_PTR[11-i];
	}
	*/

	msg_dec[0] = AES_PTR[11];
	msg_dec[1] = AES_PTR[10];
	msg_dec[2] = AES_PTR[9];
	msg_dec[3] = AES_PTR[8];

	AES_PTR[14] = 0;
	AES_PTR[15] = 0;
}

/** main
 *  Allows the user to enter the message, key, and select execution mode
 *
 */
int main()
{
	// Input Message and Key as 32x 8-bit ASCII Characters ([33] is for NULL terminator)
	unsigned char msg_ascii[33];
	unsigned char key_ascii[33];
	// Key, Encrypted Message, and Decrypted Message in 4x 32-bit Format to facilitate Read/Write to Hardware
	unsigned int key[4];
	unsigned int msg_enc[4];
	unsigned int msg_dec[4];

	printf("Select execution mode: 0 for testing, 1 for benchmarking: ");
	scanf("%d", &run_mode);

	if (run_mode == 0) {
		// Continuously Perform Encryption and Decryption
		while (1) {
			int i = 0;
			printf("\nEnter Message:\n");
			scanf("%s", msg_ascii);
			printf("\n");
			printf("\nEnter Key:\n");
			scanf("%s", key_ascii);
			printf("\n");
			encrypt(msg_ascii, key_ascii, msg_enc, key);
			printf("\nEncrpted message is: \n");
			for(i = 0; i < 4; i++){
				printf("%08x", msg_enc[i]);
			}
			printf("\n");
			decrypt(msg_enc, msg_dec, key);
			printf("\nDecrypted message is: \n");
			for(i = 0; i < 4; i++){
				printf("%08x", msg_dec[i]);
			}
			printf("\n");
		}
	}
	else {
		// Run the Benchmark
		int i = 0;
		int size_KB = 2;
		// Choose a random Plaintext and Key
		for (i = 0; i < 32; i++) {
			msg_ascii[i] = 'a';
			key_ascii[i] = 'b';
		}
		// Run Encryption
		clock_t begin = clock();
		for (i = 0; i < size_KB * 64; i++)
			encrypt(msg_ascii, key_ascii, msg_enc, key);
		clock_t end = clock();
		double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
		double speed = size_KB / time_spent;
		printf("Software Encryption Speed: %f KB/s \n", speed);
		// Run Decryption
		begin = clock();
		for (i = 0; i < size_KB * 64; i++)
			decrypt(msg_enc, msg_dec, key);
		end = clock();
		time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
		speed = size_KB / time_spent;
		printf("Hardware Encryption Speed: %f KB/s \n", speed);
	}
	return 0;
}
