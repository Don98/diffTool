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

