class MaxHeap():

    def __init__(self, items=[], build=0):
        self.swap = 0
        # choose only one of the following function to build your heap
        if (build == 0):
            self.build_heap(items)
        else:
            self.build_insertion(items)

    # ===== TODO =====
    # Implement the functions below
    def siftUp(self, index):
        if int(index/2) - 1 >= 0:
            if self.items[int(index/2)-1] < self.items[index-1]:
                self.items[int(index/2)-1], self.items[index-1] = self.items[index-1], self.items[int(index/2)-1]
                self.swap += 1
                self.siftUp(int(index/2))

    def siftDown(self, index):
        if index <= int(self.numItems / 2):
            if index == int(self.numItems/2) and self.numItems % 2 == 0:
                if self.items[2*index-1] >= self.items[index-1]:
                    self.items[index-1], self.items[2*index-1] = self.items[2*index-1], self.items[index-1]
                    self.swap += 1
            else:
                if self.items[2*index-1] >= self.items[index-1] or self.items[2*index] >= self.items[index-1]:
                    if self.items[2*index] >= self.items[2*index-1]:
                        self.items[index-1], self.items[2*index] = self.items[2*index], self.items[index-1]
                        self.swap += 1
                        self.siftDown(2*index+1)
                    else:
                        self.items[index-1], self.items[2*index-1] = self.items[2*index-1], self.items[index-1]
                        self.swap += 1
                        self.siftDown(2*index)

    def build_heap(self, inlist):
        self.items = inlist
        self.numItems = len(inlist)
        for i in range(int(self.numItems/2), 0, -1):
            self.siftDown(i)

    def build_insertion(self, inlist):
        self.items = []
        self.numItems = 0
        for i in inlist:
            self.items.append(i)
            self.numItems += 1
            self.siftUp(self.numItems)

a = [7,6,5,8,9,4,3,0,1,2]
b = [19,10,15,17,2,5,3,18,11,16,6,4,8,7,9,13,12,1,0,14]


heap = MaxHeap(a,1)
print("build_insertion:")
print(heap.items)
print("Number of swap =", heap.swap)
heap = MaxHeap(a,0)
print("build_heap:")
print(heap.items)
print("Number of swap =", heap.swap)

heap = MaxHeap(b,1)
print("build_insertion:")
print(heap.items)
print("Number of swap =", heap.swap)
heap = MaxHeap(b,0)
print("build_heap:")
print(heap.items)
print("Number of swap =", heap.swap)