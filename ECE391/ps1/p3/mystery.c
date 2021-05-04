/*
 * tab:2
 *
 * mystery.c
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
 * Filename:      mystery.c
 * History:
 *    AH    1    Sun Jan 26 2020
 *        First written.
 */

#include "mystery.h"

int32_t mystery_c(int32_t x, int32_t y)
{
    if (x > 0 && y > 0)
    {
        int32_t greaterNumber, quotient, remainder;
        greaterNumber = (x > y) ? x : y;
        // loop begins
        quotient = greaterNumber / x;
        remainder = greaterNumber % x;
        while (remainder != 0)
        {
            greaterNumber++;
            quotient = greaterNumber / x;
            remainder = greaterNumber % x;
        }
        quotient = greaterNumber / y;
        remainder = greaterNumber % y;
        while (remainder != 0)
        {
            greaterNumber++;
            quotient = greaterNumber / x;
            remainder = greaterNumber % x;
            while (remainder != 0)
            {
                greaterNumber++;
                quotient = greaterNumber / x;
                remainder = greaterNumber % x;
            }
            quotient = greaterNumber / y;
            remainder = greaterNumber % y;
        }
        quotient = greaterNumber;
        return quotient;
    }
    return -1;
}


/* int32_t mystery_c(int32_t x, int32_t y)
{
    if (x > 0 && y > 0)
    {
        int32_t greaterNumber, quotient, remainder;
        greaterNumber = (x > y) ? x : y;
        // loop begins
        LOOP: quotient = greaterNumber;
        quotient = quotient / x;
        remainder = greaterNumber % x;
        if (remainder != 0)
        {
            greaterNumber++;
            goto LOOP;
        }
        quotient = greaterNumber;
        quotient = quotient / y;
        remainder = greaterNumber % y;
        if (remainder != 0)
        {
            greaterNumber++;
            goto LOOP;
        }
        quotient = greaterNumber;
        return quotient;
    }
    return -1;
} */
