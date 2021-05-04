# -*- coding: utf-8 -*-
#linked list module
'''
This is HW2 for CS225

Team Member:
    Zhu Zhongbo
    Yang Zhaohua
    Guan Zimu
    Xie Tian
'''
class DLinkedList:
    class __Node:
        def __init__(self, item, next = None, previous = None):
            self.item = item
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

    def __init__(self, contents = []):
        self.first = DLinkedList.__Node(None, None, None)
        self.numItems = 0
        self.first.setNext(self.first)
        self.first.setPrevious(self.first)
        for e in contents:
            self.append(e)

    def append(self, item):
        lastNode = self.first.getPrevious()
        newNode = DLinkedList.__Node(item)
        newNode.setNext(self.first)
        newNode.setPrevious(lastNode)
        lastNode.setNext(newNode)
        self.first.setPrevious(newNode)
        self.numItems += 1

    def locate(self, index):
        if index >= 0 and index < self.numItems:
            cursor = self.first.getNext()
            for i in range(index):
                cursor = cursor.getNext()
            return cursor
        raise IndexError("DLinkedList index out of range")

    def splice(self, index, other, index1, index2):
        #this method also takes the index2 into account
        if index1 <= index2:
            begin = other.locate(index1)
            end = other.locate(index2)
            self.insertList(begin, end, index)

    def insertList(self, begin, end, index):
        address = self.locate(index)
        successor = address.getNext()
        begin.setPrevious(address)
        end.setNext(successor)
        address.setNext(begin)
        successor.setPrevious(end)  
    def show(self):
        temp = self.first.getNext()
        while temp != self.first:
            print(temp.getItem())
            temp = temp.getNext()
    def swap(self,obj1,obj2):
        prev_obj1 = obj1.getPrevious()
        next_obj2 = obj2.getNext()
        prev_obj1.setNext(obj2)
        obj2.setPrevious(prev_obj1)
        obj1.setNext(next_obj2)
        next_obj2.setPrevious(obj1) 
        obj2.setNext(obj1)
        obj1.setPrevious(obj2)
    def bubbleSort(self):
        #firstNode corresponds to index 0
        firstNode = self.first.getNext();
        #secondNode corresponds to index 1
        secondNode = firstNode.getNext()
        if firstNode == self.first or secondNode == self.first:
            return
        for i in range(self.numItems-1):
            num_swap = 0
            for j in range(self.numItems-i-1):
                if firstNode.getItem()>secondNode.getItem():
                    self.swap(firstNode,secondNode)
                    num_swap += 1
                    #increment the objects after being swapped
                    secondNode = firstNode.getNext()
                else:
                    #increment to objects as index increases
                    firstNode = firstNode.getNext()
                    secondNode = secondNode.getNext()
            if num_swap == 0:
                return
            firstNode = self.first.getNext();
            secondNode = firstNode.getNext()
        return
                    
                
        
        

if __name__ == "__main__":
    from Git import upload
    
    a = DLinkedList(['a', 'b', 'c', 'd', 'e'])
    b = DLinkedList(["A","B","C","D","E"])
    a.show()
    b.show()
    print("-------")
    a.splice(3, b, 2, 4)
    a.show()
    
    upload("dl")
