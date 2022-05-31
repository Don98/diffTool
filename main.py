# coding:utf-8
import difflib
import tkinter as tk
import tkinter.filedialog
from functools import partial
from BaseBG import BaseBG
from BaseBG import TagData

class mainBG():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('数据标注工具V1.0')
        self.file = "../first_try/"
        # self.file = "../data/"
        # self.base = BaseBG(self.root,w,h,self.file)
        # self.root.resizable(width=False, height=False)
        self.root.resizable(width=True, height=True)
        self.tagData = TagData(self.root,self.file)

    # def Diff(self):
        # with open(file1,encoding='utf-8') as f1,open(file2,encoding='utf-8') as f2:
            # text1 = f1.readlines()
            # text2 = f2.readlines()
        # d = difflib.HtmlDiff()
        # with open('result1.html','w',encoding='utf-8') as f:
            # f.write(d.make_file(text1,text2))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    main = mainBG()
    main.run()