/* This program contains seven functions.
 * 
 * The function load_tuples will open a file with the name 'input_file', read the data from the file, and return a 
 * matrix of the list of tuples type. It will accept a string as filename and return a pointer to the sp_tuples struct.
 *
 * The function gv_tuples gets the value of the element at the given row and column within the matrix. It accepts 
 * mat_t as given sp_tuple struct, two integers as row and col index. And return the double typed value of that node.
 *
 * The function set_tuples sets the element at row and col to value. It accepts a matrix, row index and column index and 
 * the value at that node. This function doesn't return anything.
 *
 * The function save_tuples writes the data in a sparse matrix structure to a text file in the specified format. It accepts
 * a string of fileName and mat_t - the matrix to be written. And will output a text file.
 *
 * The function add_tuples calculates matrix addition C = A + B. It will accepts two input matrices A and B, and calculate 
 * A + B. The function will return another matrix containing the anwswer matrix.
 *
 * The function mult_tuples calculates matrix addition C = A * B. It will accepts two input matrices A and B, and calculate 
 * A * B. The function will return another matrix containing the anwswer matrix.
 *
 * The function destory_tuples will free all memory associated with the given matrix. It accepts the sp_tuples struct mat_t as matrix.
 * This function return nothing but void.
 *
 */



#include "sparsemat.h"

#include <stdio.h>
#include <stdlib.h>



/*
 * load_tuples -- Creates and fills a sp_tuple structure from the given file
 * INPUTS:        fileName - character array containing the name of the input file
 * OUTPUTS:       None 
 * RETURN:        A pointer to the sp_tuples structure. 
 * SIDE EFFECTS:  None
 */
sp_tuples * load_tuples(char* input_file)
{
	
	FILE *in;                        /* file pointer to the input file. */
	int num_row, num_col, row, col;  /* the size of the matrix and the row and column index. */
  double value;                    /* the value of one node in matrix. */
	sp_tuples *list = NULL;

  /* open the input file as a stream. */
	in = fopen(input_file, "r");  
  /* if failed, return NULL to caller. */   
	if (NULL == in)
		return NULL;

  /* allocate the memory space for a sp_tuples structure as the matrix. */
	list = malloc(sizeof(sp_tuples));

  /* get the intager values of the number of rows and columns. */
	fscanf(in, "%d %d", &num_row, &num_col);
  /* assign the num_row and num_col to the m, n field of the structure. */
	list->m = num_row;
	list->n = num_col;
  /* initialize the nz field to be zero and the tuple_head field to be NULL. */
	list->nz = 0;
	list->tuples_head = NULL;

  /* use a while loop to continuously read the data of every node. */
  while (EOF != fscanf(in, "%d %d %lf", &row, &col, &value))
    /* call set_tuples function to insert every node read into the matrix structure. */
  	set_tuples(list, row, col, value);

  /* close the file stream. */
	fclose(in);
  /* return the struct pointer list to caller. */
  return list;
}



/*
 * gv_tuples --  gv_tuples gets the value of the element at the given row and column within the matrix.
 * INPUTS:       mat_t as given sp_tuple struct, two integers as row and col index
 * OUTPUTS:      None 
 * RETURN:       the value of the element at the given row and column within the matrix.
 * SIDE EFFECTS: None
 */
double gv_tuples(sp_tuples * mat_t,int row,int col)

{	
  /* use a for loop to traverse every node in the matrix struct. */
	for (sp_tuples_node *cur = mat_t->tuples_head ; NULL != cur ; cur = cur->next)
    /* if the current node's row and column indexes are the same as input parameter */
		if (cur->row == row && cur->col == col)
      /* return the current node's value to caller. */
			return cur->value;
  /* else, return 0. */
  return 0;
}



/*
 * set_tuples -- set the element at row and col to value in a given matrix.
 * INPUTS:       a matrix, row index and column index and the value at that node.
 * OUTPUTS:      None 
 * RETURN:       None
 * SIDE EFFECTS: None
 */
