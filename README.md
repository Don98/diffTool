# diffTool
A diffTool for annotated data set

因为标注数据的需求，所以自己写了个python程序来完成标注所需要的操作问题。

因为我们数据标注有如下几个事情要做：

- 查看模型跑的结果
- 把结果和比较的文件的源码对应在一起
- 把变化前后两个文件对应位置放在一起比较
- 录入标注结果

根据以上的要求，我们需要实现的需求有如下几点：

- 1、一个窗口界面，所有的操作最好都能够通过点击来实现 √
- 2、窗口界面要能够显示多个文件（类似谷歌浏览器的多标签）
- 3、要能够显示出两个文件的差异
- 4、能够点击结果文件然后跳转到对应的源码文件 √
- 5、能够通过点击就完成标注结果的录入。 √





突发奇想，想记录在实现这一个软件过程中给我帮助，解决一些问题的网页：

- 1. https://blog.csdn.net/JNingWei/article/details/78298771
  2. https://www.delftstack.com/zh/howto/python-tkinter/how-to-pass-arguments-to-tkinter-button-command/
  3. https://www.pynote.net/archives/1004
  4. https://www.delftstack.com/zh/howto/python-tkinter/how-to-close-a-tkinter-window-with-a-button/
  5. https://www.runoob.com/python/python-tk-frame.html
  6. https://blog.csdn.net/qq_41555580/article/details/118607123
  7. https://groups.google.com/g/python-cn/c/GN2LfwLoJ98/m/DnjNoNtZWIwJ?pli=1
  8. https://www.delftstack.com/zh/howto/python-tkinter/how-to-create-a-new-window-with-a-button-in-tkinter/
  9. https://www.delftstack.com/zh/howto/python-tkinter/how-to-change-tkinter-button-color/
  10. https://blog.csdn.net/qq_21238607/article/details/108824662
  11. https://blog.csdn.net/qq_28123095/article/details/79331756
  12. https://www.runoob.com/python/python-tk-canvas.html
  13. https://blog.csdn.net/qq_35981895/article/details/107311844
  14. https://blog.csdn.net/w15977858408/article/details/104173780
  15. https://www.thinbug.com/q/38594978
  16. https://blog.csdn.net/w15977858408/article/details/104173780
  17. https://wenku.baidu.com/view/528ab4080366f5335a8102d276a20029bd646328.html
  18. https://blog.csdn.net/weixin_43794311/article/details/124682879
  19. https://blog.csdn.net/wujuxKkoolerter/article/details/123750144
  20. https://www.runoob.com/python/python-tk-checkbutton.html
  21. https://blog.csdn.net/weixin_45774074/article/details/123293411
  22. https://blog.csdn.net/chaodaibing/article/details/108749234
  23. [鼠标事件](https://blog.csdn.net/qq_44168690/article/details/104882776)

这星期开完组会，老师提了新需求，需要优先实现新需求了，新需求有如下几点：

- 把所有内容都放在一个屏幕内，左边放commit文件，主屏幕放比对文件内容，下边放比对工具的操作（需要评估的操作）
- 把text变成可调整的，目前实现思路为：把两个text放入一个frame中，然后占据frame的所有内容，当frame的大小被调整的时候（只能够上下挪动），text的大小也会被挪动
- 挪动的实现思路：在需要挪动的部件边缘增加一个看不到的细长条部件块，当鼠标在这个位置的时候才能够挪动部件（和需要挪动的不见融合）
- 操作评估的拜访，主要展示stmt层次的操作，token层次的操作由下拉列表来实现，当下拉的时候才展现token层次的操作。

大致的需求效果图如下：

![image-20220605024357888](C:\Users\10622\AppData\Roaming\Typora\typora-user-images\image-20220605024357888.png)

- 1. [python中tkinter窗口位置\坐标\大小等知识的科普](https://blog.csdn.net/dhjabc_1/article/details/105428853)
  2. [tkinter中ttk控件的width-height设置](https://blog.csdn.net/qq_35981895/article/details/107311844)
  3. [Canvas绘制控件——关于Python的tkinter模块Canvas控件绘制组件的一些问题(scrollregien)：画布的滚动超出预定范围](https://icode.best/i/75816642283712)
  4. [【Python cursor指针】——Python Tkinter Cursor鼠标指针属性值](https://blog.csdn.net/weixin_46625757/article/details/122517061?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_title~default-0-122517061-blog-102582099.pc_relevant_default&spm=1001.2101.3001.4242.1&utm_relevant_index=2)
  5. [Python tkinter 设计用鼠标拖动控件、控件缩放算法及程序](https://blog.csdn.net/qfcy_/article/details/122615118)
  6. [Python的包tkinter中的canvas.winfo_height()或canvas.winfo_width()返回值1的解决](https://blog.csdn.net/RobertChenGuangzhi/article/details/105425187)
  7. [https://www.javaroad.cn/questions/303594](https://www.javaroad.cn/questions/303594)
  8. [Tkinter 组件详解之Listbox](https://www.cxyzjd.com/article/qq_41556318/85108351)

