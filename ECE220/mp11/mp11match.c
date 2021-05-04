/* this .c file contains one function called match_requests, which initialize and use Dijkstra algorithm to find the shortest path 
   between node in the source set and destination set. It accepts a copy of the graph, a pyramid tree containing all vertices in the
   graph, a “blank” heap, and two requests as parameter. If the source or destination node set is empty or the path requires more 
   than MAX_PATH_LENGTH nodes return 0, otherwise, return 1. */

#include <stdint.h>
#include <stdio.h>

#include "visualize.h"
#include "mp11.h"

/*
 * match_requests -- initialize and use Dijkstra algorithm to find the shortest path between node in the source set and destination set.
 * INPUTS:           a copy of the graph, a pyramid tree containing all vertices in the graph, a “blank” heap, and two requests
 * OUTPUTS:          None 
 * RETURN:           if the source or destination node set is empty or the path requires more than MAX_PATH_LENGTH nodes return 0, otherwise, return 1
 * SIDE EFFECTS:     None
 */
int32_t
match_requests (graph_t* g, pyr_tree_t* p, heap_t* h,
		request_t* r1, request_t* r2,
		vertex_set_t* src_vs, vertex_set_t* dst_vs, path_t* path)
{
    /* initialization, set the number of the starting and ending points to be 0 */
    src_vs->count = 0;
    dst_vs->count = 0;
    /* find the starting points that matches the request 1 */
    find_nodes(&(r1->from), src_vs, p, 0);
    /* remove the founded starting points that do not match the request 2*/
    trim_nodes(g, src_vs, &(r2->from));
    /* find the ending points that matches the request 1 */
    find_nodes(&(r1->to), dst_vs, p, 0); 
    /* remove the founded ending points that do not match the request 2*/
    trim_nodes(g, dst_vs, &(r2->to));

    /* If the source node set or the destination node set is empty, return 0 */
    if (0 == src_vs->count || 0 == dst_vs->count)
        return 0;
    /* return the return value of dijkstra function, 1 if success, 0 otherwise */
    /* if the path requires more than MAX_PATH_LENGTH nodes, return 0 is included*/
    return dijkstra(g, h, src_vs, dst_vs, path);
}
