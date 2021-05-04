; Assuming user will only enter ' ' 0-9 *+/-
; Result can be either negative or positive

; your main program should be just a few calls to subroutines, e.g.,

; the main subroutine is simply three calls to subroutines, which respecrtively save the inputs, 
; calculate the final answer and print it to the screen.

                .ORIG x3000
MAIN            LD R1, ADDR                     ; load the address to save the inputs
	            JSR INPUT                       ; jump to the subroutine to get input
 	            JSR EVALUATE                    ; jump to the subroutine to calculate 
	            ADD	R6, R0, #0	                ; store the result in R6
 	            JSR PRINT                       ; jump to the subroutine to print the answer to screen

	            HALT                            ; stop the lc3 machine

ADDR	        .FILL x5000                     ; the address to save the inputs

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; get input from the keyboard and store it in memory per MP2 specifications
; input: R1 - starting address of the memory to store the expression string
; output: input from the keyboard stored in memory starting from the address passed in R1

; In this subroutine:
; R2:load the negative of the ascii of the character, play as a tester
; R3:input of subroutine MULTIPLY, store the multiple digit number
; R4:input of subroutine MULTIPLY, store #10
; R5:signal of POP/PUSH
; R6:count how many digit are putting into stack
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; this subroutine serves to accept the keyboard inputs and save them to memory. First, the program save the current registers' values to memory so
; as not to erease them. Then the program use trap vectors GETC and OUT to accept an input and echo it on screen. To achieve the challenge assignment,
; the program use stack to receive inputs with multiple digits like 234, in the loop, the program would push every numbers onto stack and keep iteration
; until a space is accepted, then the stack would pop all the numbers and respectively multipy them with 1, 10 ... and add them up so that the challenge 
; is achieved. Since operators only take one digit, it won't be affected. Every time there is an input space, the subroutine would jump to DECODE 
; subroutine to decode and save it. The subroutine would end only when there's an new line char input. Finally the former values of registers will be restored.
		
; add your code from Lab 3 here
INPUT
            	ST R7, SaveR7_INPUT	        	; store the initial values of the registers when the subroutine begins
            	ST R6, SaveR6_INPUT             
            	ST R5, SaveR5_INPUT             
            	ST R4, SaveR4_INPUT            
            	ST R3, SaveR3_INPUT             
            	ST R2, SaveR2_INPUT             
            	ST R1, SaveR1_INPUT             
            	ST R0, SaveR0_INPUT             

            	AND	R6,R6,#0			        ; initialize R6

NEXT_C	        GETC				            ; read a character from kb and store in R0
            	OUT				                ; echo the character on the screen
            	LD R2, NEG_NEW_LINE		        ; get the negative of the ascii of '\n'
            	ADD	R2, R2, R0		    	    ; if character == '\n'
            	BRz	STOP_INPUT		            ; stop reading
            	LD R2, NEG_SPACE	        	; get the negative of the ascii of ' ' 
            	ADD	R2, R2, R0			        ; if character == ' '
            	BRz	STACK_GET		            ; get the digit/operator from stack
            	JSR	DECODE			            ; jump to subroutine decode
            	JSR PUSH			            ; push the digit/operator into stack
            	ADD	R6, R6, #1			        ; increase the stack counter
            	BRnzp NEXT_C			        ; read the next character
    	
STACK_GET
            	ST R1, SaveR1_SG		        ; save initial R1
            	AND	R2, R2, #0			        ; initialize R2
            	AND	R1, R1, #0			        ; initialize R1
            	ADD	R1, R1, #10		            ; initialize R1 to 10
            	AND	R4, R4, #0			        ; initialize R4
            	ADD	R4, R4, #1			        ; initialize R4 to 1

GET	            JSR	POP			                ; pop the digit/operator out of stack e.g.R0 = 2
            	ADD	R3, R0, #0			        ; ready for multiply
            	JSR	MULTIPLY		            ; the digit of current digit place(n) * 10^n
            	ADD	R2, R2, R0			        ; add it to the result
            	ADD	R6, R6, #-1			        ; decrease the stack counter
            	BRnz STORE_INPUT		        ; store the multiple digit/operator
            	ADD	R3, R1, #0			        ; 10^(n+1)
            	JSR	MULTIPLY		            ;
            	ADD	R4, R0, #0			        ; put 10^(n+1) into next mult process
            	BRnzp GET			            ; get the next digit place

