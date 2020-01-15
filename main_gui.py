# -*- coding: utf-8 -*- 
import datetime
import tkinter as tk
import glob
import numpy as np
#from PIL import Image, ImageTk
from functools import partial
#import tkinter
from  tkinter import ttk  #导入内部包
dpartment=[100,120,121,150,210,220,230,310,325,350,750,756,754,570,160,510,530]


def reflashmonth():

    b = np.loadtxt('202001.csv',dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5))
    print(b) 


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
    return year,month,day

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


def person_pd_ID():
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
    fullID=dict(zip(number123,allname) )
    print(persenID)
    print(pdID)
    return number123,persenID,pdID,fullID





class mainpage(object):
    def __init__(self, master=None):
        self.root = master 
        
        self.page = tk.Frame(self.root) 
        self.page.grid()
        #self.dport='760'
        
        #建立button
        self.Button = tk.Button(self.page, text=u'DP100總經理室', font=('Arial', 12),justify = tk.LEFT,command=partial(self.secpage,'100')) 
        self.Button.grid(column=0,row=0, sticky=tk.W) 
        self.Button = tk.Button(self.page, text=u'DP120品保', font=('Arial', 12),justify = tk.LEFT,command=partial(self.secpage,'120')) 
        self.Button.grid(column=1,row=0,sticky=tk.W) 
        self.Button = tk.Button(self.page, text=u'DP121測試', font=('Arial', 12),justify = tk.LEFT,command=partial(self.secpage,'121')) 
        self.Button.grid(column=2,row=0, sticky=tk.W)  
        self.Button = tk.Button(self.page, text=u'DP150稽核室', font=('Arial', 12),justify = tk.LEFT,command=partial(self.secpage,'150')) 
        self.Button.grid(column=3,row=0, sticky=tk.W) 
        self.Button = tk.Button(self.page, text=u'DP210人資總務', font=('Arial', 12),justify = tk.LEFT,command=partial(self.secpage,'210')) 
        self.Button.grid(column=4,row=0,sticky=tk.W)          
        self.Button = tk.Button(self.page, text=u'DP220財快', font=('Arial', 12),justify = tk.LEFT,command=partial(self.secpage,'220')) 
        self.Button.grid(column=5,row=0, sticky=tk.W) 
        self.Button = tk.Button(self.page, text=u'DP230資訊', font=('Arial', 12),justify = tk.LEFT,command=partial(self.secpage,'230')) 
        self.Button.grid(column=0,row=1,sticky=tk.W) 
        self.Button = tk.Button(self.page, text=u'DP310業務', font=('Arial', 12),justify = tk.LEFT,command=partial(self.secpage,'310')) 
        self.Button.grid(column=1,row=1, sticky=tk.W) 
        self.Button = tk.Button(self.page, text=u'DP325 IPC', font=('Arial', 12),justify = tk.LEFT,command=partial(self.secpage,'325')) 
        self.Button.grid(column=2,row=1,sticky=tk.W) 
        self.Button = tk.Button(self.page, text=u'DP350產品中心', font=('Arial', 12),justify = tk.LEFT,command=partial(self.secpage,'350')) 
        self.Button.grid(column=3,row=1, sticky=tk.W) 
        self.Button = tk.Button(self.page, text=u'DP750研一', font=('Arial', 12),justify = tk.LEFT,command=partial(self.secpage,'750')) 
        self.Button.grid(column=4,row=1,sticky=tk.W)
        self.Button = tk.Button(self.page, text=u'DP756研二', font=('Arial', 12),justify = tk.LEFT,command=partial(self.secpage,'756')) 
        self.Button.grid(column=5,row=1, sticky=tk.W) 
        self.Button = tk.Button(self.page, text=u'DP754軟體研發', font=('Arial', 12),justify = tk.LEFT,command=partial(self.secpage,'754')) 
        self.Button.grid(column=0,row=2,sticky=tk.W) 
        self.Button = tk.Button(self.page, text=u'DP570技轉', font=('Arial', 12),justify = tk.LEFT,command=partial(self.secpage,'570')) 
        self.Button.grid(column=1,row=2, sticky=tk.W) 
        self.Button = tk.Button(self.page, text=u'DP160 RMA', font=('Arial', 12),justify = tk.LEFT,command=partial(self.secpage,'160')) 
        self.Button.grid(column=2,row=2,sticky=tk.W) 
        self.Button = tk.Button(self.page, text=u'DP510採購', font=('Arial', 12),justify = tk.LEFT,command=partial(self.secpage,'510')) 
        self.Button.grid(column=3,row=2,sticky=tk.W)    
        self.Button = tk.Button(self.page, text=u'DP530船務', font=('Arial', 12),justify = tk.LEFT,command=partial(self.secpage,'530')) 
        self.Button.grid(column=4,row=2,sticky=tk.W)         
       
        self.Button = tk.Button(self.page, text=u'DP750', font=('Arial', 12),justify = tk.LEFT,command=partial(self.secpage,'750')) 
        self.Button.grid(column=5,row=2,sticky=tk.W)         
       
        varspace=tk.StringVar()
        varspace.set("總共建制人數:"+ str(len(number123))+'位' )
        spaceLabel= tk.Label(self.page,textvariable=varspace, font=('Arial', 12),justify = tk.LEFT )
        spaceLabel.grid(column=0, row=3, sticky=tk.W)
        
        
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=4, sticky=tk.W)

        #從資料夾抓取以建檔名稱
        filename=[]
        sourcefile=glob.glob(r'../datasets/personout/*')
        print('sourcefile',sourcefile)
        for a in sourcefile:
            finalname=a.split("/")
            filename.append(finalname[-1])
        print ('finalname',filename)
        print('len(filename',len(filename))
        line1=5

        for dpart in dpartment:

            print('dpartment',dpart)
            locals()['self.var'+str(dpart)]=tk.StringVar()
            locals()['self.var'+str(dpart)].set(str(dpart)+'部門:  ')
        #         locals()['textLabel'+str(dpart)] = tk.Label(window,textvariable=locals()['var'+str(dpart)], bg='green', font=('Arial', 12), width=30, height=2,justify = tk.LEFT)#显示文字内容 
            locals()['self.textLabel'+str(dpart)] = tk.Label(self.page,textvariable=locals()['self.var'+str(dpart)], bg='green', font=('Arial', 12),justify = tk.LEFT)#显示文字内容
            locals()['self.textLabel'+str(dpart)].grid(column=0, row=line1, sticky=tk.W) #自动对齐,side：方位

        #         line1=line1+1
            print('line1',line1)
            gpart=[]
            for c,v in pdID.items():
                if str(v)==str(dpart):
                    gpart.append(c)
                    print('number',c)
            column01=1
            for personq in gpart:
                print('personq',personq)
                print('persenID',persenID[personq])
                locals()['self.var'+str(personq)]=tk.StringVar()
                locals()['self.var'+str(personq)].set(persenID[personq])
                locals()['self.textLabel'+str(personq)] = tk.Label(self.page,textvariable=locals()['self.var'+str(personq)], font=('Arial', 12),justify = tk.LEFT)#显示文字内容 
                locals()['self.textLabel'+str(personq)].grid(column=column01, row=line1, sticky=tk.W) #自动对齐,side：方位
                column01=column01+1
    #                 if column01==len(gpart)-1:
    #                     line1=line1+1

            line1=line1+1 
