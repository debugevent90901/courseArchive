# this is the exercise 3 of HW3

class Solution:
    class __Node:
        def __init__(self, val, left, right):
            self.val = val
            self.left = left
            self.right = right

    def __init__(self, content):
        self.array = content
        self.length = len(content)

    def find_min(self):
        ans = self.find_min_helper()
        return ans.val

    def find_min_helper(self, left=0, right=None):
        if right is None:
            right = self.length - 1
        if left == right:
            return self.__Node(self.array[left], None, None)
        mid = int((left + right) / 2)
        node1 = self.find_min_helper(left, mid)
        node2 = self.find_min_helper(mid + 1, right)
        if node1.val < node2.val:
            root_node = self.__Node(node1.val, node1, node2)
            return root_node
        else:
            root_node = self.__Node(node2.val, node2, node1)
            return root_node

    def second_min(self):
        tree = self.find_min_helper()
        min_val = tree.val
        temp = tree
        content = []
        while temp.left is not None and temp.right is not None:
            content.append(temp.right.val)
            temp = temp.left
        temp_solution = Solution(content)
        second_min_val = temp_solution.find_min()
        return min_val, second_min_val


# tests here
import numpy as np

testing_array = list(np.random.randint(1, 100, size=20))
print("begin of the tests")
for i in testing_array:
    print(i)
print("after finding the minimal two values")
solution = Solution(testing_array)
a, b = solution.second_min()
print("the result is: (%d, %d)" % (a, b))