SaveR1_SG   	.FILL x0000

STORE_INPUT
	            LD R1, SaveR1_SG		        ; restore R1
            	ADD	R0, R2, #0			        ; put the final result back to R0
            	STR	R0, R1, #0		         	; store the multiple digit/operator
            	ADD	R1, R1, #1		        	; next address
            	BRnzp NEXT_C		        	; next character

STOP_INPUT
	            JSR	POP		                	; get the last operator
            	STR	R0, R1, #0		        	; store the last operator
            	ADD	R1, R1, #1	         		; next address
            	LD R0, NEG_NEW_LINE		
            	STR	R0, R1, #0		        	; store 2's complement of '\n' into the last address

            	LD R6, SaveR6_INPUT		        ; restore the register at the end of the subroutine
            	LD R5, SaveR5_INPUT             
            	LD R4, SaveR4_INPUT             
            	LD R3, SaveR3_INPUT             
            	LD R2, SaveR2_INPUT             
            	LD R1, SaveR1_INPUT             
            	LD R0, SaveR0_INPUT             
            	LD R7, SaveR7_INPUT             
            	RET				                ; end the subroutine
            
SaveR7_INPUT	.FILL x0000                     ; used to store values of registers temporily
SaveR6_INPUT	.FILL x0000                     
SaveR5_INPUT	.FILL x0000                     
SaveR4_INPUT	.FILL x0000                     
SaveR3_INPUT	.FILL x0000                     
SaveR2_INPUT	.FILL x0000                     
SaveR1_INPUT	.FILL x0000                     
SaveR0_INPUT	.FILL x0000                     


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; find the real value of operand, or keep the 2's complement ASCII value if operator
; input: R0 holds the input
; output: R0

; In this subroutine:
; R2:load the negative of the ascii of the character, play as a tester
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; in this subroutine, the program would decode the input numbers from ASCII values to numerical values and save them in memory starting with x5000. If 
; the input is a operator, the program would save its negative ASCII values to memory. To achieve the second challenge, I add some extra function to the
; program. First compare the input with ASCII value of 9, if bigger, then the input is invalid. Then compare with ASCII 0, if bigger, the input is valid
; numbers and we substract it with ASCII value of 0 and we get its numerical value. SO we store it in memory and end the subroutine. If the input is 
; smaller than ASCII 0, we respectively compare it with negative value of ASCII +-*/, if equal, than the input is valid operator and we take its 2's 
; complement value by taking its 1's complement and add 1. So we can store it in memory. If none of the four operators' ASCII values match, the input is
; invalid. To deal with invalid input, we use trap vector PUTS and .STRINGZ to output " Error invalid input " to screen. This subroutine also stores the 
; values of the used registers in the beginning and restore them at the end of the subroutine.

; add your code from Lab 3 here
DECODE
                ST R7, SaveR7_DECODE	        ; store the initial registers
            	ST R2, SaveR2_DECODE

            	LD R2, NEG_ASCII_NINE	        ; get the negative of the ascii of '9'
            	ADD	R2, R2, R0			        ; if character > '9'
               	BRp	ERROR_INVALID		        ; invalid input
            	LD R2, NEG_ASCII_ZERO	        ; get the negative of the ascii of '0'
            	ADD	R2, R2, R0		    	    ; if character >= 0, <= 9
            	BRzp DIG_DECODE		            ; decode the ascii of digits
            	LD R2, NEG_PLUS		            ; get the negative of the ascii of '+'
             	ADD R2, R2, R0		        	; if character == '+'
            	BRz OP_DECODE	            	; decode
              	LD R2, NEG_MINUS	        	; get the negative of the ascii of '-'
              	ADD R2, R2, R0		        	; if character == '-'
            	BRz OP_DECODE		            ; decode
            	LD R2, NEG_MULTI	        	; get the negative of the ascii of '*'
            	ADD R2, R2, R0	        		; if character == '*'
               	BRz OP_DECODE		            ; decode
            	LD R2, NEG_DIV	            	; get the negative of the ascii of '/'
            	ADD	R2, R2, R0	        		; if character == '/'
            	BRz OP_DECODE	            	; decode
            	BRnzp ERROR_INVALID	        	; error invalid input

