import re
# regexkeywords = r"(?<=\s)" + "return" + r"(?=\s)"
regexkeywords = r"(?<=\s)return(.*)"
a = "\treturn; a"
a = re.sub(regexkeywords, " [key] " + "return;" + " [end] ", a)
print(a)