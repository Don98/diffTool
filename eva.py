import difflib
import tkinter as tk
import tkinter.filedialog
from functools import partial
import os
from tkinter import *
from tkinter import scrolledtext
from threading import Thread, RLock
import idlelib.colorizer as idc
import idlelib.percolator as idp

class Eva():
    def __init__(self,root,file_name):
        self.file_name = file_name
        self.root = root
        self.Window = tk.Toplevel(self.root)
        
        self.set_size()
        self.build()
        
    def set_size(self):
        self.w = self.root.winfo_screenwidth() * 3 / 4; self.h = self.root.winfo_screenheight() * 3 / 4
        self.ws = self.root.winfo_screenwidth()
        self.hs = self.root.winfo_screenheight()
        x = (self.ws/2) - (self.w/2)
        y = (self.hs/2) - (self.h/2)
        self.Window.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
            
    # def draw_text():        
    def get_content(self,file_name):
        with open(self.file_name + "/" + "Srcfile.java","r") as f:
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
            content = ""
            pos = 1
            for i in data:
                content += str(pos).ljust(nums," ") + i
                pos += 1
            return content
            
    def draw_layout(self):
        self.text = []
        self.text = tk.Text(self.Window,width = 95,height = 53,font = 10)   
        data = self.get_content(self.file_name + "/" + "Srcfile.java")
        self.text.insert(0.0,data)
    
        self.text.pack()
        self.text.place(x=5,y=10)
        # idc.color_config(self.text)
        # self.text.focus_set()
        # p = idp.Percolator(self.text)
        # d = idc.ColorDelegator()
        # p.insertfilter(d)

        self.text["state"] = "disabled"
        nums = 50 * 100
        self.text.yview_scroll(nums, "units")
        
        
        self.text0 = tk.Text(self.Window,width = 95,height = 53,font = 10)
        # scroll0 = tk.Scrollbar(self.text0)
        # scroll0.pack(side=tk.RIGHT,fill=tk.Y)
         
        # scroll0.config(command=self.text0.yview)
        # self.text0.config(yscrollcommand=scroll0.set)
        
        data = self.get_content(self.file_name + "/" + "Dstfile.java")
        
        self.text0.insert(0.0,data)
    
        self.text0.pack()
        self.text0.place(x=970,y=10)
        self.text0["state"] = "disabled"
            
        
    def draw_layout123(self):
        self.edit_frame = Canvas(self.Window, height=200, width=400,
                                 bg="white", highlightthickness=0)
        self.edit_frame.pack()
        self.line_text = Text(self.edit_frame, width=7, height=200, spacing3=5,
                              bg="#DCDCDC", bd=0, font=("等线等线 (Light)", 14), takefocus=0, state="disabled",
                              cursor="arrow")
        self.line_text.pack(side="left", expand="no")
        self.update()
        self.edit_text = scrolledtext.ScrolledText(self.edit_frame, height=1, wrap="none", spacing3=5,
                                                   width=self.winfo_width() - self.line_text.winfo_width(), bg="white",
                                                   bd=0, font=("等线等线 (Light)", 14), undo=True, insertwidth=1)
        self.edit_text.vbar.configure(command=self.scroll)
        self.edit_text.pack(side="left", fill="both")
        self.line_text.bind("<MouseWheel>", self.wheel)
        self.edit_text.bind("<MouseWheel>", self.wheel)
        self.edit_text.bind("<Control-v>", lambda e: self.get_txt_thread())
        self.edit_text.bind("<Control-V>", lambda e: self.get_txt_thread())
        self.edit_text.bind("<Key>", lambda e: self.get_txt_thread())
        self.show_line()

    def wheel(self, event):
        self.line_text.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.edit_text.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    def scroll(self, *xy):
        self.line_text.yview(*xy)
        self.edit_text.yview(*xy)

    def get_txt_thread(self):
        Thread(target=self.get_txt).start()

    def get_txt(self):
        self.thread_lock.acquire()
        if self.txt != self.edit_text.get("1.0", "end")[:-1]:
            self.txt = self.edit_text.get("1.0", "end")[:-1]
            self.show_line()
        else:
            self.thread_lock.release()

    def show_line(self):
        sb_pos = self.edit_text.vbar.get()
        self.line_text.configure(state="normal")
        self.line_text.delete("1.0", "end")
        txt_arr = self.txt.split("\n")
        if len(txt_arr) == 1:
            self.line_text.insert("1.1", " 1")
        else:
            for i in range(1, len(txt_arr) + 1):
                self.line_text.insert("end", " " + str(i))
                if i != len(txt_arr):
                    self.line_text.insert("end", "\n")
        if len(sb_pos) == 4:
            self.line_text.yview_moveto(0.0)
        elif len(sb_pos) == 2:
            self.line_text.yview_moveto(sb_pos[0])
            self.edit_text.yview_moveto(sb_pos[0])
        self.line_text.configure(state="disabled")
        try:
            self.thread_lock.release()
        except RuntimeError:
            pass
        

    def build(self):
        self.draw_layout()