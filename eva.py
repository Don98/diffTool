import difflib
import tkinter as tk
import tkinter.filedialog
from functools import partial
import os
from tkinter import *
from tkinter import scrolledtext
from threading import Thread, RLock
from javaHighlighter import JavaSyntaxHighlighter
from EvaAction import EvaAction

class Eva():
    def __init__(self,root,file_name):
        self.file_name = file_name
        self.root = root
        self.Window = tk.Toplevel(self.root)
        
        self.set_size()
        self.build()
        
    def set_size(self):
        self.w = self.root.winfo_screenwidth() * 3 / 4; self.h = self.root.winfo_screenheight() * 3 / 4 + 20
        self.ws = self.root.winfo_screenwidth()
        self.hs = self.root.winfo_screenheight()
        x = (self.ws/2) - (self.w/2)
        y = (self.hs/2) - (self.h/2)
        self.Window.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
            
    # def draw_text():        
    def get_content(self,file_name,text):
        with open(file_name,"r") as f:
            data = f.readlines()
        nums = 0
        length = len(data)
        if(length < 10):
            nums = 2
        elif(length < 100):
            nums = 3
        elif(length < 1000):
            nums = 4
        elif(length < 10000):
            nums = 5
        jsh = JavaSyntaxHighlighter(text,nums)
        num = 0
        content = []
        for i in data:
            content.append(jsh.highlight(i))
        return jsh.translate(content)
            
    def draw_layout(self):
        self.text = []
        self.text = tk.Text(self.Window,width = 95,height = 53,font = 10)   
        self.text = self.get_content(self.file_name + "/" + "Srcfile.java",self.text)
        self.text.pack()
        self.text.place(x=5,y=30)
        self.text["state"] = "disabled"
        # nums = 50 * 100
        # self.text.yview_scroll(nums, "units")
        
        
        self.text0 = tk.Text(self.Window,width = 95,height = 53,font = 10)
        self.text0 = self.get_content(self.file_name + "/" + "Dstfile.java",self.text0)
        self.text0.pack()
        self.text0.place(x=970,y=30)
        self.text0["state"] = "disabled"
            

    def to_eva(self,method):
        self.evaAction = EvaAction(self.Window,self.file_name, self.text, self.text0, method)
        
        
    def set_button(self):
        self.button0 = tk.Button(self.Window,width=10, height=1, text='SE-Mapping', bg='skyblue', command=partial(self.to_eva,"Se_actionList")).place(x = 100, y = 2)
        self.button1 = tk.Button(self.Window,width=10, height=1, text='GT', bg='skyblue', command = partial(self.to_eva,"GT_actionList")).place(x = 320, y = 2)
        self.button2 = tk.Button(self.Window,width=10, height=1, text='MTD', bg='skyblue', command = partial(self.to_eva,"MTD_actionList")).place(x = 540, y = 2)
        self.button3 = tk.Button(self.Window,width=10, height=1, text='IJM', bg='skyblue', command = partial(self.to_eva,"IJM_actionList")).place(x = 760, y = 2)
        self.button4 = tk.Button(self.Window,width=10, height=1, text='退出', bg='skyblue', command = self.destroy).place(x = 980, y = 2)
    
    def destroy(self):
        self.Window.destroy();
    
    def build(self):
        self.set_button()
        self.draw_layout()