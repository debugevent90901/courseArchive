
/* This program contains four functions.
 * 
 * The function createMaze is aimed to read data from an input file and create a structure maze with malloced memory.
 * It accepts only one parameter, the character array containing the name of the maze file. It will return a filled 
 * maze structure that represents the contents of the input file. 
 *
 * The function destoryMaze is aimed to destroy the maze and free all the malloced memory in heap. It accepts one parameter,
 * pointer to maze structure that contains all necessary information, It will nothing.
 *
 * The function printMaze is is aimed to print the maze to console in a human-readable format. It accepts the pointer to maze 
 * structure with all necessary maze information and will return nothing.     
 *
 * The function solveMazeDFS is aimed to solve the maze questions. I write it with the help of the provided pseudocode of a
 * depth first search algortham. It accepts three parameter. maze as the pointer to maze structure with all necessary maze
 * information, col as the column of the current cel, row as the row of the current cell. It will marks maze cells as visited
 * or part of the solution path. It will return 0 if the maze is unsolvable, 1 if it is solved.
 */

#include <stdio.h>
#include <stdlib.h>
#include "maze.h"

/*
 * createMaze -- Creates and fills a maze structure from the given file
 * INPUTS:       fileName - character array containing the name of the maze file
 * OUTPUTS:      None 
 * RETURN:       A filled maze structure that represents the contents of the input file
 * SIDE EFFECTS: None
 */
maze_t * createMaze(char * fileName)
{
    // Your code here. Make sure to replace following line with your own code.
    FILE *in;                 /* file pointer to the input file. */
    maze_t *maze = NULL;      /* an empty pointer to the malloced memory space for structure maze. */
    int width, height;        /* the x and y dememsions of the input maze. */

    /* open the input file as a stream. */
    in = fopen(fileName, "r");
    /* get the intager values of width and height. */
    fscanf(in, "%d %d\n", &width, &height);

    /* malloc the memory space took up by structure maze. */
    maze = malloc(sizeof(maze_t)); 

    /* set the width and height fields of the structure maze to be the input width and height. */
    maze->width = width;
    maze->height = height;
    /* first step to malloc memory space for the cells field of structure maze, which is a 2-demensional array. */
    maze->cells = malloc(sizeof(char *) * height);

    /* the second step to malloc for cells field, using a loop to malloc memory for each line. */
    for(int i = 0 ; i < height ; i++)
      maze->cells[i] = malloc(sizeof(char) * width);

    char word;            /* temporily holds the current input char. */                                 
    int m = 0, n = 0;     /* x, y indexes of the 2-demensional array maze->cells. */
    /* use fgetc() to get every char input from stream until EOF, when the file ends. */
    while ((word = fgetc(in)) != EOF)
      {
        /* if the char is \n, the current line is over. */
        if (word == '\n')
        {
          /* reset column index to be 0 and increment the row index. */
          m++; n = 0;
        }

        else
        {
          /* else write the char to corresponding position of cells. */
          maze->cells[m][n] = word;

          /* if the char is 'S', set the startRow/Column fields of structure maze. */
          if(word == 'S')
          {
            maze->startRow = m;
            maze->startColumn = n;
          }
          /* if the char is 'E', set the endRow/Column fields of structure maze. */
          if(word == 'E')
          {
            maze->endRow = m;
            maze->endColumn = n;
          }

          /* increment column index and prepare for next fgetc(). */
          n++;
        }     
      }
    /* close the file stream. */
    fclose(in);
    /* return the pointer to maze back to caller. */
    return maze;
}

/*
 * destroyMaze -- Frees all memory associated with the maze structure, including the structure itself
 * INPUTS:        maze -- pointer to maze structure that contains all necessary information 
 * OUTPUTS:       None
 * RETURN:        None
 * SIDE EFFECTS:  All memory that has been allocated for the maze is freed
 */
void destroyMaze(maze_t * maze)
{
    // Your code here.
    /* use a loop to free each line of the maze's malloced memory respectively. */
    for (int i=0 ; i < maze->height ; i++)
      free(maze->cells[i]);

    /* free the 2-demensional array maze->cells. */
    free(maze->cells);
    /* free the structure maze. */
    free(maze);
    /* this function return nothing. */
    return;
}

/*
 * printMaze --  Prints out the maze in a human readable format (should look like examples)
 * INPUTS:       maze -- pointer to maze structure that contains all necessary information 
 *               width -- width of the maze
 *               height -- height of the maze
 * OUTPUTS:      None
 * RETURN:       None
 * SIDE EFFECTS: Prints the maze to the console
 */
void printMaze(maze_t * maze)
{
    // Your code here.
    /* use two nested loops to iterate through the 2-demensional array cells and print each element. */
    for(int i = 0 ; i < maze->height ; i++)
    {   
      for(int j = 0 ; j < maze->width ; j++)
        printf("%c", maze->cells[i][j]);
      /* print a newline char when one row is finished. */
      printf("\n");
    }

    /* this function also return nothing. */
    return;
}

/*
 * solveMazeDFS -- recursively solves the maze using depth first search,
 * INPUTS:               maze -- pointer to maze structure with all necessary maze information
 *                       col -- the column of the cell currently beinging visited within the maze
 *                       row -- the row of the cell currently being visited within the maze
 * OUTPUTS:              None
 * RETURNS:              0 if the maze is unsolvable, 1 if it is solved
 * SIDE EFFECTS:         Marks maze cells as visited or part of the solution path
 */ 
int solveMazeDFS(maze_t * maze, int col, int row)
{
    // Your code here. Make sure to replace following line with your own code.

    /* if the value at current cell is 'E', it means the program just found the end and return 1. */
    if (maze->cells[row][col] == 'E')
    {
      /* reset the value at start to be 'S'. */
      maze->cells[maze->startRow][maze->startColumn]='S';
      /* success. return 1. */
      return 1;
    }
    /* check if the current cell is out of boundary. If so, return 0. */
    else if (row < 0 || col < 0 || col >= maze->width || row >= maze->height)
        return 0;
    /* check whether the cell had been reached before or is a wall. If so, return 0. */
    else if (maze->cells[row][col] == '%' || maze->cells[row][col] == '.')
        return 0;

    else
    {
      /* set the current cell to be '.', assume it is a right solution. */
      maze->cells[row][col] = '.';

      /* do the recursion and judge in four direction. If in one direction the recursion returns 1, then return 1. */
      if (solveMazeDFS(maze, col - 1, row) == 1)
        return 1;

      if (solveMazeDFS(maze, col + 1, row) ==1 )
        return 1;

      if (solveMazeDFS(maze, col, row - 1) == 1)
        return 1;

      if (solveMazeDFS(maze, col, row + 1) == 1)
        return 1;

      /* if four direction all return 0, reset the current cell to be '~', it's not part of a solution. */
      maze->cells[row][col] = '~';

      /* unsuccess. return 0. */
      return 0;

    }
}