# this is the exercise 1 of HW3

class PyList(list):
    def __init__(self, content=[], size=20):
        self.items = [None] * size
        self.numItems = 0
        self.size = size
        for e in content:
            self.append(e)

    def __contains__(self, item):
        for i in range(self.numItems):
            if self.items[i] == item:
                return True
        return False

    def __eq__(self, other):
        if (type(self) != type(other)):
            return False
        if self.numItems != other.numItems:
            return False
        for i in range(self.numItems):
            if (self.items[i] != other.items[i]):
                return False
        return True

    def __setitem__(self, index, obj):
        if index >= 0 and index <= self.numItems - 1:
            self.items[index] = obj
            return
        print("the index is %d" % index)
        print("the limit is %d" % self.numItems)
        raise IndexError("Pylist assignment index out of range.")

    def __getitem__(self, index):
        if index >= 0 and index <= self.numItems - 1:
            return self.items[index]
        raise IndexError("Pylist index out of range.")

    def append(self, item):
        if self.numItems == self.size:
            self.allocate()
        self.items[self.numItems] = item
        self.numItems += 1

    def __add__(self, other):
        result = PyList(size=self.numItems + other.numItems)
        for i in range(self.numItems):
            result.append(self.items[i])
        for i in range(other.numItems):
            result.append(other.items[i])
        return result

    def insert(self, i, x):
        if self.numItems == self.size:
            self.allocate()
        if i < self.numItems:
            for j in range(self.numItems - 1, i - 1, -1):
                self.items[j + 1] = self.items[j]
            self.items[i] = x
            self.numItems += 1
        else:
            self.append(x)

    def delete(self, index):
        if (self.numItems == self.size / 4):
            self.deallocate()
        if index >= self.numItems:
            raise IndexError("PyList index out of range.")
        else:
            for i in range(index, self.numItems - 1):
                self.items[i] = self.items[i + 1]
            self.numItems -= 1
            return

    def allocate(self):
        newlength = 2 * self.size
        newList = [None] * newlength
        for i in range(self.numItems):
            newList[i] = self.items[i]
        self.items = newList
        self.size = newlength

    def deallocate(self):
        newlength = int(self.size / 2)
        newList = [None] * newlength
        for i in range(self.numItems):
            newList[i] = self.items[i]
        self.items = newList
        self.size = newlength

    def show(self):
        for i in range(self.numItems):
            print(self.items[i].time, " , ", self.items[i].val)

    #    def merge_add(self):
    def merge_add(self, left, mid, right):
        i = left
        j = mid + 1
        k = 0
        #        print("left: ",left," mid: ",mid," right: ",right)
        temp = PyList(self.items[left:right + 1], len(self.items[left:right + 1]))
        while i <= mid and j <= right:
            #            print("(i,j) = (%d,%d)"%(i,j))
            #            print("the i th: ",self.items[i])
            #            print("the j th: ",self.items[j])
            #            print("the right is %d"%right)
            if self.items[i].time < self.items[j].time:
                temp.items[k] = self.items[i]
                #                print("if:self.items[i]: ",self.items[i])
                i = i + 1
            else:
                temp.items[k] = self.items[j]
                #                print("else:self.items[j]: ",self.items[j])
                #                print("the temp.items[0] is ",temp.items[0])
                j = j + 1
            k = k + 1

        while i <= mid:
            temp.items[k] = self.items[i]
            i = i + 1
            k = k + 1
        while j <= right:
            temp.items[k] = self.items[j]
            j = j + 1
            k = k + 1
        for i in range(temp.numItems):
            self.items[left + i] = temp.items[i]
        del temp

    #    def mergeSort(self):
    def mergeSort(self, left=0, right=None):
        if right == None:
            right = self.numItems - 1
        if (left < right):
            mid = left + (right - left) // 2
            self.mergeSort(left, mid)
            self.mergeSort(mid + 1, right)
            self.merge_add(left, mid, right)


class Request:
    def __init__(self, arrive_date, depart_date):
        self.arrive = arrive_date
        self.depart = depart_date


class RoomBooking:
    class __Event:
        def __init__(self, time, arr_or_dep):
            self.time = time
            self.val = arr_or_dep

    # class methods
    def __init__(self, k):
        self.numRooms = k

    def book(self, content):
        new_list = self.rearrange(content)
        new_list.show()
        temp = 0
        for i in range(new_list.numItems):
            temp += new_list[i].val
            if temp >= self.numRooms:
                return False
        return True

    def rearrange(self, content):
        result = PyList()
        for i in content:
            result.append(self.__Event(i.arrive, 1))
            result.append(self.__Event(i.depart, -1))
        result.mergeSort()
        return result


import numpy as np

service = RoomBooking(100)
# generate testing lists
test = []
for i in range(1000):
    a = np.random.randint(1, 366)
    b = np.random.randint(1, 30)
    req = Request(a, a+b)
    test.append(req)
print(service.book(test))
