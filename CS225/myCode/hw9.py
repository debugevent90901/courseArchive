# -*- coding: utf-8 -*-

# ex.1 max heap implementation
class MaxHeap:
    def __init__(self, content=[]):
        self.heap = content
        self.build_heap()
        
    def build_heap(self):
        for i in range(int(len(self.heap)/2), 0, -1):
            self.sift_down(i)
    
    def insert(self, val):
        self.heap.append(val)
        self.sift_up(len(self.heap))
    
    def retrieve_max(self):
        return self.heap[0]
        
    def delete_max(self):
        self.heap[0] = self.heap[-1]
        self.heap = self.heap[:-1]
        self.sift_down(1)
    
    def sift_down(self, i, length=None):
        if length == None:
            length = len(self.heap)
        if i <= int(length / 2):
            if i == int(length/2) and length % 2 == 0:
                if self.heap[2*i-1] >= self.heap[i-1]:
                    self.heap[i-1], self.heap[2*i-1] = self.heap[2*i-1], self.heap[i-1]
                    self.sift_down(2*i-1, length)
            else:
                if self.heap[2*i-1] >= self.heap[i-1] or self.heap[2*i] >= self.heap[i-1]:
                    if self.heap[2*i] >= self.heap[2*i-1]:
                        self.heap[i-1], self.heap[2*i] = self.heap[2*i], self.heap[i-1]
                        self.sift_down(2*i+1, length)
                    else:
                        self.heap[i-1], self.heap[2*i-1] = self.heap[2*i-1], self.heap[i-1]
                        self.sift_down(2*i, length)

    def sift_up(self, i):
        if int(i/2) - 1 >= 0:
            if self.heap[int(i/2)-1] < self.heap[i-1]:
                self.heap[int(i/2)-1], self.heap[i-1] = self.heap[i-1], self.heap[int(i/2)-1]
                self.sift_up(int(i/2))

# ex1.2 heapSort implementation
def heapSort(content):
    mh = MaxHeap(content)
    for i in range(len(content), 1, -1):
        mh.heap[0], mh.heap[i-1] = mh.heap[i-1], mh.heap[0]
        mh.sift_down(1, i-1)
    return mh.heap

def test1_1():
    h = MaxHeap([6, 4, 9, 7, 6, 10, 1, 5, 2, 3])
    print(h.heap)
    #h.insert(8)
    h.delete_max()
    print(h.heap)

def test1_2():
    a = [6, 4, 9, 7, 6, 10, 1, 5, 2, 3]
    print(heapSort(a))
    b = [34, 5, 21, 4, 98, 7, 1453, 666, 114514, 8964, 1, 12, 1919810]
    print(heapSort(b))

def main():
    test1_1()
    test1_2()


if __name__ == "__main__":
    main()