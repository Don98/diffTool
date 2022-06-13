import difflib
import tkinter as tk
import tkinter.filedialog
from functools import partial
from tkinter.messagebox import showinfo
from Data import Data
import os
from tkinter import *
class ScrollFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent) # create a frame (self)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")      # Canvas to scroll
        self.viewPort = tk.Frame(self.canvas, background="#ffffff")     # This frame will hold the child widgets
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview) 
        self.canvas.configure(yscrollcommand=self.vsb.set)      # Attach scrollbar action to scroll of canvas

        
        self.vsb.bind("<MouseWheel>", self.processWheel)
        self.vsb.pack(side="right", fill="y")       # Pack scrollbar to right - change as needed
        self.canvas.pack(side="left", fill="both", expand=True)     # Pack canvas to left and expand to fill - change as needed
        self.canvas_window = self.canvas.create_window(
            (0,0), 
            window=self.viewPort, 
            anchor="nw",            
            tags="self.viewPort",
            )       # Add view port frame to canvas

        self.viewPort.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)
        self.first = True
        self.onFrameConfigure(None) # Initial stretch on render

    def processWheel(self,event):
        a= int(-(event.delta)/60)
        self.canvas.yview_scroll(a,'units')
        
    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)

    def on_mousewheel(self, event):
        '''Allows the mousewheel to control the scrollbar'''
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def bnd_mousewheel(self):
        '''Binds the mousewheel to the scrollbar'''
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def unbnd_mousewheel(self):
        '''Unbinds the mousewheel from the scrollbar'''
        self.canvas.unbind_all("<MouseWheel>")

    def delete_all(self):
        '''Removes all widgets from the viewPort, only works if grid was used'''
        children = self.viewPort.winfo_children()
        for child in children:
            child.grid_remove() 
