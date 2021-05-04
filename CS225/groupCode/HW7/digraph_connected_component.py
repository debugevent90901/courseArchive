# -*- coding: utf-8 -*-

class DiGraph:
    def __init__(self,edges=[]):
        self.vertexList = VertexList(edges)
        for e in edges:
            self.addEdge(e)
            ## Modification
            # for directed graph, we only need to store one direction - (in, out)
            # self.addEdge((e[1],e[0])) 
    def addEdge(self,edge):
        # locate the related vertex according to the edge given
        vertex = self.vertexList.locate(edge[0]) # edge[0] is the incoming vertex
        edgelist = vertex.edges # get the edgelist object for this incoming vertex
        if edgelist != None:
            # add outcoming vertex to the edgelist
            edgelist.add(edge[1])
        else:
            # construct a new Edgelist object if this vertex has no edgelist yet
            edgelist = EdgeList(edge[1])
        vertex.setEdges(edgelist)
    def __iter__(self):
        vertices = self.vertexList
        for v in vertices:
            x = vertices.locate(v)
            y = x.edges
            if y != None:
                for z in y:
                    yield (v,z)
    def insertVertex(self,item):
        if not (item in self.vertexList):
            self.vertexList.append(item)
    def deleteVertex(self,item):
        return self.vertexList.remove(item)
    def insertEdge(self,edge):
        self.vertexList.addVertex(edge)
        self.addEdge(edge)
        ## Modification, only one direction now
        # self.addEdge((edge[1],edge[0]))
    def deleteEdge(self,edge):
        self.__deleteEdge(edge)
        ## Modification, only one direction now
        # self.__deleteEdge((edge[1],edge[0]))
    def __deleteEdge(self,edge):
        if not (edge[0] in self.vertexList):
            print("There is no edge", edge)
            return False
        vertexlocation = self.vertexList.locate(edge[0])
        edgelist = vertexlocation.getEdges()
        if edgelist == None:
            print("There is no edge", edge)
            return False
        res = edgelist.remove(edge[1])
        if res == False:
            print("There is no edge", edge)
        return res
    def outgoingEdges(self,item):
        vertex = self.vertexList.locate(item)
        if vertex == None:
            print("There is no vertex", item)
            return []
        edgelist = vertex.getEdges()
        if edgelist == None:
            return []
        res = []
        for v in edgelist:
            res.append((item,v))
        return res

    #DFS traverse using recursion
    def allDFS(self):
        numVertices = self.vertexList.getlength()
        initlist = [None]* numVertices
        self.tree = PyList(initlist,numVertices)
        for i in range(numVertices):
            newgraph = DiGraph([])
            self.tree[i] = newgraph
        for s in self.vertexList:
            self.mark = [None] * numVertices
            self.dfsPos = 1
            self.dfsNum = [1] * numVertices
            self.finishingTime = 1
            self.finishTime = [1] * numVertices
            idx = self.vertexList.index(s)
            if self.mark[idx] == None:
                self.mark[idx] = s
                self.dfsNum[idx] = self.dfsPos
                self.dfsPos += 1
                self.dfs(s,idx)
    def dfs(self,vertex,index):
        for e in self.outgoingEdges(vertex):
            idx = self.vertexList.index(e[1])
            if self.mark[idx] == None:
                self.tree[index].insertEdge(e)
                self.__traverseTreeEdge(e)
                self.mark[idx] = e[1]
                self.dfs(e[1],index)
        self.backtrack(vertex)
    def __traverseTreeEdge(self,e):
        idx = self.vertexList.index(e[1])
        self.dfsNum[idx] = self.dfsPos
        self.dfsPos += 1
    def backtrack(self,vertex):
        idx = self.vertexList.index(vertex)
        self.finishTime[idx] = self.finishingTime
        self.finishingTime += 1
    
    def singleDFS(self, stack, vertex):
        numVertices = self.vertexList.getlength()
        self.mark = [None] * numVertices
        self.dfsPos, self.finishingTime = 1, 1
        self.dfsNum, self.finishTime = [1] * numVertices, [1] * numVertices
        idx = self.vertexList.index(vertex)
        self.mark[idx] = vertex
        self.dfsNum[idx] = self.dfsPos
        self.dfsPos += 1
        self.DFS(stack, vertex, idx)
        tmp = []
        for i in stack:
            if i != None:
                tmp.append(i)
        return tmp
        
    def DFS(self, stack, vertex, index):
        for e in self.outgoingEdges(vertex):
            idx = self.vertexList.index(e[1])
            if self.mark[idx] == None:
                self.__traverseTreeEdge(e)
                self.mark[idx] = e[1]
                self.DFS(stack, e[1], index)
        stack.push(vertex)
        self.backtrack(vertex)
    
    def reverse(self):
        tmp = []
        for i in self:
            self.deleteEdge(i)
            tmp.append((i[1], i[0]))
        res = DiGraph(tmp)
        return res
    
    def stronglyConnectedComponent(self):
        ans = []
        zhan = Stack()
        numVertices = self.vertexList.getlength()
        visited = PyList(numVertices * [False], numVertices)
        for i in self.vertexList:
            index = self.vertexList.index(i)
            if visited[index] == False:
                path = self.singleDFS(zhan, i)
                for j in path:
                    visited[self.vertexList.index(j)] = True
        reverse_DiGraph = self.reverse()
        while not zhan.isEmpty():
            newZhan = Stack()
            current = zhan.pop()
            if visited[reverse_DiGraph.vertexList.index(current)] == True:
                tmp = reverse_DiGraph.singleDFS(newZhan, current)
                for j in tmp:
                    visited[reverse_DiGraph.vertexList.index(j)] = False
                SET = set()
                for k in ans:
                    SET = SET.union(set(k))
                newPath = list(set(tmp) - SET)
                ans.append(newPath)
        return ans

