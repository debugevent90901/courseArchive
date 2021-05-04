;
; The code given to you here implements the histogram calculation that 
; we developed in class.  In programming lab, we will add code that
; prints a number in hexadecimal to the monitor.
;
; Your assignment for this program is to combine these two pieces of 
; code to print the histogram to the monitor.
;
; If you finish your program, 
;    ** commit a working version to your repository  **
;    ** (and make a note of the repository version)! **


	        .ORIG	x3000		    ; starting address is x3000


;
; Count the occurrences of each letter (A to Z) in an ASCII string 
; terminated by a NUL character.  Lower case and upper case should 
; be counted together, and a count also kept of all non-alphabetic 
; characters (not counting the terminal NUL).
;
; The string starts at x4000.
;
; The resulting histogram (which will NOT be initialized in advance) 
; should be stored starting at x3F00, with the non-alphabetic count 
; at x3F00, and the count for each letter in x3F01 (A) through x3F1A (Z).
;
; table of register use in this part of the code
;    R0 holds a pointer to the histogram (x3F00)
;    R1 holds a pointer to the current position in the string
;       and as the loop count during histogram initialization
;    R2 holds the current character being counted
;       and is also used to point to the histogram entry
;    R3 holds the additive inverse of ASCII '@' (xFFC0) aka #-64
;    R4 holds the difference between ASCII '@' and 'Z' (xFFE6), aka #-26
;    R5 holds the difference between ASCII '@' and '`' (xFFE0), aka #-32
;    R6 is used as a temporary register
;

	        LD R0, HIST_ADDR      	; point R0 to the start of the histogram
	
	        ; fill the histogram with zeroes 
	        AND R6, R6, #0		    ; put a zero into R6
	        LD R1, NUM_BINS		    ; initialize loop count to 27
	        ADD R2, R0, #0		    ; copy start of histogram into R2

	        ; loop to fill histogram starts here
HFLOOP	    STR R6, R2, #0		    ; write a zero into histogram
	        ADD R2, R2, #1		    ; point to next histogram entry
	        ADD R1, R1, #-1		    ; decrement loop count
	        BRp HFLOOP		    ; continue until loop count reaches zero

	        ; initialize R1, R3, R4, and R5 from memory
	        LD R3, NEG_AT		    ; set R3 to additive inverse of ASCII '@', #-64
	        LD R4, AT_MIN_Z		    ; set R4 to difference between ASCII '@' and 'Z', #-26
	        LD R5, AT_MIN_BQ		    ; set R5 to difference between ASCII '@' and '`', #-32
	        LD R1, STR_START		    ; point R1 to start of string

    	    ; the counting loop starts here
COUNTLOOP
	        LDR R2, R1, #0		    ; read the next character from the string
	        BRz PRINT_HIST		    ; found the end of the string

	        ADD R2, R2, R3		    ; subtract '@' from the character
	        BRp AT_LEAST_A		    ; branch if > '@', i.e., >= 'A'
NON_ALPHA
	        LDR R6, R0, #0		    ; load the non-alpha count
	        ADD R6, R6, #1		    ; add one to it
	        STR R6, R0, #0		    ; store the new non-alpha count
	        BRnzp GET_NEXT		    ; branch to end of conditional structure
AT_LEAST_A
	        ADD R6, R2, R4		    ; compare with 'Z'
	        BRp MORE_THAN_Z         ; branch if > 'Z'

; note that we no longer need the current character
; so we can reuse R2 for the pointer to the correct
; histogram entry for incrementing
ALPHA	    ADD R2, R2, R0		    ; point to correct histogram entry
        	LDR R6, R2, #0		    ; load the count
	        ADD R6, R6, #1		    ; add one to it
	        STR R6, R2, #0		    ; store the new count
    	    BRnzp GET_NEXT		    ; branch to end of conditional structure