class EvaAction():
    def __init__(self,true_root,root,file_name,text,text0,ws,hs,bar_buttom,bar_right):
        self.true_root = true_root
        self.file_name = file_name
        self.buttons = []
        self.Window = root
        self.ws = ws
        self.hs = int(hs * 7 / 8)
        self.bar_buttom = bar_buttom
        self.bar_right  = bar_right
        # self.Window = tk.Toplevel(self.root)
        # self.Window.title(method)
        self.text = text
        self.text0= text0
        self.all_positions = [[]]
        
        
        self.the_index = {"Se_actionList":0,"GT_actionList":1,"MTD_actionList":2,"IJM_actionList":3}
        
        
        self.selected_indices = -1
        self.checkbuttons = []
        self.buttons_var = []
        self.actionList =[]
        
        self.set_buttons()
        # self.method = method
        self.win = 0
        self.pos = 0
        self.pos0= 0
        self.to_eva("Se_actionList")
        # self.set_size()
        # self.build()
    
    def set_label(self):
        self.read_file()
        # self.label = tk.Label(self.windows0, text='总共需要标注数量为：' + str(len(self.actionList)),fg='black',font=('Arial', 12)).place(x=self.all_positions[0][2], y=0)
        # print(int(self.all_positions[1][2] / 2) - 340)
        # self.label = tk.Label(self.windows0, text='总共需要标注数量为：' + str(len(self.actionList)),fg='black',font=('Arial', 12),bg="white",width = int(self.all_positions[1][2] / 2),height=1).place(x = 340, y=4)
        self.label = tk.Label(self.windows0, text='总共需要标注数量为：' + str(len(self.actionList)),fg='black',font=('Arial', 12),bg="white").place(x = 440, y=4)
        self.draw_layout()
        self.win += 1
    
    def to_eva(self,method):
        # self.evaAction = EvaAction(self.windows1,self.file_name, self.text, self.text0, method, self.buttons)
        if(self.win > 0):
            self.confirm()
        self.method = method
        self.Data = Data(self.file_name,self.method)
        self.Data.set_pos(self.the_index[self.method])
        self.set_label()
    def print_value(self):
        for i in self.all_points:
            print(i.get())
    def save_points(self):
        pass
    def point_algorithm(self):
        self.confirm()
        self.points = tk.Toplevel(self.true_root)
        self.points.title("打分")
        self.points.geometry()
        w = 720 ; h = 700
        a = self.true_root.winfo_screenwidth()
        b = self.true_root.winfo_screenheight()
        x = (a/2) - (w/2)
        y = (b/2) - (h/2)
        self.points.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.point_window = tk.Frame(self.points,width = w, height = h)
        self.point_window.place(x = 0, y = 0)
        self.title_tips = tk.Frame(self.point_window,width = w, height = h / 6)
        self.title_tips.place(x = 0,y = 0)
        self.title_tips.config(bg = "white")
        self.title_label0 = tk.Label(self.title_tips, text='为工具打分，分数越高，表示越容易理解',fg='black',font=('Arial', 12),bg="white")
        self.title_label0.place(x = 200, y= 10)
        self.title_label1 = tk.Label(self.title_tips, text='如果认为两个工具一样好，就打一样分数',fg='black',font=('Arial', 12),bg="white")
        self.title_label1.place(x = 200, y= 50)
        self.title_label2 = tk.Label(self.title_tips, text='(难以理解) 0 --> 4 (易于理解)',fg='black',font=('Arial', 12),bg="white")
        self.title_label2.place(x = 240, y= 90)
        
        self.algorithms_scores = tk.Frame(self.point_window,width = w, height = h - h / 6)
        self.algorithms_scores.place(x = 0, y = h / 6)
        self.algorithms_scores.config(bg = "white")
        
        methods = [" ","SE","GT","MTD","IJM"]
        self.all_points = [IntVar(),IntVar(),IntVar(),IntVar()]
        for i in range(5):
            tk.Label(self.algorithms_scores, text = methods[i] ,fg='black',font=('Arial', 12),bg="white").place(x = 120,y = 80 + i * 80)
            if(i == 0):
                for j in range(5):
                    tk.Label(self.algorithms_scores, text=str(j),fg='black',font=('Arial', 12),bg="white").place(x = 240 + 60 * j , y = 80 + i * 80)
            else:
                for j in range(5):
                    Radiobutton(self.algorithms_scores,text = "",variable=self.all_points[i-1],value=j,command=self.print_value,bg = "white").place(x = 240 + 60 * j , y = 80 + i * 80)
        self.point_button_save = tk.Button(self.algorithms_scores,width=10, height=1, text='保存打分结果', bg='#00BFFF', command = self.save_points)
        self.point_button_save.place(x = 320, y = 480)
        
    def set_buttons(self):
        self.all_positions.append([0,0,self.ws,30])
        self.windows0 = tk.Frame(self.Window, width = self.all_positions[1][2], height = self.all_positions[1][3],bg="white")
        self.windows0.place(x = self.all_positions[1][0], y = self.all_positions[1][1])
        self.buttons = []
        self.button0 = tk.Button(self.windows0,width=10, height=1, text='SE-Mapping', bg='#00BFFF', command=partial(self.to_eva,"Se_actionList"))
        self.button0.place(x = 0, y = 2)
        self.button1 = tk.Button(self.windows0,width=10, height=1, text='GT', bg='#00BFFF', command = partial(self.to_eva,"GT_actionList"))
        self.button1.place(x = 80, y = 2)
        self.button2 = tk.Button(self.windows0,width=10, height=1, text='MTD', bg='#00BFFF', command = partial(self.to_eva,"MTD_actionList"))
        self.button2.place(x = 160, y = 2)
        self.button3 = tk.Button(self.windows0,width=10, height=1, text='IJM', bg='#00BFFF', command = partial(self.to_eva,"IJM_actionList"))
        self.button3.place(x = 240, y = 2)
        self.button4 = tk.Button(self.windows0,width=10, height=1, text='打分', bg='#00BFFF', command = self.point_algorithm)
        self.button4.place(x = 320, y = 2)
        self.buttons.append(self.button0)
        self.buttons.append(self.button1)
        self.buttons.append(self.button2)
        self.buttons.append(self.button3)
        self.buttons.append(self.button4)
        
    # def set_size(self):
        # self.w = 720 ; self.h = 700
        # self.ws = self.root.winfo_screenwidth()
        # self.hs = self.root.winfo_screenheight()
        # x = (self.ws/2) - (self.w/2)
        # y = (self.hs/2) - (self.h/2)
        # self.Window.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
            
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
        self.listbox.itemconfig(selected_indices[0],bg="#5395a4")
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
        
        self.token_frame = ScrollFrame(self.token_windows)
        self.token_frame.place(x = 0, y = 0, width = int(3 * self.all_positions[3][2] / 4), height = self.all_positions[3][3])
        self.token_frame.delete_all()
        for i in all_tokens:
            self.checkbuttons.append(tk.Checkbutton(self.token_frame.viewPort, text = str(nums) + "/" + str(len(all_tokens)) + " " + i, variable = self.buttons_var[index][nums], onvalue = 1, offvalue = 0, height=1,width = int(3 * self.all_positions[3][2] / 4),bg="white"))
            self.checkbuttons[-1].grid(column = 0, columnspan = 2)
            self.checkbuttons[-1].bind("<MouseWheel>", self.token_frame.processWheel)
            self.checkbuttons[-1].config(anchor = "w")
            # self.checkbuttons[-1].select()
            nums += 1
        self.checkbuttons[0]['command'] = self.select_all;
        self.set_button()


    def draw_layout(self):
        self.all_positions.append([0,30,self.ws,self.hs - 30])
        self.content_windows = tk.Frame(self.Window, width = self.all_positions[2][2], height = self.all_positions[2][3],bg="white")
        self.content_windows.place(x = self.all_positions[2][0], y = self.all_positions[2][1])
        
        self.all_positions.append([0,0,int(self.ws / 2),self.hs - 30])
        self.stmts_windows = tk.Frame(self.content_windows, width = self.all_positions[3][2], height = self.all_positions[3][3],bg="white")
        self.token_windows = tk.Frame(self.content_windows, width = self.all_positions[3][2], height = self.all_positions[3][3],bg="white")
        self.token_windows.place(x = self.all_positions[3][2], y = self.all_positions[3][1])
        
        # self.content_windows.config(bg = "red")
        
        self.all_stmts = tk.StringVar(value=self.stmts)

        self.listbox = tk.Listbox(self.stmts_windows,listvariable=self.all_stmts,selectmode='single')
        self.listbox.pack(fill = BOTH, expand = True)
        self.stmts_windows.place(x = self.all_positions[3][0], y = self.all_positions[3][1], width = self.all_positions[3][2], height = self.all_positions[3][3])
        self.stmts_windows.update()
        self.stmts_windows.config(bg = "green")
        self.listbox.bind('<<ListboxSelect>>', self.items_selected) 
      
    def get_win(self):
        return self.win
          
    def confirm(self):
        self.Data.updated_buttonvar(self.buttons_var)
        self.Data.update()
        self.Data.save_file()
        methods = ["Se_actionList","GT_actionList","MTD_actionList","IJM_actionList"]
        # index = methods.index(self.method)
        self.buttons[self.the_index[self.method]].config(bg="#E8E8ED")
        # self.dest11roy()
    
    def __destroy__(self):
        self.confirm()
        
    def destroy(self):
        self.scroll([0,0])
        self.Window.destroy();
        
    def reset(self):
        pass
    
    def dechose(self):
        for i in range(len(self.buttons_var[self.selected_indices][1:])):
            # print(1 - self.buttons_var[self.selected_indices][1 + i].get())
            self.buttons_var[self.selected_indices][1 + i].set(1 - self.buttons_var[self.selected_indices][1 + i].get())
        self.Data.updated_buttonvar(self.buttons_var)
        
    def set_button(self):
        # self.button0 = tk.Button(self.Window,width=10, height=1, text='修改', bg='skyblue', command=self.reset).place(x = 630, y = 120)
        # self.button1 = tk.Button(self.token_windows,width=10, height=1, text='保存并退出', bg='#E8F6FF', command=self.confirm)
        # self.button1.place(x = int(6.5 * self.all_positions[3][2] / 8), y = self.all_positions[3][3] / 2 - 50)
        self.button2 = tk.Button(self.windows0,width=10, height=1, text='Token反选', bg='#00BFFF', command=self.dechose)
        self.button2.place(x = self.all_positions[3][2], y = 0)
    
    def read_file(self):
        self.stmts, self.tokens, self.actionList = self.Data.read_file()
        for i , stmt in enumerate(self.stmts):
            self.stmts[i] = str(i) + " : " + stmt
        self.Data.create_read_resultfile()
        self.Data.split_data()
        self.buttons_var = self.Data.create_buttonvar()
        # print(len(self.stmts))
        # print(len(self.buttons_var))
            
    
    def build(self):
        pass
        # self.set_button()
        # self.draw_layout()