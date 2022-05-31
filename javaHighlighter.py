import re

class JavaSyntaxHighlighter:
    def __init__(self,text,blank):
        self.columns = 0
        self.blank = blank
        self.text = text
        self.config_all()
        self.line = ""  # 保存当前处理的行
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
        self.regexkeywords = [r"(?<=\s)" + w + r"(?=\s)" for w in self.keywords]
   
    def config_all(self):
        self.text.tag_config("[note]", foreground="green")
        self.text.tag_config("[key]", foreground="blue")
        self.text.tag_config("[string]", foreground="grey")
        self.text.tag_config("[opr]", foreground="red")
        self.text.tag_config("[None]", foreground="black")

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
        for r, w in zip(self.regexkeywords, self.keywords):
            codeline = re.sub(r, " [key] " + w + " [end] ", codeline)
        self.line = codeline + noteline

    def highlight_operator(self):
        '高亮运算符'
        line = self.line
        opr = ['=', '(', ')', '{', '}', '|', '+', '-', '*', '/', '<', '>']
        for o in opr:
            line = line.replace(o, " [opr] " + o + " [end] ")  # 未实现关于字符串内的运算符处理
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
            i = self.split_classify(i)
            for j in i:
                self.text.insert("end",j[1],j[0])            
            # self.text.insert("end",i[-1][1].strip() + "\n","[None]")            
            self.text.insert("end",str(nums).ljust(self.blank," "),"[None]")
            nums += 1
        for i in range(nums):
            if(self.text.get(i + 0.0 ,i + 0.1) == " "):
                self.text.delete(i + 0.0,i + 0.1)
        return self.text
                

    def highlight(self, line):
        '单行代码高亮'
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
            pos = find_note.span()[0]  # 标记注释位置
        self.highlight_note(note)  # 处理行尾注释
        self.highlight_keyword(pos)  # 处理关键字
        self.highlight_string(pos)  # 处理字符串
        self.highlight_operator()  # 处理运算符
        return self.line  # 返回处理好的行

