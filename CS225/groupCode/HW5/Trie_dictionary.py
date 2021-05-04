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
            #def __listdif(a, b):
            #    a.remove(b)
            #    return a
            if life < maxlife - 1:
                return
            if node == None:
                return 
            #print(node.item,item)
            if node.item == "#" and item == []:
                if life == maxlife - 1:
                    res_list.append(temp)
                    #__difference(item[0:], node.next, maxlife, life, temp, res_list)        #这句是用来处理一个单词是另一个单词前缀，但都满足条件的情况
                    #print(res_list)
                    return
                else:
                    return
            if not (node.item != "#" and item != []):
                return
            #if item == []:   #处理dictionary中单词比given word长的情况
            #    if life == maxlife - 1:
            #        __difference(item[0:], node.follows, maxlife, life, temp + node.item, res_list)
            #        __difference(item[0:], node.next, maxlife, life, temp + node.item, res_list)
            #        return
            #    else:
            #        return
            if item != None:
                key = item[0]
                #print(item)
                if node.item != key:
                    __difference(item[1:], node.follows, maxlife, life - 1, temp + node.item, res_list)   #不等于生命值减1
                else:
                    __difference(item[1:], node.follows, maxlife, life, temp + node.item, res_list)
                #print(item)
                __difference(item[0:], node.next, maxlife, life, temp, res_list)              #查next，除了改成node.next其他都不变
            #else:
            #    __difference(item[0:], node.follows, maxlife, life, temp + node.item, res_list)
            #    __difference(item[0:], node.next, maxlife, life, temp + node.item, res_list)
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

    # a print function which can print out structure of tries
    # to help better understand
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
gzm = Trie()
#gzm.insert("zerres")
gzm.insert("gerie")
gzm.insert("gre")
gzm.insert("grll")
gzm.insert("gzml")
gzm.insert("tercesrsdfdhvudhsfhsa")
gzm.insert("gtrcesfdsdcvr")
# gzm.insert("taijule")
# gzm.insert("gzme")
# print("checking if gzm is real a huge dalao")
# print("taijule" in gzm)
# gzm.print_trie(gzm.start)
#print(gzm.difference("gerces"))
print(gzm.difference("gr"))