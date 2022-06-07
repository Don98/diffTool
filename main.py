# coding:utf-8
import difflib
import tkinter as tk
import tkinter.filedialog
from functools import partial
from BaseBG import TagData
from eva import Eva

class mainBG():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('数据标注工具V1.0')
        # self.root.config(bg="white")
        # self.file = "../first_try/"
        self.file = "../data/"
        
        self.root.resizable(width=False, height=False)    
        # self.root.resizable(width=True, height=True)    
        self.ws = self.root.winfo_screenwidth()
        self.hs = self.root.winfo_screenheight()
        print(self.ws,self.hs)
        self.set_size()
        
        # first stage : build navigation bar
        self.navigation = tk.Frame(self.root,width=self.ws/8,height=int(6 * self.hs / 8))
        self.navigation.pack()
        self.navigation.place(x = 0,y = 0)
        self.navigation.config(bg="blue")
        
        self.tagData = TagData(self,self.root,self.navigation,self.file,self.ws / 8,int(6 * self.hs / 8))

    def open_windows(self,name,pos):
        self.newWindow = Eva(self.root,self.file + "/" + name,self.ws - self.ws / 8,int(6 * self.hs / 8))
        # print(name)
        # self.tags.append(pos)
        # del self.newWindow

    def set_size(self,x = 0,y = 0):
        # x = (ws/2) - (w/2)
        # y = (hs/2) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (self.ws, self.hs, 0, 0))
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    main = mainBG()
    main.run()