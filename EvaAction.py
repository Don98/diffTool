import difflib
import tkinter as tk
import tkinter.filedialog
from functools import partial
from tkinter.messagebox import showinfo
from ComBoPicker import Combopicker
import os

class EvaAction():
    def __init__(self,root,file_name,text,text0,method):
        self.file_name = file_name
        self.root = root
        self.Window = tk.Toplevel(self.root)
        self.text = text
        self.text0= text0
        self.method = method
        self.pos = 0
        self.pos0= 0
        
        self.checkbuttons = []
        self.buttons_var = []
        self.set_size()
        self.build()
        self.selected_indices = -1
        self.the_index = {"Se_actionList":0,"GT_actionList":1,"MTD_actionList":2,"IJM_actionList":3}
        
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
            for i in self.buttons_var[self.selected_indices][1:]:
                i.set(0)
        if(self.buttons_var[self.selected_indices][0].get() == 1):
            for i in self.buttons_var[self.selected_indices][1:]:
                i.set(1)

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
        self.checkbuttons = []
        all_tokens = [self.actionList[index][0]] + self.actionList[index][1]
        nums = 0
        for i in all_tokens:
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
        
    def update_record(self,data):
        data[0] = data[0][0]
        for i in range(1,len(data)):
            for j in range(len(data[i])):
                if(j == 0):
                    data[i][j][1] = str(self.buttons_var[i-1][0].get())
                    if(len(self.buttons_var[i-1]) > 1):
                        data[i][j][3] = str(self.buttons_var[i-1][1].get())
                    else:
                        data[i][j][3] = ""
                else:
                    data[i][j][3] = str(self.buttons_var[i-1][j+1].get())
        return data
    
    def first_write(self):
        records = []
        for i in range(len(self.stmts)):
            record = []
            tmp = []
            if(len(self.tokens[i]) >= 1):
                tmp.extend([self.stmts[i].replace(","," "),str(self.buttons_var[i][0].get()),self.tokens[i][0].replace(","," "),str(self.buttons_var[i][1].get())])
            else:
                tmp = [self.stmts[i].replace(","," "),str(self.buttons_var[i][0].get()),"",""]
            record.append(tmp)
            for j in range(1,len(self.tokens[i])):
                # print(i,j,len(self.tokens[i]),len(self.buttons_var[i]))
                record.append(["","",self.tokens[i][j].replace(","," "),str(self.buttons_var[i][j + 1].get())])
            records.append(record)
        return records
        
    def save_file(self,data,the_pos):
        # with open()
        content = ""
        # print(len(data))
        for i in range(len(data)):
            if(i != the_pos and i != 3):
                content += data[i]
                content += "=" * 50 + "\n"
            elif(i != the_pos and i == 3):
                content += data[i] + "\n"
            else:
                print(data[i][0][0])
                content += data[i][0][0] + "\n"
                content += "-" * 50 + "\n"
                for j in range(1,len(data[i])):
                    for p in range(len(data[i][j])):
                        content += ",".join(data[i][j][p]) + "\n"
                    content += "-" * 50 + "\n"
                if(i != 3):
                    content += "=" * 50 + "\n"
                
            
        with open(self.file_name + "/" + "result.txt","w") as f:
            f.write(content)
        
    def split_data(self,data,the_pos):
        data = data.split("="*50 + "\n")
        data[the_pos] = data[the_pos].split("-"*50 + "\n")[:-1]
        for j in range(len(data[the_pos])):
            data[the_pos][j] = data[the_pos][j].split("\n")[:-1]
            for p in range(len(data[the_pos][j])):
                data[the_pos][j][p] = data[the_pos][j][p].split(",")
        return data
                
    def confirm(self):
        path = self.file_name + "/" + "result.txt"
        methods = ["SE_Mapping","GT","MTD","IJM"]
        if(not os.path.isfile(path)):
            with open(path, "w") as f:            
                f.write(methods[0]+"\n")
                f.write("-"*50 + "\n")
                for i in methods[1:]:
                    f.write("="*50 + "\n")
                    f.write(i+"\n")
                    f.write("-"*50 + "\n")
        with open(path, "r") as f:
            data = f.read()
        the_pos = self.the_index[self.method]
        data = self.split_data(data,the_pos)
        if(len(data[the_pos]) == 1):
            data[the_pos] = self.first_write()
            data[the_pos].insert(0,[methods[the_pos]])
        else:  
            data[the_pos] = self.update_record(data[the_pos])
        self.save_file(data,the_pos)
        self.destroy()
    
    def destroy(self):
        self.Window.destroy();
        
    def reset(self):
        pass
        # self.all_stmts[self.selected_indices]["state"] = "None"
        # self.listbox.select_set(self.selected_indices)
        
    def set_button(self):
        self.button0 = tk.Button(self.Window,width=10, height=1, text='修改', bg='skyblue', command=self.reset).place(x = 630, y = 120)
        self.button1 = tk.Button(self.Window,width=10, height=1, text='确认', bg='skyblue', command=self.confirm).place(x = 80, y = 600)
    
    def read_file(self):
        filepath = self.file_name + "/" + self.method + ".txt"
        with open(filepath, "r") as f:
            data = f.read().split("==================================================")
        self.stmts = []
        self.tokens= []
        tmp   = []
        for i in data[1:]:
            i = i.split("TOKEN MAPPING:")
            if(len(i) == 1):
                self.stmts.append(i[0].strip())
                self.tokens.append([])
            else:
                self.stmts.append(i[0].strip())
                tmp = []
                for j in i[1].split("\n"):
                    tmp.append(j.strip())
                self.tokens.append(tmp)
        self.actionList = []
        for i in range(len(self.tokens)):
            if(len(self.tokens[i]) >= 1):
                self.tokens[i] = self.tokens[i][1:]
            if(len(self.tokens) == 1 and self.tokens[i][0] == ""):
                self.tokens[i] = []
            for j in range(len(self.tokens[i])):
                if(self.tokens[i][j] == ""):
                    self.tokens[i].pop(j)
        for i in range(len(self.tokens)):
            buton_var = [tk.IntVar()]
            buton_var[-1].set(1)
            for j in self.tokens[i]:
                buton_var.append(tk.IntVar())
                buton_var[-1].set(1)
            self.buttons_var.append(buton_var)
        for i in range(len(self.stmts)):
            self.actionList.append([self.stmts[i],self.tokens[i]])
            
    
    def build(self):
        self.read_file()
        self.label = tk.Label(self.Window, text='总共需要标注数量为：' + str(len(self.actionList)),fg='black',font=('Arial', 12)).place(x=30, y=30)
        self.set_button()
        self.draw_layout()