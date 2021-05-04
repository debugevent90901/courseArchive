# this is for homework exercise 2

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
        if item == []:
            return True
        if node is None:
            return False
        key = item[0]
        if node.item == key:
            item.pop(0)
            return Trie.__contains(node.follows, item)
        return Trie.__contains(node.next, item)

    def insert(self, item):
        self.start = Trie.__insert(self.start, list(item))

    @staticmethod
    def __insert(node, item):
        if item == []:
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
        if (root == None):
            return
        if (root.item != '#'):
            print(root.item, '-', end='')
        else:
            print(root.item, end='')
        self.print_trie(root.follows, level_f + 1)
        if (root.next != None):
            print('\n')
            str_sp = ' ' * level_f * 3
            print(str_sp + '|')
            print(str_sp, end='')
        self.print_trie(root.next, level_f)
        return


gzm = Trie()
gzm.insert("gzm")
gzm.insert("taijule")
gzm.insert("tql")
print("checking if gzm is real a huge dalao")
print("taijule" in gzm)
gzm.print_trie(gzm.start)
