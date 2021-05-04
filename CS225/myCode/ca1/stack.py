# this is the stack definition

class Stack(object):
    class Node(object):
        def __init__(self, val):
            self.val = val
            self.next = None

    def __init__(self):
        self.top = None

    def peek(self):
        if self.top is not None:
            return self.top.val
        else:
            return None

    def push(self, n):
        n = self.Node(n)
        n.next = self.top
        self.top = n
        return n.val

    def pop(self):
        if self.top is None:
            return None
        else:
            tmp = self.top.val
            self.top = self.top.next
            return tmp

    def isempty(self):
        if None == self.peek():
            return True
        else:
            return False

    def show(self):
        if self.top is None:
            return
        temp = self.top
        while temp is not None:
            print(temp.val)
            temp = temp.next
