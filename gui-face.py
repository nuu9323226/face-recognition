import tkinter 
import datetime,re
from tkinter import Tk, Label, Entry, Radiobutton, IntVar
def recordfile():
    hhq=open(dataframe, 'r')  
    lines = hhq.readlines() 
    last_line = lines[-1]      
    return last_line

def month_and_day():
    x = datetime.datetime.now()
    
    # x.month=10
    if x.month<10 and x.month>=1:
        month='0'+str(x.month)
        #print (month)
    else :
        month=str(x.month)
    if x.day<10 and x.day>=1:
        day='0'+str(x.day)
        #print (day)
    else:
        day=str(x.day)  
    year=str(x.year)
    return year+month+day



def read_train_object():
    train_name = open('/home/vincent/facenet/models/name.txt','r') 
    
    lines = train_name.readlines()
    count=0
    for a in lines:
        b=a.split('\n')
        lines[count]=b[0]
        count += 1
    train_name.close
    return lines



today=month_and_day()
dataframe = '/home/vincent/facenet/models/'+today+'-Full'

# 步驟二：建立主視窗。
mainWin = Tk()
var = IntVar()
operation = [ '+', '-', '*', '/']

# 視窗標題
mainWin.title("face-gui")
# 視窗大小
mainWin.geometry("640x280")

# 步驟三：建立視窗控制項元件。
# 建立標籤

var1 = tkinter.StringVar()
a1='辨識中..'
var1.set(a1)


allname=read_train_object()
print(allname)
name123=[]
number123=[]
pd123=[]
for a in allname:
    print(a)
    all_23=a.split("_")
    print(all_23)
    number15=all_23[0]
    name15=all_23[1]
    pd15=all_23[2]
    number123.append(number15)
    name123.append(name15)
    pd123.append(pd15)
    
print(name123)
print(number123)
print(pd123)

persenID = dict(zip(number123, name123))
pdID = dict(zip(number123, pd123))
print(persenID)
print(pdID)


firstLabel = Label(mainWin, text='辨識中..' ,font=('Arial',50) )        
successLabel = Label(mainWin, text="門禁限制",font=('Arial',50),fg="#DC143C" )

resultLabel = Label(mainWin, text="辨識身份",font=('Arial',50))
personLabel = Label(mainWin,  text='                 ',font=('Arial',50),fg="#9400D3" )

pdLabel = Label(mainWin, text="部門為",font=('Arial',50))
pdresultLabel = Label(mainWin,  text='                 ',font=('Arial',50),fg="#9400D3" )        

mainWin.update()

while True:

    hhi=recordfile()
    #b'Pass,ID:030704,Good:04,FU:01,FD:02,Stranger:11,Ready:00\r\n'
    mainWin.after(10)
    if re.findall("Open", hhi) or re.findall("Pass", hhi):
        autosave=hhi
        print(autosave)
        strangercount=re.findall("Stranger:+[0-9]+[0-9]", autosave)
        strangercount1=strangercount[0].split(":")
        print(strangercount1)
        
        if re.findall("Open", autosave):
            print(re.findall("ID:+[0-9]+[0-9]", hhi) )
            idd=re.findall("ID:+[0-9]+[0-9]", hhi)
            print(idd)
            iddd=idd[0].split(":")
            realID=iddd[1]

            person = tkinter.StringVar()
            person.set(persenID[realID]+'                            ')

            pd = tkinter.StringVar()
            pd.set('DP '+pdID[realID]+'             ')       

            firstLabel = Label(mainWin, text='辨識中..',font=('Arial',50) )        
            successLabel = Label(mainWin,text="辨識成功",font=('Arial',50),fg="#40E0D0" )

            resultLabel = Label(mainWin, text="辨識身份",font=('Arial',50))
            personLabel = Label(mainWin,  textvariable=person,font=('Arial',50),fg="#9400D3" )

            pdLabel = Label(mainWin, text="部門為",font=('Arial',50))
            pdresultLabel = Label(mainWin,  textvariable=pd,font=('Arial',50),fg="#9400D3" )



        elif re.findall("Pass", autosave) and int(strangercount1[1])<=8:
            print(re.findall("ID:+[0-9]+[0-9]", hhi) )
            idd=re.findall("ID:+[0-9]+[0-9]", hhi)
            print(idd)
            iddd=idd[0].split(":")
            realID=iddd[1]

            person = tkinter.StringVar()
            person.set(persenID[realID]+'                            ')

            pd = tkinter.StringVar()
            pd.set('DP '+pdID[realID]+'             ')       

            firstLabel = Label(mainWin, text='辨識中..' ,font=('Arial',50) )        
            successLabel = Label(mainWin, text="辨識失敗",font=('Arial',50),fg="#DC143C" )

            resultLabel = Label(mainWin, text="辨識身份",font=('Arial',50))
            personLabel = Label(mainWin,  text="             ",font=('Arial',50),fg="#9400D3" )

            pdLabel = Label(mainWin, text="提醒          ",font=('Arial',50),fg="#DC143C")
            pdresultLabel = Label(mainWin, text="請勿兩人同時辨識",font=('Arial',28),fg="#9400D3" )
        
        elif re.findall("Pass", autosave) and int(strangercount1[1])>=8:
            firstLabel = Label(mainWin, text='辨識中..' ,font=('Arial',50) )        
            successLabel = Label(mainWin, text="門禁限制",font=('Arial',50),fg="#DC143C" )

            resultLabel = Label(mainWin, text="辨識身份",font=('Arial',50))
            personLabel = Label(mainWin,  text="陌生人     ",font=('Arial',50),fg="#9400D3" )

            pdLabel = Label(mainWin, text="提醒    ",font=('Arial',50),fg="#DC143C")
            pdresultLabel = Label(mainWin,  text="請看鏡頭重新辨識",font=('Arial',28),fg="#9400D3" )            
        

        
        mainWin.update()
        #mainWin.mainloop()

    # 版面配置

    firstLabel.grid(row=1,column=0, sticky='w')
    successLabel.grid(row=1,column=1, sticky='w')
    resultLabel.grid(row=2,column=0, sticky='w')
    personLabel.grid(row=2,column=1, sticky='w')
    pdLabel.grid(row=3,column=0, sticky='w')
    pdresultLabel.grid(row=3,column=1, sticky='w')

    #mainWin.update()
    # 步驟四： 進入事件處理迴圈。
#mainWin.mainloop()
