# -*- coding: utf-8 -*-
#pylist module
'''
This is HW2 for CS225

Team Member:
    Zhu Zhongbo
    Yang Zhaohua
    Guan Zimu
    Xie Tian
'''
class PyList(list):
    def __init__(self, content=[], size=20):
        super().__init__()
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
        print("the index is %d"%index)
        print("the limit is %d"%self.numItems)
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

    def show(self):
        for i in range(self.numItems):
            print(self.items[i])

    # define selection sort
    def findMin(self):
        ans = 0
        for i in range(self.numItems):
            if self.items[i]<self.items[ans]:
                ans = i
        return ans

    def selectionSort(self):
        num = self.numItems
        result = []
        while num != 0:
            min_index = self.findMin()
            result.append(self.items[min_index])
            self.delete(min_index)
            num -= 1
        assert(self.numItems == 0)
        for i in result:
            self.append(i)
        return

    # define bubble sort
    def swap(self,index1,index2):
        self.items[index2],self.items[index1] = self.items[index1],self.items[index2]
    def bubbleSort(self):
        #whole loop
        for i in range(self.numItems-1):
            num_swap = 0
            #one pass 
            for j in range(self.numItems-i-1):
                if self.items[j] > self.items[j+1]:
                    self.swap(j,j+1)
                    num_swap += 1
            #one pass but nothing changes
            if num_swap == 0:
                return 
        return

    # define merge_add(self):
    def merge_add(self,left,mid,right):
        i=left
        j=mid+1
        k=0
        temp = PyList(self.items[left:right+1],len(self.items[left:right+1]))
        while i <= mid and j<= right:
            if self.items[i]<self.items[j]:
                temp.items[k] = self.items[i]
                i=i+1
            else:
                temp.items[k] = self.items[j]
                j=j+1
            k=k+1
        while i<=mid:
            temp.items[k] = self.items[i]
            i=i+1
            k=k+1
        while j<=right:
            temp.items[k] = self.items[j]
            j=j+1
            k=k+1
        for i in range(temp.numItems):
            self.items[left+i] = temp.items[i]
        del temp

    # def mergeSort(self):
    def mergeSort(self,left = 0,right = None):
        if right == None:
            right = self.numItems - 1
        if (left<right):
            mid = left+(right-left)//2
            self.mergeSort(left,mid)
            self.mergeSort(mid+1,right)
            self.merge_add(left,mid,right)

    # define the improved insertion sort
    def binarySearch(self,value,start,end):
        mid = (start+end)//2
        if self[mid] == value:
            assert(type(start) == int)
            return mid
        if start == end:
            #then value is a little smaller than self[start]
            assert(type(start) == int)
            return start
        elif self[mid]<value:
            #go to right half
            return self.binarySearch(value,mid+1,end)
        elif self[mid]>value:
            #go to the left half
            return self.binarySearch(value,start,mid)

    def move_elements(self,value,index,cur_index):
        for i in range(cur_index,index,-1):
            self[i] = self[i-1]
        self[index] = value

    def insertionSort(self):
        for i in range(1,self.numItems):
            #this will loop from the start to the beginning
            value = self[i]
            if value>=self[i-1]:
                continue
            else:
                index = self.binarySearch(value,0,i-1)
                self.move_elements(value,index,i)

    # def mergeSortTHR(self):
    def mergeSortTHR(self,left = 0,right = None,thr = 10):
        if right == None:
            right = self.numItems-1
        #add one threshold
        if (right-left+1)<thr:
            self.mergeSortBubble(left,right)
        else:
            mid = left+(right-left)//2
            self.mergeSortTHR(left,mid,thr)
            self.mergeSortTHR(mid+1,right,thr)
            self.merge_add(left,mid,right)
    def mergeSortBubble(self,left,right):
        #whole loop
        numItems = right-left+1
        for i in range(numItems-1):
            num_swap = 0
            #one pass 
            for j in range(left,left+numItems-i-1):
                if self.items[j] > self.items[j+1]:
                    self.swap(j,j+1)
                    num_swap += 1
            #one pass but nothing changes
            if num_swap == 0:
                return 
        return

    

