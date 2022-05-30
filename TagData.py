
class TagData():
    def __init__(self,root,w,h):
        self.root = root
        self.w = w
        self.h = h
        self.file = ""
        self.build_main()

    def choice_filedir(self):    
        self.file = tk.filedialog.askdirectory()
        self.txt_path.set(self.file)
            
    def build_main(self):   
        
        self.window = tk.Frame(self.root,width=self.w,height=self.h,padx=0,pady=0)
        self.window.pack()
        self.window.place(x=0,y=0)
        
        label = tk.Label(self.window, text='请选择需要标注数据的文件夹位置：',fg='black',font=('Arial', 12)).place(x=30, y=30)


        button10 = tk.Button(self.window,width=10, height=1, text='选择文件夹', bg='skyblue', command=self.choice_filedir).place(x=610, y=75)
        button11 = tk.Button(self.window,width=10, height=1, text='确认', bg='skyblue', command=self.to_main).place(x=self.w/2 - 100, y=130)
        button12 = tk.Button(self.window,width=10, height=1, text='关闭', bg='skyblue', command=self.destroy).place(x=self.w/2 + 50, y=130)

    def to_main(self):
        self.window.destroy()
        self.base = BaseBG(self.root,self.w,self.h)

    def destroy(self):
        self.root.destroy()
