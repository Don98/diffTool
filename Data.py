import tkinter as tk
import os
import copy
class Data():
    def __init__(self,file_name,method):
        self.file_name = file_name
        self.method = method
        self.data = []
        self.methods = ["SE_Mapping","GT","MTD","IJM"]
        self.exist = True
        
    def print_button(self):
        for i in self.buttons_var:
            for j in i:
                print(j.get(),end = " | ")
            print()
        
    def get_data(self):
        return self.data
    
    def get_prec(self):
        self.stmt_pre = 0
        self.token_pre = 0
        token_nums = 0
        for i in self.buttons_var:
            self.stmt_pre += i[0].get()
            for j in i[1:]:
                token_nums += 1
                self.token_pre += j.get()
        return str(self.stmt_pre) + "/" + str(len(self.buttons_var)),str(self.token_pre) + "/" + str(token_nums)
    
    def save_file(self):
        # self.print_button()
        content = ""
        for i in range(len(self.data)):
            if(i != self.the_pos and i != 3):
                content += self.data[i]
                content += "=" * 50 + "\n"
            elif(i != self.the_pos and i == 3):
                content += self.data[i] + "\n"
            else:
                prec = self.get_prec()
                content += self.data[i][0][0] + " : " + prec[0] + " || " + prec[1] + "\n"
                content += "-" * 50 + "\n"
                for j in range(1,len(self.data[i])):
                    for p in range(len(self.data[i][j])):
                        content += ",".join(self.data[i][j][p]) + "\n"
                    content += "-" * 50 + "\n"
                if(i != 3):
                    content += "=" * 50 + "\n"
                
            
        with open(self.file_name + "/" + "result.txt","w") as f:
            f.write(content)
    
    def updated_buttonvar(self,buttons_var):
        self.buttons_var = buttons_var
    
    def update(self):
        if(len(self.data[self.the_pos]) == 1):
            self.data[self.the_pos] = self.first_write()
            self.data[self.the_pos].insert(0,[self.methods[self.the_pos]])
        else:  
            self.data[self.the_pos] = self.update_record()
    
    def update_record(self):
        self.data[self.the_pos][0] = self.data[self.the_pos][0][0]
        for i in range(1,len(self.data[self.the_pos])):
            for j in range(len(self.data[self.the_pos][i])):
                if(j == 0):
                    self.data[self.the_pos][i][j][1] = str(self.buttons_var[i-1][0].get())
                    if(len(self.buttons_var[i-1]) > 1):
                        self.data[self.the_pos][i][j][3] = str(self.buttons_var[i-1][1].get())
                    else:
                        self.data[self.the_pos][i][j][3] = ""
                else:
                    self.data[self.the_pos][i][j][3] = str(self.buttons_var[i-1][j+1].get())
        return self.data[self.the_pos]
        
    def first_write(self):
        records = []
        for i in range(len(self.stmts)):
            record = []
            tmp = []
            if(len(self.tokens[i]) >= 1):
                tmp.extend([self.stmts[i].replace(","," "),str(self.buttons_var[i][0].get()),self.tokens[i][0].replace(","," "),str(self.buttons_var[i][1].get())])
            else:
                tmp = [self.stmts[i].replace(","," "),str(self.buttons_var[i][0].get()),"",""]
            record.append(tmp)
            for j in range(1,len(self.tokens[i])):
                # print(i,j,len(self.tokens[i]),len(self.buttons_var[i]))
                record.append(["","",self.tokens[i][j].replace(","," "),str(self.buttons_var[i][j + 1].get())])
            records.append(record)
        self.records = records
        return records
        
        
    def create_read_resultfile(self):
        path = self.file_name + "/" + "result.txt"
        if(not os.path.isfile(path)):
            self.exist = False
            with open(path, "w") as f:            
                f.write(self.methods[0]+"\n")
                f.write("-"*50 + "\n")
                for i in self.methods[1:]:
                    f.write("="*50 + "\n")
                    f.write(i+"\n")
                    f.write("-"*50 + "\n")
        with open(path, "r") as f:
            self.data = f.read()
        os.remove(path)
        
    def set_pos(self,the_pos):
        self.the_pos = the_pos
    
    def split_data(self):
        the_pos = self.the_pos
        self.data = self.data.split("="*50 + "\n")
        self.data[the_pos] = self.data[the_pos].split("-"*50 + "\n")[:-1]
        for j in range(len(self.data[the_pos])):
            self.data[the_pos][j] = self.data[the_pos][j].split("\n")[:-1]
            for p in range(len(self.data[the_pos][j])):
                self.data[the_pos][j][p] = self.data[the_pos][j][p].split(",")
    
    def get_buttons_var(self):
        return self.buttons_var
    
    def get_stmts(self):
        return self.stmts
    def get_tokens(self):
        return self.tokens
    def get_actionList(self):
        return self.actionList
    def get_stmtToToken(self):
        return self.stmt_tokens
    def get_tokenToStmt(self):
        return self.token_stmts
    def getResultByIndex(self,index,col):
        return self.buttons_var[index][col]
    def setResultByIndex(self,index,col,val):
        self.buttons_var[index][col] = val
        
    def updateUsingData(self,updatedData):
        # print(updatedData.stmt_tokens)
        StmtsNums = []
        the_stmts = updatedData.get_stmts()
        for index, stmt in enumerate(the_stmts):
            for i, myStmt in enumerate(self.stmts):
                if(stmt == myStmt):
                    self.setResultByIndex(i,0,updatedData.getResultByIndex(index,0))      
                    StmtsNums.append(i)
        TokenNums = []
        the_dict = updatedData.get_tokenToStmt()
        the_dict1 = updatedData.get_stmtToToken()
        for j, myTokens in enumerate(self.tokens):
            for pos,myToken in enumerate(myTokens):
                if(myToken in the_dict):
                    the_stmt = the_dict[myToken]
                    the_index= the_stmts.index(the_stmt)
                    ths_pos  = the_dict1[the_stmt].index(myToken)
                    self.setResultByIndex(j,pos + 1,updatedData.getResultByIndex(the_index,ths_pos + 1))
                    TokenNums.append([j,pos])
        return StmtsNums, TokenNums
        
    def create_buttonvar(self):
        self.buttons_var = []
        if(not self.exist or len(self.data[self.the_pos]) <= 1):
            for i in range(len(self.tokens)):
                buton_var = [tk.IntVar()]
                buton_var[-1].set(1)
                for j in self.tokens[i]:
                    buton_var.append(tk.IntVar())
                    buton_var[-1].set(1)
                self.buttons_var.append(buton_var)
        else:
            for i in self.data[self.the_pos][1:]:
                buton_var = [tk.IntVar()]
                buton_var[-1].set(int(i[0][1]))
                for j in i:
                    if(j[3] == ""):
                        continue
                    buton_var.append(tk.IntVar())
                    buton_var[-1].set(int(j[3]))
                self.buttons_var.append(buton_var)
        
        # self.print_button()
        
        return self.buttons_var
        
    def read_file(self):
        filepath = self.file_name + "/" + self.method + ".txt"
        with open(filepath, "r") as f:
            data = f.read().split("==================================================")
        self.stmts = []
        self.tokens= []
        self.stmt_tokens = {}
        self.token_stmts = {}
        tmp   = []
        for i in data[1:]:
            i = i.split("TOKEN MAPPING:")
            if(len(i) == 1):
                self.stmts.append(i[0].strip())
                self.tokens.append([])
            else:
                self.stmts.append(i[0].strip())
                tmp = []
                for j in i[1].split("\n"):
                    tmp.append(j.strip())
                    
                self.tokens.append(tmp)
                
        self.actionList = []
        for i in range(len(self.tokens)):
            if(len(self.tokens[i]) >= 1):
                self.tokens[i] = self.tokens[i][1:]
            if(len(self.tokens) == 1 and self.tokens[i][0] == ""):
                self.tokens[i] = []
            for j in range(len(self.tokens[i])):
                if(self.tokens[i][j] == ""):
                    self.tokens[i].pop(j)
        for i in range(len(self.stmts)):
            self.stmt_tokens[self.stmts[i]] = tuple(self.tokens[i])
            for token in self.tokens[i]:
                self.token_stmts[token] = self.stmts[i]
            self.actionList.append([self.stmts[i],self.tokens[i]])
        # print(self.stmt_tokens)
        # for i in self.stmt_tokens.keys():
            # print(self.stmt_tokens[i])
        return copy.deepcopy(self.stmts), copy.deepcopy(self.tokens), copy.deepcopy(self.actionList)
    