; subtracting as below yields the original character minus '`'
MORE_THAN_Z
    	    ADD R2, R2, R5		    ; subtract '`' - '@' from the character
    	    BRnz NON_ALPHA		    ; if <= '`', i.e., < 'a', go increment non-alpha
    	    ADD R6, R2, R4		    ; compare with 'z'
    	    BRnz ALPHA		        ; if <= 'z', go increment alpha count
    	    BRnzp NON_ALPHA		    ; otherwise, go increment non-alpha

GET_NEXT
	        ADD R1, R1, #1		    ; point to next character in string
    	    BRnzp COUNTLOOP		    ; go to start of counting loop



PRINT_HIST

; you will need to insert your code to print the histogram here

; do not forget to write a brief description of the approach/algorithm
; for your implementation, list registers used in this part of the code,
; and provide sufficient comments
            
; description:
; The program overall is a loop with 27 iterations. In every loop, my program will first print the character (like @, A, B...) orderly using the trap vector OUT, then print a
; space character, then print the 4-bit hex number one-by-one in four times. Finally my program will print a new line character and increase/decrease the address/counter and 
; move to next iteration. When the 27 iterations is done, the lc3 will halt. To print the value of 4-bit hex number encoding with ascii code, I divide the 16-bit memory space
; into 4 parts. [15:12], [11:8], [7:4], [3:0], each represent a hex number. I using AND operation with xF000, x0F00, x00F0, x000F to get them independently. After that, I use 
; the right shift respectively 12 times, 8 times, 4 times, 0 times to get the value of the first, second, third, fourth number. Right shift is namely devide by 2, and I use the
; minus 2 continuously controlled by a sub-loop to simulate the devision. Since I have calculated the values, I compared them with 9. Bigger than 9 means the char is a letter 
; between A to F and I should add the ascii value of A-10 to it to print. Smaller means the char is a number and only need to add the ascii value of zero to print. I write four
; blocks codes to print the four characters in a loop. 

; Registers Table

; R0 : hold the char to be printed by traped vector OUT
; R1 : stores the current processing hist's address
; R2 : serves as a counter with value 27 to control the loop
; R3 : stores the current processing symbol (@) or character (A-Z) 's ascii code to print
; R4 : used to store the value after right shift (devision by 2) and used to hold some parameters used in program, such as xF000
; R5 : used as a counter to control the times to right shift and used to hold some parameters used in program, such as #48
; R6 : hold the value in the current hist or the value after right shift operation temporily
; R7 : not used in the program

            LD R1, HIST_ADDR        ; load the starting address of the histogram into register R1
            LD R2, NUM_BINS         ; load the number of bins to be print in R2, which will serve as an overall counter
            LD R3, AT               ; load the ascii value of @ into R3, preparing for the coming printing

PRINT_SYM   ADD R0, R3, #0          ; load the ascii value of @ in R0 to print
            OUT                     ; print the char @ (A,B...in future loops)

PRINT_SP    LD R0, SPACE            ; load the space character into R0 to print
            OUT                     ; print the space character

            LDR R6, R1, #0          ; load the value(the first bin's value) stored in R1's value as the address to R6
            LD R4, FIRST            ; load the xF000 to R4, preparing for the AND operation to get the [15;12] bits of the first bin's value
            AND R5, R5, #0          ; initialize the R5 register
            ADD R5, R5, #12         ; set R5=12, which will serve as a counter of the right shift operation(namely division by 2)
            AND R6, R6, R4          ; get the [15:12] bits of the first bin's value, which exactly is the value of the first char to be print
SHIFT_ONE   AND R4, R4, #0          ; initialize the R4 register
            ADD R4, R4, #-1         ; set R4=-1, which will store the value of the following division

