/* This program contains five functions, two of which are helper functions I declare, the rest of which are required to code.
 * 
 * The function find_nodes will fill the vertex set vs with the array indices of any graph vertices found to be in range of 
 * locale loc. It accepts array index nnum, vertex set pointer vs, pyramid tree pointer p, locale pointer loc as parameters 
 * and return nothing. 
 *
 * The function trim_nodes is designed to remove any graph vertices that are not in range of a locale from a vertex set. It 
 * accepts graph pointer g, vertex set pointer vs and locale pointer loc. The function will directly operate the vertex set 
 * and will not return anything. 
 *
 * The function dijkstra is aimed to use a modified Dijkstra algorithm to find the shortest path between any node in the source
 * set the destination set. It will accept a copy of graph, the heap pointer h, the starting and ending points set pointer src, 
 * dest, the path pointer path. Fill the path with answer and return void.
 *
 * The function insert is the help function I declared to operate the heap. It accepts a copy of graph, the heap pointer and a 
 * element, inserting the element into the heap with proper sorting and return void.
 *
 * The function pop is the helper function I declared to operate the heap. It accepts a copy of graph and the heap pointer, pop
 * and delete the top element in heap, after which the function will resort the heap. The function will return the top element in heap. 
 */

#include <stdint.h>
#include <stdio.h>
#include "mp11.h"

#define MY_INFINITY   1000000000

/* a macro that represents the undefined situation, which has value -1 */
#define UNDEF -1
/* two macro that represents whether the vertex has been traversed by dijkstra algorithm */
/* 0 means not reached, 1 means reached */
#define REACHED 1
#define UNREACHED 0

/*
 * find_nodes --  fill the vertex set vs with the array indices of any graph vertices found to be in range of locale loc
 * INPUTS:        array index nnum, vertex set pointer vs, pyramid tree pointer p, locale pointer loc 
 * OUTPUTS:       None 
 * RETURN:        None
 * SIDE EFFECTS:  None 
 */
void
find_nodes (locale_t* loc, vertex_set_t* vs, pyr_tree_t* p, int32_t nnum)
{
    // Do not modify the following line nor add anything above in the function.
    record_fn_call ();
    /* if the array index is out of the boundary of the number of nodes, return nothing */
    if (nnum > p->n_nodes) 
        return;

    else
    {   
        /* if 4*nnum+1 is out of the boundary of the number of nodes, the current node is a leaf node */
        if (4 * nnum + 1 > p->n_nodes)
        {   
            /* if the current node is in range of the given locale */
            if (in_range(loc, p->node[nnum].x, p->node[nnum].y_left))
            {
                /* put its id in the vs->id array and increment the vs->count field */
                vs->id[vs->count] = p->node[nnum].id;
                vs->count++;
            }
            /* returns to caller with nothing */
            return;
        }
        /* else the current node is an internal node */
        else
        {   
            /* if the current x, y coordinates are too big, recursively call find_nodes with nnum=4*nnum+1 */
            if(p->node[nnum].x >= ((loc->x) - (loc->range)) && p->node[nnum].y_left >= ((loc->y) - (loc->range)))
                find_nodes (loc, vs, p, 4 * nnum + 1);
            /* if the current x coordinates is too small and y coordinate is too big, recursively call find_nodes with nnum=4*nnum+2 */
            if(p->node[nnum].x <= ((loc->x) + (loc->range)) && p->node[nnum].y_left >= ((loc->y) - (loc->range)))
                find_nodes (loc, vs, p, 4 * nnum + 2);
            /* if the current x coordinates is too big and y coordinate is too small, recursively call find_nodes with nnum=4*nnum+3 */
            if(p->node[nnum].x >= (loc->x - loc->range) && p->node[nnum].y_right <= ((loc->y) + (loc->range)))
                find_nodes (loc, vs, p, 4 * nnum + 3);
            /* if the current x, y coordinates are too small, recursively call find_nodes with nnum=4*nnum+4 */
            if(p->node[nnum].x <= (loc->x + loc->range) && p->node[nnum].y_right <= ((loc->y) + (loc->range)))
                find_nodes (loc, vs, p, 4 * nnum + 4);
            return;
        }
    }
   
}

