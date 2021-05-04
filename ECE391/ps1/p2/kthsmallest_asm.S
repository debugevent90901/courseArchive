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
#   eax - Return Value, pivot
#   ebx - arr[]
#   ecx - left, index i
#   edx - right
#   edi - k, arr[j]
#   esi - index j


kthSmallest_asm:
   # old base pointer in stack, new function begins
   # set new ebp = esp, stack pointer
   pushl %ebp
   movl %esp, %ebp

   # --- YOUR CODE HERE ---
   # movl $1, %eax
   # caller-saved ebx, ecx, edx, edi, %esi
   # pushl %eax
   pushl %ebx
   pushl %ecx
   pushl %edx
   pushl %edi
   pushl %esi


   # load arguments
   # 4(%ebp) is the eip (in stack when call)
   # %ebx = arr[]
   movl 8(%ebp), %ebx
   # %ecx = i = left
   movl 12(%ebp), %ecx
   # %edx =  right
   movl 16(%ebp), %edx
   # %edi = k
   # movl 20(%ebp), %edi

   # set %esi = j = left
   movl %ecx, %esi
LOOP:
   # j < right
   cmpl %edx, %esi
   jge LOOP_DONE
   # load arr[j] to edi
   movl (%ebx, %esi, 4), %edi
   # load pivot to eax
   movl (%ebx, %edx, 4), %eax
   # compare arr[j] and pivot
   cmpl %edi, %eax
   jl CONTINUE
   # load %eax=&arr[i]; %edi=&arr[j]
   leal (%ebx, %ecx, 4), %eax
   leal (%ebx, %esi, 4), %edi
   pushl %edi
   pushl %eax
   call swap
   popl %eax
   popl %edi

   incl %ecx

CONTINUE:
   # %edx =  right
   # IF YOU DELETE THIS LINE, THE PROGRAM WILL CRASH
   # I DON'T KNOW WHY
   movl 16(%ebp), %edx
   incl %esi
   jmp LOOP

LOOP_DONE:
   # load %eax=&arr[i]; %edi=&arr[right]
   leal (%ebx, %ecx, 4), %eax
   leal (%ebx, %edx, 4), %edi
   pushl %edi
   pushl %eax
   call swap
   popl %eax
   popl %edi
   # %edx =  right
   # IF YOU DELETE THIS LINE, THE PROGRAM WILL CRASH
   # I DON'T KNOW WHY
   movl 16(%ebp), %edx

   # load %edi = k
   movl 20(%ebp), %edi
   cmpl %edi, %ecx
   # equal, no need to recursion
   je FINISH
   # recursion case1
   jg RECURSION1
   # recursion case2
   jle RECURWSION2

RECURSION1:
   movl 12(%ebp), %esi
   subl $1, %ecx
   pushl %edi
   pushl %ecx
   pushl %esi
   pushl %ebx
   call kthSmallest_asm
   popl %ebx
   popl %ecx
   popl %edx
   popl %edi
   jmp DONE

RECURWSION2:
   addl $1, %ecx
   pushl %edi
   pushl %edx
   pushl %ecx
   pushl %ebx
   call kthSmallest_asm
   popl %ebx
   popl %ecx
   popl %edx
   popl %edi
   jmp DONE

# restore callee-saved %edi, %ebx
# reversed order
FINISH:
   # load arr[k] to %eax
   movl (%ebx, %edi, 4), %eax
   popl %esi
   popl %edi
   popl %edx
   popl %ecx
   popl %ebx
   # popl %eax
   # ----------------------

DONE:
   # function ends
   leave
   ret
