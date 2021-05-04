# -*- coding: utf-8 -*-

from PyList import PyList

class SPyList(PyList):
    def __init__(self,contents=[],size=10):
        self.items = [None] * size
        self.keys = []                         #modification                     
        self.numItems = 0
        self.size = size
        for e in contents:
            self.append(e)
    
    def append(self,item):
        if (type(item) is not dict):
            raise TypeError("Wrong Element Tpye, dict Type Expected")
        if (item['key'] in self.keys):          #modification
            raise KeyError("Key already exists")
        if self.numItems == self.size:
            self.allocate()
        self.items[self.numItems] = item
        self.numItems += 1
        self.keys.append(item['key'])           #modification
        
    def __setitem__(self,index,val):
        if (type(val) is not dict):
            raise TypeError("Wrong Element Tpye, dict Type Expected")
        if index >= 0 and index < self.numItems:
            old_key = self.items[index]['key']          #modification
            if(val['key']!=old_key and val['key'] in self.keys):
                raise KeyError("Key already exists")
            self.keys.remove(old_key)
            self.keys.append(val['key'])
            self.items[index] = val
            return
        raise IndexError("PyList assignment index out of range")
        
    def __add__(self,other):
        raise SyntaxError("Add operation not defined")  #modification
        
    def insert(self,i,x):
        if(type(x) is not dict):
            raise TypeError("Wrong Element Tpye, dict Type Expected")
        if (x['key'] in self.keys):                      #modification
            raise KeyError("Key already exists")
        if self.numItems == self.size:
            self.allocate()
        if i < self.numItems:
            for j in range(self.numItems-1,i-1,-1):
                self.items[j+1] = self.items[j]
            self.items[i] = x
            self.numItems += 1
            self.keys.append(x['key'])
        else:
            self.append(x)
            
    def projection(self, projectList):
        newContent = []
        for item in self.items:
            if (item == None):
                continue
            newItem = {}
            for key in item.keys():
                if (key in projectList):
                    newItem[key] = item[key]
            newContent.append(newItem)
        return PyList(newContent)
    
    def projection_m(self, projectList):
        newContent = []
        for item in self.items:
            if (item == None):
                continue
            newItem = {}
            for key in item.keys():
                if (key in projectList):
                    newItem[key] = item[key]
            newContent.append(newItem)
        # If there are duplicated elements, raise an error
        for i in range(len(newContent) - 1):
            if (newContent[i] in newContent[i+1:]):
                raise ValueError("Duplicated records after projection")
        return PyList(newContent)
    
    def equi_join(self, other):
        if(type(other) is not SPyList):
            raise TypeError("Wrong Argument Tpye, SPyList Type Expected")
        newContent=[]
        for selfItem in self.items:
            if (selfItem == None):
                continue
            for otherItem in other.items:
                if (otherItem == None):
                    continue
                commonKeys = set(selfItem.keys()).intersection(set(otherItem.keys()))  # When calculating the time complexity, don't use this function
                continueFlag = 0
                for key in commonKeys:
                    if (selfItem[key] != otherItem[key]):
                        continueFlag  = 1
                        break
                if (continueFlag):
                    continue
                joinRecord = selfItem.copy()
                for otherKey in set(otherItem.keys()).difference(set(selfItem.keys())):  # When calculating the time complexity, don't use this function
                    joinRecord[otherKey] = otherItem[otherKey]
                newContent.append(joinRecord)
        return SPyList(newContent)
    
    # implement sort() method here:
    def sort(self):
        # sort the keys
        self.keys.sort()
        # create a new dictionary with keys: index
        key_index = {}
        newContent = [None] * len(self.keys)
        for i in range(len(self.keys)):
            key_index[self.keys[i]] = i
        for i in range(len(self.keys)):
            item = self.items[i]
            index = key_index[item['key']]
            newContent[index] = item
        return SPyList(newContent)
            
    
    # implement equi_join_new() method using sort() function here
    def equi_join_new(self, other):
        # sort first
        self = self.sort()
        other = other.sort()
        if(type(other) is not SPyList):
            raise TypeError("Wrong Argument Tpye, SPyList Type Expected")
        newContent=[]
        self_idx = 0
        other_idx = 0
        self_len = self.numItems
        other_len = other.numItems
        while (self_idx < self_len and other_idx < other_len):
            selfItem = self.items[self_idx]
            otherItem = other.items[other_idx]
            if (selfItem['key'] < otherItem['key']):
                self_idx += 1
                continue
            elif (selfItem['key'] > otherItem['key']):
                other_idx += 1
                continue
            commonKeys = set(selfItem.keys()).intersection(set(otherItem.keys()))
            continueFlag = 0
            for key in commonKeys:
                if (selfItem[key] != otherItem[key]):
                    continueFlag  = 1
                    break
            if (continueFlag):
                continue
            joinRecord = selfItem.copy()
            for otherKey in set(otherItem.keys()).difference(set(selfItem.keys())):
                joinRecord[otherKey] = otherItem[otherKey]
            newContent.append(joinRecord)
            self_idx += 1
            other_idx += 1
        return SPyList(newContent)