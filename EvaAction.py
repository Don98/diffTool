import difflib
import tkinter as tk
import tkinter.filedialog
from functools import partial
from tkinter.messagebox import showinfo
from ComBoPicker import Combopicker
from Data import Data
import os

class EvaAction():
    def __init__(self,root,file_name,text,text0,method,buttons):
        self.file_name = file_name
        self.buttons = buttons
        self.root = root
        self.Window = tk.Toplevel(self.root)
        self.Window.title(method)
        self.text = text
        self.text0= text0
        self.method = method
        self.win = 0
        self.pos = 0
        self.pos0= 0
        
        self.the_index = {"Se_actionList":0,"GT_actionList":1,"MTD_actionList":2,"IJM_actionList":3}
        
        self.Data = Data(self.file_name,self.method)
        self.Data.set_pos(self.the_index[self.method])
        
        self.selected_indices = -1
        self.checkbuttons = []
        self.buttons_var = []
        self.actionList =[]
        self.set_size()
        self.build()
        
    def set_size(self):
        self.w = 720 ; self.h = 650
        self.ws = self.root.winfo_screenwidth()
        self.hs = self.root.winfo_screenheight()
        x = (self.ws/2) - (self.w/2)
        y = (self.hs/2) - (self.h/2)
        self.Window.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
            
    def get_pos(self,action):
        parts = action.split(" => ")
        two_nums = []
        if(len(parts) == 1):
            num = parts[0][parts[0].find("LINE:") + 6:-1]
            two_nums.append(num)
            two_nums.append(num)
        else:
            two_nums.append(parts[0][parts[0].find("LINE:") + 6:-1])
            two_nums.append(parts[1][parts[1].find("LINE:") + 6:-1])
        return [int(i) for i in two_nums]
        
    def scroll(self, two_nums):
        self.text.yview_scroll(two_nums[0] - self.pos, "units")
        self.text0.yview_scroll(two_nums[1] - self.pos0, "units")
        self.pos += two_nums[0] - self.pos
        self.pos0+= two_nums[1] - self.pos0
        
    def items_selected(self,event):
        selected_indices = self.listbox.curselection()
        action = ",".join([self.listbox.get(i) for i in selected_indices])
        two_nums = self.get_pos(action)
        self.scroll(two_nums)
        self.draw_tokens(selected_indices[0])
        self.selected_indices = selected_indices[0]

    def select_all(self):
        if(self.buttons_var[self.selected_indices][0].get() == 0):
            for i in range(len(self.buttons_var[self.selected_indices][1:])):
                self.buttons_var[self.selected_indices][1 + i].set(0)
        if(self.buttons_var[self.selected_indices][0].get() == 1):
            for i in range(len(self.buttons_var[self.selected_indices][1:])):
                self.buttons_var[self.selected_indices][1 + i].set(1)
        self.Data.updated_buttonvar(self.buttons_var)

    def draw_tokens(self,index):
        for i in self.checkbuttons:
            i.destroy()
        if(self.selected_indices != -1):
            tmp = []
            for i in self.buttons_var[self.selected_indices]:
                tmp.append(i.get())
            if(len(self.actionList[self.selected_indices]) < 3):
                self.actionList[self.selected_indices].append(tmp)
            else:
                self.actionList[self.selected_indices][2] = tmp
            self.Data.updated_buttonvar(self.buttons_var)
        self.checkbuttons = []
        all_tokens = [self.actionList[index][0]] + self.actionList[index][1]
        nums = 0
        for i in all_tokens:
            # print(i,len(self.buttons_var))
            self.checkbuttons.append(tk.Checkbutton(self.Window, text = i, variable = self.buttons_var[index][nums], onvalue = 1, offvalue = 0, height=1,width = 90,bg="white"))
            self.checkbuttons[-1].place(x = 40, y = 320 + 20 * nums)
            self.checkbuttons[-1].config(anchor = "w")
            # self.checkbuttons[-1].select()
            nums += 1
        self.checkbuttons[0]['command'] = self.select_all;


    def draw_layout(self):
        self.all_stmts = tk.StringVar(value=self.stmts)

        self.listbox = tk.Listbox(self.Window,listvariable=self.all_stmts,width = 80, height=12,selectmode='single')
        self.listbox.pack()
        self.listbox.place(x = 60 , y = 80)
        self.listbox.bind('<<ListboxSelect>>', self.items_selected) 


    def to_eva(self,method):
        pass
      
    def get_win(self):
        return self.win
          
    def confirm(self):
        self.Data.updated_buttonvar(self.buttons_var)
        self.Data.update()
        self.Data.save_file()
        methods = ["Se_actionList","GT_actionList","MTD_actionList","IJM_actionList"]
        index = methods.index(self.method)
        self.buttons[index].config(bg="grey")
        self.win = 1
        self.destroy()
    
    def __destroy__(self):
        self.confirm()
        
    def destroy(self):
        self.Window.destroy();
        
    def reset(self):
        pass
    def set_button(self):
        # self.button0 = tk.Button(self.Window,width=10, height=1, text='修改', bg='skyblue', command=self.reset).place(x = 630, y = 120)
        self.button1 = tk.Button(self.Window,width=10, height=1, text='保存并退出', bg='skyblue', command=self.confirm).place(x = 80, y = 620)
    
    def read_file(self):
        self.stmts, self.tokens, self.actionList = self.Data.read_file()
        self.Data.create_read_resultfile()
        self.Data.split_data()
        self.buttons_var = self.Data.create_buttonvar()
        # print(len(self.stmts))
        # print(len(self.buttons_var))
            
    
    def build(self):
        self.read_file()
        self.label = tk.Label(self.Window, text='总共需要标注数量为：' + str(len(self.actionList)),fg='black',font=('Arial', 12)).place(x=30, y=30)
        self.set_button()
        self.draw_layout()