DEVIS_ONE   ADD R4, R4, #1          ; R4=R4+1, a simulation of the division
            ADD R6, R6, #-2         ; simulate the division by continuously adding -2
            BRzp DEVIS_ONE          ; after -2, if the value still positive, then jump back for another minus
            ADD R6, R4, #0          ; after one division, we assign the value to R6 again for next right shift
            ADD R5, R5, #-1         ; minus 1 to the right shift counter
            BRp SHIFT_ONE           ; if positive, it means the right shift is not done, so jump back for another right shift
            ADD R6, R4, #-9         ; compare the final answer to 9
            BRp LET_ONE             ; if bigger than 9, it means the char is a letter, jump to translate the letter to ascii code
            LD R5, ASCII_ZERO       ; if not bigger than 9, the char is a number, so load the zero's ascii code to R5
            ADD R0, R5, R4          ; add the zero's ascii code to the value we get, and we get its ascii code
            BRnzp   PRINT_ONE       ; under all circumstance jump to the print code
LET_ONE     LD R5, ASCII_A          ; load A-10's ascii code to R5
            ADD R0, R5, R4          ; add the A-10's ascii code to the value we get, and we now get its ascii code
PRINT_ONE   OUT                     ; print the first char
            
            LDR R6, R1, #0          ; load the value(the first bin's value) stored in R1's value as the address to R6
            LD R4, SECOND           ; load the x0F00 to R4, preparing for the AND operation to get the [11;8] bits of the first bin's value
            AND R5, R5, #0          ; initialize the R5 register
            ADD R5, R5, #8          ; set R5=8, which will serve as a counter of the right shift operation(namely division by 2)
            AND R6, R6, R4          ; get the [11:8] bits of the first bin's value, which exactly is the value of the second char to be print
SHIFT_BI    AND R4, R4, #0          ; initialize the R4 register
            ADD R4, R4, #-1         ; set R4=-1, which will store the value of the following division

DEVIS_BI    ADD R4, R4, #1          ; R4=R4+1, a simulation of the division
            ADD R6, R6, #-2         ; simulate the division by continuously adding -2
            BRzp DEVIS_BI           ; after -2, if the value still positive, then jump back for another minus
            ADD R6, R4, #0          ; after one division, we assign the value to R6 again for next right shift
            ADD R5, R5, #-1         ; minus 1 to the right shift counter
            BRp SHIFT_BI            ; if positive, it means the right shift is not done, so jump back for another right shift
            ADD R6, R4, #-9         ; compare the final answer to 9
            BRp LET_BI              ; if bigger than 9, it means the char is a letter, jump to translate the letter to ascii code
            LD R5, ASCII_ZERO       ; if not bigger than 9, the char is a number, so load the zero's ascii code to R5
            ADD R0, R5, R4          ; add the zero's ascii code to the value we get, and we get its ascii code
            BRnzp   PRINT_BI        ; under all circumstance jump to the print code
LET_BI      LD R5, ASCII_A          ; load A-10's ascii code to R5
            ADD R0, R5, R4          ; add the A-10's ascii code to the value we get, and we now get its ascii code
PRINT_BI    OUT                     ; print the second char

            LDR R6, R1, #0          ; load the value(the first bin's value) stored in R1's value as the address to R6
            LD R4, THIRD            ; load the x00F0 to R4, preparing for the AND operation to get the [7;4] bits of the first bin's value
            AND R5, R5, #0          ; initialize the R5 register
            ADD R5, R5, #4          ; set R5=4, which will serve as a counter of the right shift operation(namely division by 2)
            AND R6, R6, R4          ; get the [7:4] bits of the first bin's value, which exactly is the value of the third char to be print
SHIFT_TRI   AND R4, R4, #0          ; initialize the R4 register
            ADD R4, R4, #-1         ; set R4=-1, which will store the value of the following division

DEVIS_TRI   ADD R4, R4, #1          ; R4=R4+1, a simulation of the division
            ADD R6, R6, #-2         ; simulate the division by continuously adding -2
            BRzp DEVIS_TRI          ; after -2, if the value still positive, then jump back for another minus
            ADD R6, R4, #0          ; after one division, we assign the value to R6 again for next right shift
            ADD R5, R5, #-1         ; minus 1 to the right shift counter
            BRp SHIFT_TRI           ; if positive, it means the right shift is not done, so jump back for another right shift
            ADD R6, R4, #-9         ; compare the final answer to 9
            BRp LET_TRI             ; if bigger than 9, it means the char is a letter, jump to translate the letter to ascii code
            LD R5, ASCII_ZERO       ; if not bigger than 9, the char is a number, so load the zero's ascii code to R5
            ADD R0, R5, R4          ; add the zero's ascii code to the value we get, and we get its ascii code
            BRnzp   PRINT_TRI       ; under all circumstance jump to the print code