/*
 * trim_nodes --  remove any graph vertices that are not in range of a locale from a vertex set
 * INPUTS:        a copy of graph, vertex set pointer vs, locale pointer loc 
 * OUTPUTS:       None 
 * RETURN:        None
 * SIDE EFFECTS:  None 
 */
void
trim_nodes (graph_t* g, vertex_set_t* vs, locale_t* loc)
{
    int32_t tmp[MAX_IN_VERTEX_SET], i = 0;      /* a temporily array to hold the element in the vertex set, i is the index, initialize to 0 */
    /* traverse all the vertex in the vertex set vs points to */
    for (int32_t j = 0 ; j <= vs->count - 1 ; j++) 
    {
        /* if the vertex is in range of locale, put it in the temporily array */
        if (in_range(loc, g->vertex[vs->id[j]].x, g->vertex[vs->id[j]].y)) 
        {
            /* if the number of element is out of boundary, break */
            if (i >= MAX_IN_VERTEX_SET)
                break;
            /* put it in the temporily array and increment the tmp array index */
            tmp[i] = vs->id[j]; i++;
        }
    }
    /* set the vs->count to be i, the number of elements */
    vs->count = i;
    /* traverse the tmp array and put its index back to vs->id array */
    for (int32_t k = 0 ; k <= i - 1 ; k++) 
        vs->id[k] = tmp[k];
}

/*
 * insert   --   insert an element to the heap
 * INPUTS:       a copy of graph, the heap pointer and the element to be inserted 
 * OUTPUTS:      None 
 * RETURN:       None
 * SIDE EFFECTS: None 
 */
void insert (graph_t *g, heap_t* h, int32_t new_elt)
{
    /* increment the n_elts field and add the new element at last */
    h->elt[h->n_elts++] = new_elt;        
    int i = h->n_elts - 1;           /* the pointer to the index of element to be adjust */      
    /* while the index isn't points to the top */        
    while (0 != i)
    {
        int j = (i - 1) / 2;         /* the pointer to the parent of the element i points to */
        /* if the new element is bigger than parent element, the sort is over and the function ends */              
        if (g->vertex[h->elt[j]].from_src < g->vertex[new_elt].from_src)
            break;
        /* move down the parents element */
        h->elt[i] = h->elt[j];
        /* set i to be its parents, ready for next loop */             
        i = j;                             
    }
    /* adjust the new element to its position */
    h->elt[i] = new_elt;   
    /* returns to caller with nothing */
    return;                 
}

/*
 * pop     --    pop the top element of the heap and delete it
 * INPUTS:       a copy of graph, the heap pointer 
 * OUTPUTS:      None 
 * RETURN:       the top element in the heap
 * SIDE EFFECTS: None 
 */
int32_t pop (graph_t* g, heap_t* h)
{
    int32_t top = h->elt[0];    /* the top element in the heap */
    /* decrement the n_elts field */
    h->n_elts--;      
    /* if the heap isn't empty after pop */
    if (0 != h->n_elts)
    {   
        int32_t i = 0, j = 2 * i + 1;           /*i is the index to the element to be adjust, j is i's left child */
        int32_t tmp = h->elt[h->n_elts];        /* tmp is the original last element in the heap */       
        /* continusously up-shift the parent element */                                                 
        while (j <= h->n_elts - 1)                              
        {
            /* if there's a smaller right child, set j to be the right child */
            if (j < h->n_elts - 1 && g->vertex[h->elt[j]].from_src > g->vertex[h->elt[j+1]].from_src)     
                j++;
            /* if the element to be adjust is smaller than other child, the sort is over and the function ends */
            if (g->vertex[tmp].from_src <= g->vertex[h->elt[j]].from_src)                                   
                break;
            /* else, move the child to its parent */
            h->elt[i] = h->elt[j];     
            /* update i and j for next loop, i becomes the smaller child, j is the new left child */                          
            i = j;                                              
            j = 2 * i + 1;                                       
        }
        /* adjust the element to its position */
        h->elt[i] = tmp;
    }      
    /* return top to its caller */                                                                       
    return top;
}

