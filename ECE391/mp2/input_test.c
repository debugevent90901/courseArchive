/*
 * tab:4
 *
 * input.c - source file for input control to maze game
 *
 * "Copyright (c) 2004-2009 by Steven S. Lumetta."
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
 * Author:        Steve Lumetta
 * Version:       5
 * Creation Date: Thu Sep  9 22:25:48 2004
 * Filename:      input.c
 * History:
 *    SL    1    Thu Sep  9 22:25:48 2004
 *        First written.
 *    SL    2    Sat Sep 12 14:34:19 2009
 *        Integrated original release back into main code base.
 *    SL    3    Sun Sep 13 03:51:23 2009
 *        Replaced parallel port with Tux controller code for demo.
 *    SL    4    Sun Sep 13 12:49:02 2009
 *        Changed init_input order slightly to avoid leaving keyboard in odd state on failure.
 *    SL    5    Sun Sep 13 16:30:32 2009
 *        Added a reasonably robust direct Tux control for demo mode.
 */

#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/io.h>
#include <termio.h>
#include <termios.h>
#include <unistd.h>
#include <sys/time.h>

#include "assert.h"
#include "input.h"
#include "maze.h"
#include "module/tuxctl-ioctl.h"
/* set to 1 and compile this file by itself to test functionality */
#define TEST_INPUT_DRIVER  1

/* set to 1 to use tux controller; otherwise, uses keyboard input */
#define USE_TUX_CONTROLLER 1
#define max_time 5999
#define sec_per_min 60
#define bitmask 0x0F
#define led_point 0x02000000
/* stores original terminal settings */
static struct termios tio_orig;
static int fd;
/* 
 * init_input
 *   DESCRIPTION: Initializes the input controller.  As both keyboard and
 *                Tux controller control modes use the keyboard for the quit
 *                command, this function puts stdin into character mode
 *                rather than the usual terminal mode.
 *   INPUTS: none
 *   OUTPUTS: none
 *   RETURN VALUE: 0 on success, -1 on failure 
 *   SIDE EFFECTS: changes terminal settings on stdin; prints an error
 *                 message on failure
 */
int init_input() {
    struct termios tio_new;
    int ldisc_num;
    /*
     * Set non-blocking mode so that stdin can be read without blocking
     * when no new keystrokes are available.
     */
    if (fcntl(fileno(stdin), F_SETFL, O_NONBLOCK) != 0) {
        perror("fcntl to make stdin non-blocking");
        return -1;
    }

    /*
     * Save current terminal attributes for stdin.
     */
    if (tcgetattr(fileno(stdin), &tio_orig) != 0) {
        perror ("tcgetattr to read stdin terminal settings");
        return -1;
    }

    /*
     * Turn off canonical (line-buffered) mode and echoing of keystrokes
     * to the monitor.  Set minimal character and timing parameters so as
     * to prevent delays in delivery of keystrokes to the program.
     */
    tio_new = tio_orig;
    tio_new.c_lflag &= ~(ICANON | ECHO);
    tio_new.c_cc[VMIN] = 1;
    tio_new.c_cc[VTIME] = 0;
    if (tcsetattr(fileno(stdin), TCSANOW, &tio_new) != 0) {
        perror("tcsetattr to set stdin terminal settings");
        return -1;
    }

    fd = open("/dev/ttyS0", O_RDWR | O_NOCTTY);
    ldisc_num = N_MOUSE;
    ioctl(fd, TIOCSETD, &ldisc_num);

    ioctl(fd, TUX_INIT);
    /* Return success. */
    return 0;
}

/* 
 * get_command
 *   DESCRIPTION: Reads a command from the input controller.  As some
 *                controllers provide only absolute input (e.g., go
 *                right), the current direction is needed as an input
 *                to this routine.
 *   INPUTS: cur_dir -- current direction of motion
 *   OUTPUTS: none
 *   RETURN VALUE: command issued by the input controller
 *   SIDE EFFECTS: drains any keyboard input
 */
