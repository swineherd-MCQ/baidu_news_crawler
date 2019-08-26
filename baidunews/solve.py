import re
pat1="id=(.*?)&"
fp=open('F:/abc.txt','r',encoding='utf-8')
a=[]
for i in fp:
    thisdata=re.compile(pat1).findall(i)[0]
    a.append(thisdata)
    print(thisdata)
print(a)
