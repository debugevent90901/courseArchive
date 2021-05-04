# this is the exercise 3 of this homework
# this code will make use of the Hall's Marriage Theorem

# The BiGraph contains two sets of vertexes vA & vB
# It is a undirected graph
# It has these methods:
#   addEdge                 add edge to both vertex in vA & vB
#   insertVertexToA         insert vertex to set vA
#   insertVertexToB         insert vertex to set vB
#   deleteVertex            delete vertex from the graph (vA & vB)
#   insertEdge              insert edge and its vertexes into the graph
#   insertEdges             insert edges into the graph
#   deleteEdge              delete edge from the graph
#   outgoingEdges           output a list of outgoing edges of corresponding vertex

class BiGraph:
    # The input of the graph should be an edge (tuple) (A, B)
    # A should be the vertex in set vA or added to A
    # B should be the vertex in set vB or added to B
    # wrong input would break the structure of bipartite graph, which is not acceptable
    def __init__(self, edges=[]):
        self.vA = VertexList()
        self.vB = VertexList()
        for e in edges:
            self.insertEdge(e)

    # iterate edges in vA & vB
    def __iter__(self):
        for v in self.vA:
            x = self.vA.locate(v)
            y = x.edges
            if y != None:
                for z in y:
                    yield (v, z)
        for v in self.vB:
            x = self.vB.locate(v)
            y = x.edges
            if y != None:
                for z in y:
                    yield (v, z)

    # add edge to both vertex in vA & vB (due to the graph is a undirected graph)
    def addEdge(self, edge):
        # Add edge to vertex set A
        vertexA = self.vA.locate(edge[0])
        edgelistA = vertexA.edges
        if edgelistA != None:
            edgelistA.add(edge[1])
        else:
            edgelistA = EdgeList(edge[1])
        vertexA.setEdges(edgelistA)
        # Add edge to vertex set B
        vertexB = self.vB.locate(edge[1])
        edgelistB = vertexB.edges
        if edgelistB != None:
            edgelistB.add(edge[0])
        else:
            edgelistB = EdgeList(edge[0])
        vertexB.setEdges(edgelistB)

    # insert vertex to set vA
    def insertVertexToA(self, item):
        self.vA.addVertex(item)
    # insert vertex to set vB
    def insertVertexToB(self, item):
        self.vB.addVertex(item)

    # delete vertex from the graph (vA & vB)
    def deleteVertex(self, item):
        if item in self.vA:
            self.vB.delEdgeWithItem(item)
            return self.vA.remove(item)
        else:
            self.vA.delEdgeWithItem(item)
            return self.vB.remove(item)

    # The input should be an edge (tuple) (A, B)
    # A should be the vertex in set vA or added to A
    # B should be the vertex in set vB or added to B
    # wrong input would break the structure of bipartite graph, which is not acceptable
    def insertEdge(self, edge):
        if edge[0] in self.vB or edge[1] in self.vA:
            raise Exception("Wrong Input")
        self.vA.addVertex(edge[0])
        self.vB.addVertex(edge[1])
        self.addEdge(edge)

    # The input should be a list consists of edges
    def insertEdges(self,edges):
        for e in edges:
            self.insertEdge(e)

    # delete edge from the graph
    def deleteEdge(self, edge):
        if not (edge[0] in self.vA):
            print("There is no edge", edge)
            return False
        vertexloc = self.vA.locate(edge[0])
        edgelistA = vertexloc.getEdges()
        if edgelistA == None:
            print("There is no edge", edge)
            return False
        res = edgelistA.remove(edge[1])
        if res == False:
            print("There is no edge", edge)
            return res
        if not (edge[1] in self.vB):
            print("There is no edge", edge)
            return False
        vertexloc = self.vB.locate(edge[1])
        edgelistB = vertexloc.getEdges()
        if edgelistB == None:
            print("There is no edge", edge)
            return False
        res = edgelistB.remove(edge[0])
        if res == False:
            print("There is no edge", edge)
        return res

    # output a list of outgoing edges of corresponding vertex
    def outgoingEdges(self, item):
        vertex = self.vA.locate(item)
        if vertex == None:
            vertex = self.vB.locate(item)
        if vertex == None:
            print("There is no vertex", item)
            return []
        edgelist = vertex.getEdges()
        if edgelist == None:
            return []
        res = []
        for v in edgelist:
            res.append((item, v))
        return res

    def PerfectMatch(self):
        # adopt the Hall Marriage theorem
        total_set = self.vA.package() + self.vB.package()
        all_subsets = BiGraph.__find_subsets(total_set)
        all_subsets.remove([])
        for i in all_subsets:
            set_size = len(i)
            temp_set = set()
            for j in i:
                for edge in self.outgoingEdges(j):
                    temp_set.add(edge[1])
            num_neighbors = len(temp_set)
            if set_size > num_neighbors:
                return False
        return True

    @staticmethod
    def __find_subsets(content):
        if len(content) == 0:
            return [[]]
        subset = []
        first = content[0]
        res = content[1:]
        for partial_subset in BiGraph.__find_subsets(res):
            subset.append(partial_subset)
            subset.append([first]+partial_subset)
        return subset

