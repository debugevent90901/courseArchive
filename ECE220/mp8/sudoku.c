/* This program contains eight functions, 2 of which are already provided, 5 of which are required to write,
 * 1 of which is defined by myself to reduce work load.
 * 
 * The function is_val_in_row is aimed to judge whether the input number is valid in rows. It accepts 3 parameters,
 * the input number, the row index and the sudoku. It will return 1 if "val" already existed in row of array sudoku.
 *
 * The function is_val_in_col is aimed to judge whether the input number is valid in columns. It accepts 3 parameters,
 * the input number, the column index and the sudoku. It will return 1 if "val" already existed in column of array sudoku.
 * 
 * The function is_val_in_3x3_zone is aimed to judge whether the input number is valid in the corresponding 3x3 zone. It 
 * accepts 3 parameters, the input number, the row index and the sudoku. It will eturn 1 if "val" already existed in the zone.
 *
 * The function is_val_valid is aimed to judge whether the input number is valid. It accepts 4 parameters, the input number,
 * the row and column index and the sudoku. It will return true if the val is can be filled in the given entry.
 *
 * The function is_all_assigned is defined by myself and is aimed to judge whether all the cells are filled. It accepts one 
 * parameter, that is the sudoku. It will return 1 if all the cells are filled with valid numbers.
 *
 * The function solve_sudoku is aimed to solve the sudoku questions. I write it with the help of the provided pseudocode of a
 * typical backtracking algorithm. It accepts sudoku as parameter and stores the answer in corresponding cells and return 1
 * once all the cells are filled. It will first judge whether all the cells are filled, if so, return 1; else it will find
 * an unfilled cell using two loops. Then it will iterate through 9 valid numbers and recursivly solve the problem. And 
 * backtracking if the current number cannot solve the problem.
 */

#include "sudoku.h"

/*-------------------------------------------------------------------------------------------------
   Start here to work on your MP
  -------------------------------------------------------------------------------------------------*/

/* You are free to declare any private functions if needed. */

/* Function: is_all_assigned
   Return true if all the cells are assigned with valid values, else return 0. */
int is_all_assigned(const int sudoku[9][9])
{
  /* a traversal through all the cells using two loops, one in width, the other in height. */
  for (int i = 0 ; i <= 8 ; i++)
  {
    for (int j = 0 ; j <= 8 ; j++)
    {
      /* if there exists one cell that has not been assigned with valid values, the function returns 0. */
      if (! sudoku[i][j])
        return 0;
    }
  }

  /* else, the function will return 1. */
  return 1;
}

/* Function: is_val_in_row
   Return true if "val" already existed in ith row of array sudoku. */
int is_val_in_row(const int val, const int i, const int sudoku[9][9]) {

  /* judge whether the input is out of bound. */
  assert(i>=0 && i<9);

  /* BEG TODO */
  /* a traversal through the columns. */
  for (int j = 0 ; j <= 8 ; j++)
    /* if the current cell has been assigned with the input value, the function will return 1. */
    if (sudoku[i][j] == val)
      return 1;

  /* if all the cells in this row haven't been assigned with the input val, then the function will return 0. */  
  return 0;
  /* END TODO */
}

/* Function: is_val_in_col
   Return true if "val" already existed in jth column of array sudoku. */
int is_val_in_col(const int val, const int j, const int sudoku[9][9]) {

  /* judge whether the input is out of bound. */
  assert(j>=0 && j<9);

  /* BEG TODO */
  /* a traversal through the rows. */
  for (int i = 0 ; i <= 8 ; i++)
    /* if the current cell has been assigned with the input value, the function will return 1. */
    if (sudoku[i][j] == val)
      return 1;

  /* if all the cells in this column haven't been assigned with the input val, then the function will return 0. */
  return 0;
  /* END TODO */
}

/* Function: is_val_in_3x3_zone
   Return true if val already existed in the 3x3 zone corresponding to (i, j) */
