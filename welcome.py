# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 16:36:53 2019

@author: rain
"""
#!/usr/bin/env python
#-*- coding:utf-8 -*-
import tkinter as tk
from tkinter.messagebox import *
from annatation import welcome1

root = tk.Tk() 
b99 = tk.Button(root, text='清除',width=12,command=welcome1)
b122 = tk.Button(root, text='清除',width=12)
b99.place(x = 0, y = 0)
b122.place(x = 0, y = 30)
root.mainloop()