# Definition of VertexList Class
class VertexList:
    class __Vertex:
        def __init__(self, item, next=None, previous=None):
            self.item = item
            self.next = next
            self.previous = previous
            self.edges = None

        def getItem(self):
            return self.item

        def getNext(self):
            return self.next

        def getPrevious(self):
            return self.previous

        def getEdges(self):
            return self.edges

        def setItem(self, item):
            self.item = item

        def setNext(self, next):
            self.next = next

        def setPrevious(self, previous):
            self.previous = previous

        def setEdges(self, edge):
            self.edges = edge

    def __init__(self, edges=[]):
        self.dummy = VertexList.__Vertex(None, None, None)
        self.numVertices = 0
        self.dummy.setNext(self.dummy)
        self.dummy.setPrevious(self.dummy)
        self.contentSet = set()
        for e in edges:
            self.addVertex(e[0])
            self.addVertex(e[1])

    def addVertex(self, vertex):
        if vertex not in self:
            self.contentSet.add(vertex)
            self.__append(vertex)

    def __iter__(self):
        cursor = self.dummy
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            yield cursor.getItem()

    def __append(self, item):
        lastVertex = self.dummy.getPrevious()
        newVertex = VertexList.__Vertex(item, self.dummy, lastVertex)
        lastVertex.setNext(newVertex)
        self.dummy.setPrevious(newVertex)
        self.numVertices += 1

    def __contains__(self, item):
        if item in self.contentSet:
                return True
        return False

    def locate(self, vertex):
        cursor = self.dummy
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            item = cursor.getItem()
            if vertex == item:
                return cursor
        return None

    # if we remove a vertex directly, then the corresponding edgeList will also be influenced
    # so we must:
    # 1. find the item(a vertex here).
    # 2. see if this vertex has many edges from itself:
    #        yes: don't delete it
    #        no: delete it by removing this from the linked list
    def remove(self, item):
        cursor = self.dummy
        location = None
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            vertex = cursor.getItem()
            edgelist = cursor.edges
            if edgelist != None:
                if item in edgelist:
                    print(item, "cannot be deleted, as it appears in an edge.")
                    return False
            if vertex == item:
                location = cursor
        if location == None:
            print(item, "is not a vertex.")
            return False
        nextVertex = location.getNext()
        prevVertex = location.getPrevious()
        prevVertex.setNext(nextVertex)
        nextVertex.setPrevious(prevVertex)
        self.numVertices -= 1
        return True

    # delete edges contains corresponding item: edge is a tuple
    # usage: vertexList[xxx].delEdgeWithItem([vertex1, vertex2])
    def delEdgeWithItem(self, item):
        cursor = self.dummy
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            edgelist = cursor.edges
            if edgelist != None:
                if item in edgelist:
                    edgelist.remove(item)

    def getlength(self):
        return self.numVertices

    def package(self):
        res = []
        for i in self:
            res.append(i)
        return res

# Definition of EdgeList Class
class EdgeList:
    class __Edge:
        def __init__(self, item, next=None, previous=None):
            self.item = item # this should be a tuple
            self.next = next
            self.previous = previous

        def getItem(self):
            return self.item

        def getNext(self):
            return self.next

        def getPrevious(self):
            return self.previous

        def setItem(self, item):
            self.item = item

        def setNext(self, next):
            self.next = next

        def setPrevious(self, previous):
            self.previous = previous

    def __init__(self, edge):
        self.first = EdgeList.__Edge(edge, None, None)
        self.first.setNext(self.first)
        self.first.setPrevious(self.first)
        self.numEdges = 1

    def add(self, edge):
        lastEdge = self.first.getPrevious()
        newEdge = EdgeList.__Edge(edge, self.first, lastEdge)
        lastEdge.setNext(newEdge)
        self.first.setPrevious(newEdge)
        self.numEdges += 1

    def __iter__(self):
        cursor = self.first
        for i in range(self.numEdges):
            yield cursor.getItem()
            cursor = cursor.getNext()

    def __contains__(self, item):
        cursor = self.first
        for i in range(self.numEdges):
            vertex = cursor.getItem()
            if vertex == item:
                return True
            cursor = cursor.getNext()
        return False

    def remove(self, item):
        cursor = self.first
        for i in range(self.numEdges):
            vertex = cursor.getItem()
            if vertex == item:
                nextVertex = cursor.getNext()
                prevVertex = cursor.getPrevious()
                prevVertex.setNext(nextVertex)
                nextVertex.setPrevious(prevVertex)
                self.numEdges -= 1
                if (cursor == self.first):
                    self.first = nextVertex
                return True
            cursor = cursor.getNext()
        return False


if __name__ == "__main__":
    a = BiGraph([('A','F'),('B','F'),('B','G'),('C','E')])
    for i in a:
        print(i)
    print()
    a.insertEdge(('B','E'))
    a.deleteEdge(('B','G'))
    a.deleteVertex('A')
    for i in a:
        print(i)
    print(a.outgoingEdges('B'))
    print("\n-----------\n")
    a = BiGraph([("b1","g3"),("b2","g3"),("b3","g1"),("b3","g2")])
    print(a.PerfectMatch())
    a = BiGraph([("b1","g3"),("b2","g3"),("b3","g1"),("b3","g2"),("b2","g2")])
    print(a.PerfectMatch())