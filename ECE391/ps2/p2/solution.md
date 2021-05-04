### P2 Solution

1. MTCP_BIOC_ON should be sent when a button is about to be either pressed or released. It enables Button interrupt-on-change. MTCP_ACK is returned. 
MTCP_LED_SET should be sent to set the User-set LED display values. It sets the User-set LED display values. These will be displayed on the LED displays when the LED display is in USR mode (see the MTCP_LED_USR and MTCP_LED_CLK commands). The first byte of argument specifies which of the LED's to set, and also determines how many bytes will follow - one byte for each led to set. It returns MTCP_ACK.

2. MTCP_ACK responds when the MTC successfully completes a command. It is returned by MTCP_BIOC_ON, MTCP_BIOC_OFF, MTCP_DBG_OFF, and MTCP_LED_SET. It means the command finished successfully. The value of MTCP_ACK is (((0x0)&7) | (((0x0)&0x18)<<1) | 0x40), which will be conveyed to the computer.
MTCP_BIOC_EVENT is the byte 0 of MTCP_BIO_EVT that is generated when the Button Interrupt-on-change mode is enabled and a button is either pressed or released. It means changes in button. The status of eight buttons are transmitted in the following 2 bytes. The value of MTCP_BIOC_EVENT is (((0x1)&7) | (((0x1)&0x18)<<1) | 0x40), which will be conveyed to the computer.
MTCP_RESET is generated when the device re-initializes itself after a power-up, a RESET button press, or an MTCP_RESET_DEV command. It means resetting the system. The value of MTCP_RESET is (((0x6)&7) | (((0x6)&0x18)<<1) | 0x40), which will be conveyed to the computer.

3. The function tuxctl_handle_packet is called in the context of interrupt handler (we should not let the interrupt handler sleep), and the data is sent over the serial line with low speed which means that waiting for the buffer to be available takes enough time to crash the system.