cmd_t get_command(dir_t cur_dir) {
    static dir_t prev_cur = DIR_STOP; /* previous direction sent  */
    static dir_t pushed = DIR_STOP;   /* last direction pushed    */
#if (USE_TUX_CONTROLLER == 0) /* use keyboard control with arrow keys */
    static int state = 0;             /* small FSM for arrow keys */
#endif
    cmd_t command;
    int ch;
    unsigned long buttom = 0;
    //printf("%l\n", buttom);
    /*
     * If the direction of motion has changed, forget the last
     * direction pushed.  Otherwise, it remains active.
     */
    if (prev_cur != cur_dir) {
        pushed = DIR_STOP;
        prev_cur = cur_dir;
    }
    
    /* Read all characters from stdin. */
    while ((ch = getc(stdin)) != EOF) {

    /* Backquote is used to quit the game. */
    if (ch == '`')
        return CMD_QUIT;
    
#if (USE_TUX_CONTROLLER == 0) /* use keyboard control with arrow keys */
    /*
     * Arrow keys deliver the byte sequence 27, 91, and 'A' to 'D';
     * we use a small finite state machine to identify them.
     */
    if (ch == 27)
        state = 1; 
    else if (ch == 91 && state == 1)
        state = 2;
    else {
        if (state == 2 && ch >= 'A' && ch <= 'D') {
            switch (ch) {
                case 'A': pushed = DIR_UP; break;
                case 'B': pushed = DIR_DOWN; break;
                case 'C': pushed = DIR_RIGHT; break;
                case 'D': pushed = DIR_LEFT; break;
            }
        }
        state = 0;
    }
#else 
    printf("hahahahaha\n");
    buttom = 0;
    while (!buttom)
    {
        ioctl(fd, TUX_BUTTONS, &buttom);
        printf("%x\n", buttom);
    }
    if ((buttom & 0x00000080)) // R
        pushed = DIR_RIGHT;
    else if (buttom & 0x00000040) // L
        pushed = DIR_LEFT;
    else if (buttom & 0x00000020)
        pushed = DIR_DOWN;
    else if (buttom & 0x00000010)
        pushed = DIR_UP;
    else
        pushed = DIR_STOP;
    
#endif
    }

    /*
     * Once a direction is pushed, that command remains active
     * until a turn is taken.
     */
    if (pushed == DIR_STOP)
        command = TURN_NONE;
    else
        command = (pushed - cur_dir + NUM_TURNS) % NUM_TURNS;

    return command;
}

/* 
 * shutdown_input
 *   DESCRIPTION: Cleans up state associated with input control.  Restores
 *                original terminal settings.
 *   INPUTS: none
 *   OUTPUTS: none
 *   RETURN VALUE: none 
 *   SIDE EFFECTS: restores original terminal settings
 */
void shutdown_input() {
    (void)tcsetattr(fileno(stdin), TCSANOW, &tio_orig);
}

/* 
 * display_time_on_tux
 *   DESCRIPTION: Show number of elapsed seconds as minutes:seconds
 *                on the Tux controller's 7-segment displays.
 *   INPUTS: num_seconds -- total seconds elapsed so far
 *   OUTPUTS: none
 *   RETURN VALUE: none 
 *   SIDE EFFECTS: changes state of controller's display
 */
void display_time_on_tux(int num_seconds) {
// #if (USE_TUX_CONTROLLER != 0)
// #error "Tux controller code is not operational yet."
// #endif
    unsigned long min, sec;
    unsigned long min1, min2, sec1, sec2;
    unsigned long led_val;
    unsigned long led_on;
    unsigned long arg;
    if (num_seconds > max_time)
        num_seconds = num_seconds % max_time;
    min = num_seconds / sec_per_min;
    sec = num_seconds - min * sec_per_min;
    min1 = (min / 10) & bitmask;
    min2 = (min % 10) & bitmask;
    sec1 = (sec / 10) & bitmask;
    sec2 = (sec % 10) & bitmask;

    led_val = min1 << 12 | min2 << 8 | sec1 << 4 | sec2;
    if (min1)
        led_on = 0x000F0000;
    else
        led_on = 0x00070000;
    arg = led_point | led_on | led_val;

    /* Call the ioctl to set the leds*/
    ioctl(fd, TUX_SET_LED, arg);
}

#if (TEST_INPUT_DRIVER == 1)
int main() {
    int i = 0;
    unsigned long buttom = 0;
    unsigned char val,c;
    unsigned int R, L, D, U, C, B, A, S;
    int t1,t2;
    /* Grant ourselves permission to use ports 0-1023 */
    if (ioperm(0, 1024, 1) == -1) {
        perror("ioperm");
        return 3;
    }
    printf("switch the power! press . to continue.\n");
    while ((c = getc(stdin)) != '.');
    init_input();
    printf("initialization finished!\n");
    while ((c = getc(stdin)) != '.' && c != ',');
    display_time_on_tux(83);
    printf("check whether LED shows 123!\n");
    printf("press . to continue. press , to quit\n");
    while ((c=getc(stdin)) != '.' && c!= ',');
    if (c == ',')
        return 0;
    printf("Now show the buttom value\n");

    t2 = time(NULL);
    t1 = t2;
    while ((t2-t1)<10)
    {
        ioctl(fd, TUX_BUTTONS, &buttom);
        printf("The buttom value:\n");
        printf("%x\n", buttom);
        val = buttom & 0x000000FF;
        R = (val & 0x80)>>7;
        L = (val & 0x40) >> 6;
        D = (val & 0x20) >> 5;
        U = (val & 0x10) >> 4;
        C = (val & 0x08) >> 3;
        B = (val & 0x04) >> 2;
        A = (val & 0x02) >> 1;
        S = (val & 0x01);
        printf("R L D U C B A S\n");
        printf("%d %d %d %d %d %d %d %d\n", R, L, D, U, C, B, A, S);
        while (time(NULL) - t2 < 1);
        t2 = time(NULL);
    }
}
#endif
