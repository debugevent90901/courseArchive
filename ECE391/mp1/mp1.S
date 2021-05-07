
.data					# section declaration

        # Useful offset constants for accessing members of a 
        # struct mp1_blink_struct structure
        LOCATION   = 0    
        ON_CHAR    = 2
        OFF_CHAR   = 3 
        ON_LENGTH  = 4
        OFF_LENGTH = 6
        COUNTDOWN  = 8
        STATUS     = 10
        NEXT       = 12

        STRUCT_SIZE = 16

# Pointer to head of list (initialized to NULL)
mp1_list_head:
        .long   0

.text					# section declaration

# Export the function symbol names

.global mp1_rtc_tasklet
.global mp1_ioctl


# void mp1_poke(void);
#
# Interface: Register-based arguments (not C-style)
#    Inputs: %cl  - The byte you wish to write
#            %eax - Offset from the start of video memory that you wish
#                   to write to
#    Outputs: Text-mode video screen is written to at location %eax with
#            the byte in %cl
# Registers: Clobbers EDX
mp1_poke:
        
	movl    vmem_base_addr(, 1), %edx
	movb    %cl, (%edx, %eax, 1)
	ret

# void mp1_rtc_tasklet(unsigned long);
#
# update the state of the game
# Interface:    C-style functions
#   Inputs:     Does not rely on inputs
#   Outputs:    The image displayed on screen blinks
#   Return:     Returns nothing
#   Registers:  Nothing will be clobbered 
mp1_rtc_tasklet:
        # initialize new stack frame
        pushl %ebp
        movl %esp, %ebp
        # callee-saved registers
        pushl %eax
        pushl %ebx
        pushl %ecx

        movl mp1_list_head, %ebx        # cursor in linkedList header

# traverse the linkedList
iterate:
        cmpl $0, %ebx                   # check whether the linkedList ends                   
        je finish
        decw COUNTDOWN(%ebx)            # decrement struct.COUNTDOWN
        cmpw $0, COUNTDOWN(%ebx)
        je update_status                # update status if COUNTDOWN=0
        jmp next

update_status:
        movl $0, %eax                   # set %eax empty since only the lower 16-bits matters in mp1_poke 
        movw LOCATION(%ebx), %ax
        addw %ax, %ax                   # a character takes up 2 bytes, so multiply 2
        # jump to either on_char block or off_char block according to struct.STATUS
        cmpw $0, STATUS(%ebx)   
        je on_char
        jmp off_char

on_char:
        movb ON_CHAR(%ebx), %cl         # set the byte to write
        call mp1_poke
        movw ON_LENGTH(%ebx), %ax
        movw %ax, COUNTDOWN(%ebx)       # set new COUNTDOWN
        movw $1, STATUS(%ebx)           # flip the struct.STATUS
        jmp next                        
# the following off_char block is similar to on_char block
off_char:
        movb OFF_CHAR(%ebx), %cl
        call mp1_poke                
        movw OFF_LENGTH(%ebx), %ax
        movw %ax, COUNTDOWN(%ebx)
        movw $0, STATUS(%ebx)
        jmp next                        

next:
        movl NEXT(%ebx), %ebx          
        jmp iterate                     
finish:
        # restore callee-saved registers
        popl %ecx
        popl %ebx
        popl %eax
        # function ends
        leave 
        ret


# int mp1_ioctl (unsigned long arg, unsigned long cmd);
#
# dispatcher function
# Interface:    Register-based arguments (not C-style)
#   Inputs:     %esi holds the cmd
#               leave arg in stack, they will be called by core functions
#   Return:     This subroutine returns -1 for invalid cmd
# Registers:    Clobbers ESI, EAX
mp1_ioctl:
        movl 8(%esp), %esi              # 8(%esp) -- cmd; 4(%esp) -- arg
        # %esi <0 or %esi > 3
        cmpl $0, %esi
        jl invalid
        cmpl $3, %esi
        jg invalid
        # valid cmd jumps out and end
        jmp *jump_table(, %esi, 4)
        jmp ioctl_return

invalid:
        movl $-1, %eax

ioctl_return:
	ret


