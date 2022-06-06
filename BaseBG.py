import difflib
import tkinter as tk
import tkinter.filedialog
from functools import partial
from eva import Eva
import os

class BaseBG():
    def __init__(self,root):
        self.root = root
        self.w = 720
        self.h = 200
        self.file = ""
        self.set_size()
        self.build_main()

    def set_size(self):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws/2) - (self.w/2)
        y = (hs/2) - (self.h/2)
        self.root.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))

    def choice_filedir(self):    
        self.file = tk.filedialog.askdirectory()
        self.txt_path.set(self.file)
            
    def build_main(self):   
        
        self.window = tk.Frame(self.root,width=self.w,height=self.h,padx=0,pady=0)
        self.window.pack()
        self.window.place(x=0,y=0)
        
        label = tk.Label(self.window, text='请选择需要标注数据的文件夹位置：',fg='black',font=('Arial', 12)).place(x=30, y=30)
        l1 = tk.Label(self.window, text='标注数据集文件夹：', font=('Arial', 12)).place(x=30, y=80)

        self.txt_path = tk.StringVar()
        text1 = tk.Entry(self.window, textvariable = self.txt_path, show = None, width=60)
        text1.place(x=180,y=80)

        button10 = tk.Button(self.window,width=10, height=1, text='选择文件夹', bg='skyblue', command=self.choice_filedir).place(x=610, y=75)
        button11 = tk.Button(self.window,width=10, height=1, text='确认', bg='skyblue', command=self.to_main).place(x=self.w/2 - 100, y=130)
        button12 = tk.Button(self.window,width=10, height=1, text='关闭', bg='skyblue', command=self.destroy).place(x=self.w/2 + 50, y=130)

    def to_main(self):
        self.window.destroy()
        self.tagData = TagData(self.root,self.file)
        del self

    def destroy(self):
        self.root.destroy()