# Definition of VertexList Class, a linked list
class VertexList:
    class  __Vertex:
        def __init__(self,item,next=None,previous=None):
            self.item=item # the vertex content
            self.next=next
            self.previous=previous
            self.edges=None # vertices related to this vertex
        def getItem(self):
            return self.item
        def getNext(self):
            return self.next
        def getPrevious(self):
            return self.previous
        def getEdges(self):
            return self.edges
        def setItem(self,item):
            self.item = item
        def setNext(self,next):
            self.next = next
        def setPrevious(self,previous):
            self.previous = previous
        def setEdges(self,edge):
            self.edges = edge
    
    def __init__(self,edges=[]):
        self.dummy = VertexList.__Vertex(None,None,None)
        self.numVertices = 0
        self.dummy.setNext(self.dummy)
        self.dummy.setPrevious(self.dummy)
        for e in edges:
            self.addVertex(e)
    def __iter__(self):
        cursor = self.dummy
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            yield cursor.getItem()
    def append(self,item):
        lastVertex = self.dummy.getPrevious()
        newVertex = VertexList.__Vertex(item,self.dummy,lastVertex)
        lastVertex.setNext(newVertex)
        self.dummy.setPrevious(newVertex)
        self.numVertices += 1
    def __contains__(self,item):
        cursor = self.dummy
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            vertex = cursor.getItem()
            if vertex == item:
                return True
        return False
    # locate the vertex location using its vertex value
    def locate(self,vertex): 
        cursor = self.dummy
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            item = cursor.getItem()
            if vertex == item:
                return cursor
    # add new vertex if possible for the new edge
    def addVertex(self,edge):
        node1 = edge[0]
        node2 = edge[1]
        if not (node1 in self):
            self.append(node1)
        if not (node2 in self):
            self.append(node2)
    # remove a vertex
    def remove(self,item):
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
    def index(self,item):
        cursor = self.dummy
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            if cursor.getItem() == item:
                return i
        return -1
    def getlength(self):
        return self.numVertices
    
# Definition of EdgeList Class, also a linked list
class EdgeList:
    class __Edge:
        def __init__(self,item,next=None,previous=None):
            self.item=item
            self.next=next
            self.previous=previous
        def getItem(self):
            return self.item
        def getNext(self):
            return self.next
        def getPrevious(self):
            return self.previous
        def setItem(self,item):
            self.item = item
        def setNext(self,next):
            self.next = next
        def setPrevious(self,previous):
            self.previous = previous
    
    def __init__(self,edge):
        self.first = EdgeList.__Edge(edge,None,None)
        self.first.setNext(self.first)
        self.first.setPrevious(self.first)
        self.numEdges = 1
    def add(self,edge):
        lastEdge = self.first.getPrevious()
        newEdge = EdgeList.__Edge(edge,self.first,lastEdge)
        lastEdge.setNext(newEdge)
        self.first.setPrevious(newEdge)
        self.numEdges += 1
    def __iter__(self):
        cursor = self.first
        for i in range(self.numEdges):
            yield cursor.getItem()
            cursor = cursor.getNext()
    def __contains__(self,item):
        cursor = self.first
        for i in range(self.numEdges):
            vertex = cursor.getItem()
            if vertex == item:
                return True
            cursor = cursor.getNext()
        return False
    def remove(self,item):
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

