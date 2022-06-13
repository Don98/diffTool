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
from tkinter import messagebox
from ctypes import *
class _PointAPI(Structure): # 用于getpos()中API函数的调用
    _fields_ = [("x", c_ulong), ("y", c_ulong)]

class Eva():
    def __init__(self,true_root,root,file_name,the_index,ws,hs,bar_buttom,bar_right):
        self.true_root = true_root
        self.file_name = file_name
        self.the_index = the_index
        self.root = root
        self.bar_buttom = bar_buttom
        self.bar_right  = bar_right
        self.methods = ["Se_actionList","GT_actionList","MTD_actionList","IJM_actionList"]
        self.ws = ws
        self.hs = hs
        self.font = tkFont.Font(family="microsoft yahei", size=12, weight="normal")
        self.m_len = self.font.measure("n")
        self.all_positions = []
        # self.root = tk.Toplevel(self.root)
        # self.root.title(file_name.split("/")[-1])
        # self.root = tk.Frame(self.root, width = self.ws,height = self.hs)
        
        self.build()
    def get_filename(self):
        return self.file_name
    
    def get_content(self,file_name,text,text1):
        with open(file_name,"r") as f:
            data = f.readlines()
        jsh = JavaSyntaxHighlighter(data,text,text1)
        content = []
        nums = 0
        for i in data:
            content.append(jsh.highlight(i))
            nums += 1
        return jsh.translate(content)
    
    def processWheel(self,event):
        a= int(-1*(event.delta/60))
        self.line_text0.yview_scroll(a,'units') 
        self.text.yview_scroll(a,'units')
        return "break" 
    def processWheel1(self,event):
        a= int(-1*(event.delta/60))
        self.line_text1.yview_scroll(a,'units') 
        self.text1.yview_scroll(a,'units')
        return "break" 
        
    def set_line_windows(self):
        self.line_windows0 = tk.Frame(self.windows2,width = 40, height = self.hs - 30, bg = '#f5f5f5')
        self.line_text0 = tk.Text(self.line_windows0, font = self.font, bg = '#f5f5f5')  
        self.line_text0.pack(fill = BOTH, expand = True)
        self.line_windows0.place(x = 5, y = 5, width = 40, height = self.hs - 30)
        self.line_windows0.update()
        self.line_text0.bind("<MouseWheel>", self.processWheel)
        
    def set_line_windows1(self):
        self.line_windows1 = tk.Frame(self.windows4,width = 40, height = self.hs - 30, bg = '#f5f5f5')
        self.line_text1 = tk.Text(self.line_windows1, font = self.font, bg = '#f5f5f5')  
        self.line_text1.pack(fill = BOTH, expand = True)
        self.line_windows1.place(x = 5, y = 5, width = 40, height = self.hs - 30)
        self.line_windows1.update()
        self.line_text1.bind("<MouseWheel>", self.processWheel1)
    
    def set_two_textWindows(self):
        self.windows1.place(x = self.all_positions[3][0], y = self.all_positions[3][1],width = self.all_positions[3][2], height = self.all_positions[3][3])
        self.windows2.place(x = 0, y = 0, width = self.all_positions[3][2] / 2, height = self.all_positions[3][3] + 5)
        self.text_windows0.place(x = 45, y = 5, width = self.all_positions[3][2] / 2 - 40, height = self.all_positions[3][3] + 5)
        self.text_windows0.update()
        self.windows4.place(x = self.all_positions[3][2] / 2, y = 0,width = self.all_positions[3][2] / 2, height = self.all_positions[3][3] + 5)
        self.text_windows1.place(x = 45, y = 5, width = self.all_positions[3][2] / 2 - 40, height = self.all_positions[3][3] + 5)
        self.text_windows1.update()
        self.line_windows0.place(x = 5, y = 5, width = 40, height = self.all_positions[3][3] + 5)
        self.line_windows0.update()
        self.line_windows1.place(x = 5, y = 5, width = 40, height = self.all_positions[3][3] + 5)
        self.line_windows1.update()
        
    def get_text(self):
        return self.text
        
    def get_text1(self):
        return self.text1
    
    def draw_layout(self):
        
        self.texts = []
        # first text window 
        self.all_positions.append([0, 30, self.ws, self.hs - 35])
        self.windows1 = tk.Frame(self.root,width = self.all_positions[3][2], height = self.all_positions[3][3])
        self.windows1.place(x = self.all_positions[3][0], y = self.all_positions[3][1])
        
        self.windows2 = tk.Frame(self.windows1,width = self.all_positions[3][2] / 2, height = self.all_positions[3][3] + 5)
        self.windows2.place(x = 0, y = 0)
        self.windows2.config(bg = "white")
        # self.text_windows0 = tk.Frame(self.windows2,width = self.ws / 2 - 40, height = self.hs - 30)
        self.text_windows0 = tk.Frame(self.windows2,width = self.all_positions[3][2] / 2 - 40, height = self.all_positions[3][3] + 5,bg="white")
        # self.text_windows0.place(x = 45, y = 5)
        
        self.set_line_windows()
        self.text = tk.Text(self.text_windows0, font = self.font)   
        self.text.place(x = 0, y = 0)
        self.text.pack(fill = BOTH, expand = True)
        self.text_windows0.place(x = 45, y = 5, width = self.all_positions[3][2] / 2 - 40, height = self.all_positions[3][3] + 5)
        self.text_windows0.update()
        self.text, self.line_text0 = self.get_content(self.file_name + "/" + "Srcfile.java",self.text,self.line_text0)
        self.text.bind("<MouseWheel>", self.processWheel)
        self.text["state"] = "disabled"
        self.line_text0["state"] = "disabled"
        
        self.texts.append(self.text)
        self.texts.append(self.line_text0)
        
        # Second text window
        
        # self.windows3 = tk.Frame(self.root,width = self.ws, height = self.hs - 30)
        # self.windows3.place(x = self.ws, y = 30)
        
        self.windows4 = tk.Frame(self.windows1,width = self.all_positions[3][2] / 2, height = self.all_positions[3][3] + 5)
        self.windows4.place(x = self.all_positions[3][2] / 2, y = 0)
        self.windows4.config(bg = "white")
        self.text_windows1 = tk.Frame(self.windows4,width = self.all_positions[3][2] / 2 - 40, height = self.all_positions[3][3] + 5,bg="white")
        # self.text_windows1.place(x = 45, y = 5)
        
        self.set_line_windows1()
        self.text1 = tk.Text(self.text_windows1, font = self.font)   
        self.text1.place(x = 0, y = 0)
        self.text1.pack(fill = BOTH, expand = True)
        self.text_windows1.place(x = 45, y = 5, width = self.all_positions[3][2] / 2 - 40, height = self.all_positions[3][3] + 5)
        self.text_windows1.update()
        self.text1, self.line_text1 = self.get_content(self.file_name + "/" + "Srcfile.java",self.text1,self.line_text1)
        self.text1.bind("<MouseWheel>", self.processWheel1)
        self.text1["state"] = "disabled"
        self.line_text1["state"] = "disabled"
        
        self.texts.append(self.text1)
        self.texts.append(self.line_text1)
            
    
    def destroy(self):
        # messagebox.showinfo(title="提示", message="你还有"+ str(4 - self.count) + "份还未标注")
        self.root.destroy();
    def reset_label(self):
        self.windows0.place(x = self.all_positions[2][0], y = self.all_positions[2][1], width = self.all_positions[2][2], height = self.all_positions[2][3])

    def set_label(self):
        self.all_positions.append([0,0,self.ws,30])
        self.windows0 = tk.Frame(self.root, width = self.all_positions[2][2], height = self.all_positions[2][3], bg = "white")
        self.windows0.place(x = self.all_positions[2][0], y = self.all_positions[2][1])
        self.label = tk.Label(self.windows0, text = str(self.the_index) + " : " +self.file_name.split("/")[-1],fg='black',font=('Arial', 12),bg="white").place(x=10, y=10)
    
    def to_resize(self,nums,dx,dy,sign):
        # print(self.all_positions[1])
        for i in nums:
            self.all_positions[i] = [self.all_positions[i][0], self.all_positions[i][1], self.all_positions[i][2] + sign * dx, self.all_positions[i][3]+dy]
        self.root.place(x = self.all_positions[1][0], y = self.all_positions[1][1], width = self.all_positions[1][2], height = self.all_positions[1][3])
        self.set_two_textWindows()
        self.reset_label()
        # self.bar_buttom.place(x = self.all_positions[4][0], y = self.all_positions[4][1], width = self.all_positions[4][2], height = self.all_positions[4][3])
        # self.bar_right.place(x = self.all_positions[5][0], y = self.all_positions[5][1], width = self.all_positions[5][2], height = self.all_positions[5][3])
    
    def resize_l(self,event,dx):
        self.all_positions[1][0] += dx
        self.all_positions[5][0] += dx
        self.to_resize([0,1,2,3],dx,0,-1)
        
    def resize_t(self,event,dy):
        self.all_positions[4][1] += dy
        self.to_resize([0,1,3,5],0,dy,1)
        
    # def set_adjust(self):
        # self.bar_right.bind("<B1-Motion>", self.resize_l)
        # self.bar_buttom.bind("<B1-Motion>", self.resize_t)
        
    def set_bar_place(self,a_pos,b_pos):
        self.all_positions.append(a_pos)
        self.all_positions.append(b_pos)
        
    def build(self):
        self.all_positions.append([self.root.winfo_screenwidth() - self.ws + 5 , 0 , self.ws,self.hs])
        self.all_positions.append([self.root.winfo_screenwidth() - self.ws + 5 , 0 , self.ws,self.hs])
        # self.root = tk.Frame(self.root, width = self.ws,height = self.hs)
        # self.root.place(x = self.all_positions[1][0], y = self.all_positions[1][1])
        # self.root.config(bg="red")
        self.set_label()
        # self.set_button()
        self.draw_layout()
        # self.set_adjust()