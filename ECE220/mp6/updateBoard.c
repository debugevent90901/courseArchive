/* 
 * This .c file contains 3 functions essential to the simulation of Game of Life.
 *  
 * The countLiveNeighbor function is aimed to count the number of the live neighbors of a given cell.
 * It accepts five paramenters, a pointer towards the board, two ints of the size of the board, and two ints of the position of a cell.
 * It returns the number of the live neighbors of the given cell.
 * 
 * The updateBoard function is aimed to update the board to next status following the rules provided.
 * It accepts three paramenters, a pointer towards the board, two ints of the size of the board.
 * It doesn't have a return value since it's declared as void, but the board stored in the memory will be updated.
 * 
 * The aliveStable function is aimed to check whether the board's status is stable. If unchanged after update, then the current board is stable.
 * It accepts three paramenters, a pointer towards the board, two ints of the size of the board.
 * It returns 0 if the board will change after update. Else, it will return 1.
 *
 */ 



/*
 * countLiveNeighbor
 * Inputs:
 * board: 1-D array of the current game board. 1 represents a live cell.
 * 0 represents a dead cell
 * boardRowSize: the number of rows on the game board.
 * boardColSize: the number of cols on the game board.
 * row: the row of the cell that needs to count alive neighbors.
 * col: the col of the cell that needs to count alive neighbors.
 * Output:
 * return the number of alive neighbors. There are at most eight neighbors.
 * Pay attention for the edge and corner cells, they have less neighbors.
 */

int countLiveNeighbor(int* board, int boardRowSize, int boardColSize, int row, int col)
{
	int num = 0;	/* the number of the live neighbor. */

	/* the nested loop iterates through the 9 cells around the given cell. */
	for (int m = row - 1; m <= row + 1; m++)
	{
		for (int n = col - 1; n <= col + 1; n++)
		{
			/* if indexes of thr cells' positions are out of boundary, continue and skip them. */
			if (m < 0 || n < 0 || m >= boardRowSize || n >= boardColSize || (m == row && n == col))
				continue;

			/* else if the neighbor cell is alive, the local variable num will have an increment. */
			else 
				if (* (board + (m * boardColSize + n)) == 1)
					num += 1;
		}
	}

	/* return the number of alive neighbors. */
	return num;
}

/*
 * Update the game board to the next step.
 * Input: 
 * board: 1-D array of the current game board. 1 represents a live cell.
 * 0 represents a dead cell
 * boardRowSize: the number of rows on the game board.
 * boardColSize: the number of cols on the game board.
 * Output: board is updated with new values for next step.
 */

void updateBoard(int* board, int boardRowSize, int boardColSize)
{
	int next_board[boardRowSize * boardColSize]; /* a temporary array with same size as board to store intermidate data. */
	int live_num;	/* the number of a cell's live neighbors. */

	/* iterate through every element in array to copy the data in board to next_board. */
	for (int i = 0; i <= boardRowSize * boardColSize - 1; i++)
		next_board[i] = * (board + i);

	/* the nested loop iterates through the every cell on the board. */
	/* in this block the program applies the rules to the board's next status. */
	for (int m = 0; m <= boardRowSize - 1; m++)
	{
		for(int n = 0; n <= boardColSize - 1; n++)
		{
			/* calculate the number of a cell's live neighbors, call the last function. */
			live_num = countLiveNeighbor(board, boardRowSize, boardColSize, m, n);

			/* if a cell has live neighbors less than 2 or more than 3, it will die. */
			/* if a cell has 3 live neighbors, it will alive. */
			/* else, the status of a cell will remain unchanged. */
			next_board[m * boardColSize + n] = (live_num < 2 || live_num > 3) ? 0 : ((live_num == 3) ? 1 : * (board + (m * boardColSize + n)));
		}
	}

	/* update the board, copying changes in array next_board back to board. */
	for (int i = 0; i <= boardRowSize * boardColSize - 1; i++)
		* (board + i) = next_board[i];

	/* since declared as void, the function has no return value. */
	return;
}

/*
 * aliveStable
 * Checks if the alive cells stay the same for next step
 * board: 1-D array of the current game board. 1 represents a live cell.
 * 0 represents a dead cell
 * boardRowSize: the number of rows on the game board.
 * boardColSize: the number of cols on the game board.
 * Output: return 1 if the alive cells for next step is exactly the same with 
 * current step or there is no alive cells at all.
 * return 0 if the alive cells change for the next step.
 */ 


int aliveStable(int* board, int boardRowSize, int boardColSize)
{
	int copy[boardRowSize * boardColSize];	/* a temporary array with same size as board to store intermidate data. */
	int is_alive = 1;	/* the return value. 1 means stable. */

	/* iterate through every element in the array to copy the data in board to copy, preparing for comparation. */
	for (int m = 0; m <= boardRowSize * boardColSize - 1; m++)
		copy[m] = * (board + m);

	/* update the data in copy to next status by calling the last function we write. */
	/* in this way, the original data in board won't be changed. */
	updateBoard(copy, boardRowSize, boardColSize);

	/* iterate through every corresponding element in copy and board to compare. */
	/* if there exists one pair of elements that are different, the current status is not stable and thus return 0. */
	for (int n = 0; n <= boardRowSize * boardColSize - 1; n++)
		if (copy[n] != * (board + n))
			is_alive = 0;

	/* else, the current status is stable, return 1.*/
	return is_alive;
}



				
				
			

