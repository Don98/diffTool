import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
def Wheel(event):#鼠标滚轮动作
    # print(str(-1*(event.delta/120)))#windows系统需要除以120
    text2.yview_scroll(int(-1*(event.delta/120)), "units")
    text1.yview_scroll(int(-1*(event.delta/120)), "units")
    return "break" 
def ScrollCommand(*xx):#在滚动条上点击、拖动等动作
    # print(*xx)
    text1.yview(*xx)
    text2.yview(*xx)
root=tk.Tk()
frame1=tk.Frame(root)
frame1.place(x = 0,y = 0)
text1=tk.Text(frame1,width = 10)
text1.pack(fill = BOTH, expand = True)
for ii in range(50):
    text1.insert(tk.INSERT,str(ii)+'\n')#便于展示效果
frame2=tk.Frame(root)
font = tkFont.Font(family="microsoft yahei", size=12, weight="normal")
m_len = font.measure("m")
n_len = font.measure("n")
text2=tk.Text(frame2,font = font,wrap = "word")
text2.pack(fill = BOTH, expand = True)
frame2.place(x = 50,y = 0,width = 1080)
frame2.update()
print(text2.winfo_width(),text2.winfo_height(),m_len,n_len,text2.winfo_width() / m_len)
text2.insert(tk.INSERT,str('CANNOT_CLEAR_STATISTIC_CONSTRUCTED_FROM_EXTERNAL_MOMENTS("statistics constructed from external moments cannot be clearedCANNOT_CLEAR_STATISTI"),')+'\n')
text1.bind("<MouseWheel>", Wheel)
text2.bind("<MouseWheel>", Wheel)

print(text2.get("1.0","1.%d" % (text2.winfo_width() / m_len)))
print(text2.get("2.0","2.5"))

root.mainloop()