int is_val_in_3x3_zone(const int val, const int i, const int j, const int sudoku[9][9]) {
   
  /* judge whether the input is out of bound. */
  assert(i>=0 && i<9);
  
  /* BEG TODO */
  /* a traversal through the corresponding 3x3 zone using two loops, one in width and the other in height. */
  for (int m = i - (i % 3) ; m <= i - (i % 3) + 2 ; m++)
  {
    for (int n = j - (j % 3) ; n <=  j - (j % 3) + 2 ; n++)
    {
      /* if the current cell has been assigned with the input value, the function will return 1. */
      if (sudoku[m][n] == val)
        return 1;
    }
  }

  /* if the current cell in this zone has been assigned with the input value, the function will return 1. */
  return 0;
  /* END TODO */
}

/* Function: is_val_valid
   Return true if the val is can be filled in the given entry. */
int is_val_valid(const int val, const int i, const int j, const int sudoku[9][9]) {

  /* judge whether the input is out of bound. */
  assert(i>=0 && i<9 && j>=0 && j<9);

  /* BEG TODO */
  /* if the input hasn't assigned in the corresponding row, column and 3x3 zone, then the input is valid. */
  if ((is_val_in_row(val, i, sudoku) == 0) && (is_val_in_col(val, j, sudoku) == 0) && (is_val_in_3x3_zone(val, i, j, sudoku) == 0))
    return 1;
  /* else, the input has been used and is nit valid. */
  else
    return 0;
  /* END TODO */
}

/* Procedure: solve_sudoku
   Solve the given sudoku instance. */
int solve_sudoku(int sudoku[9][9]) {

  /* BEG TODO. */
  int i, j; /* indexes used in following loops, representing the current cell. */

  /* if all the cells are assigned with valid inputs, the function ends and return 1. */
  if (is_all_assigned(sudoku))
    return 1;

  /* else, the function finds a cell that has not been filled. */
  else 
  {
    int flag = 0; /* a flag that represents whether a unfilled cell is found. If found, it will be 1. */
    /* a traversal through all the cells using two loops, one in width, the other in height. */
    for (int m = 0 ; m <= 8 ; m++)
    {
      for (int n = 0 ; n <= 8 ; n++)
      {
        /* if the current cell's value is 0, then it hasn't been filled. */
        if (! sudoku[m][n])
        {
          /* assign their indexes in the block to i,j to pass to following recursion. */
          i = m; j = n;
          /* set the flag to be 1. */
          flag = 1;
          /* a unfilled cell is found, break the loops. */
          break;
        }
      }
      /* do the judgement, if an unfilled cell is found, then break the outer loop too. */
      if (flag == 1) 
        break;
    }
  }

  /* an iteration through 1-9, which can be assigned to cells. */
  for (int num = 1; num <= 9; num++)
  {
    /* if this number is valid to assign to the current cell. */
    if (is_val_valid(num, i, j, sudoku))
    {
      /* then assign this number to this cell. */
      sudoku[i][j] = num;

      /* recursion, call the function itself again in the function. */
      /* another judgement, if the function return 1, the all the cells are filled. */
      if (solve_sudoku(sudoku))
        return 1;

      /* else, reset the cell to backtracking. */
      sudoku[i][j] = 0;
    }
  }

  /* the function won't return 1 until all the cells are filled. */
  return 0;
  /* END TODO. */
}

/* Procedure: print_sudoku */
void print_sudoku(int sudoku[9][9])
{
  int i, j;
  for(i=0; i<9; i++) {
    for(j=0; j<9; j++) {
      printf("%2d", sudoku[i][j]);
    }
    printf("\n");
  }
}

/* Procedure: parse_sudoku */
void parse_sudoku(const char fpath[], int sudoku[9][9]) {
  FILE *reader = fopen(fpath, "r");
  assert(reader != NULL);
  int i, j;
  for(i=0; i<9; i++) {
    for(j=0; j<9; j++) {
      fscanf(reader, "%d", &sudoku[i][j]);
    }
  }
  fclose(reader);
}


