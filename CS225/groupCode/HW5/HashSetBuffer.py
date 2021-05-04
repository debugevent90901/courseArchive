# this is for homework exercise 1 (ii)

class HashSet:
    class __Placeholder:
        def __init__(self):
            pass

        def __eq__(self, other):
            return False

    def __init__(self, contents=[]):
        self.size = 6
        self.buffer_size = int(self.size * 0.5)
        self.items = [None] * (self.size + self.buffer_size)
        self.numItems = 0
        for e in contents:
            self.add(e)

    def add(self, item):
        if HashSet.__add(item, self.items, self.size, self.buffer_size):
            self.numItems += 1
            load = self.numItems / len(self.items)
            if load >= 0.75:
                self.size *= 2
                self.buffer_size = int(self.size * 0.5)
                newitems = [None] * (self.size + self.buffer_size)
                self.items = HashSet.__rehash(self.items, newitems, self.size, self.buffer_size)

    @staticmethod
    def __add(item, items, size, buffer_size):
        index = hash(item) % size
        location = -1
        while items[index] is not None:
            if items[index] == item:
                return False
            if location < 0 and type(items[index]) == HashSet.__Placeholder:
                location = index
                break
            index = (index + 1) % (size + buffer_size)
        if location < 0:
            location = index
        items[location] = item
        return True

    @staticmethod
    def __rehash(olditems, newitems, size, buffer_size):
        for e in olditems:
            if e is not None and type(e) != HashSet.__Placeholder:
                HashSet.__add(e, newitems, size, buffer_size)
        return newitems

    def __contains__(self, item):
        index = hash(item) % self.size
        while self.items[index] is not None:
            if self.items[index] == item:
                return True
            index = (index + 1) % len(self.items)
        return False

    def delete(self, item):
        if HashSet.__remove(item, self.items, self.size, self.buffer_size):
            self.numItems -= 1
            load = max(self.numItems, 20) / len(self.items)
            if load <= 0.25:
                self.size = self.size // 2
                self.buffer_size = int(0.5 * self.size)
                newitems = [None] * (self.size + self.buffer_size)
                self.items = HashSet.__rehash(self.items, newitems, self.size, self.buffer_size)
        else:
            raise KeyError("Item not in HashSet")

    @staticmethod
    def __remove(item, items, size, buffer_size):
        index = hash(item) % size
        while items[index] is not None:
            if items[index] == item:
                nextIndex = (index + 1) % len(items)
                if items[nextIndex] is None:
                    items[index] = None
                else:
                    items[index] = HashSet.__Placeholder()
                return True
            index = (index + 1) % (size + buffer_size)
        return False

    def show(self):
        print("the size of the list is: ", self.size)
        print("the size of the buffer is: ", self.buffer_size)
        for item in self.items:
            if item is not None and type(item) != self.__Placeholder:
                print(item)
        print("then show the items stored in the buffer region again")
        for i in range(self.size, self.buffer_size + self.size):
            if self.items[i] is not None and type(self.items[i]) != HashSet.__Placeholder:
                print(self.items[i])


content = [5,4,10,11,17,16]
print(content)
hashset = HashSet(content)
hashset.show()