DIG_DECODE
            	ADD	R0, R2, #0			        ; get the real value of the digit
            	BRnzp DECODE_RETURN		        ; return R0
OP_DECODE
            	NOT	R0, R0			            ; 1's complement of ascii of operator
            	ADD	R0, R0, #1			        ; 2's complement of ascii of operator
            	BRnzp DECODE_RETURN		        ; return R0
        
DECODE_RETURN
            	LD R2, SaveR2_DECODE	        ; restore the registers
            	LD R7, SaveR7_DECODE
            	RET				                ; end the subroutine

ERROR_INVALID
            	LEA	R0, ERROR		            ; print the error message
            	PUTS
            	HALT

ERROR		    .STRINGZ "\nError invalid input"
SaveR2_DECODE	.FILL x0000
SaveR7_DECODE	.FILL x0000


NEG_NEW_LINE    .FILL #-10
NEG_SPACE       .FILL #-32
NEG_PLUS        .FILL #-43 
NEG_MINUS       .FILL #-45
NEG_MULTI       .FILL #-42
NEG_DIV         .FILL #-47
NEG_ASCII_NINE  .FILL #-57
NEG_ASCII_ZERO  .FILL #-48
NEW_LINE	    .FILL #10
ASCII_ZERO  	.FILL #48
ASCII_PLUS	    .FILL #43
ASCII_MINUS	    .FILL #45
ASCII_MULTI	    .FILL #42
ASCII_DIV	    .FILL #47
STACK_TEST	    .FILL x0FFF

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Print value stored in register R0 in decimal format
; input: R0 - holds the input
; output: signed decimal value printed on the display

; In this subroutine:
; R0:store the result for subroutines
; R1:store every digit place(remainder of dividing)
; R2:count how many digit are putting into stack
; R3:store the number being divided
; R4:store #10 as a divisor, in order to print numbers in every digit place
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; This subroutine will print the answer calculated in subroutine EVALUATE to screen with the form of a decimal number. The subroutine will use the following 
; algorithm using another subroutine DIVIDE. Divide the value to print by 10 and store the quotient for further use and push the remainder on to stack. If the 
; quotient is not 0, the program go back to divide the quotient by zero again and push the remainder on to stack. When the quotient is zero, pop values of the
; stack one at a time till the stack is empty. Add each value with the ASCII value 0 and use the trap vector OUT to print to screen. This subroutine also stores 
; the values of the used registers in the beginning and restore them at the end of the subroutine.


; add your code here
PRINT
	            ST R7, SaveR7_PRINT		        ; store the initial registers
            	ST R6, SaveR6_PRINT
            	ST R5, SaveR5_PRINT
            	ST R4, SaveR4_PRINT
            	ST R3, SaveR3_PRINT
            	ST R2, SaveR2_PRINT
            	ST R1, SaveR1_PRINT
            	ST R0, SaveR0_PRINT

            	AND	R4, R4, #0			        ; initialize R4 to 10
            	ADD	R4, R4, #10		            ; as a divisor
            	ADD	R2, R2, #0			        ; initialize R2 to 0
            	ADD	R3, R0, #0			        ; give the result to R3
            	BRzp DEC			            ; if result < 0
            	NOT	R3, R3			
            	ADD	R3, R3, #1			        ; take the absolute value of result
            	LD R0, ASCII_MINUS		        ; print out '-'
            	OUT
DEC	            JSR	DIVIDE		            	; result divide by 10
	            ADD	R3, R0, #0		        	; give the result of dividing back to R3
	            ADD	R0, R1, #0		        	; give the remainder to R0
	            JSR	PUSH		            	; push it to the stack
	            ADD	R2, R2, #1		        	; stack counter plus 1
	            ADD	R3, R3, #0		        	; whether dividing is end
	            BRz	PRINT_OUT	            	; print out the decimal number
	            BRnzp DEC			            ; continue dividing

PRINT_OUT
	            JSR	POP		                	; pop the number in the highest decimal number place
            	LD R1, ASCII_ZERO	        	; ascii of '0'
            	ADD	R0, R0, R1			        ; ascii of the number
            	OUT				                ; print out
            	ADD	R2, R2, #-1		        	; stack counter decrease 1
            	BRnz END_PRINT		            ; if all number are popped, end print
            	BRnzp PRINT_OUT		            ; pop and print next decimal number

