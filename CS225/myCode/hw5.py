# -*- coding: utf-8 -*-


# ex.1 (i)
# HashSet Reorgnisation, no Place_holder
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
                # ? 有load的情况下真的会放满吗，第二个判断能不能删？
                if self.items[index] is None or index == len(self.items) - 1:
                    break
                else:
                    if hash(self.items[index]) % len(self.items) <= location:
                        self.items[location] = self.items[index]
                        self.items[index] = None
                        location = index
                index = index + 1
        else:
            raise KeyError("Item not in HashSet")

def testEX1a():
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

# ex.1 (ii)
# hashset buffer
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
                # 真的有必要int吗？
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

def testEX1b():
    content = [5,4,10,11,17,16]
    print(content)
    hashset = HashSet(content)
    hashset.show()

# ex.2
class Trie:
    class TrieNode:
        def __init__(self, item, next=None, follows=None):
            self.item = item
            self.next = next
            self.follows = follows

    def __init__(self):
        self.start = None

    def __contains__(self, item):
        return Trie.__contains(self.start, list(item))

    @staticmethod
    def __contains(node, item):
        if node is None:
            return False
        if not item:
            if node.item == "#":
                return True
            else:
                return False
        key = item[0]
        if node.item == key:
            item.pop(0)
            return Trie.__contains(node.follows, item)
        return Trie.__contains(node.next, item)

    def extend_one(self, item):
        def __extend_one(item, node, temp="", res_list=[]):
            if not item:
                while True:
                    if node is None:
                        return res_list
                    if node.follows.item == "#":
                        res_list.append(temp + node.item)
                    node = node.next
            key = item[0]
            if node.item == key:
                temp = temp + item.pop(0)
                return __extend_one(item, node.follows, temp, res_list)
            return __extend_one(item, node.next, temp, res_list)
        if item in self:
            print("item already in dictionary!")
            return
        node = self.start
        return __extend_one(list(item), node)

    def prefix(self, item):
        def __prefix(item, node, maxlength, temp="", res_list=[], length=0):
            if length >= maxlength or node == None:
                return res_list
            if node.item == "#" and maxlength - 1 >= length >= maxlength - 2:
                res_list.append(temp)
            key = item[0]
            if node.item == key:
                temp = temp + item.pop(0)
                length = length + 1
                return __prefix(item, node.follows, maxlength, temp, res_list, length)
            return __prefix(item, node.next, maxlength, temp, res_list, length)
        if item in self:
            print("item already in dictionary!")
            return
        node = self.start
        maxlength = len(list(item))
        return __prefix(list(item), node, maxlength)

    def difference(self, item):
        def __difference(item, node, maxlife, life, temp="", res_list=[]):
            if life < maxlife - 1:
                return
            if node == None:
                return 
            if node.item == "#" and item == []:
                if life == maxlife - 1:
                    res_list.append(temp)
                    return
                else:
                    return
            if not (node.item != "#" and item != []):
                return
            if item != None:
                key = item[0]
                if node.item != key:
                    __difference(item[1:], node.follows, maxlife, life - 1, temp + node.item, res_list)   #不等于生命值减1
                else:
                    __difference(item[1:], node.follows, maxlife, life, temp + node.item, res_list)
                __difference(item[0:], node.next, maxlife, life, temp, res_list)              #查next，除了改成node.next其他都不变
            return res_list
        if item in self:
            print("item already in dictionary!")
            return
        node = self.start
        maxlife = len(list(item))
        return __difference(list(item), node, maxlife, maxlife)

    def insert(self, item):
        self.start = Trie.__insert(self.start, list(item))

    @staticmethod
    def __insert(node, item):
        if not item:
            newnode = Trie.TrieNode("#")
            return newnode
        if node is None:
            key = item.pop(0)
            newnode = Trie.TrieNode(key)
            newnode.follows = Trie.__insert(newnode.follows, item)
            return newnode
        else:
            key = item[0]
            if node.item == key:
                item.pop(0)
                node.follows = Trie.__insert(node.follows, item)
                node.follows.pre = node
            else:
                node.next = Trie.__insert(node.next, item)
            return node

    def print_trie(self, root, level_f=0):
        if root is None:
            return
        if root.item != '#':
            print(root.item, '-', end='')
        else:
            print(root.item, end='')
        self.print_trie(root.follows, level_f + 1)
        if root.next is not None:
            print('\n')
            str_sp = ' ' * level_f * 3
            print(str_sp + '|')
            print(str_sp, end='')
        self.print_trie(root.next, level_f)
        return

def testEX2():
    gzm = Trie()
    gzm.insert("gerie")
    gzm.insert("gre")
    gzm.insert("grll")
    gzm.insert("grlla")
    gzm.insert("gzml")
    gzm.insert("tercesrsdfdhvudhsfhsa")
    gzm.insert("gtrcesfdsdcvr")
    print(gzm.prefix("grllab"))

def main():
    # testEX1a()
    # testEX1b()
    testEX2()

if __name__ == "__main__":
    main()