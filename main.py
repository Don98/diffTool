# coding:utf-8
import difflib
import tkinter as tk
import tkinter.filedialog
from functools import partial
from BaseBG import TagData
from eva import Eva
from EvaAction import EvaAction

class mainBG():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('数据标注工具V1.0')
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
        # [self.ws - 2, 0, 5, self.hs]
        self.bar_right = tk.Frame(self.root, width = 5,height = int(6 * self.hs / 8),cursor = 'sb_h_double_arrow')
        self.bar_right.place(x = self.ws / 8,y = 0)
        self.bar_right.config(bg = "black")
        
        self.tagData = TagData(self,self.root,self.navigation,self.file,self.ws / 8 - 2,int(6 * self.hs / 8)-5,self.bar_buttom,self.bar_right)
        
        self.text_place = tk.Frame(self.root,width=self.ws - self.ws / 8,height=int(6 * self.hs / 8) - 5)
        self.text_place.place(x = self.ws / 8 + 5,y = 0)
        self.text_place.config(bg="white")
        
        self.eva_place  = tk.Frame(self.root,width = self.ws, height = int(2 * self.hs / 8))
        self.eva_place.place(x = 0, y = int(6 * self.hs / 8))
        self.eva_place.config(bg="white")
        
        
    def resize_l(self,event):
        self.tagData.resize_l(event)
        self.newWindow.resize_l(event)
    
    def resize_t(self,event):
        self.tagData.resize_t(event)
        self.newWindow.resize_t(event)
        
    def set_bar(self):
        self.bar_right.bind("<B1-Motion>", self.resize_l)
        self.bar_buttom.bind("<B1-Motion>", self.resize_t)

    def open_windows(self,name,pos):
        self.newWindow = Eva(self.root,self.text_place,self.file + "/" + name,pos,self.ws - self.ws / 8,int(6 * self.hs / 8) - 5,self.bar_buttom,self.bar_right)
        self.newWindow.set_bar_place([0,int(6 * self.hs / 8) - 5,self.ws, 5],[self.ws / 8,0,5,int(6 * self.hs / 8)])
        self.set_bar()
        self.set_eva(self.newWindow.get_text(),self.newWindow.get_text1(),self.newWindow.get_filename())
        
    def set_eva(self,text,text0,file_name):
        self.eva_windows = EvaAction(self.eva_place,file_name, text, text0, self.ws, int(2 * self.hs / 8))

    def set_size(self,x = 0,y = 0):
        # x = (ws/2) - (w/2)
        # y = (hs/2) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (self.ws, self.hs, 0, 0))
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    main = mainBG()
    main.run()