END_PRINT
            	LD R0, SaveR0_PRINT		        ; restore the register
            	LD R6, SaveR6_PRINT
            	LD R5, SaveR5_PRINT
            	LD R4, SaveR4_PRINT
            	LD R3, SaveR3_PRINT
            	LD R2, SaveR2_PRINT
            	LD R1, SaveR1_PRINT
            	LD R7, SaveR7_PRINT
            	RET				                ; end the subroutine

SaveR7_PRINT	.FILL x0000
SaveR6_PRINT	.FILL x0000
SaveR5_PRINT	.FILL x0000
SaveR4_PRINT	.FILL x0000
SaveR3_PRINT	.FILL x0000
SaveR2_PRINT	.FILL x0000
SaveR1_PRINT	.FILL x0000
SaveR0_PRINT	.FILL x0000
	

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; input: R1 - start address of the expression string
; output: R0 - the numerical value of the end result

; In this subroutine:
; R0:store input/result for subroutines
; R1:address of current operator/operand
; R2:load the negative of the ascii of the character, play as a tester
; R3:input 1 for operating subroutine
; R4:input 2 for operating subroutine
; R5:signal of POP/PUSH
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; This subroutine is the most important one in this mp and it will calculate the result of operands and operators stored in memory. The subroutine contains a loop and at the 
; start of the loop, the program will detect whether there's a new line char, if so, the subroutine will end. In other case, as the flow chart offered in mp2.pdf implies, judge 
; the current value, if the value is an operand, push it on to the stack and go on next iteration in next memory location. If is not a operand, then pop two values from stack 
; and detect stack underflow, if not, jump to subroutine of +-*/ to apply the operation and push the result again onto the stack. When a new line char is loaded from memory, 
; if the stack has only one value, then the value in the stack is the final result, else the input chars in subroutine INPUT is invalid, so we need to print "Invalid Expression".
; This subroutine also stores the values of the used registers in the beginning and restore them at the end of the subroutine.

; your code goes here
EVALUATE
	            ST R7, SaveR7_EVAL		        ; store the initial register
            	ST R1, SaveR1_EVAL 
            	ST R2, SaveR2_EVAL
            	ST R3, SaveR3_EVAL
            	ST R4, SaveR4_EVAL
            	ST R5, SaveR5_EVAL

EVAL_LOOP
            	LDR	R0, R1, #0			        ; load operator/operand in current address
            	LD R2, NEW_LINE		            ; get the ascii of '\n'
            	ADD	R2, R2, R0		        	; if memory is end
            	BRz	END_EVAL		            ; end evaluate

            	ADD	R2, R0, #0			        ; if operator( R0 < 0 )
            	BRn	OPERATOR		            ; go judging operator
            	JSR	PUSH			            ; if not(operand), push the operand into the stack
            	ADD	R1, R1, #1		        	; next address
            	BRnzp EVAL_LOOP		            ; load next operator/operand	

OPERATOR
IF_PLUS	        LD R2, ASCII_PLUS	        	; get the ascii of '+'
            	ADD R2, R2, R0		          	; if operator == '+'
            	BRnp IF_MINUS		        	; if not, go to judge next operator
            	JSR	POP			                ; pop first value
            	ADD	R3, R0, #0		        	; store in R3
            	JSR	POP			                ; pop second value
            	ADD	R4, R0, #0		        	; store in R4
            	ADD	R5, R5, #0	            	; if underflow
            	BRp	INVALID_EX	            	; invalid expression
            	ADD	R0, R3, R4		        	; add two operands
            	JSR	PUSH		            	; push the result to the stack
            	ADD	R1, R1, #1		        	; next address
            	BRnzp EVAL_LOOP	            	; load next operator/operand
    
IF_MINUS
            	LD R2, ASCII_MINUS	        	; get the ascii of '-'
              	ADD R2, R2, R0		        	; if operator == '-'
            	BRnp IF_MULT		        	; if not, go to judge next operator
             	JSR	POP		                	; pop first value
            	ADD	R4, R0, #0	        		; store in R4
            	JSR	POP			                ; pop second value
            	ADD	R3, R0, #0		        	; store in R3
            	ADD	R5, R5, #0		        	; if underflow
            	BRp	INVALID_EX	            	; invalid expression
            	JSR	MINUS		            	; R0 = R3 - R4
            	JSR	PUSH		            	; push the result to the stack
            	ADD	R1, R1, #1	        		; next address
            	BRnzp EVAL_LOOP	            	; load next operator/operand
 
