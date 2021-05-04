# -*- coding: utf-8 -*-

class PyList(list):
    def __init__(self, contents=[], size=20):
        self.items = [None] * size
        self.numItems = 0
        self.size = size
        for e in contents:
            self.append(e)

    def __contains__(self, item):
        for i in range(self.numItems):
            if self.items[i] == item:
                return True
        return False

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        if self.numItems != other.numItems:
            return False
        for i in range(self.numItems):
            if self.items[i] != other.items[i]:
                return False
        return True

    def __setitem__(self, index, val):
        if index >= 0 and index < self.numItems:
            self.items[index] = val
            return
        raise IndexError("PyList assignment index out of range")

    def __getitem__(self, index):
        if index >= 0 and index < self.numItems:
            return self.items[index]
        raise IndexError("PyList index out of range")

    def __add__(self, other):
        result = PyList(size=self.numItems + other.numItems)
        for i in range(self.numItems):
            result.append(self.items[i])
        for i in range(other.numItems):
            result.append(other.items[i])
        return result

    def append(self, item):
        if self.numItems == self.size:
            self.allocate()
        self.items[self.numItems] = item
        self.numItems += 1

    def insert(self, i, x):
        if self.numItems == self.size:
            self.allocate()
        if i < self.numItems:
            for j in range(self.numItems - 1, i, -1):
                self.items[j + 1] = self.items[j]
            self.items[i] = x
            self.numItems += 1
        else:
            self.append(x)

    def delete(self, index):
        if self.numItems <= self.size / 4:
            self.deallocate()
        if index <= self.numItems:
            for j in range(index, self.numItems - 1):
                self.items[j] = self.items[j + 1]
            self.numItems -= 1
            self.items[self.numItems] = None
        else:
            raise IndexError("PyList index out of range")

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

    def printList(self):
        print("The list has size %d and %d items" % (self.size, self.numItems))
        print(self.items)

    def selectionSort(self):
        for i in range(self.numItems - 1):
            minIndex = i
            for j in range(i + 1, self.numItems):
                if self.items[minIndex] > self.items[j]:
                    minIndex = j
            if i == minIndex:
                continue
            else:
                self.items[i], self.items[minIndex] = self.items[minIndex], self.items[i]

    def bubbleSort1(self):
        for i in range(self.numItems - 1):
            for j in range(self.numItems - 1 - i):
                if self.items[j] > self.items[j+1]:
                    self.items[j], self.items[j+1] = self.items[j+1], self.items[j]

    # another bubbleSort
    def bubbleSort2(self):
        while True:
            is_swaped = 0
            for i in range(self.numItems):
                if self.items[i+1] != None and self.items[i] > self.items[i+1]:
                    self.items[i], self.items[i+1] = self.items[i+1], self.items[i]
                    is_swaped += 1
            if is_swaped == 0:
                break

    # with binary search
    def insertionSort_b(self):
        for i in range(1, self.numItems):
            left, right = 0, i - 1
            tmp = self.items[i]
            while left <= right:
                mid = left + (right - left) // 2
                if self.items[mid] > tmp:
                    right = mid - 1
                else:
                    left = mid + 1
            for j in range(i - 1, left - 1, -1):
                self.items[j + 1] = self.items[j]
            self.items[left] = tmp

    # without binary search
    def insertionSort1(self):
        for i in range(self.numItems):
            key = self.items[i]
            j = i - 1
            while j >= 0 and key < self.items[j]:
                self.items[j+1] = self.items[j]
                j -= 1
            self.items[j+1] = key

    # another version
    def insertionSort2(self):
        n = self.numItems
        if n == 1:
            return self
        for i in range(1, n):
            for j in range(i, 0, -1):
                if self.items[j] < self.items[j-1]:
                    self.items[j], self.items[j-1] = self.items[j-1], self.items[j]
                else:
                    break

    def mergeSort(self, front=0, end=None, is_thr=True, parameter=10, method=insertionSort_b):
        if end == None:
            end = self.numItems - 1
        if is_thr == True and ((end - front + 1) <= parameter):
            method(self)
        else:
            mid = front + (end - front) / 2
            self.mergeSort(front, mid)
            self.mergeSort(mid + 1, end)
            self.merge(front, mid, end)

    def merge(self, front, mid, end):
        LeftSubArray = PyList(self.items[front:mid + 1])
        RightSubArray = PyList(self.items[mid + 1:end + 1])
        idxLeft, idxRight = 0, 0
        LeftSubArray.append('inf')
        RightSubArray.append('inf')
        for i in range(front, end + 1):
            if LeftSubArray[idxLeft] < RightSubArray[idxRight]:
                self.items[i] = LeftSubArray[idxLeft]
                idxLeft += 1
            else:
                self.items[i] = RightSubArray[idxRight]
                idxRight += 1

    def qSort(self):
        if self.numItems <= 1:
            return self
        pivot = self.items[0]
        print(pivot)
        list1 = PyList([], self.numItems)
        listp = PyList([], self.numItems)
        list2 = PyList([], self.numItems)
        for i in range(self.numItems):
            if self.items[i] < pivot:
                list1.append(self.items[i])
            else:
                if self.items[i] == pivot:
                    listp.append(self.items[i])
                else:
                    list2.append(self.items[i])
        slist1 = list1.qSort()
        slist2 = list2.qSort()
        return slist1 + listp + slist2

    def quickSort(self, first=0, last=None):
        if last == None:
            last = self.numItems - 1
        if first >= last:
            return
        pivit = self.items[first]
        low, high = first, last
        while low < high:
            while low < high and self.items[high] >= pivit:
                high -= 1
            self.items[low] = self.items[high]
            while low < high and self.items[low] < pivit:
                low += 1
            self.items[high] = self.items[low]
        self.items[low] = pivit
        self.quickSort(first, low - 1)
        self.quickSort(low + 1, last)

    def radixSort(self, numdigits=8, digits=10):
        sortedlist = self
        for i in range(numdigits):
            print("%d digit" % i)
            sortedlist = sortedlist.Ksort(i, digits)
        return sortedlist

    def Ksort(self, round, digits):
        bucket = PyList([])
        for k in range(digits):
            newlist = PyList([], self.numItems)
            bucket.append(newlist)
        for i in range(self.numItems):
            item = self.items[i]
            item1 = item // (digits**round) % digits
            print("%d is placed at position %d" % (item, item1))
            bucket[item1].append(item)
        result = bucket[0]
        for k in range(digits - 1):
            result = result + bucket[k + 1]
        return result

