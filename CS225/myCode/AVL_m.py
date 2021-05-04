# -*- coding: utf-8 -*-

from queue import Fifo

class AVLTree:

    class AVLNode:
        def __init__(self, item, height=0, left=None, right=None):
            self.item = item
            self.height = height
            self.left = left
            self.right = right

        def __iter__(self):
            if self.left != None:
                for elt in self.left:
                    yield elt
            yield self.item, self.height
            if self.right != None:
                for elt in self.right:
                    yield elt

    def __init__(self):
        self.root = None

    def __iter__(self):
        if self.root != None:
            return self.root.__iter__()
        else:
            return [].__iter__()
    
    @staticmethod
    def iterDFS(root):
        # using the pre-order: root--left--right
        if root is not None:
            yield root.item
        else:
            return
        if root.left is not None:
            for i in AVLTree.iterDFS(root.left):
                yield i
        if root.right is not None:
            for j in AVLTree.iterDFS(root.right):
                yield j

    @staticmethod
    def iterBFS(root):
        queue = Fifo()
        assert (root is not None)
        queue.pushback(root)
        while not queue.isEmpty():
            node = queue.popfront()
            yield node.item
            if node.left is not None:
                queue.pushback(node.left)
            if node.right is not None:
                queue.pushback(node.right)

    # the same as BST
    def find(self, item):
        def __find(root, item):
            if root == None:
                return False
            if item == root.getitem():
                return True
            if item < root.getitem():
                return __find(root.getLeft(), item)
            else:
                return __find(root.getRight(), item)

        return __find(self.root, item)

    def insert(self, item):
        def __insert(item, node):
            if node == None:
                node = AVLTree.AVLNode(item)
            elif item < node.item:
                node.left = __insert(item, node.left)
                if AVLTree.__height(node.left) - AVLTree.__height(node.right) == 2:
                    if item < node.left.item:
                        node = AVLTree.__singleRightRotate(node)
                    else:
                        node = AVLTree.__doubleRightRotate(node)
            else:
                node.right = __insert(item, node.right)
                if AVLTree.__height(node.right) - AVLTree.__height(node.left) == 2:
                    if item > node.right.item:
                        node = AVLTree.__singleLeftRotate(node)
                    else:
                        node = AVLTree.__doubleLeftRotate(node)
            node.height = max(AVLTree.__height(node.left), AVLTree.__height(node.right)) + 1
            return node
        self.root = __insert(item, self.root)
    
    def delete(self, item):
        def __delete(item, node):
            # element not found
            if node == None:
                return None
            # search for element
            elif item < node.item:
                node.left = __delete(item, node.left)
            elif item > node.item:
                node.right = __delete(item, node.right)
            # element found with 2 children
            elif node.left != None and node.right != None:
                tmp = AVLTree.__findMin(t.right);
                node.item = tmp.item
                node.right = __delete(node.item, node.right)
            # with 1 or 0 child
            else:
                tmp = node
                if node.left == None:
                    node = node.right
                elif node.right == None:
                    node = node.left
            if node == None:
                return None
            node.height = max(AVLTree.__height(node.left), AVLTree.__height(node.right)) + 1
            # if node is unbalance, if left node is deleted, right case
            if AVLTree.__height(node.left) - AVLTree.__height(node.right) == 2:
                # right right case
                if AVLTree.__height(node.left.left) - AVLTree.__height(node.left.right) == 1:
                    return AVLTree.__singleLeftRotate(node)
                # right left case
                else:
                    return AVLTree.__doubleLeftRotate(node)
            # if right node is deleted, left case
            elif AVLTree.__height(node.right) - AVLTree.__height(node.left) == 2:
                # left left case
                if AVLTree.__height(node.right.right) - AVLTree.__height(node.right.left) == 1:
                    return AVLTree.__doubleRightRotate(node)
                # left right case
                else:
                    return AVLTree.__doubleRightRotate(node)
            return node
        self.root = __delete(item, self.root)
    
    # ===== Auxiliary Functions =====
    # They all have '__' as prefixes to indicate that they are private methods to the class
    def __findMin(node):
        if node == None:
            return None
        elif node.left == None:
            return node
        else:
            return __findMin(node.left)

    def __height(node):
        if node == None:
            return -1
        else:
            return node.height
    
    def __singleLeftRotate(node):
        tmp = node.right
        node.right = tmp.left
        tmp.left = node
        node.height = max(AVLTree.__height(node.left), AVLTree.__height(node.right)) + 1
        tmp.height = max(AVLTree.__height(node.right), AVLTree.__height(node)) + 1
        return tmp

    def __singleRightRotate(node):
        print(node.item)
        tmp = node.left
        node.left = tmp.right
        tmp.right = node
        node.height = max(AVLTree.__height(node.left), AVLTree.__height(node.right)) + 1
        tmp.height = max(AVLTree.__height(node.left), AVLTree.__height(node)) + 1
        return tmp

    def __doubleLeftRotate(node):
        node.right = AVLTree.__singleRightRotate(node.right)
        return AVLTree.__singleLeftRotate(node)
    
    def __doubleRightRotate(node):
        node.left = AVLTree.__singleLeftRotate(node.left)
        return AVLTree.__singleRightRotate(node)


'''
tree = AVLTree()
for x in  [8,4,9,3,1,11,0,6,5,2,12,13,10]:
    tree.insert(x)
iter = tree.iterBFS(tree.root)
for i in iter:
    print(i, end=' ')
'''
tree = AVLTree()
for x in  [5, 4, 6, 3, 2]:
    tree.insert(x)
