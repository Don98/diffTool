import re
import tkinter as tk

class JavaSyntaxHighlighter:
    def __init__(self,content,text,text1):
        self.columns = 0
        # self.blank = blank
        self.text  = text
        self.text1 = text1
        self.file_lines = content
        # self.labels = labels
        self.config_all()
        self.lines_nums = 0
        self.line = ""  # 保存当前处理的行
        # self.regexkeywords.append()
        # print(self.regexkeywords[-1])
   
    def config_all(self):
        self.text.tag_config("[note]", foreground="green")
        self.text.tag_config("[key]", foreground="blue")
        self.text.tag_config("[string]", foreground="grey")
        self.text.tag_config("[opr]", foreground="red")
        self.text.tag_config("[None]", foreground="black")
        self.keywords = \
            ["abstract", "assert", "boolean", "break", "byte",
             "case", "catch", "char", "class", "const",
             "continue", "default", "do", "double", "else",
             "enum", "extends", "final", "finally", "float",
             "for", "goto", "if", "implements", "import",
             "instanceof", "int", "interface", "long", "native",
             "new", "package", "private", "protected", "public",
             "return", "strictfp", "short", "static", "super",
             "switch", "synchronized", "this", "throw", "throws",
             "transient", "try", "void", "volatile", "while"]
        self.regexkeywords = [r"(?<=\s)" + w + r"(?=\s)" for w in self.keywords] + [r"(?<=\s)return;"]
        self.keywords.append("return;")
        # for r, w in zip(self.regexkeywords, self.keywords):
            # print(r,w)

    def highlight_note(self, note):
        '高亮注释行'
        if note != "":  # note为空,表示行尾无注释
            # self.text.insert("end",str(columns).center(self.blank," ") + note,"note")
            self.line = self.line.replace(note, " [note] " + note + " [end] ")

    def highlight_string(self, pos):
        '高亮字符串'
        codeline = self.line[:pos]  # 代码部分
        noteline = self.line[pos:]  # 不处理行尾注释
        strlist = re.findall(r'\".*?\"|\'.*?\'', codeline)  # 搜索所有字符串
        if strlist is not None:
            for string in strlist:
                codeline = codeline.replace(string, " [str] " + string + " [end] ")
        self.line = codeline + noteline

    def highlight_keyword(self, pos):
        '高亮关键字'
        codeline = " " + self.line[:pos] + " "
        noteline = self.line[pos:]
        # if(self.lines_nums >= 70 and self.lines_nums <= 75):
            # print("|||",codeline , "||",noteline)
        for r, w in zip(self.regexkeywords, self.keywords):
            codeline = re.sub(r, " [key] " + w + " [end] ", codeline)
        self.line = codeline[1:-1] + noteline

    def highlight_operator(self):
        '高亮运算符'
        line = self.line
        opr = ['=', '(', ')', '{', '}', '|', '+', '-', '*', '/', '<', '>']
        line = line.replace("//","777777")
        
        # if(self.lines_nums >= 70 and self.lines_nums <= 75):
            # print("|| ",self.lines_nums-1, "||",line)
        for o in opr:
            line = line.replace(o, " [opr] " + o + " [end] ")  # 未实现关于字符串内的运算符处理
        line = line.replace("777777","//")
        self.line = line

    def split_classify(self,data):
        data = data.split(" [end] ")
        res = []
        name = [" [note] ", " [key] ", " [str] ", " [opr] ","[None]"]
        for i in data:
            pos = -1
            for j in range(4):
                if(name[j] in i):
                    pos = j
                    break
            if(pos == -1):
                res.append((name[4],i))
            else:
                tmp = i.split(name[pos])
                # print(tmp)
                res.append((name[4],tmp[0]))
                res.append((name[pos],tmp[1]))
        return res

    def translate(self, data=""):
        res = []
        nums = 1
        for i in data:    
            # if(nums >= 70 and nums <= 80):
                # print(nums,i)
            i = self.split_classify(i)
            # if(nums >= 70 and nums <= 80):
                # print(nums,i)
            for j in i:
                self.text.insert("end",j[1],j[0])               
            nums += 1
        for i in range(nums):
            if(self.text.get(i + 0.0 ,i + 0.2) == "  "):
                self.text.delete( i + 0.0 ,i + 0.2)
            elif(self.text.get(i + 0.0 ,i + 0.1) == " "):
                self.text.delete(i + 0.0,i + 0.1)
        now_lines = self.text.get(1.0,"end")[:-1].split("\n")
        pos = 0
        # print(self.file_lines[40:50])
        
        for i in now_lines:
            self.text1.insert("end",str(pos+1) + "\n")
            pos += 1
        # for i in self.file_lines:
            # i = i.strip()
            # now_lines[pos] = now_lines[pos].strip()
            # if(pos >= 70 and pos <= 90):
                # print(pos+1,i,now_lines[pos],len(i),len(now_lines[pos]))
            # if(i == now_lines[pos]):
                # self.text1.insert("end",str(pos+1) + "\n")
                # pos += 1
            # else:
                # self.text1.insert("end",str(pos+1) + "\n")
                # lines_nums = len(i)
                # while(lines_nums > 0):
                    # self.text1.insert("end","\n")
                    # lines_nums -= len(now_lines[pos].strip())
                    # pos += 1
        return self.text,self.text1
                

    def highlight(self, line):
        '单行代码高亮'
        self.lines_nums += 1
        self.line = line
        if self.line.strip() == '': return line  # 空串不处理
        global note  # 注释
        note = ""
        find_note = re.match(r'/(/|\*)(.*)|\*(.*)|(.*)\*/$', self.line.strip())  # 查找单行注释
        if find_note:  # 处理单行注释
            note = find_note.group()
            self.highlight_note(note)
            return self.line
        pos = len(self.line)
        find_note = re.search(r'(?<=[){};])(.*)/(/|\*).*$', self.line.strip())  # 查找行尾注释
        if find_note:
            note = find_note.group()  # 标记行尾注释
            pos = find_note.span()[0] + self.line.count("\t") # 标记注释位置
            # print(find_note.span(),note,self.line.count("\t"),self.line[pos:])
        # if(self.lines_nums >= 70 and self.lines_nums <= 75):
            # print("|| ",self.lines_nums-1, self.line)
        # if(self.lines_nums >= 70 and self.lines_nums <= 75):
            # print("|||",self.lines_nums ,self.line)
        self.highlight_note(note)  # 处理行尾注释
        self.highlight_keyword(pos)  # 处理关键字
        self.highlight_string(pos)  # 处理字符串
        self.highlight_operator()  # 处理运算符
        return self.line  # 返回处理好的行

