/*
 * tab:2
 *
 * kthsmallest_asm.S - Implementation of Assembly QuickSelect
 *
 * Permission to use, copy, modify, and distribute this software and its
 * documentation for any purpose, without fee, and without written agreement is
 * hereby granted, provided that the above copyright notice and the following
 * two paragraphs appear in all copies of this software.
 *
 * IN NO EVENT SHALL THE AUTHOR OR THE UNIVERSITY OF ILLINOIS BE LIABLE TO
 * ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL
 * DAMAGES ARISING OUT  OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION,
 * EVEN IF THE AUTHOR AND/OR THE UNIVERSITY OF ILLINOIS HAS BEEN ADVISED
 * OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * THE AUTHOR AND THE UNIVERSITY OF ILLINOIS SPECIFICALLY DISCLAIM ANY
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.  THE SOFTWARE
 * PROVIDED HEREUNDER IS ON AN "AS IS" BASIS, AND NEITHER THE AUTHOR NOR
 * THE UNIVERSITY OF ILLINOIS HAS ANY OBLIGATION TO PROVIDE MAINTENANCE,
 * SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS."
 *
 * Author:        Harsh Agrawal
 * Version:       1
 * Creation Date: Tue Jan 26 2021
 * Filename:      kthsmallest_asm.S
 * History:
 *    HA    1    Tue Jan 26 2021
 *        First written.
 */

.text
.global kthSmallest_asm

# kthsmallest ASM (Assembly)
# Finds the kth smallest element in an array
# Declaration is in kthsmallest.h
#
# Registers:
#   eax - Return Value
#   ebx - parameter left
#   ecx - parameter right
#   esi - parameter arr
#   edx - data read/load from/to memory
#   edi - data read/load from/to memory

# Local Variables on the Stack:
# ------j------ <---ESP
# ------i------
# ----pivot----

kthSmallest_asm:
   pushl %ebp
   movl %esp, %ebp

   #--- YOUR CODE HERE ---
   # store the callee-saved reg.
   pushl %ebx    
   pushl %esi
   pushl %edi
   # allocate for three local var.
   subl $12, %esp  

   movl 8(%ebp), %esi  # ESI <- arr   
   movl 12(%ebp), %ebx # EBX <- left
   movl 16(%ebp), %ecx # ECX <- right

   movl (%esi,%ecx,4), %edx  # int pivot = arr[right];
   movl %edx, 8(%esp)
   movl %ebx, 4(%esp)        # int i = left;
   movl %ebx, (%esp)         # int j = left;

   loop:
   # loop-checking condition
   movl (%esp), %edx
   cmpl %ecx, %edx           # (j - right)
   jge  loop_out
   # condition for if statement
   movl (%esp), %edx
   movl (%esi,%edx,4), %edi
   movl 8(%esp), %edx
   cmpl %edi, %edx  # (pivot-arr[j])
   jl   if_out
   pushl %ecx
   # PUSH &arr[j]
   movl -24(%ebp), %edx  # EDX <- j
   leal (%esi,%edx,4), %edi # EDI <- &arr[j]
   pushl %edi 
   # PUSH &arr[i]
   movl -20(%ebp), %edx # EDX <- i
   leal (%esi,%edx,4), %edi # EDI <- &arr[i]
   pushl %edi
   call swap
   addl $8, %esp
   popl %ecx
   # i++
   movl 4(%esp), %edx
   incl %edx
   movl %edx, 4(%esp)
   # j++
   if_out:
   movl (%esp), %edx
   incl %edx
   movl %edx, (%esp)
   jmp loop

   loop_out:
   # Calling swap
   pushl %ecx
   # PUSH &arr[right]
   leal (%esi,%ecx,4), %edx
   pushl %edx
   # PUSH &arr[i]
   movl -20(%ebp), %edx
   leal (%esi,%edx,4), %edi
   pushl %edi
   call swap
   addl $8, %esp
   popl %ecx

   movl 4(%esp), %edx # EDX <- i
   movl 20(%ebp), %edi # EDI <- k
   cmpl %edx, %edi # (k - i)
   jl left_array   # k < i
   jg right_array  # k > i
   # k == i: return value goes to EAX
   movl (%esi,%edi,4), %eax
   jmp done 

   left_array:
   movl 20(%ebp), %edx
   pushl %edx # push k
   movl -20(%ebp), %edx
   decl %edx  
   pushl %edx # push i-1
   pushl %ebx # push left
   pushl %esi # push arr
   call kthSmallest_asm
   addl $16, %esp
   jmp done 

   right_array:
   movl 20(%ebp), %edx
   pushl %edx # push k
   pushl %ecx # push right
   movl -20(%ebp), %edx
   incl %edx
   pushl %edx # push i+1
   pushl %esi # push arr
   call kthSmallest_asm
   addl $16, %esp  

   done:   
   addl $12, %esp # tear down local var.
   popl %edi
   popl %esi
   popl %ebx
   #----------------------

   leave
   ret
