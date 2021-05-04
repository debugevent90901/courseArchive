/*
 * tab:2
 *
 * mystery_asm.S - Assembly mystery
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
 * Author:        Aamir Hasan
 * Version:       1
 * Creation Date: Sun Jan 26 2020
 * Filename:      mystery_asm.S
 * History:
 *    AH    1    Sun Jan 26 2020
 *        First written.
 */

.data

.text
.global mystery_asm

# mystery (Assembly)
# Calculates the mystery function of the two input numbers
# 
# Registers:
#   eax - For devision op & Return Value
#   ebx - x
#   ecx - y
#   edx - For division op
#   edi - greater number

# aim: calculate the lcm of x, y
mystery_asm:
  # old base pointer in stack, new function begins
  pushl %ebp
  # set new ebp = esp, stack pointer
  movl %esp, %ebp

  # callee saved %ebx, %edi
  pushl %ebx
  pushl %edi

  # load arguments, "-": push; "+": pop
  # load %edi = first arg, %ebx = first arg  
  movl 12(%ebp), %edi
  movl 12(%ebp), %ebx
  # load %ecx = second arg (y)
  movl 8(%ebp), %ecx
  # 4(%ebp) is the eip (in stack when call)

  # first arg shall > 0
  cmpl $0, %ebx
  jle invalid_input

  # second arg shall > 0
  cmpl $0, %ecx
  jle invalid_input

  # 2 args should be different
  # should be %ecx < %ebx, if so, go to loop
  cmpl %ebx, %ecx
  je invalid_input
  jl op_loop

  # %ecx > %ebx, set %edi = %ecx, otherwise %edi = %ebx is the greater number
  movl 8(%ebp), %edi

  # when the loop begins, %ebx=x, %ecx=y, %edi=max(x, y)
op_loop:
  # set %edx = 0
  xorl %edx, %edx
  # %eax = %edi
  # set the return value initially = the greater number
  movl %edi, %eax
  # idiv signed division
  # %edx concat %eax / %ebx --> %eax ----- %edx
  # since %edx=0, simply %edi/%ebx, %eax=quotient, %edx=remainder	
  idiv %ebx
  # remainder is not 0 --> increment %edi and back to loop
  cmpl $0, %edx
  jne repeat 

  # now %edi = %ebx * %eax
  # same
  # %edi/%ecx, %eax=quotient, %edx=remainder	
  xorl %edx, %edx
  movl %edi, %eax
  idiv %ecx
  # remainder is not 0 --> increment %edi and back to loop
  cmpl $0, %edx
  jne repeat  
  
  # now %edi = %ecx * %eax
  # also %edi = %ebx * some number
  # set eax = edi
  movl %edi, %eax
  jmp finish 

  # edi ++, back to loop
repeat:
  incl %edi
  jmp op_loop

# set eax=-1, return -1
invalid_input:
  movl $-1, %eax

# restore callee-saved %edi, %ebx
# reversed order
finish:
  popl %edi
  popl %ebx

# function ends
  leave
  ret