/*
 * dijkstra  --  use a modified Dijkstra algorithm to find the shortest path between any node in the source set the destination set
 * INPUTS:       a copy of graph, the heap pointer h, the starting and ending points set pointer src, dest, the path pointer path
 * OUTPUTS:      None 
 * RETURN:       return 1 if a path is found that can fit into the path structure, otherwise return 0
 * SIDE EFFECTS: None 
 */
int32_t
dijkstra (graph_t* g, heap_t* h, vertex_set_t* src, vertex_set_t* dest,
          path_t* path)
{
    /* I reverse the start and end in the beginning, so that the backtracking using .pred won't make the path reversed */
    /* I declare the vertex.is_reached field in header file, representing whether the vertex has been reached */

    /* initialize the heap,set n_elts field to be 0 */
    h->n_elts = 0;
    /* traverse all the vertex in the graph */
    for (int32_t i = 0 ; i <= g->n_vertices - 1 ; i++) 
    {   
        /* set their is_reached field to be UNREACHED and from_src field to be infinite */
        g->vertex[i].is_reached = UNREACHED;
        g->vertex[i].from_src = MY_INFINITY;
    }
    /* traverse all the ending vertex in graph */
    for (int32_t j = 0; j < dest->count; j++) 
    {
        /* set all the vertex's pred field to be UNDEF and from_src field to be 0 and insert it in heap */
        g->vertex[dest->id[j]].pred = UNDEF;
        g->vertex[dest->id[j]].from_src = 0;
        insert(g, h, dest->id[j]);
    }
    /* while the heap is not empty */
    while (0 != h->n_elts) 
    {
        /* pop the smallest element in heap and assign it to a declared int32_t variable index */
        int32_t index = pop(g, h);  
        /* set the vertex's is_reached field to be REACHED */
        g->vertex[index].is_reached = REACHED;
        /* traverse all the neighbors of this vertex */
        for (int32_t k = 0 ; k <= g->vertex[index].n_neighbors - 1 ; k++)
        {
            /* if the neighbor hasn't been reached and the from_src distance of the neighbor is bigger than the distance through the vertex */
            if (REACHED != g->vertex[g->vertex[index].neighbor[k]].is_reached && g->vertex[index].from_src + g->vertex[index].distance[k] < g->vertex[g->vertex[index].neighbor[k]].from_src) 
            {
                /* set the neighbor's from_src to be the distance through the vertex, set the predecessor to be the vertex */
                g->vertex[g->vertex[index].neighbor[k]].from_src = g->vertex[index].from_src + g->vertex[index].distance[k];
                g->vertex[g->vertex[index].neighbor[k]].pred = index;
                /* insert the neighbor in heap */
                insert(g, h, g->vertex[index].neighbor[k]);
            }
        }
    }
    /* since the start and end is reversed, we now need to find the starting point with least distance to end instead */
    int32_t dist_min = MY_INFINITY; /* the minimal distance from the ending points, initialize to infinite */
    int32_t src_pt = UNDEF;         /* the starting points that optimize the dist_min, initialize to undefine */

    /* traverse the starting points to find dist_min and src_pt */
    for (int32_t m = 0 ; m < src->count - 1 ; m++) 
    {   
        /* if the from_src distance is smaller than current dist_min */
        if (g->vertex[src->id[m]].from_src < dist_min) 
        {
            /* reset the dist_min and src_pt */
            dist_min = g->vertex[src->id[m]].from_src;
            src_pt = src->id[m];
        }
    }
    /* initialize the path, set n_vertices be 0 and tot_dist be dist_min */
    path->n_vertices = 0;
    path->tot_dist = dist_min;

    int32_t n = src_pt;     /* conditional index used in while loop, initialize to start point */
    /* while still defined */
    while (UNDEF != n)
    {
        /* if the path requires more than MAX_PATH_LENGTH nodes, return 0 */ 
        if (path->n_vertices >= MAX_PATH_LENGTH) 
            return 0;
        /* fill the path->id array, increment the n_vertices and update the index n */
        path->id[path->n_vertices] = n;
        path->n_vertices++;
        n = g->vertex[n].pred;
    }
    /* success, return 1 */
    return 1;
}