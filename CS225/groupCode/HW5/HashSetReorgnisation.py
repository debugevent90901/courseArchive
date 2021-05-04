# this is for homework exercise 1 (i)

class HashSet:
    def __init__(self, contents=[]):
        self.items = [None] * 20
        self.numItems = 0
        for e in contents:
            self.add(e)

    def add(self, item):
        if HashSet.__add(item, self.items):
            self.numItems += 1
            load = self.numItems / len(self.items)
            if load >= 0.75:
                self.items = HashSet.__rehash(self.items, [None] * 2 * len(self.items))

    @staticmethod
    def __add(item, items):
        index = hash(item) % len(items)
        location = -1
        while items[index] is not None:
            if items[index] == item:
                return False
            index = (index + 1) % len(items)
        if location < 0:
            location = index
        items[location] = item

    @staticmethod
    def __rehash(olditems, newitems):
        for e in olditems:
            if e is not None:
                HashSet.__add(e, newitems)
        return newitems

    def __contains__(self, item):
        index = hash(item) % len(self.items)
        while self.items[index] is not None:
            if self.items[index] == item:
                return True
            index = (index + 1) % len(self.items)
        return False

    def find(self, item):
        index = hash(item) % len(self.items)
        while self.items[index] is not None:
            if self.items[index] == item:
                return index
            index = (index + 1) % len(self.items)
        return None

    def delete(self, item):
        if self.find(item) is not None:
            location = self.find(item)
            self.items[location] = None
            index = location + 1
            while True:
                if self.items[index] is None or index == len(self.items)-1:
                    break
                else:
                    if hash(self.items[index]) % len(self.items) <= location:
                        self.items[location] = self.items[index]
                        self.items[index] = None
                        location = index
                index = index + 1
        else:
            raise KeyError("Item not in HashSet")


a = HashSet([3, 1, 21, 23, 43, 6, 41, 26, 9, 10])
print(a.items)
a.delete(21)
a.delete(41)
a.delete(3)
a.delete(26)
a.delete(10)
a.delete(1)
a.delete(9)
print(a.items)