# -*- coding: utf-8 -*-

#  DN<=>A<=>B<=>C<=>D<=> ...<=>Z<=>(back to Dummy Node)
# ↑
# first


class DLinkedList:
    class __Node:
        def __init__(self, item=None, next=None, previous=None):
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

    def __init__(self, contents=[]):
        self.first = DLinkedList.__Node(None, None, None)
        self.numItems = 0
        self.first.setNext(self.first)
        self.first.setPrevious(self.first)
        for e in contents:
            self.append(e)
    
    def __add__(self, other):
        result = DLinkedList()
        cursor = self.first.next
        while cursor != self.first:
            result.append(cursor.item)
            cursor = cursor.next
        cursor = other.first.next
        while cursor != other.first:
            result.append(cursor.item)
            cursor = cursor.next
        return result

    def printList(self):
        tmp = self.first.next
        nodes = []
        for i in range(self.numItems):
            nodes.append(str(tmp.item))
            tmp = tmp.next
        print("The DLinkedList has %d items" % self.numItems)
        print(' <-> '.join(nodes))

    def append(self, item):
        lastNode = self.first.getPrevious()
        newNode = DLinkedList.__Node(item, self.first, lastNode)
        lastNode.setNext(newNode)
        self.first.setPrevious(newNode)
        self.numItems += 1

    def locate(self, index):
        if index >= 0 and index < self.numItems:
            cursor = self.first.getNext()
            for _ in range(index):
                cursor = cursor.getNext()
            return cursor
        raise IndexError("DLinkedList index out of range")

    # modified in lab
    def splice_m(self, index, other, index1, index2, insert_en=True):
        if index1 <= index2:
            if insert_en:
                begin = other.locate(index1)
                end = other.locate(index2)
                self.insertList(begin, end, index)
                self.numItems += index2 - index1 + 1
            # If there is no insertion, then cut the self list by index1 and index2
            else:
                begin = self.locate(index1)
                end = self.locate(index2)
                self.first.setPrevious(end)
                self.first.setNext(begin)
                begin.setPrevious(self.first)
                end.setNext(self.first)
                self.numItems = index2 - index1 + 1

    # original design
    def splice(self, index, other, index1, index2):
        if index1 <= index2:
            begin = other.locate(index1)
            end = other.locate(index2)
            self.insertList(begin, end, index)
            self.numItems += index2 - index1 + 1

    def insertList(self, begin, end, index):
        address = self.locate(index)
        successor = address.getNext()
        begin.setPrevious(address)
        end.setNext(successor)
        address.setNext(begin)
        successor.setPrevious(end)

####################### bubbleSort ############################

    def bubbleSort(self):
        while True:
            is_swaped = 0
            ptr = self.first.getNext()
            while ptr != self.first:
                if ptr.getNext().item != None and ptr.item > ptr.getNext().item:
                    ptr.item, ptr.getNext().item = ptr.getNext().item, ptr.item
                    is_swaped += 1
                ptr = ptr.getNext()
            if is_swaped == 0:
                break

####################### selectioSort ############################

# sorting by swaping the items between nodes, not changing the nodes themselves

    def selectionSort_m(self):
        cursor1 = self.first.getNext()
        while cursor1.getNext() != self.first:
            minNode = cursor1
            cursor2 = cursor1.getNext()
            while cursor2 != self.first:
                if minNode.getItem() > cursor2.getItem():
                    minNode = cursor2
                cursor2 = cursor2.getNext()
            if cursor1 == minNode:
                cursor1 = cursor1.getNext()
            else:
                tmp = cursor1.getItem()
                cursor1.setItem(minNode.getItem())
                minNode.setItem(tmp)
                cursor1 = cursor1.getNext()

    # in-place
    # same as slides
    def selectionSort(self):
        firstNode = self.first.getNext()
        lastNode = self.first.getPrevious()
        self.first.setNext(self.first)
        self.first.setPrevious(self.first)
        counter = self.numItems
        outlast = self.first
        while counter != 0:
            location = self.getMinimum(firstNode, lastNode)
            if location == firstNode:
                firstNode = location.getNext()
            else:
                if location == lastNode:
                    lastNode = location.getPrevious()
                else:
                    self.cut(firstNode, lastNode, location)
            self.addLocation(outlast, location)
            outlast = location
            counter -= 1

    # getMinimum() determines the node with the minimum item
    def getMinimum(self, first, last):
        minimum = first.getItem()
        cursor = first
        location = first
        while cursor != last:
            cursor = cursor.getNext()
            item = cursor.getItem()
            if item < minimum:
                minimum = item
                location = cursor
        return location

    #cut() deletes the node with the minimum item from the inlist:
    #location is actually the min node that you found
    def cut(self, first, last, location):
        prev = location.getPrevious()
        next = location.getNext()
        prev.setNext(next)
        next.setPrevious(prev)

    # addLocation() adds the node with the minimum item to the outlist
    def addLocation(self, outlast, location):
        location.setPrevious(outlast)
        location.setNext(self.first)
        outlast.setNext(location)
        self.first.setPrevious(location)

