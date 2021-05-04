# -*- coding: utf-8 -*-

from PyList import PyList
import numpy as np

# ex.1
class Request:
    def __init__(self, arrive_date, depart_date):
        self.arrive = arrive_date
        self.depart = depart_date

class RoomBooking:
    class __Event:
        def __init__(self, time, arr_or_dep):
            self.time = time
            self.val = arr_or_dep

    def __init__(self, k):
        self.numRooms = k

    def book(self, content):
        new_list = self.rearrange(content)
        new_list.show()
        temp = 0
        for i in range(new_list.numItems):
            temp += new_list[i].val
            if temp >= self.numRooms:
                return False
        return True

    def rearrange(self, content):
        result = PyList()
        for i in content:
            result.append(self.__Event(i.arrive, 1))
            result.append(self.__Event(i.depart, -1))
        result.mergeSort()
        return result

def testEX1():
    service = RoomBooking(100)
    # generate testing lists
    test = []
    for i in range(1000):
        a = np.random.randint(1, 366)
        b = np.random.randint(1, 30)
        req = Request(a, a+b)
        test.append(req)
    print(service.book(test))

# ex.2
class StackError(Exception):
    def __init__(self, msg):
        self.info = msg
    pass

class Queue:
    class __Stack:
        def __init__(self, size=20):
            self.items = [None] * size
            self.size = size
            self.numItems = 0

        def top(self):
            if self.numItems == 0:
                raise StackError("stack is empty")
            return self.items[self.numItems - 1]

        def allocate(self):
            new_size = int(self.size * 2)
            new_items = [None] * new_size
            for i in range(self.numItems):
                new_items[i] = self.items[i]
            self.size = new_size
            self.items = new_items

        def deallocate(self):
            new_size = int(self.size / 2)
            new_items = [None] * new_size
            for i in range(self.numItems):
                new_items[i] = self.items[i]
            self.size = new_size
            self.items = new_items

        def empty(self):
            if self.numItems == 0:
                return True
            return False

        def push(self, item):
            if self.numItems == self.size:
                self.allocate()
            self.items[self.numItems] = item
            self.numItems += 1

        def pop(self):
            if self.numItems <= self.size / 4:
                self.deallocate()
            if self.numItems != 0:
                self.numItems -= 1
                item = self.items[self.numItems]
                return item
            raise StackError("stack is empty")

    def __init__(self, size=20):
        self.stack1 = self.__Stack(size)
        self.stack2 = self.__Stack(size)
        self.numItems = 0
        self.size = size

    def enqueue(self, item):
        self.stack1.push(item)
        self.numItems += 1

    def dequeue(self):
        if self.stack1.empty() and self.stack2.empty():
            raise StackError("empty queue")
        if self.stack2.empty():
            while not self.stack1.empty():
                temp = self.stack1.pop()
                self.stack2.push(temp)
            self.numItems -= 1
            return self.stack2.pop()
        else:
            self.numItems -= 1
            return self.stack2.pop()

def testEX2():
    queue = Queue(20)
    for i in range(100):
        queue.enqueue(i)
    for i in range(100):
        a = queue.dequeue()
        print(a)
    for i in range(40):
        queue.enqueue(i)
    for i in range(40):
        a = queue.dequeue()
        print(a)

def main():
    testEX2()

if __name__ == "__main__":
    main()
