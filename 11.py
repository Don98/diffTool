#添加回调函数
#同普通的按键一样，它也是有回调函数的，当我们选中按钮时就会触发

from tkinter import *

window = Tk()

r_value = IntVar()
def r_print():
    print(r_value.get())
Radiobutton(window,text='Python',variable=r_value,value=1,command=r_print).pack()
Radiobutton(window,text='Scratch',variable=r_value,value=2,command=r_print).pack()
Radiobutton(window,text='C++',variable=r_value,value=3,command=r_print).pack()

window.mainloop()
