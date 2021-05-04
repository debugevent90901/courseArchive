# -*- coding: utf-8 -*-
# cs225 assignment8 ex1

import numpy as np

# the implementation will generate a random undirected graph
def MaxSpanningTree(n, weight_range = [1, 20]):
    def __generateMAT(n):
        mat = np.random.randint(weight_range[0], weight_range[1]+1, (n, n))
        for i in range(n):
            for j in range(n):
                if i == j:
                    mat[i, j] = 0
                elif i > j:
                    mat[i, j] = mat[j, i]
        print("Cost Matrix:\n", mat, "\n")
        return mat

    # edge in form of (cost, vertex1, vertex2), where vertex1 < vertex2
    mat, edges, edges_reversed = __generateMAT(n), [], []
    sum = mat.sum()
    for i in range(n):
        for j in range(n):
            if i < j:
                edges.append((mat[i, j], i, j))
                edges_reversed.append((sum-mat[i, j], i, j))
    # Sort the edge list
    edges_reversed = sorted(edges_reversed, key=lambda x: x[0])

    for i in edges:
        print("edge: ", (i[1], i[2]), "weight: ", i[0])

    # We use index from 0 to n - 1
    CC_lst = [[i] for i in range(n)]
    MST_edges = []
    while len(CC_lst) > 1:
        curr_edge = edges_reversed.pop(0)
        for CC in CC_lst:
            if curr_edge[1] in CC:
                CC_1 = CC.copy()
            if curr_edge[2] in CC:
                CC_2 = CC
        # Merge two connected component
        if CC_1 == CC_2:
            continue
        CC_lst.remove(CC_1)
        CC_lst.remove(CC_2)
        CC_1.extend(CC_2)
        CC_lst.append(CC_1)
        MST_edges.append((curr_edge[1], curr_edge[2]))

    # Output the result
    print("\nMaxSpanningTree:\n", MST_edges)


def main():
    MaxSpanningTree(4)


if __name__ == "__main__":
    main()