void set_tuples(sp_tuples * mat_t, int row, int col, double value)
{
  sp_tuples_node *new_node = NULL;            /* a new node structure holding the input data. */
  /* allocate memory for new_node with su_tuples_node data type. */
  new_node = malloc(sizeof(sp_tuples_node));  
  /* initialize the new_node, filling its fields with input data and set the next field to be NULL. */
  new_node->value = value;                    
  new_node->row = row;
  new_node->col = col;
  new_node->next = NULL;

  /* if the input matrix‘s tuple_head is NULL */
  if (NULL == mat_t->tuples_head && 0 != value)
  {
    /* initialize the tuple_head field, setting it pointing to new_node. */
    mat_t->tuples_head = new_node;
    /* increment the nz field. */
    mat_t->nz++;
    return;
  }
  
  sp_tuples_node *cur = mat_t->tuples_head; /* a pointer to the mat_t->tuple_head. intiial state fot traverse. */
  sp_tuples_node * prev = NULL;             /* a pointer to NULL, which will hold the previous node in traverse. */

  /* while the nodes are not over, traverse the matrix. */
  while(NULL != cur)
  {
    /* if the current row and column matches */
    if (cur->row == row && cur->col == col)
    {
      /* if the value is 0, delete the node. */
      if (0 == value)
      {
        /* if the current node is the first one */
        if (cur == mat_t->tuples_head)
          /* set mat_t's tuple_head field to be the node after current node. */
          mat_t->tuples_head = cur->next;
        else
          /* else set the previous node's next field to be current node's next field. */
          prev->next = cur->next;  
        
        /* decrement the nz field. */
        mat_t->nz--;
        /* since the new_node hasn't been used, let's free its memory space. */
        free(new_node);
        return;
      }
      
      /* else, set the node's current value to be the input value. */
      else
      {
        cur->value = value;
        /* free the unused memory space of new_node. */
        free(new_node);
        return;
      }
    }

    /* if the value is not 0 and the current row and column indexes are behind that data in new_node. */
    else if ((cur->row > row || (cur->row == row && cur->col > col)) && 0 != value)
    {
      /* insert the new_node before current node. */
      /* set the new_node's next field, pointing to current node. */
      new_node->next = cur;

      /* if the current node is the first one */
      if (cur == mat_t->tuples_head)
        /* set mat_t's tuple_head field to be the new_node. */
        mat_t->tuples_head = new_node;
      else
        /* else set the previous node's next field to be current node's next field. */
        prev->next = new_node;

      /* increment the nz field. */
      mat_t->nz++;
      return;
    }

    /* prepare for next node. */
    /* set the prev node to be current node and set the current node to be its next field. */
    prev = cur;
    cur = cur->next;
  }

  /* if the input indexs are bigger than any nodes in matrix. */
  /* the new_node should be insert at the end. */
  if (0 != value)
  {
    /* set the previous node's next field, pointing to new_node. */
    prev->next = new_node;
    /* increment the nz field. */
    mat_t->nz++;
    return;
  }
}



/*
 * save_tuples -- writes the data in a sparse matrix structure to a text file in the specific format.
 * INPUTS:        fileName - character array containing the name of the matrix file; mat_t - the matrix to be written.
 * OUTPUTS:       a text file in the specific format containing data of the given matrix.
 * RETURN:        None
 * SIDE EFFECTS:  None
 */
void save_tuples(char * file_name, sp_tuples * mat_t)
{
	FILE *out;   /* file pointer to the output file. */

  /* open the output file as a stream. */
	out = fopen(file_name, "w");

  /* print the number of rows and columns of matrix to file. */
	fprintf(out, "%d %d\n", mat_t->m, mat_t->n);

  /* use a for loop to traverse every nodes. */
	for (sp_tuples_node *cur = mat_t->tuples_head ; NULL != cur ; cur = cur->next)
    /* print the data of every node to output file. */
		fprintf(out, "%d %d %f\n", cur->row, cur->col, cur->value);

  /* close the file stream. */
  fclose(out);
	return;
}



/*
 * add_tuples -- calculate the matrix C = A + B
 * INPUTS:       two matrices with data type as sp_tuples.
 * OUTPUTS:      None 
 * RETURN:       A pointer to the return matrix C
 * SIDE EFFECTS: None
 */
