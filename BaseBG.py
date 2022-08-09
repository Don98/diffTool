import difflib
import tkinter as tk
import tkinter.filedialog
from functools import partial
import os
from ctypes import *
from shutil import copyfile
import shutil
import zipfile

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

class _PointAPI(Structure): # 用于getpos()中API函数的调用
    _fields_ = [("x", c_ulong), ("y", c_ulong)]
class TagData():
    def __init__(self,parent,true_root,root,file,ws,hs,bar_buttom,bar_right):
        self.parent = parent
        self.true_root = true_root
        self.root = root
        self.ws = ws
        self.hs = hs
        self.file = file
        self.bound = {}
        self.all_positions = []
        self.bar_buttom = bar_buttom
        self.bar_right  = bar_right
        self.save_nums = 0
        self.now_button = -1
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
        # self.base = BaseBG(self.root)
        # self.to_build()
        tk.messagebox.showwarning('提示', "请将工具和data文件夹放在同一个目录下，谢谢。")
    
    def get_file():
        return self.file
    
    def get_tag_files(self):
    #需要增加判断是否已经标注过的方法
        paths = os.listdir(self.file)
        self.tags = []
        for i in range(len(paths)):
            if(os.path.isfile(self.file + "/" + paths[i] + "/result.txt") and os.path.isfile(self.file + "/" + paths[i] + "/points.txt")):
                self.tags.append(i)
        return paths
            
    def set_label(self):
        self.files = self.get_tag_files()
        self.label = tk.Label(self.window0, text='你还需要标注数据数量为：' + str(len(self.files) - len(self.tags)) + "/" + str(len(self.files)),fg='black',font=('Arial', 12),bg = "white").place(x=10, y=10)
    
    def set_main_tk(self):
        self.root.place(width = self.all_positions[0][2],height = self.all_positions[0][3])
        self.window0.place(x = self.all_positions[1][0],y = self.all_positions[1][1], width = self.all_positions[1][2], height = self.all_positions[1][3])
        self.window.place(x = self.all_positions[2][0],y = self.all_positions[2][1], width = self.all_positions[2][2], height = self.all_positions[2][3])
        self.window1.place(x = self.all_positions[3][0],y = self.all_positions[3][1], width = self.all_positions[3][2], height = self.all_positions[3][3])
        # self.bar_buttom.place(x = self.all_positions[4][0],y = self.all_positions[4][1], width = self.all_positions[4][2], height = self.all_positions[4][3])
        # self.bar_right.place(x = self.all_positions[5][0],y = self.all_positions[5][1], width = self.all_positions[5][2], height = self.all_positions[5][3])
        
        self.bar_right.config(bg="black")
        self.bar_buttom.config(bg="black")
        # self.window1.config(bg="black")
        self.window.config(bg="white")
        
    def build_main(self):
        self.all_positions.append([0,0,self.ws,self.hs])
        self.all_positions.append([0,0,self.ws, 35])
        self.all_positions.append([0,35,self.ws, self.hs - 70])
        self.all_positions.append([0,self.hs - 35,self.ws, 35])
        self.all_positions.append([0,self.hs,self.ws * 8, 5])
        self.all_positions.append([self.ws, 0, 5, self.hs])
        
        self.window0 = tk.Frame(self.root, width = self.all_positions[1][2],height = self.all_positions[1][3])
        self.window0.config(bg="white")
        self.window  = tk.Frame(self.root, width = self.all_positions[2][2],height = self.all_positions[2][3])
        self.window1 = tk.Frame(self.root, width = self.all_positions[3][2],height = self.all_positions[3][3])
        self.window1.config(bg="white")
        # self.bar_buttom = tk.Frame(self.root, width = self.all_positions[4][2],height = self.all_positions[4][3],cursor = 'sb_v_double_arrow')
        # self.bar_right = tk.Frame(self.root, width = self.all_positions[5][2],height = self.all_positions[5][3],cursor = 'sb_h_double_arrow')
        
        self.set_main_tk()
        self.set_label()
        self.set_all_files()
        self.set_button()
        self.set_file_button()
        # self.set_adjust()
    def defaultFirst(self):
        pos = 0
        for i in range(len(self.files_button)):
            if(not i in self.tags):
                pos = i
                break
        # self.now_button = pos
        self.parent.open_windows(self.files[pos],pos)
    
    def getpos(self):
        # 调用API函数获取当前鼠标位置。返回值以(x,y)形式表示。
        po = _PointAPI()
        windll.user32.GetCursorPos(byref(po))
        return int(po.x - self.true_root.winfo_x()), int(po.y - self.true_root.winfo_y())
    def xpos(self):return self.getpos()[0]
    
    def ypos(self):return self.getpos()[1]
    
    def set_canvas(self):
        self.canvas.place(width = self.all_positions[2][2], height = self.all_positions[2][3])
        self.vbar.place(x =  self.all_positions[2][2] - 10,width = 10,height =  self.all_positions[2][3])
        self.display_files.place(width = self.all_positions[2][2],height=len(self.files) * 28)
        new_pos = self.all_positions[2][2] / 320
        self.canvas.create_window((160 * new_pos,14 * len(self.files)), window = self.display_files, width = self.all_positions[2][2], height=len(self.files) * 28) 
    
    def to_resize(self,nums,dx,dy):
        for i in nums:
            self.all_positions[i] = [self.all_positions[i][0], self.all_positions[i][1], self.all_positions[i][2] + dx, self.all_positions[i][3]+dy]
        self.set_main_tk()
        self.set_canvas()
    
    def resize_l(self,event,dx):
        # dx = self.xpos() - self.all_positions[5][0]
        # dy = self.ypos() - self.all_positions[5][1]
        self.all_positions[5][0] += dx
        self.to_resize([0,1,2,3,4],dx,0)
        
    def resize_t(self,event,dy):
        # dx = self.xpos() - self.all_positions[4][0]
        # dy = self.ypos() - self.all_positions[4][1]
        self.all_positions[3][1] += dy
        self.all_positions[4][1] += dy
        self.to_resize([0,2,5],0,dy)
        
    # def set_adjust(self):
        # self.bar_right.bind("<B1-Motion>", self.resize_l)
        # self.bar_buttom.bind("<B1-Motion>", self.resize_t)
        # self.resize()
    
    def processWheel(self,event):
        a= int(-(event.delta)/60)
        self.canvas.yview_scroll(a,'units')
        
    def set_all_files(self):
        self.canvas = tk.Canvas(self.window, width = self.all_positions[2][2], height = self.all_positions[2][3],scrollregion=(0,0,self.ws,len(self.files) * 28),bg = "white")
        self.canvas.place(x = 0, y = 0)
        
        self.display_files = tk.Frame(self.canvas, width = self.all_positions[2][2],height=len(self.files) * 28)
        
        self.vbar = tk.Scrollbar(self.canvas, orient = tk.VERTICAL) #竖直滚动条
        self.vbar.place(x =  self.all_positions[2][2] - 10,width = 10,height =  self.all_positions[2][3])
        self.vbar.configure(command=self.canvas.yview)
        self.vbar.bind("<MouseWheel>", self.processWheel)
        self.canvas.bind("<MouseWheel>", self.processWheel)

        self.canvas.config(yscrollcommand = self.vbar.set) #设置  
        self.display_files.config(bg='white')
        self.display_files.place(x = 0, y = 0)
        self.display_files.bind("<MouseWheel>", self.processWheel)
        
        new_pos = self.all_positions[2][2] / 320
        self.canvas.create_window((160 * new_pos,14 * len(self.files)), window = self.display_files, width = self.all_positions[2][2], height=len(self.files) * 28) 
        
    def set_button(self):
        self.button0 = tk.Button(self.window1,width=10, height=1, text='保存结果', bg='#00BFFF', command=self.save_result)
        self.button0.place(x = 0, y = 2)
        self.button1 = tk.Button(self.window1,width=10, height=1, text='打包结果', bg='#00BFFF', command=self.pack_result)
        self.button1.place(x = 120, y = 2)
        # self.button2 = tk.Button(self.window1,width=10, height=1, text='查看结果', bg='#00BFFF', command=self.query_result)
        # self.button2.place(x = 240, y = 2)
        
    def set_file_button(self):
        self.files_button = []
        for i in range(len(self.files)):
            self.files_button.append(tk.Button(self.display_files,width=70, height=1, text = str(i) + " : " +self.files[i], bg='white', command = partial(self.parent.open_windows,self.files[i],i),anchor="w",bd = 0))
            self.files_button[-1].place(x = 0, y = 28 * i)
            self.files_button[-1].bind("<MouseWheel>", self.processWheel)
            # self.files_button[-1]["state"] = tk.DISABLED
            
        # self.files_button[0]["state"] = tk.DISABLED
        for i in self.tags:
            self.files_button[i]["state"] = tk.DISABLED
        self.set_label()
    
    def set_buttonDiabled(self,pos):
        self.tags.append(pos)
        self.save_nums += 1
        # self.set_file_button()
        
    # def open_windows(self,name,pos):
        # self.newWindow = Eva(self.root,self.file + "/" + name)
        # print(name)
        # self.tags.append(pos)
        # del self.newWindow
        
    def get_nums(self,path):
        right = [0,0,0,0]
        all_nums =  [0,0,0,0]
        
        methods = ["Se_actionList","GT_actionList","MTD_actionList","IJM_actionList"]
        name = {"Se_actionList":0,"GT_actionList":1,"MTD_actionList":2,"IJM_actionList":3}
        # path = self.file_name + "/算法" + str(name[self.method]) + "_result.txt"
        num = 0
        for method in methods:
            with open(path + "/" + "/算法" + str(name[method]) + "_result.txt","r") as f:
                data = f.readlines()
                for i in data:
                    right[num] += int(i.split(",")[-1])
                all_nums[num] += len(data)
                num += 1
        return right,all_nums
        
    def save_result(self):
        if(self.save_nums == 0):
            tk.messagebox.showwarning('提示', "评估任务尚未完成，无法保存!")
            return;
        tk.messagebox.showwarning('提示', "保存了" + str(self.save_nums) + "个文件！")
        self.save_nums = 0
        for i in range(len(self.files)):
            self.files_button[i].destroy()
        self.set_file_button()
        
    def query_result(self):
        right = [0,0,0,0]
        all_nums =  [0,0,0,0]
        for i in self.tags:
            tmp0, tmp1 = self.get_nums(self.file + "/" + self.files[i])
            for i in range(4):
                right[i] += tmp0[i]
                all_nums[i] += tmp1[i]
        # methos = ["SE","GT","MTD","IJM"]
        methos = ["算法0","算法1","算法2","算法3"]
        show_content = "Methods\tStmt\n"
        for i in range(4):
            show_content += methos[i] + "\t : " + str(right[i]) + "/" + str(all_nums[i]) + "\n" 
        tk.messagebox.showwarning('统计结果', show_content)
    def zipDir(self,dirpath, outFullName):
        zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
        for path, dirnames, filenames in os.walk(dirpath):
            # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
            fpath = path.replace(dirpath, '')
     
            for filename in filenames:
                zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
        zip.close()
    def pack_result(self):
        # for file , index in enumerate(self.files):
        if(not os.path.isdir("result")):
            os.mkdir("result")
        result_list = []
        methods = ["Se_actionList","GT_actionList","MTD_actionList","IJM_actionList"]
        name = {"Se_actionList":0,"GT_actionList":1,"MTD_actionList":2,"IJM_actionList":3}
        # path = self.file_name + "/算法" + str(name[self.method]) + "_result.txt"
        for i in self.tags:
            if(not os.path.isdir("./result/" + self.files[i])):
                os.mkdir("./result/" + self.files[i])
            for method in methods:
                copyfile(self.file + self.files[i] + "/算法" + str(name[method]) +  "_result.txt","./result/" + self.files[i] + "/算法" + str(name[method]) +  "_result.txt")
            copyfile(self.file + self.files[i] + "/result.txt","./result/" + self.files[i] + "/result.txt")
            copyfile(self.file + self.files[i] + "/points.txt","./result/" + self.files[i] + "/points.txt")
            copyfile(self.file + self.files[i] + "/readme.md","./result/" + self.files[i] + "/readme.md")
            result_list.append("./result/" + self.files[i] + "/readme.md")
            result_list.append("./result/" + self.files[i] + "/result.txt")
            result_list.append("./result/" + self.files[i] + "/points.txt")
        self.zipDir("./result","./result.zip")
        shutil.rmtree("./result")
        if(int(len(result_list)) == 0):
            tk.messagebox.showwarning('打包结果', "没有需要打包的结果，请开始评估！")
            return;
        tk.messagebox.showwarning('打包结果', str(int(len(result_list) / 3)) + "份结果已打包完成")

    def to_main(self):
        self.window.destroy()
        self.base = BaseBG(self.root)

    def destroy(self):
        self.root.destroy()
