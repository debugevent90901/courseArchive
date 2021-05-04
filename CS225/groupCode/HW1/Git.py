# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 00:02:30 2020

@author: zzb
"""
import os

def upload():
    os.system('git add pylist.py &&\
              git add Git.py &&\
              git commit -m"updated" &&\
              git push -u origin master')
    return
    