IF_MULT	        LD R2, ASCII_MULTI	        	; get the ascii of '*'
            	ADD R2, R2, R0		        	; if character == '*'
            	BRnp IF_DIVD		        	; if not, go to judge next operator
            	JSR	POP		                	; pop first value
            	ADD	R3, R0, #0		        	; store in R3
            	JSR	POP		                	; pop second value
            	ADD	R4, R0, #0		        	; store in R4
            	ADD	R5, R5, #0		        	; if underflow
            	BRp	INVALID_EX	            	; invalid expression
            	ADD	R0, R3, R4	        		; multiply two operands
            	JSR	MULTIPLY	            	; R0 = R3 * R4
            	JSR	PUSH		            	; push the result to the stack
            	ADD	R1, R1, #1	        		; next address
            	BRnzp EVAL_LOOP	            	; load next operator/operand
    	
IF_DIVD	LD  	R2, ASCII_DIV	            	; get the ascii of '/'
	            ADD	R2, R2, R0	        		; if character == '/'
               	JSR	POP		                	; pop first value
            	ADD	R4, R0, #0		        	; store in R4
            	JSR	POP			                ; pop second value
            	ADD	R3, R0, #0		        	; store in R3
            	ADD	R5, R5, #0		        	; if underflow
            	BRp	INVALID_EX	            	; invalid expression
            	ADD	R2, R1, #0		        	; save current address
            	JSR	DIVIDE		            	; R0 = R3 / R4
            	ADD	R1, R2, #0		        	; reload avoid remainder in DIVIDE(R1) broke the data
            	JSR	PUSH		            	; push the result to the stack
            	ADD	R1, R1, #1		        	; next address
            	BRnzp EVAL_LOOP	            	; load next operator/operand
        
END_EVAL
            	JSR	POP		                	; poping out the result
            	JSR	POP			                ; judging whether the stack has 1 value
            	ADD	R5, R5, #0		        	; whether R5 = 1, which means underflow
            	BRnz INVALID_EX		            ; invalid expression
            	LD R1, SaveR1_EVAL	        	; restore the initial register
            	LD R2, SaveR2_EVAL
            	LD R3, SaveR3_EVAL
            	LD R4, SaveR4_EVAL
            	LD R5, SaveR5_EVAL
            	LD R7, SaveR7_EVAL
            	RET

INVALID_EX
            	LEA	R0, INVALID
            	PUTS
            	HALT

INVALID		    .STRINGZ "Invalid Expression"

SaveR1_EVAL 	.FILL x0000
SaveR2_EVAL	    .FILL x0000
SaveR3_EVAL	    .FILL x0000
SaveR4_EVAL	    .FILL x0000
SaveR5_EVAL	    .FILL x0000
SaveR7_EVAL	    .FILL x0000

;;;;;;;;;;;;;;;
; input: R3, R4
; out: R0
;;;;;;;;;;;;;;;
; This is a simple subroutine that add R3 and R4 together and save the result to R0. The subroutine will stores
; the values of the used registers in the beginning and restore them at the end of the subroutine.

; your code goes here
PLUS
	            ST R7, SaveR7_PLUS	            ;store the initial register
	            ADD	R0, R3, R4
	            LD R7, SaveR7_PLUS		        ;restore the registers
	            RET

SaveR7_PLUS	    .FILL x0000

;;;;;;;;;;;;;;;
; input: R3, R4
; out: R0
;;;;;;;;;;;;;;;
; this is also a simple subroutine that calculate R3-R4 and stores the result to R0. The subroutine uses plus a number's
; 2's complement to simulate the minus operation. The subroutine will stores the values of the used registers in the beginning 
; and restore them at the end of the subroutine.

; your code goes here
MINUS
	            ST R7, SaveR7_MINUS		        ; store the initial register
	            ST R4, SaveR4_MINUS	
	            NOT	R4, R4			            ; -R4-1
	            ADD	R4, R4, #1		        	; -R4
            	ADD	R0, R3, R4			        ; R3-R4
            	ST R4, SaveR4_MINUS	
            	LD R7, SaveR7_MINUS     		; restore the registers
            	RET

