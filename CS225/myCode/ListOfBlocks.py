# -*- coding: utf-8 -*-

# a linked list, where each item is an array
class Block(list):
    def __init__(self,contents=[],next=None,previous=None):
        self.next = next 
        self.previous = previous
        
        self.item = [None] * 20 # the constant K
        self.numItems = 0
        self.size = 20
        for e in contents:
            self.append(e)
    
    # Original Node Class
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
    
    # Original Pylist Class
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
            if self.items[i] != other.items[i]:
                return False
        return True
    
    def __setitem__(self,index,val):
        if index >= 0 and index < self.numItems:
            self.item[index] = val
            return
        raise IndexError("Block assignment index out of range")

    def __getitem__(self,index):
        if index >= 0 and index < self.numItems:
            return self.item[index]
        raise IndexError("Block index out of range")
    
    def __add__(self,other):
        result = PyList(size=self.numItems+other.numItems)
        for i in range(self.numItems):
            result.append(self.items[i])
        for i in range(other.numItems):
            result.append(other.items[i])
        return result
    
    def append(self,item):
        self.items[self.numItems] = item
        self.numItems += 1
    
    def insert(self,i,x):
        if i < self.numItems:
            for j in range(self.numItems-1,i,-1):
                self.items[j+1] = self.items[j]
            self.items[i] = x
            self.numItems += 1
        else:
            self.append(x)
    
    def delete(self,index):
        if index <= self.numItems:
            for j in range(index,self.numItems-1):
                self.items[j] = self.items[j+1]
            self.numItems -= 1
            self.items[self.numItems] = None
        else:
            raise IndexError("Block index out of range")

    def swap(self, l, r):
        temp = self[l]
        self[l] = self[r]
        self[r] = temp
        
    def InsertionSort(self):
        for i in range(1, self.numItems):
            for j in range(i, 0, -1):
                if self[j] > self[j-1]:
                    break
                self.swap(j, j-1)

class ListOfBlocks(Block):
    def __init__(self,contents=[]):
        self.first = Block() 
        self.numBlocks = 0 # num of blocks
        self.numItems = 0  # num of items
        self.first.setNext(self.first) 
        self.first.setPrevious(self.first)
        for e in contents:
            if e == None:
                break
            self.append(e)
            
    def __setitem__(self,index,val):
        if index < 0:
            index += self.numItems
        if index >= 0 and index < self.numItems:
            node = self.first.next
            cursor = 0
            while(cursor + node.numItems <= index):
                cursor += node.numItems
                node = node.next
            node.item[index - cursor] = val
            return
        raise IndexError("ListOfBlock assignment index out of range")

    def __getitem__(self,index):
        if index < 0:
            index += self.numItems
        if index >= 0 and index < self.numItems:
            node = self.first.next
            cursor = 0
            while(cursor + node.numItems <= index):
                cursor += node.numItems
                node = node.next
            return node.item[index - cursor]
        raise IndexError("ListOfBlock index out of range")
    
    def printList(self):
        tmp = self.first.next
        nodes = []
        for i in range(self.numBlocks):
            nodes.append(str(tmp.item))
            tmp = tmp.next
        print(' <-> '.join(nodes))
        
    def append(self,item):
        lastNode = self.first.getPrevious()
        # Add a new node with size 20 if the previous one is full
        if self.first.previous == self.first or self.first.previous.numItems == 20:
            newNode = Block(self.first,lastNode) 
            lastNode.setNext(newNode) 
            self.first.setPrevious(newNode)
            self.numBlocks += 1
            lastNode = self.first.getPrevious()
        lastNode.item[lastNode.numItems] = item
        lastNode.numItems += 1
        self.numItems += 1
    
    def insert(self, index, item):
        if index < 0:
            index += self.numItems
        if index >= 0 and index < self.numItems:
            node = self.first.next
            cursor = 0
            while(cursor + node.numItems <= index):
                cursor += node.numItems
                node = node.next
            if node.numItems < 20:
                for i in range(node.numItems - 1,index - cursor,-1):
                    node.items[i+1] = node.items[i]
                node.items[index - cursor] = item
                node.numItems += 1
            else:
                # add a new block if the current is full
                nextNode = node.getNext()
                newNode = Node(item,self.nextNode,node) 
                nextNode.setPrevious(newNode)
                node.setNext(newNode)
                self.numBlocks += 1
                # move the last item to the next block
                newNode.append(node[20])
                
                for i in range(node.numItems - 2,index - cursor,-1):
                    node.items[i+1] = node.items[i]
                node.items[index - cursor] = item
                node.numItems += 1
                self.numItems += 1
        elif index == self.numItems:
            self.append(x)
        raise IndexError("ListOfBlock index out of range")

    def delete(self, index):
        if index < 0:
            index += self.numItems
        if index >= 0 and index < self.numItems:
            node = self.first.next
            cursor = 0
            while(cursor + node.numItems <= index):
                cursor += node.numItems
                node = node.next
            if node.numItems == 1:
                lastNode = node.getPrevious()
                nextNode = node.getNext()
                lastNode.setNext(nextNode)
                nextNode.setprevious(lastNode)
            else:
                for i in range(index - cursor, node.numItems - 1):
                    node.items[i] = node.items[i+1]
                node.items[index - cursor] = item
                node.numItems -= 1
                self.numItems -= 1
        raise IndexError("ListOfBlock index out of range")
        
    def locate(self, index):
        if index >= 0 and index < self.numBlocks:
            result = self.first.next
            for i in range(index):
                result = result.next
            return result
        return IndexError("Block index out of range")
    
    def MergeSort(self):
        if self.numBlocks < 1:
            return self
        return self.mergeSort(0, self.numBlocks - 1)
    
    def mergeSort(self, l, r): 
        if l < r:
            m = (l+r)//2     
            sort1 = self.mergeSort(l, m) 
            sort2 = self.mergeSort(m + 1, r) 
            return self.merge(sort1, sort2)
        
        # Use Insertion Sort for each single block
        elif l == r:
            block = self.locate(l)
            block.InsertionSort()
            return ListOfBlocks(block.item)
        return IndexError("MergeSort index out of range")

    def merge(self, list1, list2):
        if list1.numItems == 0:
            return list2
        if list2.numItems == 0:
            return list1
        result = ListOfBlocks()
        i = j = 0
        while(i < list1.numItems or j < list2.numItems):
            if i >= list1.numItems:
                result.append(list2[j])
                j += 1
            elif j >= list2.numItems:
                result.append(list1[i])
                i += 1
            else:
                if (list1[i] < list2[j]):
                    result.append(list1[i])
                    i += 1
                else:
                    result.append(list2[j])
                    j += 1
        return result