class TagData():
    def __init__(self,root,file,ws,hs):
        self.root = root
        self.ws = ws
        self.hs = hs
        self.file = file
        if(not self.existOrNot()):
            self.run_base()
        else:
            self.to_build()
        
    def to_build(self):
        self.build_main()
    
    def existOrNot(self):
        if(os.path.isdir(self.file)):
            return True
        return False
    
    def run_base(self):
        self.base = BaseBG(self.root)
        # self.to_build()
    
    def get_file():
        return self.file
    
    def get_tag_files(self):
    #需要增加判断是否已经标注过的方法
        paths = os.listdir(self.file)
        self.tags = []
        for i in range(len(paths)):
            if(os.path.isfile(self.file + "/" + paths[i] + "/result.txt")):
                self.tags.append(i)
        # self.tags = []
        return paths
            
    def set_label(self):
        self.files = self.get_tag_files()
        self.label = tk.Label(self.window0, text='你还需要标注数据数量为：' + str(len(self.files) - len(self.tags)) + "/" + str(len(self.files)),fg='black',font=('Arial', 12)).place(x=10, y=10)
            
    def build_main(self):   
        self.window0 = tk.Frame(self.root,width=self.ws-2,height=30,padx=0,pady=0)
        self.window = tk.Frame(self.root,width=self.ws-2,height=self.hs-70,padx=0,pady=1)
        self.window1 = tk.Frame(self.root,width=self.ws-2,height=30,padx=0,pady=2)
        self.bar_buttom = tk.Frame(self.root,width=self.ws-2,height=2,padx=0,pady=3)
        self.bar_right = tk.Frame(self.root,width=5,height=self.hs,padx=1,pady=0)
        
        self.window0.place(x=0,y=0)
        self.window.place(x=0,y=35)
        self.window1.place(x=0,y=self.hs - 35)
        self.bar_buttom.place(x=0,y=self.hs - 2)
        self.bar_right.place(x=self.ws-2,y=0)
        
        self.bar_right.config(bg="black")
        self.bar_buttom.config(bg="black")
        # self.window.config(bg="red")
        
        self.set_label()
        self.set_all_files()
        self.set_button()
        self.set_file_button()
    
    def processWheel(event):
        a= int(-(event.delta)/60)
        self.canvas.yview_scroll(a,'units')
        
    def set_all_files(self):
        self.canvas = tk.Canvas(self.window,width=self.ws-2,height=self.hs-70,scrollregion=(0,0,self.ws,len(self.files) * 28),bg = "white")
        self.canvas.place(x = 0, y = 0)
        
        self.display_files = tk.Frame(self.canvas,width=600,height=len(self.files) * 28)
        
        self.vbar = tk.Scrollbar(self.canvas, orient = tk.VERTICAL) #竖直滚动条
        self.vbar.place(x = self.ws-10,width = 10,height=self.hs)
        self.vbar.configure(command=self.canvas.yview)
        self.vbar.bind("<MouseWheel>", self.processWheel)
        self.canvas.bind("<MouseWheel>", self.processWheel)

        self.canvas.config(yscrollcommand = self.vbar.set) #设置  
        self.display_files.config(bg='black')
        self.display_files.place(x = 0, y = 0)
        self.display_files.bind("<MouseWheel>", self.processWheel)
        
        self.canvas.create_window((160,700), window = self.display_files, width = 320, height=len(self.files) * 28)  #create_window

        
    def set_button(self):
        self.button0 = tk.Button(self.window1,width=10, height=1, text='保存结果', bg='skyblue', command=self.save_result).place(x = 0, y = 0)
        self.button1 = tk.Button(self.window1,width=10, height=1, text='查看结果', bg='skyblue', command=self.query_result).place(x = 120, y = 0)
        self.button2 = tk.Button(self.window1,width=10, height=1, text='打包结果', bg='skyblue', command=self.pack_result).place(x = 240, y = 0)
        
    def set_file_button(self):
        self.files_button = []
        for i in range(len(self.files)):
            self.files_button.append(tk.Button(self.display_files,width=70, height=1, text = self.files[i], bg='white', command=partial(self.open_windows,self.files[i],i),anchor="w"))
            self.files_button[-1].place(x = 0, y = 28 * i)
            self.files_button[-1]["state"] = tk.DISABLED
            
        # self.files_button[0]["state"] = tk.DISABLED
        # for i in self.tags:
            # self.files_button[i]["state"] = tk.DISABLED
        self.set_label()
        
        
    def open_windows(self,name,pos):
        self.newWindow = Eva(self.root,self.file + "/" + name)
        print(name)
        self.tags.append(pos)
        del self.newWindow
        
    def get_nums(self,path):
        right = [0,0,0,0,0,0,0,0]
        all_nums =  [0,0,0,0,0,0,0,0]
        with open(path + "/result.txt","r") as f:
            data = f.read().split("==================================================\n")
        num = 0
        for i in data:
            # print(i)
            i = i.split("--------------------------------------------------\n")
            if(len(i) <= 1):
                continue
            i = i[0].split(" : ")[1]
            i = i.strip().split(" || ")
            stmt  = i[0].split("/")
            token = i[1].split("/")
            # print(num,stmt,token)
            right[num] += int(stmt[0])
            all_nums[num] += int(stmt[1])
            right[num + 4] += int(token[0])
            all_nums[num + 4] += int(token[1])
            num += 1
        return right,all_nums
        
    def save_result(self):
        for i in range(len(self.files)):
            self.files_button[i].destroy()
        self.set_file_button()
    
    def query_result(self):
        right = [0,0,0,0,0,0,0,0]
        all_nums =  [0,0,0,0,0,0,0,0]
        for i in self.tags:
            tmp0, tmp1 = self.get_nums(self.file + "/" + self.files[i])
            for i in range(8):
                right[i] += tmp0[i]
                all_nums[i] += tmp1[i]
        methos = ["SE","GT","MTD","IJM"]
        show_content = "Methods\tStmt || Token\n"
        for i in range(4):
            show_content += methos[i] + "\t : " + str(right[i]) + "/" + str(all_nums[i]) + " || " + str(right[i+4]) + "/" + str(all_nums[i + 4]) + "\n" 
        tk.messagebox.showwarning('统计结果', show_content)
    
    def pack_result(self):
        pass

    def to_main(self):
        self.window.destroy()
        self.base = BaseBG(self.root)

    def destroy(self):
        self.root.destroy()