#             column01=1
            
#             for imagep in gpart:
#                 print('fullID[imagep]',fullID[imagep])
#                 print('imagep',imagep)
#                 try:
#                     file_resize=glob.glob(r'../datasets/personout/'+fullID[imagep]+'/*001.png')
#                 except:
#                     file_resize=glob.glob(r'../datasets/personout/'+fullID[imagep]+'/*.png')
#                 print('file_resize',file_resize)
                
                
# #                 pil_image = Image.open(r'C:\Users\23216\Desktop\1.jpg') 
                
# #                 realname=file_resize[0].split('/')
#                 print("file_resize[-1]",file_resize[-1])
#                 locals()['photo'+str(imagep)] = tk.PhotoImage(file=file_resize[0])  #file：t图片路径
#                 locals()['imgLabel'+str(imagep)]  = tk.Label(self.page,image=locals()['photo'+str(imagep)])#把图片整合到标签类中
#                 locals()['imgLabel'+str(imagep)].grid(column=column01, row=line1, sticky=tk.W)
#                 column01=column01+1
        
        
        root.mainloop()   

        
    def secpage(self,dp):
        self.page.destroy()
        secondpage(self.root,dp)
        
        
    def th3page(self):
        self.page.destroy()
        th3page(self.root)
    
class secondpage(object):
    def __init__(self, master=None,dp=0):
        self.root = master
        self.page = tk.Frame(self.root)
        self.page.grid()
        self.dp=dp
        print('selfdp',self.dp)
        self.Button = tk.Button(self.page, text=u'主畫面',font=('Arial', 12),justify = tk.LEFT,command=self.mainpage) 
        self.Button.grid(column=0,row=0, sticky=tk.W) 
        
        #空白行
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=1, sticky=tk.W)
        #空白行
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=2, sticky=tk.W)        
        
        #題字
        varspace=tk.StringVar()
        varspace.set("部門人員建制名單")
        spaceLabel= tk.Label(self.page,textvariable=varspace, font=('Arial', 12),justify = tk.LEFT )
        spaceLabel.grid(column=0, row=3, sticky=tk.W)
        
        #增減人員
        
        self.varnumber=tk.StringVar()
        self.varnumber.set("工號")
        self.numberLabel= tk.Label(self.page,textvariable=self.varnumber, font=('Arial', 12),justify = tk.RIGHT )
        self.numberLabel.grid(column=1, row=0, sticky=tk.E)        
        
        self.varname=tk.StringVar()
        self.varname.set("姓名")
        self.nameLabel= tk.Label(self.page,textvariable=self.varname, font=('Arial', 12),justify = tk.RIGHT )
        self.nameLabel.grid(column=1, row=1, sticky=tk.E)   
        
        self.varpd=tk.StringVar()
        self.varpd.set("部門異動")
        self.nameLabel= tk.Label(self.page,textvariable=self.varpd, font=('Arial', 12),justify = tk.RIGHT )
        self.nameLabel.grid(column=1, row=2, sticky=tk.E)           
        
        #填字匡
        self.numberString = tk.StringVar()
        self.entrynumber = tk.Entry(self.page, width=20, textvariable=self.numberString)
        self.entrynumber.grid(column=2, row=0, padx=1)
        
        self.nameString = tk.StringVar()
        self.entryname = tk.Entry(self.page, width=20, textvariable=self.nameString)
        self.entryname.grid(column=2, row=1, padx=1)
        
        self.pdString = tk.StringVar()
        self.entrypd = tk.Entry(self.page, width=20, textvariable=self.pdString)
        self.entrypd.grid(column=2, row=2, padx=1)        
        
                
        #按鈕
        self.addButton = tk.Button(self.page, text = '新增',command=self.add_callbackFunc )
        self.addButton.grid(column=3, row=0, pady=1, sticky=tk.W)
        
        self.reduceButton = tk.Button(self.page, text = '刪除',command=self.reduce_callbackFunc)
        self.reduceButton.grid(column=3, row=1, pady=1, sticky=tk.W)        
        
        self.reduceButton = tk.Button(self.page, text = '編輯',command=self.eddit_callbackFunc)
        self.reduceButton.grid(column=3, row=2, pady=1, sticky=tk.W)         
        
        
        #回應的字顯示
        self.add_resultString=tk.StringVar()
        self.add_resultLabel = tk.Label(self.page, textvariable=self.add_resultString,fg="#DC143C" )
        self.add_resultLabel.grid(column=0, row=1, padx=1, sticky=tk.W)        
        
        self.reduce_resultString=tk.StringVar()
        self.reduce_resultLabel = tk.Label(self.page, textvariable=self.reduce_resultString,fg="#DC143C" )
        self.reduce_resultLabel.grid(column=0, row=1, padx=1, sticky=tk.W)   
        
        self.eddit_resultString=tk.StringVar()
        self.eddit_resultLabel = tk.Label(self.page, textvariable=self.eddit_resultString,fg="#DC143C" )
        self.eddit_resultLabel.grid(column=0, row=1, padx=1, sticky=tk.W)         

        #建立名字欄
        line1=4
        gpart=[]
        for c,v in pdID.items():
            if str(v)==str(self.dp):
                gpart.append(c)
                print('number: port',c,v)
        column01=0
        print("gpart",gpart)
        
        for personq in gpart:
            
            if len(gpart)>=6:
            
                print('personq',personq)
                print('persenID',persenID[personq])
                #locals()['self.var'+str(personq)]=tk.StringVar()
                #locals()['self.var'+str(personq)].set(personq+' '+persenID[personq])
                
                #locals()['self.textLabel'+str(personq)] = tk.Label(self.page,textvariable=locals()['self.var'+str(personq)], font=('Arial', 12),justify = tk.LEFT)#显示文字内容 
                #locals()['self.textLabel'+str(personq)].grid(column=column01, row=line1, sticky=tk.W) #自动对齐,side：方位
                
                locals()['self.Button'+str(personq)]= tk.Button(self.page,text =str(personq+' '+persenID[personq]),font=('Arial', 12) ,command=partial(self.personpage1,personq) )
                locals()['self.Button'+str(personq)].grid(column=column01, row=line1, pady=1, sticky=tk.W)
                
                #self.addButton = tk.Button(self.page, text = '新增',command=self.add_callbackFunc )
                #self.addButton.grid(column=3, row=0, pady=1, sticky=tk.W)                
                
                column01=column01+1
                if column01==5:
                    line1=line1+2
                    column01=0
                    
            if len(gpart)<6:
            
                print('personq',personq)
                print('persenID',persenID[personq])
                locals()['self.var'+str(personq)]=tk.StringVar()
                locals()['self.var'+str(personq)].set(personq+' '+persenID[personq])
                #locals()['self.textLabel'+str(personq)] = tk.Label(self.page,textvariable=locals()['self.var'+str(personq)], font=('Arial', 12),justify = tk.LEFT)#显示文字内容 
                #locals()['self.textLabel'+str(personq)].grid(column=column01, row=line1, sticky=tk.W) #自动对齐,side：方位
                
                
                #======learning=====
                #button需要引數傳遞在這裡需要用到partial(funtion名稱, 2)
                #https://www.delftstack.com/zh-tw/howto/python-tkinter/how-to-pass-arguments-to-tkinter-button-command/
                #======learning=====
                
                locals()['self.Button'+str(personq)]= tk.Button(self.page,text =str(personq+' '+persenID[personq]),font=('Arial', 12) ,command=partial(self.personpage1,personq) )
                locals()['self.Button'+str(personq)].grid(column=column01, row=line1, pady=1, sticky=tk.W)
                #self.addButton = tk.Button(self.page, text = '新增',command=self.add_callbackFunc )
                #self.addButton.grid(column=3, row=0, pady=1, sticky=tk.W)                 
                
                column01=column01+1

        #建立照片欄
        line1=5
        column01=0
            
        for imagep in gpart:
            
            if len(gpart)>=6:
            
            
                print('fullID[imagep]',fullID[imagep])
                print('imagep',imagep)
                try:
                    file_resize=glob.glob(r'../datasets/personout/'+fullID[imagep]+'/*001.png')
                    print('file_resize',file_resize)
                    print("file_resize[-1]",file_resize[-1])
                except:
                    file_resize=glob.glob(r'../datasets/personout/'+fullID[imagep]+'/*.png')
                    print('file_resize',file_resize)
                    print("file_resize[-1]",file_resize[-1])
                    print('error')
