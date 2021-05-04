# multiset using explicit storage of multiplicities
class MultiSet1:
    class __Placeholder:
        def __init__(self):
            pass

        def __eq__(self, other):
            return False

    def __init__(self, contents=[]):
        self.items = [None] * 20
        self.numItems = 0
        self.numTuples = 0
        for e in contents:
            self.add(e)

    # Insertion operation
    def add(self, item):
        self.__add(item)
        self.numItems += 1
        # rehash according to the number of different element
        # because same element are represented by a tuple
        load = self.numTuples / len(self.items)
        if load >= 0.75:
            self.__rehash(0)

    def __add(self, item):
        index = hash(item) % len(self.items)
        location = -1
        while self.items[index] is not None:
            if location < 0 and type(self.items[index]) == MultiSet1.__Placeholder:
                location = index
                break
            if self.items[index][0] == item:
                self.items[index][1] += 1
                return True
            index = (index + 1) % len(self.items)
        if location < 0:
            location = index
        self.items[location] = [item, 1]
        self.numTuples += 1
        return True

    # Add tuple contains element and multiplicity into the set
    # Input: tuple contains element
    def addtuple(self, tup):
        self.__addtuple(tup)
        self.numItems += tup[1]
        load = self.numTuples / len(self.items)
        if load >= 0.75:
            self.__rehash(0)

    def __addtuple(self, tup):
        item = tup[0]
        index = hash(item) % len(self.items)
        location = -1
        while self.items[index] is not None:
            if location < 0 and type(self.items[index]) == MultiSet1.__Placeholder:
                location = index
                break
            if self.items[index][0] == item:
                self.items[index][1] += tup[1]
                return True
            index = (index + 1) % len(self.items)
        if location < 0:
            location = index
        self.items[location] = tup
        self.numTuples += 1
        return True

    # mode 0: extend
    # mode 1: shrink
    def __rehash(self, mode):
        olditems = self.items
        if mode == 0:
            self.items = [None] * 2 * len(olditems)
        else:
            self.items = [None] * (len(olditems) // 2)
        for e in olditems:
            if e is not None and type(e) != MultiSet1.__Placeholder:
                self.__addtuple(e)

    # Retrival operation 
    # return True if item is in the set
    # return False if not
    def __contains__(self, item):
        index = hash(item) % len(self.items)
        while self.items[index] is not None:
            if type(self.items[index]) != MultiSet1.__Placeholder and self.items[index][0] == item:
                return True
            index = (index + 1) % len(self.items)
        return False

    # another version of Retrival
    # return the index of the corresponding item
    # return None if not found
    def search(self, item):
        index = hash(item) % len(self.items)
        while self.items[index] is not None:
            if type(self.items[index]) != MultiSet1.__Placeholder and self.items[index][0] == item:
                return index
            index = (index + 1) % len(self.items)
        return None

    # Deletion operation
    def delete(self, item):
        if self.__remove(item):
            self.numItems -= 1
            load = max(self.numItems, 20) / len(self.items)
            if load <= 0.25:
                self.__rehash(1)
        else:
            raise KeyError("Item not in MultiSet1")

    def __remove(self, item):
        index = hash(item) % len(self.items)
        while self.items[index] is not None:
            if type(self.items[index]) != MultiSet1.__Placeholder and self.items[index][0] == item:
                if self.items[index][1] <= 1:
                    nextIndex = (index + 1) % len(self.items)
                    if self.items[nextIndex] is None:
                        self.items[index] = None
                    else:
                        self.items[index] = MultiSet1.__Placeholder()
                else:
                    self.items[index][1] -= 1
                return True
            index = (index + 1) % len(self.items)
        return False

    # Union
    def union(self, other):
        for item in other.items:
            if item is not None and type(item) != self.__Placeholder:
                self.addtuple(item)

    # Intersection
    # take the min of the multiplicity of item in 2 sets
    def intersection(self, other):
        for i in range(len(self.items)):
            e = self.items[i]
            if e is not None and type(e) != self.__Placeholder:
                index = other.search(e[0])
                self.numItems -= e[1]
                if index != None:
                    e[1] = min(e[1], other.items[index][1])
                    self.numItems += e[1]
                else:
                    self.items[i] = MultiSet1.__Placeholder()
                    self.numTuples -= 1
                load = self.numTuples / len(self.items)
                if load >= 0.75:
                    self.__rehash(0)

    # Difference
    # minus the multiplicity of the same item in another sets
    def difference(self, other):
        for i in range(len(self.items)):
            e = self.items[i]
            if e is not None and type(e) != self.__Placeholder:
                index = other.search(e[0])
                if index == None:
                    continue
                num = e[1] - other.items[index][1]
                if num >= 1:
                    self.numItems -= e[1] - num
                    e[1] = num
                else:
                    self.numItems -= e[1]
                    self.items[i] = MultiSet1.__Placeholder()
                    self.numTuples -= 1
                    load = self.numTuples / len(self.items)
                    if load >= 0.75:
                        self.__rehash(0)

    def show(self):
        for item in self.items:
            if item is not None and type(item) != self.__Placeholder:
                print(item, end=" ")
        print("\n")

# a special single Linkedlist used to implement hashing with chaining
# when adding, put the same item together
class LinkedList:
    class __Node:
        def __init__(self, item, next = None):
            self.item = item
            self.next = next

    def __init__(self, contents = []):
        self.head = None
        for e in contents:
            self.append(e)

    def __contains__(self, item):
        curr = self.__Node(None, next = self.head)
        next = self.head
        while None != next:
            curr = curr.next
            next = next.next
            if curr.item == item:
                return True
        return False

    # put the same item together when adding
    def append(self, item):
        if None == self.head:
            self.head = self.__Node(item)
            return self.head
        curr = self.head
        next = self.head.next
        flag = 0
        while None != next:
            if curr.item == item:
                flag = 1
            if flag == 1 and next.item != item:
                break
            curr = curr.next
            next = next.next
        curr.next = self.__Node(item, next)
        return curr.next

    # delete the first node with the corresponding item
    # return the previous node of the deleted node
    # return None if not found
    def delete(self, item):
        if None == self.head:
            return None
        curr = self.head
        next = self.head.next
        if curr.item == item:
            self.head = next
        while None != next:
            if next.item == item:
                curr.next = next.next
                return curr
            curr = curr.next
            next = next.next
        return None

    # search the first node with the corresponding item
    # then return the node
    # return None if not found
    def search(self, item):
        curr = self.__Node(None, next = self.head)
        next = self.head
        while None != next:
            curr = curr.next
            next = next.next
            if curr.item == item:
                return curr
        return None

    # count the number of the item in the list
    # return the number
    def count(self, item):
        curr = self.search(item)
        if None == curr:
            return 0
        num = 0
        while None != curr and curr.item == item:
            num += 1
            curr = curr.next
        return num

    def show(self):
        if None == self.head:
            print(None)
        curr = self.head
        while None != curr:
            print(curr.item, end = " ")
            curr = curr.next

# Multiset using hashing with chaining
class MultiSet2:
    def __init__(self, contents=[]):
        self.items = [None] * 50
        for e in contents:
            self.add(e)

    # Retrival operation 
    # return True if item is in the set
    # return False if not
    def __contains__(self, item):
        index = hash(item) % len(self.items)
        templist = self.items[index]
        return False if None == templist else (item in templist)

    # Insertion operation
    def add(self, item):
        index = hash(item) % len(self.items)
        templist = self.items[index]
        if templist == None:
            self.items[index] = LinkedList([item])
        else:
            templist.append(item)

    # Deletion operation
    def delete(self, item):
        index = hash(item) % len(self.items)
        if self.items[index] != None:
            self.items[index].delete(item)
            if self.items[index].head == None:
                self.items[index] = None

    # Union operation
    def union(self, other):
        for templist in other.items:
            if templist is not None:
                curr = templist.head
                while None != curr:
                    self.add(curr.item)
                    curr = curr.next

    # Intersecion operation
    # first count the number of items in another sets, save in a counter
    # keep the node until counter become 0
    # delete the redundant node in one traversal
    def intersection(self, other):
        for templist in self.items:
            if templist is not None:
                curr = templist.head
                while None != curr:
                    mark = curr
                    flag = 0
                    item = curr.item
                    num1 = num2 = other.count(item)
                    while None != curr and curr.item == item:
                        if flag != 1 and num1 <= 1:
                            mark = curr
                            flag = 1
                        else:
                            num1 -= 1
                        curr = curr.next
                    if flag == 1:
                        mark.next = curr
                    # if there is no item in another sets
                    if num2 == 0:
                        curr = mark.next
                        self.delete(item)

    # Difference operation
    # first count the number of items in another sets, save in a counter
    # delete the redundant node in one traversal until counter because 0
    def difference(self, other):
        for templist in self.items:
            if templist is not None:
                curr = templist.head
                prev = curr
                while None != curr:
                    item = curr.item
                    num1 = num2 = other.count(item)
                    next = curr.next
                    while None != next and curr.item == next.item and num1 > 1:
                        curr.next = next.next
                        next = next.next
                        num1 -= 1
                    if num2 > 0:
                        prev.next = curr.next
                        curr = curr.next
                        self.delete(item)
                    while None != curr and curr.item == item:
                        curr = curr.next
                        prev = prev.next

    # Search node with the corresponding item
    # if found        return the node
    # if not found    return None
    def search(self, item):
        index = hash(item) % len(self.items)
        templist = self.items[index]
        return None if None == templist else templist.search(item)

    # Count the item number in the multiset
    # return item number
    def count(self, item):
        index = hash(item) % len(self.items)
        templist = self.items[index]
        return 0 if None == templist else templist.count(item)

    def show(self):
        for item in self.items:
            if item is not None:
                item.show()
        print("\n")


# Test Code
print("Multisets with explicit storage")

a = MultiSet1([1,1,1,1,1,1,2,2,6,7,8,5,3,76,72,3])
print("create the list")
a.show()

a.add(2)
print("add 2:")
a.show()

a.delete(7)
print("delete 7:")
a.show()

a = MultiSet1([1,1,1,1,1,1,2,2,6,7,8,5,5,3,76,72,3])
b = MultiSet1([1,1,2,3,5,5,5,9,72,100,120])
print("a:", end=" ")
a.show()
print("b:", end=" ")
b.show()
a.union(b)
print("a U b:", end=" ")
a.show()

a = MultiSet1([1,1,1,1,1,1,2,2,6,7,8,5,5,3,76,72,3])
b = MultiSet1([1,1,2,3,5,5,5,9,72,100,120])
print("a:", end=" ")
a.show()
print("b:", end=" ")
b.show()
a.intersection(b)
print("a intersection b:", end=" ")
a.show()

a = MultiSet1([1,1,1,1,1,1,2,2,6,7,8,5,5,3,76,72,3])
b = MultiSet1([1,1,2,3,5,5,5,9,72,100,120])
print("a:", end=" ")
a.show()
print("b:", end=" ")
b.show()
a.difference(b)
print("a - b:", end=" ")
a.show()


print("Multisets with hashing with chaining")

a = MultiSet2([1,1,1,1,1,1,2,2,6,7,8,5,3,76,72,3])
print("create the list")
a.show()

a.add(2)
print("add 2:")
a.show()

a.delete(7)
print("delete 7:")
a.show()

a.delete(2)
a.delete(2)
a.delete(2)
a.delete(2)
print("over delete 2:")
a.show()

a = MultiSet2([1,1,1,1,1,1,2,2,6,7,8,5,5,3,76,72,3])
b = MultiSet2([1,1,2,3,5,5,5,9,72,100,120])
print("a:", end=" ")
a.show()
print("b:", end=" ")
b.show()
a.union(b)
print("a U b:", end=" ")
a.show()

a = MultiSet2([1,1,1,1,1,1,2,2,6,7,8,5,5,3,76,72,3])
b = MultiSet2([1,1,2,3,5,5,5,9,72,100,120])
print("a:", end=" ")
a.show()
print("b:", end=" ")
b.show()
a.intersection(b)
print("a intersection b:", end=" ")
a.show()

a = MultiSet2([1,1,1,1,1,1,2,2,6,7,8,5,5,3,76,72,3])
b = MultiSet2([1,1,2,3,5,5,5,9,72,100,120])
print("a:", end=" ")
a.show()
print("b:", end=" ")
b.show()
a.difference(b)
print("a - b:", end=" ")
a.show()


print("time comparison between two method")
import time
a = MultiSet1([])
start = time.time()
for i in range(10000):
    a.add(i)
end = time.time()
print(end-start)

a = MultiSet2([])
start = time.time()
for i in range(10000):
    a.add(i)
end = time.time()
print(end-start)