####################### insertionSort ############################

    def insertionSort(self):
        cursor = self.first.getNext()
        self.first.setNext(self.first)
        self.first.setPrevious(self.first)
        while cursor != self.first:
            # keep a record of the next cursor position
            cursor1 = cursor.getNext()
            self.addout(cursor)
            cursor = cursor1

    def addout(self, cursor):
        cursor2 = self.first.getNext()
        while cursor2 != self.first and cursor2.getItem() < cursor.getItem() and cursor2.getNext() != self.first:
            cursor2 = cursor2.getNext()
        # insert before cursor2
        if cursor2 != self.first and cursor2.getItem() >= cursor.getItem():
            previous = cursor2.getPrevious()
            previous.setNext(cursor)
            cursor.setNext(cursor2)
            cursor.setPrevious(previous)
            cursor2.setPrevious(cursor)
        # insert at the end of the output
        else:
            cursor2.setNext(cursor)
            cursor.setNext(self.first)
            cursor.setPrevious(cursor2)
            self.first.setPrevious(cursor)
    
####################### mergeSort ############################

# bugs in slide code, slightly modified

    def mergeSort(self, threshold = 2):
        if self.numItems <= threshold:
            self.insertionSort()
        else:
            secondList = self.split()
            self.mergeSort(threshold)
            secondList.mergeSort(threshold)
            self.merge(secondList)

    def split(self):
        index = self.numItems // 2
        cursor = self.locate(index)
        secondList = DLinkedList([])
        lastNode1, lastNode2 = cursor.getPrevious(), self.first.getPrevious()
        self.first.setPrevious(lastNode1)
        lastNode1.setNext(self.first)
        secondList.first.setNext(cursor)
        cursor.setPrevious(secondList.first)
        lastNode2.setNext(secondList.first)
        secondList.first.setPrevious(lastNode2)
        secondList.numItems = self.numItems - index
        self.numItems = index
        return secondList

    def merge(self, other):
        firstNode, secondNode = self.first.getNext(), other.first.getNext()
        self.numItems = self.numItems + other.numItems
        current = self.first
        count = 1
        while count <= self.numItems:
            if firstNode.getItem() != None and secondNode.getItem() != None:
                if firstNode.getItem() <= secondNode.getItem():
                    current.setNext(firstNode)
                    firstNode.setPrevious(current)
                    firstNode = firstNode.getNext()
                else:
                    current.setNext(secondNode)
                    secondNode.setPrevious(current)
                    secondNode = secondNode.getNext()
            else:
                if firstNode.getItem() == None:
                    current.setNext(secondNode)
                    secondNode.setPrevious(current)
                    secondNode = secondNode.getNext()
                else:
                    current.setNext(firstNode)
                    firstNode.setPrevious(current)
                    firstNode = firstNode.getNext()
            count += 1
            current = current.getNext()
    
    ############### another version of merge sort contributed by zzb
    def helper_split(self):
        index = self.numItems//2
        cursor = self.locate(index)
        lastNode1 = cursor.getPrevious()
        lastNode2 = self.first.getPrevious()
        self.first.setPrevious(lastNode1)
        lastNode1.setNext(self.first)
        secondList = DLinkedList([])
        secondList.first.setNext(cursor)
        cursor.setPrevious(secondList.first)
        lastNode2.setNext(secondList.first)
        secondList.first.setPrevious(lastNode2)
        temp = self.numItems
        self.numItems = index
        secondList.numItems = temp - index
        return secondList

    def MergeSort(self):
        if self.numItems <= 4:
            self.bubbleSort()
        else:
            secondList = self.helper_split()
            self.MergeSort()
            secondList.MergeSort()
            self.Merge(secondList)
            del secondList
        return

    def Merge(self, secondList):
        total_length = self.numItems + secondList.numItems
        firstNode = self.first.getNext()
        secondNode = secondList.first.getNext()
        dummyNode = self.__Node()
        head = dummyNode
        while firstNode != self.first and secondNode != secondList.first:
            if firstNode.getItem() < secondNode.getItem():
                dummyNode.setNext(firstNode)
                firstNode.setPrevious(dummyNode)
                firstNode = firstNode.getNext()
            else:
                dummyNode.setNext(secondNode)
                secondNode.setPrevious(dummyNode)
                secondNode = secondNode.getNext()
            dummyNode = dummyNode.getNext()
        if firstNode == self.first:
            dummyNode.setNext(secondNode)
            secondNode.setPrevious(dummyNode)
            while secondNode != secondList.first:
                secondNode = secondNode.getNext()
            secondNode.getPrevious().setNext(self.first)
            self.first.setPrevious(secondNode.getPrevious())
        elif secondNode == secondList.first:
            dummyNode.setNext(firstNode)
            firstNode.setPrevious(dummyNode)
        self.first.setNext(head.getNext())
        head.getNext().setPrevious(self.first)
        del head
        self.numItems = total_length
        
    def qsort(self):
        if self.numItems <= 1:
            return self
        pivot = self.first.next.item
        list1 = DLinkedList()
        listp = DLinkedList()
        list2 = DLinkedList()
        current = self.first.next
        while current != self.first:
            if current.item < pivot:
                list1.append(current.item)
            else:
                if current.item == pivot:
                    listp.append(current.item)
                else:
                    list2.append(current.item)
            current = current.next
        slist1 = list1.qsort()
        slist2 = list2.qsort()
        return slist1 + listp + slist2
    
    def radixSort(self, numdigits, digits):
        sortedlist = self
        for i in range(numdigits):
            sortedlist = sortedlist.Ksort(i, digits)
        return sortedlist

    def Ksort(self, round, digits):
        bucket = [None] * digits
        for i in range(digits):
            bucket[i] = DLinkedList()
        cursor = self.first.next
        while cursor != self.first:
            item = cursor.item
            item1 = item // (digits ** round) % digits
            bucket[item1].append(item)
            cursor = cursor.next
        result = bucket[0]
        for k in range(digits-1):
            result = result + bucket[k+1]
        return result