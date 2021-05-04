# -*- coding: utf-8 -*-
# main.py
"""
This is CS225 HW1.

Group Member:
Zhu Zhongbo
Guan Zimu
Xie Tian
Yang Zhaohua
"""

from Git import upload

class PyList(list):
    def __init__(self, content=[], size = 20):
        self.items = [None]*size
        self.numItems = 0
        self.size = size
        for e in content:
            self.append(e)
    def __contains__(self,item):
        for i in range(self.numItems):
            if self.items[i] == item:
                return True
        return False
    def __eq__(self,other):
        if (type(self) != type(other)):
            return False
        if self.numItems != other.numItems:
            return False
        for i in range(self.numItems):
            if (self.items[i] != other.items[i]):
                return False
        return True
    def __setitem__(self,index,val):
        if index >= 0 and index <= self.numItems-1:
            self.items[index] = val
            return
        raise IndexError("Pylist assignment index out of range.")
    def __getitem__(self,index):
        if index >= 0 and index <= self.numItems-1:
            return self.items[index]
        raise IndexError("Pylist index out of range.")
    def append(self,item):
        if self.numItems == self.size:
            self.allocate()
        self.items[self.numItems] = item
        self.numItems += 1
    def __add__(self,other):
        result = PyList(size=self.numItems+other.numItems)
        for i in range(self.numItems):
            result.append(self.items[i])
        for i in range(other.numItems):
            result.append(other.items[i])
        return result
    def insert(self,i,x):
        if self.numItems == self.size:
            self.allocate()
        if i < self.numItems:
            for j in range(self.numItems-1,i-1,-1):
                self.items[j+1] = self.items[j]
            self.items[i] = x
            self.numItems += 1
        else:
            self.append(x)
    def delete(self,index):
        if (self.numItems == self.size/4):
            self.deallocate()
        if index >= self.numItems:
            raise IndexError("PyList index out of range.")
        else:
            for i in range(index,self.numItems-1):
                self.items[i] = self.items[i+1]
            self.numItems -= 1
            return
    def allocate(self):
        newlength = 2 * self.size
        newList = [None] * newlength
        for i in range(self.numItems):
            newList[i] = self.items[i]
        self.items = newList
        self.size = newlength
    def deallocate(self):
        newlength = int(self.size / 2)
        newList = [None] * newlength
        for i in range(self.numItems):
            newList[i] = self.items[i]
        self.items = newList
        self.size = newlength
    def delete_last(self,k):
        if k>self.numItems:
            self.numItems = 0
            self.size = 1
            self.items = [None]*self.size
            return
        else:
            rest = self.numItems - k
            self.numItems = rest
            while (self.numItems <= int(self.size/4)):
                self.deallocate()
            return
    def src(self,e,f,g):
        if self.numItems == 0:
            return e
        if self.numItems == 1:
            return f(self.items[0])
        if self.numItems > 1:
            length = self.numItems
            length1 = int(length/2)
            length2 = length - length1
            list1 = PyList(self.items[0:length1],length1)
            list2 = PyList(self.items[length1:self.numItems],length2)
            return g(list1.src(e,f,g),list2.src(e,f,g))

class DoubleStack:
    class __Node:
        def __init__(self,val = None,next_node = None,prev_node = None):
            self.val = val
            self.next = next_node
            self.prev = prev_node
        def getNext(self):
            return self.next
        def getPrev(self):
            return self.prev
        def getVal(self):
            return self.val
        def setNext(self,node):
            self.next = node
        def setPrev(self,node):
            self.prev = node
        def setVal(self,val):
            self.val = val
    def __init__(self,content = []):
        self.head = self.__Node(None,None,None)
        self.end = self.__Node(None,None,None)
        self.head.setNext(self.end)
        self.head.setPrev(self.head)
        self.end.setPrev(self.head)
        self.end.setNext(self.end)
        for i in content:
            self.pushback(i)
    def pushback(self,val):
        newNode = self.__Node(val)
        newNode.setPrev(self.end.getPrev())
        newNode.setNext(self.end)
        (self.end.getPrev()).setNext(newNode)
        self.end.setPrev(newNode)
    def pushfront(self,val):
        newNode = self.__Node(val)
        newNode.setNext(self.head.getNext())
        newNode.setPrev(self.head)
        (self.head.getNext()).setPrev(newNode)
        self.head.setNext(newNode)
    def popback(self):
        result = self.end.getPrev().getVal()
        self.end.getPrev().getPrev().setNext(self.end)
        self.end.setPrev(self.end.getPrev().getPrev())
        return result
    def popfront(self):
        result = self.head.getNext().getVal()
        self.head.getNext().getNext().setPrev(self.head)
        self.head.setNext(self.head.getNext().getNext())
        return result
    def __len__(self):
        temp = self.head
        counter = 0
        while temp.getNext() != temp:
            temp = temp.getNext()
            counter += 1
        return counter-1

if __name__ == "__main__":
    a = list(range(50))
    pylist = PyList(a,128)
    #this is test 1
    print('''##############
This is test 1
##############''')
    e = 0
    f = lambda x : 1
    g = lambda x,y: x+y
    ans = pylist.src(e,f,g)
    print("the length is %d"%ans)
    #this is test2
    print('''##############
This is test 2
##############''')
    e = PyList([],0)
    f = lambda x: PyList([x+5],1)
    g = lambda x,y: x+y
    ans2 = pylist.src(e,f,g)
    for i in range(ans2.numItems):
        print(ans2.items[i])
    print("the size of the list %d"%ans2.size)
    print("the numItems of the list %d"%ans2.numItems)
    #this is test 3
    print('''##############
This is test 3 
##############''')
    e = PyList([],0)
    f = lambda x: PyList([x],1) if x>10 else PyList([],0)
    g = lambda x,y: x+y
    ans3 = pylist.src(e,f,g)
    for i in range(ans3.numItems):
        print(ans3.items[i])
    print("the size of the list %d"%ans3.size)
    print("the numItems of the list %d"%ans3.numItems)
    
    
    #this is for homework exercise 4
    print('''##################
This is exercise 4 
##################''')
    ds = DoubleStack(list(range(20)))
    print("the length of ds is %d"%len(ds))
    for i in range(5):
        a = ds.popfront()
        b = ds.popback()
        print(a,' ',b)
    new_element = [23,3343,5,65,65,36,547,5,765,757,533552,342]
    for i in new_element:
        if (i%2) == 1:
            ds.pushfront(i)
        else:
            ds.pushback(i)
    print("the length of ds is %d"%len(ds))
    for i in range(len(ds)):
        c = ds.popfront()
        print(c)


    upload()