#                 pil_image = Image.open(r'C:\Users\23216\Desktop\1.jpg') 

#                 realname=file_resize[0].split('/')
                print("file_resize[-1]",file_resize[-1])
                locals()['photo'+str(imagep)] = tk.PhotoImage(file=file_resize[-1])  #file：t图片路径
                locals()['imgLabel'+str(imagep)]  = tk.Label(self.page,image=locals()['photo'+str(imagep)])#把图片整合到标签类中
                locals()['imgLabel'+str(imagep)].grid(column=column01, row=line1, sticky=tk.W)
                column01=column01+1
                if column01==5:
                    line1=line1+2
                    column01=0
                    
            if len(gpart)<6:
                
                print('fullID[imagep]',fullID[imagep])
                print('imagep',imagep)
                try:
                    file_resize=glob.glob(r'../datasets/personout/'+fullID[imagep]+'/*001.png')
                except:
                    file_resize=glob.glob(r'../datasets/personout/'+fullID[imagep]+'/*.png')
                print('file_resize',file_resize)


#                 pil_image = Image.open(r'C:\Users\23216\Desktop\1.jpg') 

#                 realname=file_resize[0].split('/')
                print("file_resize[-1]",file_resize[-1])
                locals()['photo'+str(imagep)] = tk.PhotoImage(file=file_resize[-1])  #file：t图片路径
                locals()['imgLabel'+str(imagep)]  = tk.Label(self.page,image=locals()['photo'+str(imagep)])#把图片整合到标签类中
                locals()['imgLabel'+str(imagep)].grid(column=column01, row=line1, sticky=tk.W)
                column01=column01+1
        
        
        root.mainloop()   
    
    
    
    def mainpage(self):
        self.page.destroy()
        mainpage(self.root)
        
    def personpage1(self,personq ):
        
        print('personq',personq)
        self.page.destroy()
        personpage(self.root,personq)
  
    def add_callbackFunc(self):
        print('numberString',self.numberString.get())
        print('nameString',self.nameString.get())
        
        #======learning=====
        #self.add_resultLabel.grid_forget() 用forget可以暫時隱藏,不用這個forget是因為在恢復顯示後位置會跑掉
        #self.reduce_resultLabel.grid_remove() 用remove可以暫時隱藏,且恢復時位置不會跑掉
        #self.reduce_resultLabel.grid()  恢復顯示物件 
        #https://www.delftstack.com/zh-tw/howto/python-tkinter/how-to-hide-recover-and-delete-tkinter-widgets/
        #======learning=====
        
        #控制要顯示及隱藏的物件
        self.reduce_resultLabel.grid_remove()
        self.eddit_resultLabel.grid_remove()
        self.add_resultLabel.grid()
        
        self.add_resultString.set("{} {}新增成功".format(self.numberString.get(),self.nameString.get()))    
       
        
    def reduce_callbackFunc(self):
        print('numberString',self.numberString.get())
        print('nameString',self.nameString.get())
   
        #控制要顯示及隱藏的物件
        self.add_resultLabel.grid_remove()
        self.eddit_resultLabel.grid_remove()        
        self.reduce_resultLabel.grid()
        
        self.reduce_resultString.set("{} {}刪除成功".format(self.numberString.get(),self.nameString.get()))    
       
        
    def eddit_callbackFunc(self):
        print('numberString',self.numberString.get())
        print('nameString',self.nameString.get())
        print('pdString',self.pdString.get())
        #控制要顯示及隱藏的物件
        self.add_resultLabel.grid_remove()
        self.reduce_resultLabel.grid_remove()   
        self.eddit_resultLabel.grid()  
        
        self.eddit_resultString.set("{} {} DP{}異動成功".format(self.numberString.get(),self.nameString.get(),self.pdString.get()))        
       
        
        

        
