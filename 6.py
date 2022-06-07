import tkinter as tk

#主程序类
class main:
    
    def __init__(self):
        
        self.root = tk.Tk()     #创建根窗体

        self.btn = tk.Button(self.root, text='新建标签', command=self.addlabel)             #按钮btn
        self.cv = tk.Canvas(self.root, width=200, height=250, bg='white', )   #画布cv
        self.frm = tk.Frame(self.cv, relief='sunken')                                       #容器frm

        self.cv.create_window((0,0), window=self.frm, anchor='nw')      #在cv中绘制控件frm
        self.cv.configure(scrollregion=(0,0,self.frm.winfo_width(),self.frm.winfo_height()))    #将cv的滚动范围设为frm的大小

        self.btn.pack()     #pack布局
        self.cv.pack(fill='x')

        self.root.mainloop()

    def addlabel(self):     #新建标签

        __label = tk.Label(self.frm, text='标签', width=27, relief='sunken')
        self.cv.bind('<MouseWheel>',lambda event:self.cv.yview_scroll(int(-1*(event.delta/50)),'units'))
        __label.bind('<MouseWheel>',lambda event:self.cv.yview_scroll(int(-1*(event.delta/50)),'units'))
        #为标签绑定鼠标滚动事件
        __label.pack(side='bottom', fill='x')

        self.root.update()  #刷新窗口
        self.cv.configure(scrollregion=(0,0,self.frm.winfo_width(),self.frm.winfo_height()))
        #刷新后重新将cv的滚动范围设为frm的大小（问题出现的地方）
        
main()