# int mp1_ioctl_add(unsigned long arg)
#
# add a blinking location
# Interface:    C-style functions
#   Inputs:     a user-level pointer (arg)   
#   Return:     This subroutine returns -1 for add fail and 0 for add success
# Registers:    Cobbers EAX
mp1_ioctl_add:
        # initialize new stack frame
        pushl %ebp
        movl %esp, %ebp
        # callee-saved registers
        pushl %ebx
        pushl %ecx
        # check null arg handle possible error
        cmpl $0, 8(%ebp)
        je add_fail

        # dynamically allocate memory space
        pushl $STRUCT_SIZE    
        call mp1_malloc         # now %eax = To pointer (empty)
        addl $4, %esp          
        # check whether malloc success, handle error
        cmpl $0, %eax
        je add_fail

        # copy the structure
        pushl $STRUCT_SIZE              
        movl 8(%ebp), %ebx              # %ebx = From pointer (args)
        pushl %ebx                     
        pushl %eax                      
        call mp1_copy_from_user         # now %eax is the return value (should = 0)
        popl %ebx                       # now %ebx = To pointer (full)
        addl $8, %esp                   # restore the rest of the stack pointer
        # check whether copy success, handle error
        cmpl $0, %eax
        jne free
        cmpl $0, %ebx
        je free

        # check the location error
        # 80*25-1 = 1999, if this fails, no need to do the following
        cmpw $0, LOCATION(%ebx)
        jl free
        cmpw $1999, LOCATION(%ebx)
        jg free

        # set countdown = on_length
        movw ON_LENGTH(%ebx), %cx              # %cx = $on_length
        movw %cx, COUNTDOWN(%ebx)
        # set status = 1
        movw $1, STATUS(%ebx)

        # insertion
        movl mp1_list_head, %ecx 
        movl %ecx, NEXT(%ebx)                   
        movl %ebx, mp1_list_head            

        # call mp1_poke                 
        movl $0, %eax                   # set %eax empty since only the lower 16-bits matters in mp1_poke 
        movw LOCATION(%ebx), %ax
        addw %ax, %ax                   # a character takes up 2 bytes, so multiply 2
        movb ON_CHAR(%ebx), %cl         # set the byte to write
        call mp1_poke

add_success:
        movl $0, %eax                   
        jmp add_return
# push the corresponding pointer and call mp1_free
free:
        pushl %ebx                      
        call mp1_free                  
        addl $4, %esp                  
add_fail:
        movl $-1, %eax
add_return:
        # restore callee-saved registers
        popl %ecx
        popl %ebx
        leave
        ret


# int mp1_ioctl_remove(unsigned long arg)
#
# remove a blinking location
# Interface:    C-style functions
#   Inputs:     an integar location (16-bit originally but extended to 32-bit as input)
#   Return:     This subroutine returns -1 for remove fail and 0 for remove success
# Registers:    Cobbers EAX
mp1_ioctl_remove:
        # initialize new stack frame
        pushl %ebp
        movl %esp, %ebp
        # callee-saved registers
        pushl %ebx
        pushl %edi
        
        # search
        movl 8(%ebp), %edi              # %edi = 0x0000+LOCATION
        # check whether location is in range, 80*25-1 = 1999
        cmpw $0, %di
        jl remove_fail
        cmpw $1999, %di
        jg remove_fail
        pushl %edi                      
        call mp1_auxiliary_search
        addl $4, %esp
        # check whether the auxiliary search success, handle error
        cmpl $-1, %eax                   # %eax is the return value, the pointer we want to search
        je remove_fail

        # remove that struct
        # check whether the linkedList head exists, handle error
        movl mp1_list_head, %ebx      # %ebx = linkedList header, serves as a cursor in following search
        # nothing can be removed if mp1_list_head is empty, fail
        cmpl $0, %ebx
        je remove_fail
        # do another search to find the previous struct if head is not the target
        cmpl %ebx, %eax
        jne get_prev
        # do the following if what we want is exactly the linkedList head
        movl NEXT(%eax), %edi           
        movl %edi, %ebx                 
        movl %ebx, mp1_list_head        
        jmp free_memory                 
# this is another search which is slightly different
# it searches the previous struct of the linkedList of our target
# following block is a loop
get_prev:
        cmpl NEXT(%ebx), %eax
        je remove_struct
        movl NEXT(%ebx), %ebx
        cmpl $0, %ebx
        je remove_fail
        jmp get_prev
