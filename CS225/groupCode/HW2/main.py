#this is main function of the whole progject
'''
This is HW2 for CS225

Team Member:
    Zhu Zhongbo
    Yang Zhaohua
    Guan Zimu
    Xie Tian
'''
from Git import upload
from pylist import PyList
from dlinkedlist import DLinkedList
import numpy as np
import time
import matplotlib.pyplot as plt

#this is the test of E1: selectionSort
pylist = PyList(list(np.random.randint(100,size = 10)),size = 20)
pylist.show()
print("the result of selectionSort")
pylist.selectionSort()
pylist.show()
print("------")

#this is the test of E2: bubbleSort of PyList
pylist1 = PyList(list(np.random.randint(100,size = 10)),size = 20)
pylist1.show()
print("the result of bubbleSort: list")
pylist1.bubbleSort()
pylist1.show()
print("------")

#this is the test of E2: bubbleSort of DLinkedList
dl = DLinkedList(list(np.random.randint(100,size = 10)))
dl.show()
dl.bubbleSort()
print("the result of bubbleSort: linked list")
dl.show()
print("------")

#this is the test of E3: improved insertionSort with Binary Search
pylist2 = PyList(list(np.random.randint(100,size = 20)),size = 20)
pylist2.show()
print("the result of insertionSort: list")
pylist2.insertionSort()
pylist2.show()
print("------")

#this is the test of merge sort (without threshold)
print("test of merge sort")
pylist3 = PyList(list(np.random.randint(100,size = 10)),size = 20)
pylist3.show()
print("after merge sort")
pylist3.mergeSort()
pylist3.show()

#this is the test of merge sort with bubble sort as helper function below threshold
#pylist4 = PyList(list(np.random.randint(100,size = 100)),size = 200)
pylist4 = PyList(list(range(100,0,-1)),size = 200)
print('''
#######################################
This is the test of imporved merge sort
#######################################
''')
pylist4.show()
print("after the imporved merge sort with 10 as threshold")
pylist4.mergeSortTHR(thr = 10)
pylist4.show()
print('''
#######################################
This is the test of imporved merge sort
#######################################
''')

#then do the experiment of estimating the appropriate threshold

thresholds = list(range(30, 80))
runtimes = []
for t in range(len(thresholds)):
    runtime = 0
    for i in range(1000):
        pylist5 = PyList(list(np.random.randint(100,size=500)),size = 500)
        start = time.time()
        pylist5.mergeSortTHR(thr = thresholds[t])
        end = time.time()
        runtime += end-start
    runtimes.append(runtime)
print(runtimes)
plt.plot(thresholds, runtimes)
plt.show()
mintime = min(runtimes)
print("The min time is: %f s\nWith threshold: %d"%(mintime, thresholds[runtimes.index(mintime)]))

upload("all")