LET_TRI     LD R5, ASCII_A          ; load A-10's ascii code to R5
            ADD R0, R5, R4          ; add the A-10's ascii code to the value we get, and we now get its ascii code
PRINT_TRI   OUT                     ; print the third char


            LDR R6, R1, #0          ; load the value(the first bin's value) stored in R1's value as the address to R6
            LD R4, FOURTH           ; load the x000F to R4, preparing for the AND operation to get the [3;0] bits of the first bin's value
            AND R4, R6, R4          ; get the [3:0] bits of the first bin's value, which exactly is the value of the fourth char to be print
            ADD R6, R4, #-9         ; compare the value to 9
            BRp LET_QUAD            ; if bigger than 9, it means the char is a letter, jump to translate the letter to ascii code
            LD R5, ASCII_ZERO       ; if not bigger than 9, the char is a number, so load the zero's ascii code to R5
            ADD R0, R5, R4          ; add the zero's ascii code to the value we get, and we get its ascii code
            BRnzp   PRINT_QUAD      ; under all circumstance jump to the print code
LET_QUAD    LD R5, ASCII_A          ; load A-10's ascii code to R5
            ADD R0, R5, R4          ; add the A-10's ascii code to the value we get, and we now get its ascii code
PRINT_QUAD  OUT                     ; print the fourth char

            
            LD R0, NEW_LINE         ; load the new line character into R0 to print
            OUT                     ; print the new line character
            ADD R1, R1, #1          ; at the end of the loop we increment the R1 by 1 to print the next address
            ADD R3, R3, #1          ; at the end of the loop we increment the R3 by 1 to print the next letter character
            ADD R2, R2, #-1         ; at the end of the loop we decrease the counter R2 by 1
            BRp PRINT_SYM           ; if R2 is still positive, it means the loop is not done and should be jump to the beginning of the loop -- PRINT_SYM
            BRnzp   DONE            ; if not, it means the loop is over and should be jump to HALT under any circumstance




FIRST       .FILL xF000             ; used to get the [15:12] bits of a bit's value
SECOND      .FILL x0F00             ; used to get the [11:8] bits of a bit's value
THIRD       .FILL x00F0             ; used to get the [7:4] bits of a bit's value
FOURTH      .FILL x000F             ; used to get the [3:0] bits of a bit's value

AT          .FILL #64               ; the ascii code of char @
NEW_LINE    .FILL #10               ; the ascii code of new line character
SPACE       .FILL #32               ; the ascii code of space character
ASCII_ZERO  .FILL #48               ; the ascii code of char 0
ASCII_A     .FILL #55               ; the ascii code of char "A-10"

DONE	    HALT			        ; done


; the data needed by the program
NUM_BINS	.FILL #27	            ; 27 loop iterations
NEG_AT		.FILL xFFC0	            ; the additive inverse of ASCII '@', aka #-64
AT_MIN_Z	.FILL xFFE6	            ; the difference between ASCII '@', and 'Z' aka #-26
AT_MIN_BQ	.FILL xFFE0	            ; the difference between ASCII '@', and '`' aka #-32
HIST_ADDR	.FILL x3F00             ; histogram starting address
STR_START	.FILL x4000	            ; string starting address

; for testing, you can use the lines below to include the string in this
; program...
; STR_START	.FILL STRING	; string starting address
; STRING		.STRINGZ "This is a test of the counting frequency code.  AbCd...WxYz."



	; the directive below tells the assembler that the program is done
	; (so do not write any code below it!)

	        .END