class personpage(object):
    def __init__(self, master=None,personq=0):
        self.root = master
        self.page = tk.Frame(self.root)
        self.page.grid()
        
        self.personq=personq
        self.Button = tk.Button(self.page, text=u'主畫面',font=('Arial', 12),justify = tk.LEFT,command=self.mainpage ) 
        self.Button.grid(column=0,row=0) 
        self.Button = tk.Button(self.page, text=u'返回',font=('Arial', 12),justify = tk.LEFT,command=partial(self.secpage,pdID[personq])) 
        self.Button.grid(column=1,row=0)         
        
        
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=1, sticky=tk.W)
        
        varspace=tk.StringVar()
        varspace.set("個人頁面查詢： "+self.personq+ ' ' +persenID[personq] )
        spaceLabel= tk.Label(self.page,textvariable=varspace, font=('Arial', 12),justify = tk.LEFT )
        spaceLabel.grid(column=0, row=2, sticky=tk.W)
        
        #製作一年日期的查詢表
        newtyear,newmonth,newday=month_and_day()
        newmonth=8
        #print(newtyear)
        #print(newmonth)
        values1=[]
        #如果是12月倒數到1
        if newmonth==12 :
            for nt in range(-13,-1):
                #abs取對值
                tmonth=str(newtyear)+"/"+str(abs(nt+1))
                values1.append(tmonth )
        else :#如果是非12月倒數到1，年減1
            for ny in range(0,12):
                if int(newmonth)==0 :
                    newtyear=int(newtyear)-1
                    newmonth=12
                values1.append(str(newtyear)+'/'+str(newmonth) )
                newmonth=int(newmonth)-1
                
        print('values1',values1)
        varspace=tk.StringVar()
        varspace.set("選擇月份：")
        spaceLabel= tk.Label(self.page,textvariable=varspace, font=('Arial', 12),justify = tk.LEFT )
        spaceLabel.grid(column=0, row=3, sticky=tk.W)
        
        
        
        b = np.loadtxt('202001.csv',dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5))
        print(b)        
        
        c=b[:,[1]]
        print(c)
        
        
        comboExample = ttk.Combobox(self.page, width=13 ,values=values1, font=('Arial', 12),state="readonly") 
        
        
        print(dict(comboExample)) 
        comboExample.grid(column=0, row=3,sticky=tk.N+tk.S)
        comboExample.current(0)
        print(comboExample.current(), comboExample.get())
    
    
        self.addButton = tk.Button(self.page, text = '查詢',command=read_train_object )
        self.addButton.grid(column=0, row=3, pady=1, sticky=tk.E)        
    
    
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=4, sticky=tk.W)        
    
        #win=tk.Tk()
        tree=ttk.Treeview(self.page)#表格
        tree["columns"]=("日期","上班時間","下班時間")
        tree.column("日期",width=100)   #表示列,不显示
        tree.column("上班時間",width=100)
        tree.column("下班時間",width=100)
        
        tree.heading("日期",text="日期")  #显示表头
        tree.heading("上班時間",text="上班時間")
        tree.heading("下班時間",text="下班時間")
        #tree.insert("", insert_mode, text='name first col')
        tree.insert("",0,text=self.personq ,values=("2020/1/1","09:00","18:00")) #插入数据，
        tree.insert("",1,text=self.personq ,values=("2020/1/2","09:01","18:02"))
        tree.insert("",2,text=self.personq ,values=("2020/1/3","09:03","18:05"))
        tree.insert("",3,text=self.personq ,values=("2020/1/4","09:05","18:10"))
        
        tree.grid(columnspan=3, row=5, sticky=tk.W)       

        root.mainloop()   
        
    def mainpage(self):
        self.page.destroy()
        mainpage(self.root)

    def secpage(self,dp):
        self.page.destroy()
        secondpage(self.root,dp)



    


