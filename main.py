# coding:utf-8
import difflib
import tkinter as tk
import tkinter.filedialog
from functools import partial
from BaseBG import TagData
from eva import Eva
from EvaAction import EvaAction
from ctypes import *
from javaHighlighter import JavaSyntaxHighlighter
from win32api import GetMonitorInfo
from win32api import MonitorFromPoint
import _thread as thread
import os
class _PointAPI(Structure): # 用于getpos()中API函数的调用
    _fields_ = [("x", c_ulong), ("y", c_ulong)]

class mainBG():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('数据标注工具V3.0')
        self.root.config(bg="white")
        # self.file = "../first_try/"
        self.file = "./data/"
        
        # self.root.resizable(width=False, height=False)    
        self.root.resizable(width=True, height=True)    

        monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
        monitor = monitor_info.get('Monitor')  # 屏幕分辨率
        work = monitor_info.get('Work')
        bias = monitor[3] - work[3]
        self.ws = self.root.winfo_screenwidth()
        self.hs = self.root.winfo_screenheight() - bias
        self.now_button = -1
        print(self.ws,self.hs)
        self.file_dict = {}
        thread.start_new_thread(self.readFiles,())
        self.set_size()
        
        # first stage : build navigation bar
        self.high = int(6 * self.hs / 8)
        self.low_high = int(2 * self.hs / 8)
        self.left_width = self.ws / 8
        if(self.left_width <= 240):
            self.left_width = 230
        self.navigation = tk.Frame(self.root,width=self.left_width,height=self.high)
        self.navigation.place(x = 0,y = 0)
        self.navigation.config(bg="white")
        
        self.bar_buttom = tk.Frame(self.root, width = self.ws, height = 5, cursor = 'sb_v_double_arrow')
        self.bar_buttom.place(x = 0,y = self.high - 5)
        self.bar_buttom.config(bg = "black")
        self.bar_buttom_pos = [0,self.high - 5,self.ws,5]
        # [self.ws - 2, 0, 5, self.hs]
        self.bar_right = tk.Frame(self.root, width = 5,height = self.high,cursor = 'sb_h_double_arrow')
        self.bar_right.place(x = self.left_width,y = 0)
        self.bar_right_pos = [self.left_width,0,5,self.high]
        self.bar_right.config(bg = "black")
        
        self.tagData = TagData(self,self.root,self.navigation,self.file,self.left_width - 2,self.high-5,self.bar_buttom,self.bar_right)
        
        self.text_place = tk.Frame(self.root,width=self.ws - self.left_width,height=self.high - 5)
        self.text_place.place(x = self.left_width + 5,y = 0)
        self.text_place.config(bg="white")
        
        self.eva_place  = tk.Frame(self.root,width = self.ws, height = self.low_high)
        # self.eva_place.place(x = 0, y = high)
        # print([0,high,self.ws,int(2 * self.hs / 8)])
        self.eva_place.config(bg="white")
        
        self.tagData.defaultFirst()
        
    def readFile(self,file_name):
        with open(file_name,"r") as f:
            data = f.readlines()
            pos = len(data)
        jsh = JavaSyntaxHighlighter(data)
        content = []
        nums = 0
        for i in data:
            content.append(jsh.highlight(i))
            nums += 1
        self.file_dict[file_name] = (content,pos)
    
    def get_dict(self):
        return self.file_dict
    
    def readFiles(self):
        files = os.listdir(self.file)
        # print(files)
        for file in files:
            file_name0 = self.file + "/" + file + "/Srcfile.java"
            # self.readFile(file_name0)
            thread.start_new_thread(self.readFile,(file_name0,))
            file_name1 = self.file + "/" + file + "/Dstfile.java"
            # self.readFile(file_name1)
            thread.start_new_thread(self.readFile,(file_name1,))
    
    def getpos(self):
        # 调用API函数获取当前鼠标位置。返回值以(x,y)形式表示。
        po = _PointAPI()
        windll.user32.GetCursorPos(byref(po))
        return int(po.x - self.root.winfo_x()), int(po.y - self.root.winfo_y())
        
    def xpos(self):return self.getpos()[0]
    
    def ypos(self):return self.getpos()[1]    
        
    def resize_l(self,event):
        # print(self.bar_right_pos)
        dx = self.xpos() - self.bar_right_pos[0]
        self.bar_right_pos[0] += dx
        self.tagData.resize_l(event,dx)
        self.newWindow.resize_l(event,dx)
        self.eva_windows.resize_l(event,dx)
        self.bar_right.place(x = self.bar_right_pos[0], y = self.bar_right_pos[1], width = self.bar_right_pos[2], height = self.bar_right_pos[3])
        # pass
    
    def resize_t(self,event):
        # dy = self.ypos() - self.bar_buttom_pos[1]
        # self.bar_buttom_pos[1] += dy
        # self.bar_right_pos[3] += dy
        # self.tagData.resize_t(event,dy)
        # self.newWindow.resize_t(event,dy)
        # self.eva_windows.resize_t(event,dy)
        # self.bar_buttom.place(x = self.bar_buttom_pos[0], y = self.bar_buttom_pos[1], width = self.bar_buttom_pos[2], height = self.bar_buttom_pos[3])
        # self.bar_right.place(x = self.bar_right_pos[0], y = self.bar_right_pos[1], width = self.bar_right_pos[2], height = self.bar_right_pos[3])
        pass    
        
    def set_bar(self):
        self.bar_right.bind("<B1-Motion>", self.resize_l)
        self.bar_buttom.bind("<B1-Motion>", self.resize_t)

    def open_windows(self,name,pos):
        if(self.now_button == -1):
            self.now_button = pos
        else:
            self.tagData.files_button[self.now_button].config(bg = "white") # 上一个选中revision设置为白色
            self.eva_windows.auto_save() # 保存上一个的结果
            self.now_button = pos
        self.tagData.files_button[pos].config(bg = "#AA72AE") # 选中revision设置为紫色
        self.newWindow = Eva(self,self.root,self.text_place,self.file + "/" + name,pos,self.ws - self.left_width,self.high - 5,self.bar_buttom,self.bar_right)
        self.newWindow.set_bar_place([0,self.high - 5,self.ws, 5],[self.left_width,0,5,self.high])
        self.set_eva(self.newWindow,self.newWindow.get_filename(),pos)
        self.set_bar()
        
    def set_eva(self,newWindow,file_name,pos):
        self.eva_windows = EvaAction(newWindow,self.tagData,pos,self.root, self.eva_place,file_name, self.ws, self.low_high,self.bar_buttom,self.bar_right)
        self.tagData.set_evaAction(self.eva_windows)

    def set_size(self,x = 0,y = 0):
        # x = (ws/2) - (w/2)
        # y = (hs/2) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (self.ws, self.hs, 0, 0))
    
    # def __del__(self):
        # self.eva_windows.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    main = mainBG()
    main.run()