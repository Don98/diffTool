# coding:utf-8
import difflib
import tkinter as tk
import tkinter.filedialog
from functools import partial
import tkinter.font as tkFont
import os
from tkinter import *
from tkinter import scrolledtext
from threading import Thread, RLock
from javaHighlighter import JavaSyntaxHighlighter
from EvaAction import EvaAction
from tkinter import messagebox

class Eva():
    def __init__(self,root,file_name,ws,hs):
        self.file_name = file_name
        self.root = root
        self.methods = ["Se_actionList","GT_actionList","MTD_actionList","IJM_actionList"]
        self.ws = ws
        self.hs = hs
        self.font = tkFont.Font(family="microsoft yahei", size=12, weight="normal")
        self.m_len = self.font.measure("n")
        # self.Window = tk.Toplevel(self.root)
        # self.Window.title(file_name.split("/")[-1])
        self.Window = tk.Frame(self.root, width = self.ws,height = self.hs)
        self.count = 0
        
        # self.set_size()
        self.build()
        
    # def set_size(self):
        # self.w = self.root.winfo_screenwidth() * 3 / 4; self.h = self.root.winfo_screenheight() * 3 / 4 + 20
        # self.ws = self.root.winfo_screenwidth()
        # self.hs = self.root.winfo_screenheight()
        # x = (self.ws/2) - (self.w/2)
        # y = (self.hs/2) - (self.h/2)
        # self.Window.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
            
    # def draw_text():        
    def get_content(self,file_name,text,text1):
        with open(file_name,"r") as f:
            data = f.readlines()
        jsh = JavaSyntaxHighlighter(text,text1)
        content = []
        for i in data:
            content.append(jsh.highlight(i))
        return jsh.translate(content)
    
    def processWheel(self,event):
        a= int(-1*(event.delta/120))
        self.line_text0.yview_scroll(a,'units') 
        self.text.yview_scroll(a,'units')
        return "break" 
        
    def set_line_windows(self):
        self.line_windows0 = tk.Frame(self.windows1,width = 40, height = self.hs - 30, bg = '#f5f5f5')
        self.line_text0 = tk.Text(self.line_windows0, font = self.font, bg = '#f5f5f5')  
        self.line_text0.pack(fill = BOTH, expand = True)
        self.line_windows0.place(x = 5, y = 5, width = 40, height = self.hs - 30)
        # for i in range(500):
            # self.line_text0.insert('end',str(i) + '\n') 
        self.line_windows0.update()
        self.line_text0.bind("<MouseWheel>", self.processWheel)
        self.line_text0["state"] = "disabled"
        
    def draw_layout(self):
        self.windows1 = tk.Frame(self.Window,width = self.ws, height = self.hs - 30)
        self.windows1.place(x = 0, y = 30)
        # self.windows1.config(bg = "blue")
        
        self.windows2 = tk.Frame(self.windows1,width = self.ws / 2, height = self.hs - 30)
        self.windows2.place(x = 0, y = 0)
        self.windows2.config(bg = "blue")
        self.text_windows0 = tk.Frame(self.windows2,width = self.ws / 2 - 40, height = self.hs - 30)
        self.text_windows0.place(x = 45, y = 5)
        # self.text_windows0.config(bg = "red")
        
        self.set_line_windows()
        self.text = []
        self.text = tk.Text(self.text_windows0, font = self.font)   
        self.text.place(x = 0, y = 0)
        self.text.pack(fill = BOTH, expand = True)
        self.text_windows0.place(x = 45, y = 5, width = self.ws / 2 - 40, height = self.hs - 30)
        self.text_windows0.update()
        print(self.text.winfo_width(),self.text.winfo_height())
        self.text = self.get_content(self.file_name + "/" + "Srcfile.java",self.text,self.line_text0)
        self.text.bind("<MouseWheel>", self.processWheel)
        self.text["state"] = "disabled"
        
        print(self.line_text0.winfo_width(),self.line_text0.winfo_height())
        print(self.text.winfo_width()/self.m_len)
        # nums = 50 * 100
        # self.text.yview_scroll(nums, "units")
        
        
        self.windows3 = tk.Frame(self.windows1,width = self.ws / 2, height = self.hs - 30)
        self.windows3.place(x = self.ws / 2, y = 0)
        self.windows3.config(bg = "yellow")
        self.text0 = tk.Text(self.windows3,width = 95,height = 53,font = 10)
        self.text0 = self.get_content(self.file_name + "/" + "Dstfile.java",self.text0)
        # self.text0.pack()
        self.text0.place(x = 5, y = 5)
        self.text0["state"] = "disabled"
            

    def to_eva(self,method):
        self.evaAction = EvaAction(self.windows1,self.file_name, self.text, self.text0, method, self.buttons)
        
    def set_button(self):
        self.windows0 = tk.Frame(self.Window, width = self.ws, height = 30)
        self.windows0.place(x = 0 , y = self.hs - 30)
        self.buttons = []
        self.button0 = tk.Button(self.windows0,width=10, height=1, text='SE-Mapping', bg='skyblue', command=partial(self.to_eva,"Se_actionList"))
        self.button0.place(x = 100, y = 2)
        self.button1 = tk.Button(self.windows0,width=10, height=1, text='GT', bg='skyblue', command = partial(self.to_eva,"GT_actionList"))
        self.button1.place(x = 320, y = 2)
        self.button2 = tk.Button(self.windows0,width=10, height=1, text='MTD', bg='skyblue', command = partial(self.to_eva,"MTD_actionList"))
        self.button2.place(x = 540, y = 2)
        self.button3 = tk.Button(self.windows0,width=10, height=1, text='IJM', bg='skyblue', command = partial(self.to_eva,"IJM_actionList"))
        self.button3.place(x = 760, y = 2)
        self.button4 = tk.Button(self.windows0,width=10, height=1, text='退出', bg='skyblue', command = self.destroy).place(x = 980, y = 2)
        self.buttons.append(self.button0)
        self.buttons.append(self.button1)
        self.buttons.append(self.button2)
        self.buttons.append(self.button3)
    
    def destroy(self):
        # messagebox.showinfo(title="提示", message="你还有"+ str(4 - self.count) + "份还未标注")
        self.Window.destroy();
    
    def set_label(self):
        self.windows0 = tk.Frame(self.Window, width = self.ws, height = 30)
        self.windows0.place(x = 0, y = 0)
        self.label = tk.Label(self.windows0, text= self.file_name.split("/")[-1],fg='black',font=('Arial', 12)).place(x=10, y=10)
    
    def build(self):
        self.Window.place(x = self.root.winfo_screenwidth() - self.ws,y = 0)
        # self.Window.config(bg="red")
        self.set_label()
        # self.set_button()
        self.draw_layout()