number123,persenID,pdID,fullID =person_pd_ID()    
root = tk.Tk()
# root = tk.Toplevel()
# https://blog.csdn.net/FunkyPants/article/details/78163021

root.title('撼訊科技 門禁管理系統')
root.geometry('1000x750')

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)

menubar.add_cascade(label='開始', menu=filemenu)

# 在File中加入New、Open、Save等小菜单，即我们平时看到的下拉菜单，每一个小菜单对应命令操作。

filemenu.add_command(label='員工資料建立', command=read_train_object )
filemenu.add_command(label='出缺勤管理', command=read_train_object)
filemenu.add_command(label='後台管理', command=read_train_object)
filemenu.add_separator()    # 添加一条分隔线
filemenu.add_command(label='Exit', command=root.quit) # 用tkinter里面自带的quit()函数

# 第7步，创建一个Edit菜单项（默认不下拉，下拉内容包括Cut，Copy，Paste功能项）
editmenu = tk.Menu(menubar, tearoff=0)
# 将上面定义的空菜单命名为 Edit，放在菜单栏中，就是装入那个容器中
menubar.add_cascade(label='執行', menu=editmenu)

# 同样的在 Edit 中加入Cut、Copy、Paste等小命令功能单元，如果点击这些单元, 就会触发do_job的功能
#b=secondpage()
editmenu.add_command(label='門禁系統啟動', command=read_train_object )
editmenu.add_command(label='出缺勤紀錄日報表', command=read_train_object)
editmenu.add_command(label='陌生人管理', command=read_train_object)

# 第8步，创建第二级菜单，即菜单项里面的菜单
submenu = tk.Menu(filemenu) # 和上面定义菜单一样，不过此处实在File上创建一个空的菜单
filemenu.add_cascade(label='Import', menu=submenu, underline=0) # 给放入的菜单submenu命名为Import

# 第9步，创建第三级菜单命令，即菜单项里面的菜单项里面的菜单命令（有点拗口，笑~~~）
submenu.add_command(label='Submenu_1', command=read_train_object)   # 这里和上面创建原理也一样，在Import菜单项中加入一个小菜单命令Submenu_1

# 第11步，创建菜单栏完成后，配置让菜单栏menubar显示出来
root.config(menu=menubar)

mainpage(root)

root.mainloop()     
