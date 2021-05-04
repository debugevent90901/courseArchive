# This is the exercise 1 of the
import math
import numpy as np
import matplotlib.pyplot as plt

class RelationSet:
    class __Node:
        def __init__(self, element, next_node=None):
            self.val = element
            self.next = next_node

    def __init__(self, contents=[]):
        # the input should be a list of tuples which represent relations
        self.length = 5  # the length of one square matrix
        self.items = [None] * self.length ** 2
        self.numItems = 0
        for e in contents:
            self.add(e)

    @staticmethod
    def __add(item, items, length):
        index = RelationSet.myhash(item, length)
        if items[index] is None:
            items[index] = RelationSet.__Node(item)
        else:
            temp = items[index]
            if temp.val == item:
                return False
            while temp.next is not None:
                temp = temp.next
                if temp.val == item:
                    return False
            # now the temp points to the last element
            temp.next = RelationSet.__Node(item)
        return True

    @staticmethod
    def __rehash(olditems, newitems, length):
        for e in olditems:
            temp = e
            while temp is not None:
                RelationSet.__add(temp.val, newitems, length)
                temp = temp.next
            # if the temp is None, then go to the next entry
        return newitems

    @staticmethod
    def __remove(item, items, length):
        index = RelationSet.myhash(item, length)
        temp = items[index]
        if temp is None:
            return False
        elif temp.val == item:
            items[index] = temp.next
            return True
        while temp.next is not None:
            if temp.next.val == item:
                temp.next = temp.next.next
                return True
            temp = temp.next
        return False

    @staticmethod
    def myhash(item, length):
        # the core of the algorithm: use an 1D array to simulate 2D matrix
        a = abs(hash(item[0]) % length)
        b = abs(hash(item[1]) % length)
        index = a * length + b
        return index

    def __contains__(self, item):
        index = RelationSet.myhash(item, self.length)
        temp = self.items[index]
        while temp is not None:
            if temp.val == item:
                return True
            temp = temp.next
        return False

    def add(self, item):
        if RelationSet.__add(item, self.items, self.length):
            self.numItems += 1
            load = self.numItems / len(self.items)
            if load >= 3:
                new_length = math.ceil(self.length * 2 ** 0.5)
                self.length = new_length
                new_list = [None] * new_length ** 2
                self.items = RelationSet.__rehash(self.items, new_list, self.length)

    def delete(self, item):
        if RelationSet.__remove(item, self.items, self.length):
            self.numItems -= 1
            load = max(self.numItems, 25) / len(self.items)
            if load <= 0.25:
                new_length = math.ceil(self.length * 2 ** 0.5 / 2)
                self.length = new_length
                new_list = [None] * new_length ** 2
                self.items = RelationSet.__rehash(self.items, new_list, self.length)
        else:
            raise KeyError("Item not in HashSet")

    def symmetric(self):
        # we only need to check matrix's symmetry
        flag = 1
        for i in self.items:
            if i is None:
                continue
            else:
                temp = i
                while temp is not None:
                    if not ((temp.val[1], temp.val[0]) in self):
                        # switch the position to check relation (b,a)
                        flag = 0
                        print("the problem is: ", temp.val)
                    temp = temp.next
        if flag == 1:
            return True
        else:
            return False

    def show(self):
        print("the number of items is %d" % self.numItems)
        counter = 0
        for i in self.items:
            temp = i
            while temp is not None:
                print("line ", counter, ": ", temp.val)
                counter += 1
                temp = temp.next

    def performance(self):
        result = []
        for i in self.items:
            counter = 0
            temp = i
            while temp is not None:
                counter += 1
                temp = temp.next
            if counter != 0:
                result.append(counter)
        return result


content = []
for i in range(10000):
    val1 = np.random.randint(-100000, 100000)
    val2 = np.random.randint(-100000, 100000)
    content.append((val1, val2))
    content.append((val2, val1))
test = RelationSet(content)
#test.show()
print(test.symmetric())
test.add((10001, 10002))
print(test.symmetric())
test.add((10002, 10001))
print(test.symmetric())
test.delete((10002, 10001))
print(test.symmetric())
print(len(test.items))
print(test.length)
chain_length = test.performance()
print("the non-zero chains: ", len(chain_length))
x = list(range(len(chain_length)))
avg = sum(chain_length)/len(chain_length)
print("the average length is %f" % avg)
plt.plot(x, chain_length)
plt.show()