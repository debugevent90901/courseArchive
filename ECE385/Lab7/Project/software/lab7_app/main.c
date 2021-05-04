int main()
{
	int i = 0;
	volatile unsigned int *LED_PIO = (unsigned int*)0x70; //make a pointer to access the led PIO block
	volatile unsigned int *SW_PIO = (unsigned int*)0x60; //make a pointer to access the switch PIO block
	volatile unsigned int *KEY_PIO = (unsigned int*)0x50;

	enum states {START, ADD, HALT, CLEAR, STOP};
	*LED_PIO = 0; //clear all LEDs
	enum states current_state = START;
	enum states next_state = current_state;

	while ( (1+1) != 3) //infinite loop
	{
		for (i = 0; i < 1000; i++); //software delay
		current_state = next_state;
		switch(current_state)
		{
			case START:
				//*LED_PIO = 0x2;
				if(*KEY_PIO == 0x3)
					next_state = START;
				else if(*KEY_PIO == 0x1)
					next_state = ADD;
				else
					next_state = CLEAR;
				break;
			case ADD:
				*LED_PIO = (*LED_PIO + *SW_PIO)%0x100;
				if(*KEY_PIO == 0x3)
					next_state = START;
				else if(*KEY_PIO == 0x1)
					next_state = HALT;
				else
					next_state = CLEAR;
				break;
			case HALT:
				if(*KEY_PIO == 0x3)
					next_state = START;
				else if(*KEY_PIO == 0x1)
					next_state = HALT;
				else
					next_state = CLEAR;
				break;
			case CLEAR:
				*LED_PIO = 0x0;
				if(*KEY_PIO == 0x3)
					next_state = START;
				else if(*KEY_PIO == 0x1)
					next_state = ADD;
				else
					next_state = STOP;
				break;
			case STOP:
				if(*KEY_PIO == 0x3)
					next_state = START;
				else if(*KEY_PIO == 0x1)
					next_state = ADD;
				else
					next_state = STOP;
				break;
		}
	}
	return 1; //never gets here
}
