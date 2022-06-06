import tkinter as tk

def processWheel(event):
    a= int(-(event.delta)/60)
    c.yview_scroll(a,'units')

root = tk.Tk(className='test')

scrollbar = tk.Scrollbar(root)

c= tk.Canvas(root,background = "#D2D2D2",yscrollcommand=scrollbar.set, width=300, height=300)

scrollbar.config(command=c.yview)
scrollbar.pack(side=tk.LEFT, fill=tk.Y)

c.pack(side="left", fill="both", expand=True)

f = tk.Frame(c)
c.create_window(0,0,window=f, anchor='nw')

for i in range(10):
    label=tk.Label(f,wraplength=350 ,text=r"之乎者也 知乎知乎~！"+str(i))
    label.bind("<MouseWheel>", processWheel)
    label.pack()
    button = tk.Button(f,text="凑个数而已..")
    button.pack()
    button.bind("<MouseWheel>", processWheel)

root.update()
c.config(scrollregion=c.bbox("all"))
f.bind("<MouseWheel>", processWheel)
c.bind("<MouseWheel>", processWheel)

root.mainloop()