SaveR4_MINUS	.FILL x0000
SaveR7_MINUS	.FILL x0000

;;;;;;;;;;;;;;;;;;;
; input: R3, R4
; out: R0 = R3 x R4
;;;;;;;;;;;;;;;;;;;
; This subroutine is used to apply the multiply operation. This subroutine uses addition to simulate the multiply operation using a
; loop. As the mp instruction implies, the subroutine contains a block of codes to deal with the positive and negative operands so 
; the stack calculator supports negative operations. This subroutine also stores the values of the used registers in the beginning
; and restore them at the end of the subroutine.

; your code goes here
MULTIPLY
            	ST R7, SaveR7_MULT		        ; store the initial register
            	ST R1, SaveR1_MULT
            	ST R3, SaveR3_MULT
            	ST R4, SaveR4_MULT

            	AND	R0, R0, #0			        ; initialize R0
            	AND	R1, R1, #0		        	; initialize R1
M_SIGN_R3
            	ADD	R3, R3, #0		        	; whether R3 >= 0
            	BRzp M_POS_R3			
            	ADD	R1, R1, #-1		        	; if not, R1-1
            	NOT	R3, R3			            ; abs(R3)-1
            	ADD	R3, R3, #1		        	; abs(R3)
            	BRnzp M_SIGN_R4
M_POS_R3
            	ADD	R1, R1, #1		        	; if R3 >= 0, R1+1
M_SIGN_R4
            	ADD	R4, R4, #0		        	; whether R4 >= 0 
            	BRzp M_POS_R4			
            	ADD	R1, R1, #-1		        	; if not, R1-1
            	NOT	R4, R4			            ; abs(R4)-1
            	ADD	R4, R4, #1		        	; abs(R4)
            	BRnzp MULT
M_POS_R4
            	ADD	R1, R1, #1		        	; if R4 <= 0, R1+1
	
MULT	        ADD	R3, R3, #-1		        	; decrese the counter
	            BRn	STOP_MULT	            	; if counter = 0, stop multiply
	            ADD	R0, R0, R4	        		; mult by adding
	            BRnzp MULT			

STOP_MULT
	            ADD	R1, R1, #0		        	; only when R3 have the different sign with R4
	            BRnp MULT_RETURN	        	; R1 would be 0
	            NOT	R0, R0			            ; R0 should be negative
	            ADD	R0, R0, #1		        	; R0 = -R0
    
MULT_RETURN
	            LD R1, SaveR1_MULT		        ; store the initial register
    	        LD R3, SaveR3_MULT
    	        LD R4, SaveR4_MULT
    	        LD R7, SaveR7_MULT
            	RET			                	; end the subroutine

SaveR1_MULT	    .FILL x0000
SaveR3_MULT	    .FILL x0000
SaveR4_MULT	    .FILL x0000
SaveR7_MULT	    .FILL x0000


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; input: R3, R4
; out: R0 - quotient (R0 = R3 / R4), R1 - remainder 
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;i;
; This subroutine is used to apply the division operation. This subroutine uses substract to simulate the division operation using a
; loop. The substract operation is also simulated in the form of adding a number's 2's complement.  As the mp instruction implies, the
; subroutine contains a block of codes to deal with the positive and negative operands so the stack calculator supports negative operations.
; This subroutine also stores the values of the used registers in the beginning and restore them at the end of the subroutine.

; your code goes here
DIVIDE

            	ST R7, SaveR7_DIVI		        ; store the initial register
            	ST R3, SaveR3_DIVI
            	ST R4, SaveR4_DIVI
            	ST R2, SaveR2_DIVI

            	ADD	R4, R4, #0			        ; if R4 is 0 (divisor can't be 0)
            	BRz	INVALID_EX	            	; invalid input

            	AND	R0, R0, #0		        	; initialize R0
            	AND	R2, R2, #0		        	; initialize R2
D_SIGN_R3
            	ADD	R3, R3, #0		        	; whether R3 >= 0
            	BRzp D_POS_R3			
            	ADD	R2, R2, #-1		        	; if not, R2-1
            	NOT	R3, R3			            ; abs(R3)-1
            	ADD	R3, R3, #1		        	; abs(R3)
            	BRnzp D_SIGN_R4
D_POS_R3
            	ADD	R2, R2, #1		        	; if R3 >= 0, R2+1
