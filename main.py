import difflib
import tkinter as tk
import tkinter.filedialog
from functools import partial
from BaseBG import BaseBG

class mainBG():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('数据标注工具V1.0')
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        
        w = 720; h = 200
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.file = ""
        self.base = BaseBG(self.root,w,h)

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