class PyList_NonList:
    def __init__(self, contents=[], size=20):
        self.items = [None] * size
        self.numItems = 0
        self.size = size
        for e in contents:
            self.append(e)

    def __setitem__(self, index, val):
        if index >= 0 and index < self.numItems:
            self.items[index] = val
            return
        raise IndexError("PyList assignment index out of range")

    def __getitem__(self, index):
        if index >= 0 and index < self.numItems:
            return self.items[index]
        raise IndexError("PyList index out of range")

    def append(self, item):
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

    def insert(self, i, x):
        if self.numItems == self.size:
            self.allocate()
        if i < self.numItems:
            for j in range(self.numItems - 1, i, -1):
                self.items[j + 1] = self.items[j]
            self.items[i] = x
            self.numItems += 1
        else:
            self.append(x)

    def __add__(self, other):
        result = PyList(size=self.numItems + other.numItems)
        for i in range(self.numItems):
            result.append(self.items[i])
        for i in range(other.numItems):
            result.append(other.items[i])
        return result

    def delete(self, index):
        if self.numItems == self.size / 4:
            self.deallocate()
        if index <= self.numItems:
            for j in range(index, self.numItems - 2):
                self.items[j] = self.items[j + 1]
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

    def __contains__(self, item):
        for i in range(self.numItems):
            if self.items[i] == item:
                return True
            return False

    def __eq__(self, other):
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
        list1 = PyList([], self.numItems)
        listp = PyList([], self.numItems)
        list2 = PyList([], self.numItems)
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

    def radixSort(self, numdigits, digits):
        sortedlist = self
        for i in range(numdigits):
            sortedlist = sortedlist.Ksort(i, digits)
        return sortedlist

    def Ksort(self, round, digits):
        bucket = PyList([], digits)
        for k in range(digits):
            newlist = PyList([], self.numItems)
            bucket.append(newlist)
        for i in range(self.numItems):
            item = self.items[i]
            item1 = item // (digits ** round) % digits
            bucket[item1].append(item)
        result = bucket[0]
        for k in range(digits - 1):
            result = result + bucket[k + 1]
        return result
