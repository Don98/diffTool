# coding:utf-8
import difflib
import tkinter as tk
import tkinter.filedialog
from functools import partial
from BaseBG import TagData
from eva import Eva
from EvaAction import EvaAction
from ctypes import *
class _PointAPI(Structure): # 用于getpos()中API函数的调用
    _fields_ = [("x", c_ulong), ("y", c_ulong)]

class mainBG():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('数据标注工具V2.0')
        self.root.config(bg="white")
        # self.file = "../first_try/"
        self.file = "../data/"
        
        # self.root.resizable(width=False, height=False)    
        self.root.resizable(width=True, height=True)    
        self.ws = self.root.winfo_screenwidth()
        self.hs = self.root.winfo_screenheight()
        print(self.ws,self.hs)
        self.set_size()
        
        # first stage : build navigation bar
        self.navigation = tk.Frame(self.root,width=self.ws/8,height=int(6 * self.hs / 8))
        self.navigation.place(x = 0,y = 0)
        self.navigation.config(bg="white")
        
        self.bar_buttom = tk.Frame(self.root, width = self.ws, height = 5, cursor = 'sb_v_double_arrow')
        self.bar_buttom.place(x = 0,y = int(6 * self.hs / 8) - 5)
        self.bar_buttom.config(bg = "black")
        self.bar_buttom_pos = [0,int(6 * self.hs / 8) - 5,self.ws,5]
        # [self.ws - 2, 0, 5, self.hs]
        self.bar_right = tk.Frame(self.root, width = 5,height = int(6 * self.hs / 8),cursor = 'sb_h_double_arrow')
        self.bar_right.place(x = self.ws / 8,y = 0)
        self.bar_right_pos = [self.ws / 8,0,5,int(6 * self.hs / 8)]
        self.bar_right.config(bg = "black")
        
        self.tagData = TagData(self,self.root,self.navigation,self.file,self.ws / 8 - 2,int(6 * self.hs / 8)-5,self.bar_buttom,self.bar_right)
        
        self.text_place = tk.Frame(self.root,width=self.ws - self.ws / 8,height=int(6 * self.hs / 8) - 5)
        self.text_place.place(x = self.ws / 8 + 5,y = 0)
        self.text_place.config(bg="white")
        
        self.eva_place  = tk.Frame(self.root,width = self.ws, height = int(2 * self.hs / 8))
        # self.eva_place.place(x = 0, y = int(6 * self.hs / 8))
        # print([0,int(6 * self.hs / 8),self.ws,int(2 * self.hs / 8)])
        self.eva_place.config(bg="white")
        
        
    
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
        # print(self.bar_right_pos)
        self.bar_right.place(x = self.bar_right_pos[0], y = self.bar_right_pos[1], width = self.bar_right_pos[2], height = self.bar_right_pos[3])
    
    def resize_t(self,event):
        dy = self.ypos() - self.bar_buttom_pos[1]
        self.bar_buttom_pos[1] += dy
        self.bar_right_pos[3] += dy
        self.tagData.resize_t(event,dy)
        self.newWindow.resize_t(event,dy)
        self.eva_windows.resize_t(event,dy)
        self.bar_buttom.place(x = self.bar_buttom_pos[0], y = self.bar_buttom_pos[1], width = self.bar_buttom_pos[2], height = self.bar_buttom_pos[3])
        self.bar_right.place(x = self.bar_right_pos[0], y = self.bar_right_pos[1], width = self.bar_right_pos[2], height = self.bar_right_pos[3])
        
    def set_bar(self):
        self.bar_right.bind("<B1-Motion>", self.resize_l)
        self.bar_buttom.bind("<B1-Motion>", self.resize_t)

    def open_windows(self,name,pos):
        self.tagData.files_button[pos].config(bg = "#AA72AE")
        self.newWindow = Eva(self.root,self.text_place,self.file + "/" + name,pos,self.ws - self.ws / 8,int(6 * self.hs / 8) - 5,self.bar_buttom,self.bar_right)
        self.newWindow.set_bar_place([0,int(6 * self.hs / 8) - 5,self.ws, 5],[self.ws / 8,0,5,int(6 * self.hs / 8)])
        self.set_eva(self.newWindow.get_text(),self.newWindow.get_text1(),self.newWindow.get_line_text(),self.newWindow.get_line_text1(),self.newWindow.get_filename())
        self.set_bar()
        
    def set_eva(self,text,text0,line_text,line_text0,file_name):
        self.eva_windows = EvaAction(self.root, self.eva_place,file_name, text, text0, line_text,line_text0, self.ws, int(2 * self.hs / 8),self.bar_buttom,self.bar_right)

    def set_size(self,x = 0,y = 0):
        # x = (ws/2) - (w/2)
        # y = (hs/2) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (self.ws, self.hs, 0, 0))
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    main = mainBG()
    main.run()