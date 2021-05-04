# this is for homework exercise 2


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

    def new_delete(self, item):
        # this method is just for fun, not for homework
        def __mydelete(root, item, flags, my_parent=None):
            if root is None:
                return None
            if item < root.val:
                flags[0] = 1
                flags[1] = 0
                return __mydelete(root.left, item, flags, root)
            if item > root.val:
                flags[0] = 0
                flags[1] = 1
                return __mydelete(root.right, item, flags, root)
            if item == root.val:
                flags[2] = 1
                if root.left is None and root.right is None:
                    # the root is actully a leaf
                    if flags[0] and not flags[1]:
                        my_parent.left = None
                        del root
                        return None
                    elif flags[1] and not flags[0]:
                        my_parent.right = None
                        del root
                        return None
                return root

        def __del_min(parent, curr):
            flag = 0
            while curr.left is not None:
                flag = 1
                parent = curr
                curr = curr.left
            if flag:
                parent.left = curr.right
                return curr.val
            else:
                parent.right = curr.right
                return curr.val

        def __del_max(parent, curr):
            flag = 0
            while curr.right is not None:
                flag = 1
                parent = curr
                curr = curr.right
            if flag:
                parent.right = curr.left
                return curr.val
            else:
                parent.left = curr.left
                return curr.val

        # body of new delete
        if self.root is None:
            return False
        if self.root.right is None and self.root.left is None:
            self.root = None
            return True
        else:
            flags = [0, 0, 0]
            sub_root = __mydelete(self.root, item, flags)
            if sub_root is None:
                if flags[2]:
                    return True
                return False
            # swap for roots here
            if sub_root.right is not None:
                val = __del_min(sub_root, sub_root.right)
                assert (val is not None)
                sub_root.val = val
            else:
                val = __del_max(sub_root, sub_root.left)
                assert (val is not None)
                sub_root.val = val
        return True


tree = BST()
for x in [20, 10, 30, 5, 13, 17, 33]:
    tree.insert(x)
for x in tree:
    print(x)

# b,c = tree.find(3), tree.find(6)
# print(b,c)

tree.bad_delete(10)
tree.delete(17)
tree.delete(33)
print("--------")
for x in tree:
    print(x)
