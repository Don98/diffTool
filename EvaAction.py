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
    def __init__(self,newWindow,parent,file_pos,true_root,root,file_name,ws,hs,bar_buttom,bar_right):
        self.newWindow = newWindow
        self.parent = parent
        self.file_pos = file_pos
        self.true_root = true_root
        self.file_name = file_name
        self.buttons = []
        self.Window = root
        self.ws = ws
        self.true_hs = hs
        self.hs = int(hs * 7 / 8)
        self.bar_buttom = bar_buttom
        self.bar_right  = bar_right
        # self.Window = tk.Toplevel(self.root)
        # self.Window.title(method)
        self.all_positions = [[0,hs * 3 , self.ws , hs]]
        # print(self.all_positions[0])
        self.Window.config(bg="black")
        self.Window.place(x = self.all_positions[0][0], y = self.all_positions[0][1], width = self.all_positions[0][2], height = self.all_positions[0][3])
        
        self.the_index = {"Se_actionList":0,"GT_actionList":1,"MTD_actionList":2,"IJM_actionList":3}
        
        # self.colors = ["#FB7299","#5EBA7D","#0074CC","#E8E8ED","#00BFFF","#FDF7E2"]
        self.colors = ["#FB7299","#FB7299","#FB7299","#E8E8ED","#00BFFF","#FDF7E2"]
        
        self.tmp_data = {}
        
        self.set_buttons()
        # self.method = method
        self.win = 0
        self.to_eva("Se_actionList")
        # self.set_size()
        # self.build()
    
    def to_resize(self,nums,dx,dy,sign):
        # print(self.all_positions[0])
        for i in nums:
            self.all_positions[i] = [self.all_positions[i][0], self.all_positions[i][1], self.all_positions[i][2] + sign * dx, self.all_positions[i][3]+ sign * dy]
        self.Window.place(x = self.all_positions[0][0], y = self.all_positions[0][1], width = self.all_positions[0][2], height = self.all_positions[0][3])
        self.set_content_windows()
        # self.bar_buttom.place(x = self.all_positions[4][0], y = self.all_positions[4][1], width = self.all_positions[4][2], height = self.all_positions[4][3])
        # self.bar_right.place(x = self.all_positions[5][0], y = self.all_positions[5][1], width = self.all_positions[5][2], height = self.all_positions[5][3])
        
    def resize_l(self,event,dx):
        # dx = self.xpos() - self.all_positions[5][0]
        # dy = self.ypos() - self.all_positions[5][1]
        self.all_positions[5][0] += dx
        self.to_resize([],dx,0,1)
        
    def resize_t(self,event,dy):
        # dx = self.xpos() - self.all_positions[4][0]
        # dy = self.ypos() - self.all_positions[4][1]
        self.all_positions[0][1] += dy
        self.all_positions[4][1] += dy
        self.to_resize([0,2,3],0,dy,-1)
        
    def set_label(self):
        self.read_file()
        self.label = tk.Label(self.windows0, text='总共需要标注数量为: ' + str(len(self.actionList)),fg='black',font=('Arial', 12),bg="white")
        self.label.place(x = 440, y=4)
        self.draw_layout()
        self.win += 1
        
    def to_eva(self,method):
        # self.evaAction = EvaAction(self.windows1,self.file_name, self.text, self.text0, method, self.buttons)
        self.buttons[self.the_index[method]].config(bg=self.colors[5])
        if(self.win > 0):
            self.buttons[self.the_index[self.method]].config(bg=self.colors[3])
            self.newWindow.scroll([0,0])
            self.tmp_data[self.method] = self.Data
            self.label.config(text='总共需要标注数量为: ')
        self.method = method
        self.Data = Data(self.file_name,self.method)
        self.Data.set_pos(self.the_index[self.method])
        self.set_label()
    # def print_value(self):
        # for i in self.all_points:
            # print(i.get())
            
    def save_points(self):
        methods = ["SE","GT","MTD","IJM"]
        with open(self.file_name + "/points.txt","w") as f: 
            for i , value in enumerate(self.all_points):
                f.write(methods[i] + ":" + str(value.get()) + "\n")
        self.buttons[-1].config(bg=self.colors[3])
        tk.messagebox.showwarning('打分', "本份数据打分完毕，已保存")
        self.parent.set_buttonDiabled(self.file_pos)
        for i in self.buttons:
            i["state"] = tk.DISABLED
        for i in self.checkbuttons:
            i.destroy()
        self.listbox['state'] = tk.DISABLED
        self.points.destroy()
        
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
        
        # methods = [" ","SE","GT","MTD","IJM"]
        methods = [" ","算法0","算法1","算法2","算法3"]
        score_names = ["难以理解","较难理解","中立","较易理解","易于理解"]
        score_pos = [200,280,360,400,480,560]
        self.all_points = [IntVar(),IntVar(),IntVar(),IntVar()]
        for i in range(5):
            tk.Label(self.algorithms_scores, text = methods[i] ,fg='black',font=('Arial', 12),bg="white").place(x = 120,y = 80 + i * 80)
            if(i == 0):
                for j in range(5):
                    tk.Label(self.algorithms_scores, text=score_names[j],fg='black',font=('Arial', 12),bg="white").place(x = score_pos[j] , y = 80 + i * 80)
            else:
                for j in range(5):
                    Radiobutton(self.algorithms_scores,text = "",variable=self.all_points[i-1],value=j,bg = "white").place(x = 240 + 60 * j , y = 80 + i * 80)
        self.point_button_save = tk.Button(self.algorithms_scores,width=10, height=1, text='保存打分结果', bg=self.colors[4], command = self.save_points)
        self.point_button_save.place(x = 320, y = 480)
        
    def set_buttons(self):
    
        
        self.selected_indices = -1
        self.checkbuttons = []
        self.buttons_var = []
        self.actionList =[]
        self.all_positions.append([0,0,self.ws,30])
        self.windows0 = tk.Frame(self.Window, width = self.all_positions[1][2], height = self.all_positions[1][3],bg="white")
        self.windows0.place(x = self.all_positions[1][0], y = self.all_positions[1][1])
        self.buttons = []
        # self.button0 = tk.Button(self.windows0,width=10, height=1, text='SE-Mapping', bg=self.colors[4], command=partial(self.to_eva,"Se_actionList"))
        # self.button1 = tk.Button(self.windows0,width=10, height=1, text='GT', bg=self.colors[4], command = partial(self.to_eva,"GT_actionList"))
        # self.button2 = tk.Button(self.windows0,width=10, height=1, text='MTD', bg=self.colors[4], command = partial(self.to_eva,"MTD_actionList"))
        # self.button3 = tk.Button(self.windows0,width=10, height=1, text='IJM', bg=self.colors[4], command = partial(self.to_eva,"IJM_actionList"))
        self.button0 = tk.Button(self.windows0,width=10, height=1, text='算法0', bg=self.colors[4], command=partial(self.to_eva,"Se_actionList"))
        self.button0.place(x = 0, y = 2)
        self.button1 = tk.Button(self.windows0,width=10, height=1, text='算法1', bg=self.colors[4], command = partial(self.to_eva,"GT_actionList"))
        self.button1.place(x = 80, y = 2)
        self.button2 = tk.Button(self.windows0,width=10, height=1, text='算法2', bg=self.colors[4], command = partial(self.to_eva,"MTD_actionList"))
        self.button2.place(x = 160, y = 2)
        self.button3 = tk.Button(self.windows0,width=10, height=1, text='算法3', bg=self.colors[4], command = partial(self.to_eva,"IJM_actionList"))
        self.button3.place(x = 240, y = 2)
        self.button4 = tk.Button(self.windows0,width=10, height=1, text='打分', bg=self.colors[4], command = self.point_algorithm)
        self.button4.place(x = 320, y = 2)
        self.buttons.append(self.button0)
        self.buttons.append(self.button1)
        self.buttons.append(self.button2)
        self.buttons.append(self.button3)
        self.buttons.append(self.button4)
            
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
        # print(parts,two_nums)
        return [int(i) for i in two_nums]
        
        
    def items_selected(self,event):
        selected_indices = self.listbox.curselection()
        action = ",".join([self.listbox.get(i) for i in selected_indices])
        try:
            two_nums = self.get_pos(action)
            self.newWindow.scroll(two_nums)
            self.draw_tokens(selected_indices[0])
            # print(selected_indices[0])
            # self.listbox.itemconfig(selected_indices[0],bg="#5395a4")
            self.listbox.itemconfig(selected_indices[0],bg=self.colors[0])
            self.selected_indices = selected_indices[0]
        except:
            print(action)

    def select_all(self):
        if(self.buttons_var[self.selected_indices][0].get() == 0):
            for i in range(len(self.buttons_var[self.selected_indices][1:])):
                self.buttons_var[self.selected_indices][1 + i].set(0)
        if(self.buttons_var[self.selected_indices][0].get() == 1):
            for i in range(len(self.buttons_var[self.selected_indices][1:])):
                self.buttons_var[self.selected_indices][1 + i].set(1)
        self.Data.updated_buttonvar(self.buttons_var)

    def draw_tokens(self,index):
        tokenNum = []
        # print(index,self.tokenNums)
        for i in self.tokenNums:
            for j in i:
                if(j[0] == index):
                    tokenNum.append(j[1])
        # print(tokenNum)
        for i in self.checkbuttons:
            i.destroy()
        # print(len(self.buttons_var),self.selected_indices)
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
            self.checkbuttons.append(tk.Checkbutton(self.token_frame.viewPort, text = str(nums+1) + "/" + str(len(all_tokens)) + " " + i, variable = self.buttons_var[index][nums], onvalue = 1, offvalue = 0, height=1,width = int(3 * self.all_positions[3][2] / 4),bg="white"))
            self.checkbuttons[-1].grid(column = 0, columnspan = 2)
            self.checkbuttons[-1].bind("<MouseWheel>", self.token_frame.processWheel)
            self.checkbuttons[-1].config(anchor = "w")
            # self.checkbuttons[-1].select()
            nums += 1
            
        for i in tokenNum:
            self.checkbuttons[i].config(bg = "#FB7299")
        self.checkbuttons[0]['command'] = self.select_all;
        self.set_button()

    def set_content_windows(self):
        self.content_windows.place(x = self.all_positions[2][0], y = self.all_positions[2][1], width = self.all_positions[2][2], height = self.all_positions[2][3])
        self.token_windows.place(x = self.all_positions[3][2], y = self.all_positions[3][1], width = self.all_positions[3][2], height = self.all_positions[3][3])
        self.listbox.pack(fill = BOTH, expand = True)
        self.stmts_windows.place(x = self.all_positions[3][0], y = self.all_positions[3][1], width = self.all_positions[3][2], height = self.all_positions[3][3])
        self.stmts_windows.update()
        
    def draw_layout(self):
        self.all_positions.append([0,30,self.ws,self.hs - 30])
        self.content_windows = tk.Frame(self.Window, width = self.all_positions[2][2], height = self.all_positions[2][3],bg="white")
        
        self.all_positions.append([0,0,int(self.ws / 2),self.hs - 60])
        self.stmts_windows = tk.Frame(self.content_windows, width = self.all_positions[3][2], height = self.all_positions[3][3],bg="white")
        self.token_windows = tk.Frame(self.content_windows, width = self.all_positions[3][2], height = self.all_positions[3][3],bg="white")
        
        self.all_stmts = tk.StringVar(value=self.stmts)

        self.listbox = tk.Listbox(self.stmts_windows,listvariable=self.all_stmts,selectmode='single',bg = "white",selectbackground = self.colors[0])
        self.listbox.pack(fill = BOTH, expand = True)
        self.set_content_windows()
        self.listbox.bind('<<ListboxSelect>>', self.items_selected)
        # if(self.the_index[self.method] != 0):
        for i in range(len(self.stmtNums)):
            self.set_buttons_color(self.stmtNums[len(self.stmtNums) - i - 1],self.colors[len(self.stmtNums) - i - 1])
        
        self.all_positions.append([0 , self.true_hs * 3 - 5 , self.ws , 5])
        self.all_positions.append([self.ws / 8 , 0 , 5 , self.true_hs * 3])
        # print(self.all_positions[5])
      
    def get_win(self):
        return self.win
          
    def confirm(self):
        self.Data.updated_buttonvar(self.buttons_var)
        self.Data.update()
        self.Data.save_file()
        methods = ["Se_actionList","GT_actionList","MTD_actionList","IJM_actionList"]
        # index = methods.index(self.method)
        # self.dest11roy()
    
    def __destroy__(self):
        self.confirm()
        
    def destroy(self):
        self.newWindow.scroll([0,0])
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
        self.button2 = tk.Button(self.windows0,width=10, height=1, text='Token反选', bg=self.colors[4], command=self.dechose)
        self.button2.place(x = self.all_positions[3][2], y = 0)
    
    def set_buttons_color(self,StmtsNums,color):
        for i in StmtsNums:
            self.listbox.itemconfig(i,bg=color)
    
    def update_data(self):
        self.stmtNums = []
        self.tokenNums = []
        for i in self.the_index.keys():
            # print(self.tmp_data)
            if(i in self.tmp_data.keys() and self.the_index[i] < self.the_index[self.method]):
                StmtsNums, TokenNums = self.Data.updateUsingData(self.tmp_data[i])
                self.stmtNums.append(StmtsNums)
                self.tokenNums.append(TokenNums)
                # self.set_buttons_color(StmtsNums,TokenNums)
            if(i in self.tmp_data.keys() and self.the_index[i] == self.the_index[self.method]):
                StmtsNums, TokenNums = self.Data.updateUsingData(self.tmp_data[i])
    
    def read_file(self):
        self.stmts, self.tokens, self.actionList = self.Data.read_file()
        # print(self.Data.get_stmts())
        for i , stmt in enumerate(self.stmts):
            self.stmts[i] = str(i) + " : " + stmt
        self.Data.create_read_resultfile()
        self.Data.split_data()
        self.buttons_var = self.Data.create_buttonvar()
        # print(self.Data.get_stmts())
        self.update_data()
        
        # print(self.buttons_var)
        # print(len(self.stmts))
        # print(len(self.buttons_var))
            
    
    def build(self):
        pass
        # self.set_button()
        # self.draw_layout()