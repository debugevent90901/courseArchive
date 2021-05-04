; this program is the LC-3 assembly language of a given C code that calculates x*y and stores it in memory. 
; the program loads the values in address X_VAL and Y_VAL and stores the X_VAL * Y_VAL into address x3015
; all integers in the C code are treated as 16-bit signed values.
; the program strictly adherence to the run-time stack convention 
; On exit from foo1, its return value is stored on top of the run-time stack. 
; At the end of the program, R6 will point at address x4001 and R5 will point at x4000. 

        .ORIG x3000

        ;;R5 - frame pointer
        ;;R6 - stack pointer

        ;;MAIN - DO NOT CHANGE ANY CODE HERE
        LD R6, STACK
        LD R5, STACK

        ADD R6, R6, #-2     ; make space for local variables                  

        ; fake scanf("%d %d", &x, &y); 
        LD R0, X_VAL                                                      
        STR R0, R5, #0      ; x <- 5                                           
        LD R0, Y_VAL
        STR R0, R5, #-1     ; y <- 4
  
        ;;CALL FOO1 SUBROUTINE - DO NOT CHANGE ANY CODE HERE
        ADD R6, R6, #-1     ; push address of y on to run-time stack
        ADD R3, R5, #-1
        STR R3, R6, #0   
        ADD R6, R6, #-1     ; push address of x on to run-time stack
        STR R5, R6, #0   

        JSR FOO1

        ;;STACK TEAR-DOWN FOR FOO1 - DO NOT CHANGE ANY CODE HERE
        LDR R0, R6, #0
        ST R0, Z_VAL        ; fake printf("z = %d\n", z);
        ADD R6, R6, #3      ; pop retval and parameters from the stack
 
        ;;“return 0“ - DO NOT CHANGE ANY CODE HERE
        ADD R6, R6, #3
        HALT

STACK   .FILL x4000

X_VAL   .FILL x5
Y_VAL   .FILL x4
Z_VAL   .BLKW #1




        ;;IMPLEMENT ME: FOO1 SUBROUTINE
        ;;R0 - initlize total to be 0, serves as intermediate register to load/store values.
        ;;R1 - store the value of x and the value of x after decrement
        ;;R2 - store the value of y
        ;;R5 - frame pointer
        ;;R6 - stack pointer

FOO1    ADD R6, R6, #-1     ; allocate spot for the return value, R6 = x3FFB
    
        ADD R6, R6, #-1     ; R6 = x3FFA
        STR R7, R6, #0      ; push R7 ( return address)

        ADD R6, R6, #-1     ; R6 = x3FF9
        STR R5, R6, #0      ; push R5 (caller's frame pointer), store R5 = x4000 to R6 = x3FF9

        ADD R5, R6, #-1     ; set new frame pointer, R5 = x3FF8  
        ADD R6, R6, #-1     ; allocate memory for FOO1's local value total, R6 = x3FF8

        AND R0, R0, #0      ; generate a 0 value
        STR R0, R6, #0      ; initialize the value of total to be 0

LOOP    LDR R1, R5, #4      ; pop the address of x into R2
        LDR R1, R1, #0      ; load x = 5 in R1
        BRnz    BREAK       ; if x is equal or less than 0, jump to return value

        LDR R2, R5, #5      ; pop the address of y into R2
        LDR R2, R2, #0      ; load y = 4 in R2
        ADD R6, R6, #-1     ; R6 = x3FF7
        STR R2, R6, #0      ; push y in stack to pass to FOO2
        ADD R6, R6, #-1     ; R6 = x3FF6
        LDR R2, R5, #0      ; load the value of total in R2
        STR R2, R6, #0      ; push total in stack to pass to FOO2
        JSR FOO2            ; call the function FOO2
        LDR R0, R6, #0      ; load the value in R6 = x3FF5 to R0
        STR R0, R5, #0      ; store the value back in x3FF8
        ADD R6, R6, #3      ; pop the parameters (total, *y) passed to FOO2
        LDR R0, R5, #4      ; pop the address of x into R0
        LDR R1, R0, #0      ; load the value of x into R1
        ADD R1, R1, #-1     ; decrease x, i.e. x = x-1
        STR R1, R0, #0      ; store x's new value back to its memory address
        BRnzp LOOP          ; in all conditions jump to LOOP for next iteration

BREAK   LDR R0, R5, #0      ; load local variable total, R5 = x3FF8
        STR R0, R5, #3      ; store the value of total in allocated memory address, x3FFB

        ADD R6, R5, #1      ; pop local variable total

        LDR R5, R6, #0      ; pop the frame pointer, R5 = x4000
        ADD R6, R6, #1      ; R6 = x3FFC

        LDR R7, R6, #0      ; pop the return address
        ADD R6, R6, #1      ; R6 = x3FFB
    
        RET                 ; end the function FOO1


        ;;IMPLEMENT ME: FOO2 SUBROUTINE
        ;;R0 - store the value of y + currentTotal
        ;;R1 - store the value of total
        ;;R2 - store the value of y
        ;;R5 - frame pointer
        ;;R6 - stack pointer

FOO2    ADD R6, R6, #-1     ; allocate spot for the return value, R6 = x3FF5

        ADD R6, R6, #-1     ; R6 = x3FF4
        STR R7, R6, #0      ; push R7 ( return address)

        ADD R6, R6, #-1     ; R6 = x3FF3
        STR R5, R6, #0      ; push R5 (caller's frame pointer), store R5 = x3FF8 to R6 = x3FF3

        ADD R5, R6, #-1     ; set new frame pointer, R5 = x3FF2
        LDR R1, R5, #4      ; load the value of total in R1
        LDR R2, R5, #5      ; load the value of y in R2

        ADD R0, R1, R2      ; add R1 and R2 and store the value in R0, i.e. R0 = total + y
        STR R0, R5, #3      ; store the return value back in x3FF5

        LDR R5, R6, #0      ; pop the frame pointer
        ADD R6, R6, #1      ; R6 = x3FF4

        LDR R7, R6, #0      ; pop the return address
        ADD R6, R6, #1      ; R6 = x3FF5

        RET                 ; end the function FOO2

        .END    