# Definition of PyList class
class PyList:
    def __init__(self,contents=[],size=20):
        self.items = [None] * size
        self.numItems = 0
        self.size = size
        for e in contents:
            self.append(e)
    def __setitem__(self,index,val):
        if index >= 0 and index < self.numItems:
            self.items[index] = val
            return
        raise IndexError("PyList assignment index out of range")
    def __getitem__(self,index):
        if index >= 0 and index < self.numItems:
            return self.items[index]
        raise IndexError("PyList index out of range")
    def append(self,item):
        if self.numItems == self.size:
            self.allocate()
        self.items[self.numItems] = item
        self.numItems += 1
    def allocate(self):
        newlength = 2 * self.size
        newList = [None] * newlength
        for i in range(self.numItems):
            newList[i] = self.items[i]
        self.items = newList
        self.size = newlength
    def insert(self,i,x):
        if self.numItems == self.size:
            self.allocate()
        if i < self.numItems:
            for j in range(self.numItems-1,i,-1):
                self.items[j+1] = self.items[j]
            self.items[i] = x
            self.numItems += 1
        else:
            self.append(x)
    def __add__(self,other):
        result = PyList(size=self.numItems+other.numItems)
        for i in range(self.numItems):
            result.append(self.items[i])
        for i in range(other.numItems):
            result.append(other.items[i])
        return result
    def delete(self,index):
        if self.numItems == self.size / 4:
            self.deallocate()
        if index <= self.numItems:
            for j in range(index,self.numItems-2):
                self.items[j] = self.items[j+1]
            self.numItems -= 1
        else:
            raise IndexError("PyList index out of range")
    def deallocate(self):
        newlength = self.size / 2
        newList = [None] * newlength
        for i in range(self.numItems):
            newList[i] = self.items[i]
        self.items = newList
        self.size = newlength
    def __contains__(self,item):
        for i in range(self.numItems):
            if self.items[i] == item:
                return True
            return False
    def __eq__(self,other):
        if type(other) != type(self):
            return False
        if self.numItems != other.numItems:
            return False
        for i in range(self.numItems):
            if self.items[i] != self.items[i]:
                return False
            return True
    def qsort(self):
        if self.numItems <= 1:
            return self
        pivot = self.items[0]
        list1 = PyList([],self.numItems)
        listp = PyList([],self.numItems)
        list2 = PyList([],self.numItems)
        for i in range(self.numItems):
            if self.items[i] < pivot:
                list1.append(self.items[i])
            else:
                if self.items[i] == pivot:
                    listp.append(self.items[i])
                else:
                    list2.append(self.items[i])
        slist1 = list1.qsort()
        slist2 = list2.qsort()
        outlist = slist1 + listp + slist2
        return outlist
    def radixSort(self,numdigits,digits):
        sortedlist = self
        for i in range(numdigits):
            sortedlist = sortedlist.Ksort(i,digits)
        return sortedlist          
    def Ksort(self,round,digits):
        bucket = PyList([],digits)
        for k in range(digits):
            newlist = PyList([],self.numItems)
            bucket.append(newlist)
        for i in range(self.numItems):
            item = self.items[i]
            item1 = item // (digits ** round) % digits
            bucket[item1].append(item)
        result = bucket[0]
        for k in range(digits-1):
            result = result + bucket[k+1]
        return result

class Stack(object):
    class Node(object):
        def __init__(self, val):
            self.val = val
            self.next = None

    def __init__(self):
        self.head = None

    def top(self):
        if self.head is not None:
            return self.head.val
        else:
            return None

    def push(self, n):
        n = self.Node(n)
        n.next = self.head
        self.head = n
        return n.val

    def pop(self):
        if self.head is None:
            return None
        else:
            tmp = self.head.val
            self.head = self.head.next
            return tmp

    def isEmpty(self):
        if self.head is None:
            return True
        else:
            return False

    def show(self):
        if self.head is None:
            return
        temp = self.head
        while temp is not None:
            temp = temp.next

    def __iter__(self):
        if self.head is None:
            return
        temp = self.head
        while temp is not None:
            yield temp.val
            temp = temp.next


g = DiGraph([(1, 2), (3, 1), (2, 3), (2, 4), (3, 4), (2, 6), (4, 5), (5, 4), (6, 5), (6, 7), (7, 6), (8, 5), (7, 8), (8, 7)])
a = g.stronglyConnectedComponent()
print(a)