# delete that struct
remove_struct:
        movl NEXT(%eax), %edi  
        movl %edi, NEXT(%ebx)  
# push the removed pointer and call mp1_free
free_memory:
        pushl %eax              
        call mp1_free          
        addl $4, %esp         
remove_success:
        movl $0, %eax           
        jmp remove_return
remove_fail:
        movl $-1, %eax         
remove_return:
        # restore callee-saved registers
        popl %edi
        popl %ebx
        leave
        ret


# int mp1_ioctl_find(unsigned long arg);
#
# return a specified struct back to user-level
# Interface:    C-style functions
#   Inputs:     a user-level pointer similar to add core  
#   Return:     This subroutine returns -1 for find fail and 0 for find success
# Registers:    Cobbers EAX
mp1_ioctl_find:
	# initialize new stack frame
        pushl %ebp
        movl %esp, %ebp
        # callee-saved registers
        pushl %ebx
        pushl %edi
        # check null arg handle error
        cmpl $0, 8(%ebp)
        je find_fail

        # since the input is user-level pointer, we have to move it to kernel
        # the following operations are similar to what I done in add core
        # dynamically allocate memory space
        pushl $STRUCT_SIZE     
        call mp1_malloc         # now %eax = To pointer (empty)
        addl $4, %esp           
        # check whether malloc success, handle error
        cmpl $0, %eax
        je find_fail

        # copy the structure
        pushl $STRUCT_SIZE             
        movl 8(%ebp), %ebx              # %ebx = From pointer (args)
        pushl %ebx                      
        pushl %eax                      
        call mp1_copy_from_user         # now %eax is the return value (should = 0)
        popl %ebx                       # now %ebx = To pointer (full)
        addl $8, %esp                   
        # check whether copy success, handle error
        cmpl $0, %eax
        jne free_tmp
        cmpl $0, %ebx
        je free_tmp

        movl $0, %edi                   # set the higher 16-bit of %edi=0, convention of my auxiliary search
        movw LOCATION(%ebx), %di        # %di = the location we want to search
        
        # FIXME: MAGIC NUMBER HERE, got -1 during demo
        # check the location error
        # 80*25-1 = 1999, if this fails, no need to do the following
        cmpw $0, %di
        jl free_tmp
        cmpw $1999, %di
        jg free_tmp

        # search
        pushl %edi                      
        call mp1_auxiliary_search       # %eax is the return value, the pointer we want to search
        addl $4, %esp                   
        # check whether the auxiliary search success, handle error
        cmpl $-1, %eax
        je free_tmp

        # copy the structure
        pushl $STRUCT_SIZE              
        pushl %eax                      
        movl 8(%ebp), %eax              # %eax = input, now as output
        pushl %eax                     
        call mp1_copy_to_user           # now %eax is the return value (should = 0)
        addl $12, %esp                  
        # check whether copy success, handle error
        cmpl $0, %eax
        jne free_tmp

# success, return 0 and free the temporary memory
find_success:
        movl $0, %eax                   # return %eax = 0
        pushl %ebx                      
        call mp1_free                   # free the malloc memory
        addl $4, %esp                   
        jmp find_return
# this block perform the same free operation, but is jumpped to when error occurs
free_tmp:
        pushl %ebx                      
        call mp1_free
        addl $4, %esp
find_fail:
        movl $-1, %eax                  # fail return %eax = -1
find_return:
        # restore callee-saved registers
        popl %edi
        popl %ebx
        leave
        ret


