# -*- coding: utf-8 -*-
#Git for team work
'''
This is HW2 for CS225

Team Member:
    Zhu Zhongbo
    Yang Zhaohua
    Guan Zimu
    Xie Tian
'''
import os

def upload(function = "all"):
    if function == "all":
        os.system('git add main.py &&\
                  git add Git.py &&\
                  git add pylist.py &&\
                  git add dlinkedlist.py &&\
                  git add runtime.jpg &&\
                  git commit -m"updated" &&\
                  git push -u origin master')
    elif function == "dl":
        os.system('git add dlinkedlist.py &&\
                  git commit -m"updated" &&\
                  git push -u origin master')
    elif function == "py":
        os.system('git add pylist.py &&\
                  git commit -m"updated" &&\
                  git push -u origin master')
    elif function == "main":
        os.system('git add main.py &&\
                  git commit -m"updated" &&\
                  git push -u origin master')
    return

if __name__ == "__main__":
    upload("all")
        
    
    