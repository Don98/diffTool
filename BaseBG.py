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
    def __init__(self,root,file):
        self.root = root
        self.w = 720
        self.h = 600
        self.file = file
        if(not self.existOrNot()):
            self.run_base()
        else:
            self.to_build()
        
    def to_build(self):
        self.set_size()
        self.build_main()
    
    def existOrNot(self):
        if(os.path.isdir(self.file)):
            return True
        return False
    
    def run_base(self):
        self.base = BaseBG(self.root)
        # self.to_build()
    
    def set_size(self):
        w = 720; h = 400
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
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
            
    def build_main(self):   
        
        self.window = tk.Frame(self.root,width=self.w,height=self.h,padx=0,pady=0)
        self.window.pack()
        self.window.place(x=0,y=0)
        
        self.files = self.get_tag_files()
        
        self.label = tk.Label(self.window, text='你还需要标注数据数量为：' + str(len(self.files) - len(self.tags)) + "/" + str(len(self.files)),fg='black',font=('Arial', 12)).place(x=30, y=30)
        
        self.set_all_files()
        
        # scroll = tk.Scrollbar()
        # scroll.pack(side=tk.RIGHT,fill=tk.Y)
        # scroll.config(command = self.display_files.yview)
        # self.display_files.config(yscrollcommand=scroll.set)

        self.set_button()
        self.set_file_button()
    
    def set_all_files(self):
        self.canvas = tk.Canvas(self.window,width=480,height=197,scrollregion=(0,0,480,len(self.files) * 28),bg = "white")
        self.canvas.pack()
        self.canvas.place(x = 120, y = 80)
        
        self.display_files = tk.Frame(self.canvas,width = 480 ,height = len(self.files) * 30 - 3,padx=0,pady=0)
        
        self.vbar = tk.Scrollbar(self.canvas, orient = tk.VERTICAL) #竖直滚动条
        self.vbar.place(x = 470,width = 20,height=200)
        # self.vbar.place(x = 0,width = 470,height=197)
        self.vbar.configure(command=self.canvas.yview)

        self.canvas.config(yscrollcommand = self.vbar.set) #设置  
        # self.display_files.config(bg='black')
        self.display_files.place(x = 0, y = 0)
        
        self.canvas.create_window((240,750), window = self.display_files)  #create_window

        
    def set_button(self):
        self.button0 = tk.Button(self.window,width=10, height=1, text='保存结果', bg='skyblue', command=self.save_result).place(x = 100, y = 320)
        self.button1 = tk.Button(self.window,width=10, height=1, text='保存退出', bg='skyblue', command=self.save_quit).place(x = 320, y = 320)
        self.button2 = tk.Button(self.window,width=10, height=1, text='打包结果', bg='skyblue', command=self.pack_result).place(x = 540, y = 320)
        # self.text_update = tk.Text(self.window,width=10, height=1).place(x = 540, y = 20)
        # self.button3 = tk.Button(self.window,width=10, height=1, text='打包结果', bg='skyblue', command=self.pack_result).place(x = 40, y = 20)
        
    def set_file_button(self):
        self.files_button = []
        for i in range(len(self.files)):
            self.files_button.append(tk.Button(self.display_files,width=70, height=1, text = self.files[i], bg='white', command=partial(self.open_windows,self.files[i])))
            self.files_button[-1].place(x = 0, y = 28 * i)
        # self.files_button[0]["state"] = tk.DISABLED
        for i in self.tags:
            self.files_button[i]["state"] = tk.DISABLED
        
        
    def open_windows(self,name):
        self.newWindow = Eva(self.root,self.file + "/" + name)
        print(name)
        del self.newWindow  
        
    def save_result(self):
        pass
    
    def save_quit(self):
        pass
    
    def pack_result(self):
        pass

    def to_main(self):
        self.window.destroy()
        self.base = BaseBG(self.root)

    def destroy(self):
        self.root.destroy()