sp_tuples * add_tuples(sp_tuples * matA, sp_tuples * matB)
{
	sp_tuples *retmat = NULL;    /* the return matrix pointer, initialized to be NULL. */

  /* if the rows and columns of the two input matrices are not the same */
	if ((matA->m != matB->m) || (matA->n != matB->n))
    /* the two matrices cannot operate addition, return NULL. */
		return NULL;

  /* allocate memory space of a sp_tuples struct for retmat. */
	retmat = malloc(sizeof(sp_tuples));
  /* set the retmat's m, n field to be the same as input matrices. */
	retmat->m = matA->m; 
	retmat->n = matA->n;
  /* initialize the retmat's nz field to be zero. */
	retmat->nz = 0;

  /* use a for loop to traverse every node in input matA. */
	for (sp_tuples_node *curA = matA->tuples_head ; NULL != curA ; curA = curA->next)
    /* copy their values into the retmat using set_tuples function. */
		set_tuples(retmat, curA->row, curA->col, curA->value);
  /* use another for loop to traverse every node in input matB. */
	for (sp_tuples_node *curB = matB->tuples_head ; NULL != curB ; curB = curB->next)
    /* get retmet's value using gv_tuples, and add it with value in matB and use set_tuples to write change to retmat. */
		set_tuples(retmat, curB->row, curB->col, curB->value + gv_tuples(retmat, curB->row, curB->col));

  /* return retmat to caller. */
	return retmat;
}



/*
 * mult_tuples -- calculate the matrix C = AB
 * INPUTS:        two matrices with data type as sp_tuples.
 * OUTPUTS:       None 
 * RETURN:        A pointer to the return matrix C
 * SIDE EFFECTS:  None
 */
sp_tuples * mult_tuples(sp_tuples * matA, sp_tuples * matB)
{
	sp_tuples *retmat = NULL;     /* the return matrix pointer, initialized to be NULL. */

  /* if the matA's column doesn't equal to matB's row */
	if (matA->n != matB->m)
    /* the two matrices cannot operate multiply, return NULL. */
		return NULL;

  /* allocate memory space of a sp_tuples struct for retmat. */
	retmat = malloc(sizeof(sp_tuples));
  /* set the retmat's m, n field to be the same as input matrices. */
	retmat->m = matA->m;
	retmat->n = matB->n;
  /* initialize the retmat's nz field to be zero. */
	retmat->nz = 0;

  /* use a for loop to traverse every node in input matA. */
	for (sp_tuples_node *curA = matA->tuples_head ; NULL != curA ; curA = curA->next)
    /* use another for loop to traverse every node in input matB. */
		for (sp_tuples_node *curB = matB->tuples_head ; NULL != curB ; curB = curB->next)
      /* if the row index of current node in matB equals to the column index of current node in matA */
      if (curB->row == curA->col)
        /* perform multiply by calling gv_tuples and set_tuples. */
        /* set the node in retmat to be its original value plus nodeA's value multiply nodeB's value. */
        set_tuples(retmat, curA->row, curB->col, gv_tuples(retmat, curA->row, curB->col) + curA->value * curB->value);

  /* return retmat to caller. */
  return retmat;
}



/*
 * destroy_tuples  -- free all memory associated with the given matrix.
 * INPUTS:            the sp_tuples struct mat_t as matrix.
 * OUTPUTS:           None 
 * RETURN:            None
 * SIDE EFFECTS:      All memory that has been allocated for the maze is freed.
 */
void destroy_tuples(sp_tuples * mat_t)
{
  sp_tuples_node *cur = mat_t->tuples_head; /* a pointer to mat_t's tuple_head field. */
  sp_tuples_node *tmp = NULL;               /* a temporily pointer initialized to NULL. */

  /* use a while loop to traverse through every node in mat_t. */
  while (NULL != cur)
  {
    /* set the tmp pointer to cur pointer. */    
    tmp = cur;
    /* move the cur pointer to next node. */
    cur = cur->next;
    /* free the current node pointed by tmp pointer. */
    free(tmp);
  }

  /* free the mat_t structed as sp_tupls. */
  free(mat_t);
  return;
}