# int mp1_ioctl_sync(unsigned long arg);
#
# synchronize a new blink location with an existing one
# Interface:    C-style functions
#   Inputs:     a 32-bit argument packed by 2 16-bit location
#   Return:     This subroutine returns -1 for sync fail and 0 for sync success
# Registers:    Cobbers EAX
mp1_ioctl_sync:
# initialize new stack frame
        pushl %ebp
        movl %esp, %ebp
        # callee-saved registers
        pushl %ebx
        pushl %ecx
        pushl %edi
        # extract 2 int and check null arg
        movl 8(%ebp), %ebx             
        movl $0, %ecx                  
        movw %bx, %cx                   # now %cx = 2nd int
        # check the location error of 2nd int
        # 80*25-1 = 1999, if this fails, no need to do the following
        cmpw $0, %cx
        jl sync_fail
        cmpw $1999, %cx
        jg sync_fail

        shrl $16, %ebx                  # right shift 16-bit, now %bx = 1st int
        # check the location error of 1st int
        # 80*25-1 = 1999, if this fails, no need to do the following
        cmpw $0, %di
        jl sync_fail
        cmpw $1999, %di
        jg sync_fail

        # search 1st int
        movl $0, %edi                   # set the higher 16-bit of %edi=0, convention of my auxiliary search
        movw %bx, %di                   # %di = 1st location we want to search
        pushl %edi                      
        call mp1_auxiliary_search       
        addl $4, %esp                  
        # check whether the auxiliary search success, handle error
        cmpl $-1, %eax                          # %eax is the return value, the pointer we want to search
        je sync_fail
        movl %eax, %ebx                         # %ebx = 1st ptr

        # search 2nd int, similar to the last block
        movl $0, %edi
        movw %cx, %di
        pushl %edi
        call mp1_auxiliary_search
        addl $4, %esp
        cmpl $-1, %eax
        je sync_fail
        movl %eax, %ecx                 # %ecx = 2nd ptr

        # copy the structure partially
        movw ON_LENGTH(%ebx), %di
        movw %di, ON_LENGTH(%ecx)       
        movw OFF_LENGTH(%ebx), %di
        movw %di, OFF_LENGTH(%ecx)     
        movw COUNTDOWN(%ebx), %di
        movw %di, COUNTDOWN(%ecx)       
        movw STATUS(%ebx), %di
        movw %di, STATUS(%ecx)         

        # update the display location to %eax like the core functions above
        movl $0, %eax                  
        movw LOCATION(%ecx), %ax       
        addw %ax, %ax                  
        # jump to either on block or off block with respect to STATUS field
        cmpw $0, STATUS(%ecx)
        je set_char_off
        jmp set_char_on
set_char_on:
        movb ON_CHAR(%ecx), %cl         # set the on_char byte to write
        jmp display                     # goto display
set_char_off:
        movb OFF_CHAR(%ecx), %cl        # set the off_char byte to write
display:
        call mp1_poke                   # since parameters are already set, call mp1_poke
sync_success:
        movl $0, %eax                  
        jmp sync_return
sync_fail:
        movl $-1, %eax                 
sync_return:
        # restore callee-saved registers
        popl %edi
        popl %ecx
        popl %ebx
        leave
	ret

# int mp1_auxiliary_search (unsigned long location);
#
# auxiliary linkedList search
# Interface:    C-style functions
#   Inputs:     an integar location (16-bit originally but extended to 32-bit as input)
#   Return:     This subroutine returns -1 for search fail and the pointer for search success
# Registers:    Cobbers EAX
mp1_auxiliary_search:
        # initialize new stack frame
        pushl %ebp
        movl %esp, %ebp
        # callee-saved registers
        pushl %ebx
        pushl %edi

        movl mp1_list_head, %ebx        # cursor, %ebx = linkedList header
        movl 8(%ebp), %edi              # load the target loaction to %edi (%di actually)
        # check whether the head is empty, if so, nothing to find and fail
        cmpl $0, %ebx
        je search_fail
# a loop that traverse the linkedList
loop:
        # search success if current struct->NEXT = target
        cmpw LOCATION(%ebx), %di
        je search_success
        # update the cursor
        movl NEXT(%ebx), %ebx
        # check whether we reach the end of the linkedList, if so, search fail
        cmpl $0, %ebx
        je search_fail
        jmp loop                        # back to loop

search_fail:
        movl $-1, %eax                   # return -1
        jmp search_return
search_success:
        movl %ebx, %eax                  # return pointer stored in %eax
        jmp search_return
search_return:
        # restore callee-saved registers
        popl %edi
        popl %ebx
        leave
        ret

# jump table defined
jump_table:
.long mp1_ioctl_add, mp1_ioctl_remove, mp1_ioctl_find, mp1_ioctl_sync

.end
