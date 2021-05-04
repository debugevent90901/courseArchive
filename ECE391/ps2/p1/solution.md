### P1 Solution

1. Basically, when the number of scanned line is larger than the number specified in the Line Compare field (and is less than the height of the screen), VGA would not continually scan the following places in display memory but instead, scan starting from the 0 address in display memory until fulfilling the whole screen. Therefore, we could set the Line Compare value and put the data of status bar into the display memory beginning at 0 address to add a status bar.
 
The necessary register value settings:
Regs of Line Compare Field (10 bits)
0-7 in Line Compare Register (Index 18h)
8 in 4th bit of Overflow Register (Index 07h)
9 in 5th bit of Maximum Scan Line Register (Index 09h)
Total 10 bits indicates the number of lines of the upper window. To add a status bar, this value should be set as (height of screen - height of status bar)
Pixel Panning Mode value
5th bit of Attribute Mode Control Register (Index 10h)
This bit indicate the status of panning mode. If it is 0, the bottom window would be panned in sync with the upper window; if it is 1, the bottom window would not panned with the upper window (VGA hardware would set Pixel Shift Count and Byte Panning fields to 0). If we want the status bar to pan in sync with the main window, we could set this bit to 0; if not, i.e. we want the status bar fixed, we could set this bit to 1.
 
We do not need to set anything to make the bar been non-scrolling. Because the Preset Row Scan value, which controls the Pixel level scrolling, would be set to 0 when VGA scans the bottom window; also the Start Address, which controls the scan-line level scrolling, would be set to 0.
 
Relevant constraints:
The starting address of the upper window should not be earlier than the addresses which contains the status-bar data (it starts from 0). That's because when we are trying to split the window, the second screen has a default position which is 0, so it's obvious that the the start address (works for the top screen) is too small to overlap the bottom screen, problem will occur. We should set Start Address High Register and Start Address Low Register to achieve this.
The second limitation is that either both windows are panned by the same amount, or only the top window pans, in which case, the bottom window's panning values are fixed at 0.
Another limitation is that the Preset Row Scan field only applies to the top window -- the bottom window has an effective Preset Row Scan value of 0.


2. To write to the palette, first you must output the value of the palette entry to the PEL Address Write Mode Register (port 3C8h.) Then you should output the component values to the PEL Data Register (port 3C9h), in the order red, green, then blue. The PEL Address Write Mode Register will then automatically increment, allowing the component values of the palette entry to be written to the PEL Data Register. 
