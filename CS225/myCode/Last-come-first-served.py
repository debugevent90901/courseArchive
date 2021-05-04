# -*- coding: utf-8 -*-

# only __add method changed
# any other thing remain the same as hashset.py
# 其他所以和slides上不一样的都以slides为准

class HashSet:

    class __Placeholder:
        def __init__(self):
            pass

        def __eq__(self, other):
            return False

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
        flag = -1
        while items[index] is not None:
            if items[index] == item:
                # check if the input value is repeated
                return False
            if location < 0 and type(items[index]) == HashSet.__Placeholder:
                # check if we find a free block
                location = index
                # 这个break应该挺好的
                break
            if flag < 0:
                # swap the items
                flag = 1
                temp = items[index]
                items[index] = item
                item = temp
            index = (index + 1) % len(items)
        if location < 0:
            location = index
        items[location] = item
        return True

    @staticmethod
    def __rehash(olditems, newitems):
        for e in olditems:
            if e is not None and type(e) != HashSet.__Placeholder:
                HashSet.__add(e, newitems)
        return newitems

    def __contains__(self, item):
        index = hash(item) % len(self.items)
        while self.items[index] is not None:
            if type(self.items[index]) != HashSet.__Placeholder:
                if self.items[index] == item:
                    return True
            index = (index + 1) % len(self.items)
        return False

    def delete(self, item):
        if HashSet.__remove(item, self.items):
            self.numItems -= 1
            load = max(self.numItems, 20) / len(self.items)
            if load <= 0.25:
                self.items = HashSet.__rehash(self.items, [None] * (len(self.items) // 2))
        else:
            raise KeyError("Item not in HashSet")

    @staticmethod
    def __remove(item, items):
        index = hash(item) % len(items)
        while items[index] is not None:
            if type(items[index]) != HashSet.__Placeholder:
                if items[index] == item:
                    nextIndex = (index + 1) % len(items)
                    if items[nextIndex] is None:
                        items[index] = None
                    else:
                        items[index] = HashSet.__Placeholder()
                    return True
            index = (index + 1) % len(items)
        return False

    def show(self):
        for item in self.items:
            if item is not None and type(item) != self.__Placeholder:
                print(item, end=" ")

# test
'''
content = [21,41,1,61,81,201,101]
test = HashSet(content)
test.show()
test.delete(101)
print("\n")
test.show()
'''