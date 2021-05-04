# this is the exercise 2 of HW3

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