D_SIGN_R4
            	ADD	R4, R4, #0		        	; whether R4 > 0 
            	BRp	D_POS_R4		        	
            	ADD	R2, R2, #-1		        	; if not, R2-1
                NOT	R4, R4		            	; abs(R4)-1
            	ADD	R4, R4, #1	        		; abs(R4)
              	BRnzp DIVI
D_POS_R4
            	ADD	R2, R2, #1		        	; if R4 <= 0, R2+1
DIVI        	NOT	R4, R4			
            	ADD	R4, R4, #1		        	; -abs(R4)
DIVI_LOOP
            	ADD	R3, R3, R4		        	; R3-abs(R4) divide by subtraction
            	BRn	STOP_DIVI	            	; finish dividing, go return
            	ADD	R0, R0, #1		        	; add quotient
            	BRnzp DIVI_LOOP	            	; continue dividing
STOP_DIVI
            	NOT	R4, R4			
            	ADD	R4, R4, #1			        ; abs(R4)
            	ADD	R1, R3, R4		        	; get remainder (of all positive R3,R4)
            	ADD	R2, R2, #0		          	; only when R3 have the different sign with R4
            	BRnp DIVI_RETURN	        	; R2 would be 0
             	NOT	R0, R0		            	; R0 should be negative
            	ADD	R0, R0, #1		        	; R0 = -R0
DIVI_RETURN
            	LD R2, SaveR2_DIVI	        	; store the initial register
            	LD R3, SaveR3_DIVI
            	LD R4, SaveR4_DIVI
            	LD R7, SaveR7_DIVI
            	RET			                	; end the subroutine

SaveR2_DIVI 	.FILL x0000
SaveR3_DIVI 	.FILL x0000
SaveR4_DIVI 	.FILL x0000
SaveR7_DIVI 	.FILL x0000



;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; stack subroutines - do not modify

; PUSH subroutine
; IN: R0
; OUT: R5 (0-success, 1-fail/overflow)
; registers used: R3: STACK_END R4: STACK_TOP
;
PUSH	
            	ST R3, PUSH_SaveR3	            ; save R3
            	ST R4, PUSH_SaveR4	            ; save R4
            	AND R5, R5, #0	            	;
            	LD R3, STACK_END            	;
            	LD R4, STACk_TOP            	;
            	ADD R3, R3, #-1	            	;
            	NOT R3, R3	                	;
            	ADD R3, R3, #1	            	;
            	ADD R3, R3, R4	            	;
            	BRz OVERFLOW	            	; stack is full
            	STR R0, R4, #0	            	; no overflow, store value in the stack
            	ADD R4, R4, #-1	            	; move top of the stack
            	ST R4, STACK_TOP            	; store top of stack pointer
            	BRnzp DONE_PUSH	            	;
OVERFLOW
            	ADD R5, R5, #1	            	;
DONE_PUSH
            	LD R3, PUSH_SaveR3          	;
            	LD R4, PUSH_SaveR4          	;
            	RET

PUSH_SaveR3	    .BLKW #1                    	;
PUSH_SaveR4 	.BLKW #1                    	;


; POP subroutine
; OUT: R0, R5 (0-success, 1-fail/underflow)
; registers used: R3 STACK_START R4 STACK_TOP
;
POP	
            	ST R3, POP_SaveR3           	; save R3
            	ST R4, POP_SaveR4           	; save R3
            	AND R5, R5, #0	            	; clear R5
            	LD R3, STACK_START          	;
            	LD R4, STACK_TOP            	;
            	NOT R3, R3	                	;
            	ADD R3, R3, #1	            	;
            	ADD R3, R3, R4          		;
            	BRz UNDERFLOW	            	;
            	ADD R4, R4, #1	            	;
            	LDR R0, R4, #0	            	;
            	ST R4, STACK_TOP            	;
            	BRnzp DONE_POP	            	;
UNDERFLOW
            	ADD R5, R5, #1	            	;
DONE_POP                
            	LD R3, POP_SaveR3           	;
            	LD R4, POP_SaveR4           	;
            	RET

POP_SaveR3	    .BLKW #1                    	;
POP_SaveR4	    .BLKW #1                    	;

STACK_END   	.FILL x3FF0                 	;
STACK_START	    .FILL x4000                 	;
STACK_TOP	    .FILL x4000                 	;

                .END
