/* tuxctl-ioctl.c
 *
 * Driver (skeleton) for the mp2 tuxcontrollers for ECE391 at UIUC.
 *
 * Mark Murphy 2006
 * Andrew Ofisher 2007
 * Steve Lumetta 12-13 Sep 2009
 * Puskar Naha 2013
 */

#include <asm/current.h>
#include <asm/uaccess.h>

#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/module.h>
#include <linux/fs.h>
#include <linux/sched.h>
#include <linux/file.h>
#include <linux/miscdevice.h>
#include <linux/kdev_t.h>
#include <linux/tty.h>
#include <linux/spinlock.h>

#include "tuxctl-ld.h"
#include "tuxctl-ioctl.h"
#include "mtcp.h"

#define debug(str, ...) \
	printk(KERN_DEBUG "%s: " str, __FUNCTION__, ## __VA_ARGS__)


#define MASK 0x0F

/* the ack value */
static int ack;	
/* the stored button value, 2 bytes */
static char button[2];
/* the backup led info for reset, 6 bytes */
static char led_backup[6];
/* corresponding led values to integer 0-F */
static unsigned char led_segments[16] = {0xE7, 0x06, 0xCB, 0x8F, 0x2E, 0xAD, 0xED, 0x86, 0xEF, 0xAE, 0xEE, 0x6D, 0xE1, 0x4F, 0xE9, 0xE8};

/************************ Protocol Implementation *************************/

/* local functions--see function headers for details */
int tuxctl_ioctl_init(struct tty_struct* tty);
int tuxctl_ioctl_get_button(unsigned long arg);
int tuxctl_ioctl_set_led(struct tty_struct* tty, unsigned long arg);

/* tuxctl_handle_packet()
 * IMPORTANT : Read the header for tuxctl_ldisc_data_callback() in 
 * tuxctl-ld.c. It calls this function, so all warnings there apply 
 * here as well.
 */
void tuxctl_handle_packet (struct tty_struct* tty, unsigned char* packet)
{
    unsigned a, b, c;

    a = packet[0]; /* Avoid printk() sign extending the 8-bit */
    b = packet[1]; /* values when printing them. */
    c = packet[2];

    /*printk("packet : %x %x %x\n", a, b, c); */
	switch (a)
	{
		/* if reset, call ioctl_init and restore the previous led value */
		case MTCP_RESET:
			tuxctl_ioctl_init(tty);
			tuxctl_ldisc_put(tty, led_backup, 6);
			break;
		
		/* set ack = 1 */
		case MTCP_ACK:
			ack = 1;
			break;
		
		/* update the button value */
		case MTCP_BIOC_EVENT:
			button[0] = b & MASK;
			button[1] = c & MASK;
			break;

		default:
			break;
	}

}

/******** IMPORTANT NOTE: READ THIS BEFORE IMPLEMENTING THE IOCTLS ************
 *                                                                            *
 * The ioctls should not spend any time waiting for responses to the commands *
 * they send to the controller. The data is sent over the serial line at      *
 * 9600 BAUD. At this rate, a byte takes approximately 1 millisecond to       *
 * transmit; this means that there will be about 9 milliseconds between       *
 * the time you request that the low-level serial driver send the             *
 * 6-byte SET_LEDS packet and the time the 3-byte ACK packet finishes         *
 * arriving. This is far too long a time for a system call to take. The       *
 * ioctls should return immediately with success if their parameters are      *
 * valid.                                                                     *
 *                                                                            *
 ******************************************************************************/
int 
tuxctl_ioctl (struct tty_struct* tty, struct file* file, 
				unsigned cmd, unsigned long arg)
{
	/* jump according to the cmd */
    switch (cmd) {

	/* init the tux */	
	case TUX_INIT:
		return tuxctl_ioctl_init(tty);

	/* send stored button values to user program */
	case TUX_BUTTONS:
		return tuxctl_ioctl_get_button(arg);

	/* update the led status */
	case TUX_SET_LED:
		return tuxctl_ioctl_set_led(tty, arg);

	case TUX_LED_ACK:
	case TUX_LED_REQUEST:
	case TUX_READ_LED:
	default:
		return -EINVAL;
    }
}

int tuxctl_ioctl_init(struct tty_struct* tty)
{
	/* command to put to device */
	unsigned char cmd[2];
	/* init ack to 0 */
	ack = 0;
	/* Enable Button interrupt-on-change */
	cmd[0] = MTCP_BIOC_ON;
	/* Put the LED display into user-mode */
	cmd[1] = MTCP_LED_USR;
	/* write commands to the device */
	tuxctl_ldisc_put(tty, cmd, 2);

	return 0;
}


int tuxctl_ioctl_set_led(struct tty_struct* tty, unsigned long arg)
{
	/*
		The low 16-bits specify a number whose hexadecimal value is to be displayed on the 7-segment displays. 
		The low 4 bits of the third byte specifies which LED’s should be turned on. 
		The low 4 bits of the highest byte (bits 27:24) specify whether the corresponding decimal points should be turned on.
	*/
	unsigned char cmd[6];	// command to put to device
	int i;					// loop index

	/* if led is available, set led */
	if (ack)
	{
		/* char with higher 4-bit = 0, lower 4-bit represent if the led is on */
		unsigned char is_led_on = (unsigned char)((arg & 0x000F0000) >> 16);
		/* char with higher 4-bit = 0, lower 4-bit represent if the led has its digit on */
		unsigned char is_need_digit = (unsigned char)((arg & 0x0F000000) >> 24);

		/* set ack = 0 */
		ack = 0;

		/*
			first byte, send opcode
			2nd byte, mask all 4 leds 
			the next 4 bytes will be segment info of each led
		*/
		cmd[0] = MTCP_LED_SET;
		cmd[1] = 0x0F;

		/* traverse 4 led */
		for (i = 0; i < 4; i++)
		{	
			/* if that led should be on */
			if (0x01 == ((is_led_on >> i) & 0x01))
			{	
				/* set it to corresponding number value */
				cmd[2+i] = led_segments[(int)(arg>>(4*i) & 0x0000000F)];
				/* if need a digit, put it on */
				if (0x01 == ((is_need_digit >> i) & 0x01))
				{	
					/* 0x10 is 0b00010000, only the 4-th bit is high, which is the digit bit in the protocal */
					cmd[2+i] |= 0x10;
				}
			}
			else
				/* led is not on, set to 0 */
				cmd[2+i] = 0x00;
		}

		/* set ack back to 1 */
		ack = 1;

		/* copy to led backup */
		memcpy(led_backup, cmd, 6);
		/* write the command to the device */
		tuxctl_ldisc_put(tty, cmd, 6);
	}

	return 0;
}

int tuxctl_ioctl_get_button(unsigned long arg)
{
	/* the return value that arg pointer points to */
	unsigned int res = 0x00;
	/* local variable used to swap 2 bits in a char */
	unsigned char bit_left = 0x00, bit_done = 0x00, bit_swapped = 0x00; 

	/* invalid input return -EINVAL */
	if ((int *)arg == NULL)
		return -EINVAL;
	/*	
		7 --------------------------0
		right left down up c b a start


		1 X X X    c      b    a   start
		1 X X X  right  done  left   up
	*/

	/* res = right, down, left, up, c, b, a, start */
	/* 2 bit are not required */
	res = (button[1] << 4) | button[0];

	/* ------------ swap 2 bit in a char begins ------------*/
	/* 5 means that left is the 5-th bit in the res */
	/* 6 means that done is the 6-th bit in the res */
	bit_left = (res >> 5) & 0x01;	// bit_left = 0b0000000(left)
	bit_done = (res >> 6) & 0x01;	// bit_done = 0b0000000(done)

	bit_swapped = bit_left ^ bit_done;						// bit_swap = 0b0000000(left ^ done)
	bit_swapped = (bit_swapped << 5) | (bit_swapped << 6);	// bit_swap = 0b0(left ^ done)(left ^ done)00000

	res ^= bit_swapped;										// xor again with original bit makes a perfect swap
	/* ------------ swap 2 bit in a char ends ------------*/

	/* copy the result back to user, success return 0, else return -EINVAL */
	if (! copy_to_user((int *)arg, &res, 4))
		return -EINVAL;
	else
		return 0;
}



