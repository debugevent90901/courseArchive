# this is for homework exercise 2
import time
import random

class BST:
    class __Node:
        def __init__(self, val, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

        def getVal(self):
            return self.val

        def setVal(self, newval):
            self.val = newval

        def getLeft(self):
            return self.left

        def setLeft(self, newleft):
            self.left = newleft

        def getRight(self):
            return self.right

        def setRight(self, newright):
            self.right = newright
            # The iterator traverses the tree in the order

        # of the stored values.
        def __iter__(self):
            # print(self.val)
            # print("iter of Node")
            if self.left != None:
                # print("self.left is not None")
                for elem in self.left:
                    # print("in the for loop")
                    # print("look what I got from iter: %d" % elem)
                    yield elem
            # print("finally it's time, the self.val is %d" % self.val)
            yield self.val
            if self.right != None:
                # print("self.right is not None")
                for elem in self.right:
                    # print("now checking for the right, the right has %d" % elem)
                    yield elem

    def __init__(self):
        self.root = None

    def insert(self, val):
        def __insert(root, val):
            if root == None:
                return BST.__Node(val)
            if val < root.getVal():
                root.setLeft(__insert(root.getLeft(), val))
            else:
                root.setRight(__insert(root.getRight(), val))
            return root

        self.root = __insert(self.root, val)

    def __iter__(self):
        if self.root != None:
            # print("--------in the iter of BST--------")
            # this will be called only once
            # because the rest of the job should be finished by the iter method of Nodes
            return self.root.__iter__()
        else:
            return [].__iter__()

    def find(self, val):
        def __find(root, val):
            if root == None:
                return False
            if val == root.getVal():
                return True
            if val < root.getVal():
                return __find(root.getLeft(), val)
            else:
                return __find(root.getRight(), val)

        return __find(self.root, val)

    def delete(self, val):
        def __delete(root, val):
            if root == None:
                return root
            if val == root.getVal():
                return __merge(root.getLeft(), root.getRight())
            if val < root.getVal():
                root.setLeft(__delete(root.getLeft(), val))
                return root
            root.setRight(__delete(root.getRight(), val))
            return root

        def __merge(leftnode, rightnode):
            if rightnode == None:
                return leftnode
            if rightnode.getLeft() == None:
                rightnode.setLeft(leftnode)
                return rightnode
            __merge(leftnode, rightnode.getLeft())
            return rightnode

        self.root = __delete(self.root, val)

    # this method will iterate the sub-trees and re-insert all the elements back in
    def bad_delete(self, val):
        tmp = []

        def __bad_delete(root, val):
            if root == None:
                return root
            elif val == root.getVal():
                nonlocal tmp
                for elem in root:
                    tmp.append(elem)
                return None
            elif val < root.getVal():
                root.setLeft(__bad_delete(root.getLeft(), val))
                return root
            else:
                root.setRight(__bad_delete(root.getRight(), val))
                return root

        self.root = __bad_delete(self.root, val)
        for elem in tmp:
            if elem != val:
                self.insert(elem)
    
tree1 = BST()
tree2 = BST()
num = random.sample([i for i in range(100)], 100)
for x in num:
    tree1.insert(x)
    tree2.insert(x)

start1 = time.time()
for x in num:
    tree1.delete(x)
end1 = time.time()

start2 = time.time()
for x in tree2:
    tree2.bad_delete(x)
end2 = time.time()

good_time = end1 - start1
bad_time = end2 - start2
print(good_time)
print(bad_time)