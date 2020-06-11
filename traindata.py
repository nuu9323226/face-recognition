import datetime,os
#import os
import tkinter as tk
import tkinter.messagebox
import glob
import numpy as np
from functools import partial
from  tkinter import ttk
from ftplib import FTP
from ftplib import FTP_TLS
from tkinter import filedialog
from datetime import datetime, timedelta
import threading
import time
import pic_resize
import classifierAll
import namelist
import shutil
import sys
import csv
# windows版本打包指令 pyinstaller.exe -F -w .\user-gui-debug0427.py -i tul_logo.ico
# windows版本 更改 Arial==>微軟正黑體

global current
def deleteDuplicatedElementFromList3(listA):
    #return list(set(listA))
    return sorted(set(listA), key = listA.index)
def progress():


    global current
    current=0
    window_sign_up = tk.Tk()
    window_sign_up.geometry('380x100')
    window_sign_up.title('開始擷取影像資料')
    
    pwdLabel=tk.Label(window_sign_up, text='處理進度 ' ,font=('Arial', 12))
    pwdLabel.pack(side=tk.LEFT    )       
    
    progressbar=ttk.Progressbar(window_sign_up,orient="horizontal",length=280,mode="determinate")
    progressbar.pack(side=tk.LEFT    )   
    maxValue=100
    progressbar["maximum"]=maxValue
    
    for i in range(95):
        progressbar['value']=i ##

        progressbar.update()
        time.sleep(2)    
        if current==100:
            progressbar['value']=100
            progressbar.update()
            #time.sleep(5)
            #window_sign_up.destroy()
            break
    if current==100:
        progressbar['value']=100
        progressbar.update()
        time.sleep(2)
        window_sign_up.destroy()
    window_sign_up.mainloop()



def progress2():


    global current
    current=0
    window_sign_up = tk.Tk()
    window_sign_up.geometry('380x100')
    window_sign_up.title('開始訓練影像資料')
    
    pwdLabel=tk.Label(window_sign_up, text='處理進度 ' ,font=('Arial', 12))
    pwdLabel.pack(side=tk.LEFT    )       
    
    progressbar=ttk.Progressbar(window_sign_up,orient="horizontal",length=280,mode="determinate")
    progressbar.pack(side=tk.LEFT    )   
    maxValue=100
    progressbar["maximum"]=maxValue
    
    for i in range(95):
        progressbar['value']=i ##

        progressbar.update()
        time.sleep(2)    
        if current==100:
            progressbar['value']=100
            progressbar.update()
            #time.sleep(5)
            #window_sign_up.destroy()
            break
    if current==100:
        progressbar['value']=100
        progressbar.update()
        time.sleep(2)
        window_sign_up.destroy()
    window_sign_up.mainloop()


def hellofile(file):
    os.system("nautilus %s"%(file))
    #os.system("explorer ~") #windows版本
    #https://www.itread01.com/p/156622.html
    
    
def month_and_day():
    x = datetime.now()
    
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
def hello():
    print('helloworld')

def read_train_object():
    train_name = open(os.path.expanduser('~')+'/facenet/models/database_Employee.csv','r') 
    
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
    #print('allname',allname)
    name123=[]
    number123=[]
    pd123=[]
    pwd123=[]
    buitin123=[] #是否有影像訓練過
    enname123=[]
    
    for a in allname:
        #print(a)
        all_23=a.split(",")
        #print(all_23)
        number15=all_23[2]
        name15=all_23[3]
        enname15=all_23[4]
        pd15=all_23[5]
        pwd15=all_23[6]
        buitin15=all_23[0]
        
        number123.append(number15)
        name123.append(name15)
        pd123.append(pd15)
        pwd123.append(pwd15)
        buitin123.append(buitin15)
        enname123.append(enname15)
    #print(name123)
    #print(number123)
    #print(pd123)

    persenID = dict(zip(number123, name123))
    pdID = dict(zip(number123, pd123))
    fullID=dict(zip(number123,allname) )
    pwdID=dict(zip(number123,pwd123) )
    nameID=dict(zip(name123,number123) )
    buitinID=dict(zip(number123,buitin123) )
    ennameID=dict(zip(number123,enname123) )
    
    
    print('buitinID',str(buitinID))
    print(persenID)
    print(pdID)
    return number123,persenID,pdID,fullID,pwdID,nameID,buitinID,ennameID


#https://blog.csdn.net/i_chaoren/article/details/56296713
class secondpage(object):
    def __init__(self, master=None,dp=0):
        self.root = master
        root.geometry('750x750')

        self.page = tk.Frame(self.root)
        self.page.grid()
        
        tabControl = ttk.Notebook(self.page)          # Create Tab Control
        
        tab1 = ttk.Frame(tabControl)            # Create a tab 
        tabControl.add(tab1, text='新建立' )      # Add the tab
        
        tab2 = ttk.Frame(tabControl)            # Add a second tab
        tabControl.add(tab2, text='編輯模型' )      # Make second tab visible
        
        
        tab3 = ttk.Frame(tabControl)            # Add a second tab
        tabControl.add(tab3, text='補充影像(自動拍攝)' )      # Make second tab visible        
        

        #tabControl.grid(column=0,   row=6, sticky=tk.W)   
        tabControl.pack(expand=1, fill="both",side = tk.LEFT ) 
        
        
        
        #monty = ttk.LabelFrame(tab1, text='控件示范区1')
        
        ##monty.grid(column=0, row=0, padx=8, pady=4)        
        #monty.pack(side = "right", fill="both", expand = True) 
        
        self.vartitle=tk.StringVar()
        self.vartitle.set("新建立 步驟(1/3)" )
        self.titleLabel= tk.Label(tab1,textvariable=self.vartitle, font=('Arial', 14),justify = tk.RIGHT )
        self.titleLabel.grid(column=0, row=0, sticky=tk.W)  
       
        
        self.vartitle=tk.StringVar()
        self.vartitle.set("本次新增的員工如下，請勾選要新增的人員" )
        self.titleLabel= tk.Label(tab1,textvariable=self.vartitle, font=('Arial', 12),justify = tk.RIGHT )
        self.titleLabel.grid(column=0, row=1, sticky=tk.W)    
        
        
        self.vartitle22=tk.StringVar()
        self.vartitle22.set("檢視原始影像:" )
        self.titleLabel22= tk.Label(tab1,textvariable=self.vartitle22, font=('Arial', 12),justify = tk.RIGHT )
        self.titleLabel22.grid(column=0, row=2, sticky=tk.W)            
        
        self.Button = tk.Button(tab1, text='開啟原始影像資料夾', font=('Arial', 12),justify = tk.LEFT,command=partial(self.openfile,'~/facenet/models/person/')) 
        self.Button.grid(column=1,row=2, sticky=tk.W)               
        
        
        
        spaceLabel= tk.Label(tab1,textvariable="             " )
        spaceLabel.grid(column=0, row=3, sticky=tk.W)        
        
        
        
        sourcefile=glob.glob(r'../models/person/*')
        
        for file in sourcefile:
            if len (glob.glob(file+'/*' ))==0:
                sourcefile.remove(file)        
        
        
        self.newbuitin=[]
        fileid=[]
        count1=0
        for fileidinfo in sourcefile:
            
            #print(count1,fileidinfo)
            fileinfo=fileidinfo.split('/')
            #print(fileinfo[-1])
            idinfo=fileinfo[-1].split('_')
            #print(idinfo[0])
            count1=count1+1
            fileid.append(idinfo[0])
        
        #print('fileid',fileid)        
        
        
        for numaa in fileid:
            try:
                if "0" in buitinID[numaa] :
                    #print ('numaa',numaa)
                    self.newbuitin.append(numaa)
            except:
                print (numaa,'沒有此員工編號')
        
        countid=4
        
        for newid in self.newbuitin:
        
            #不能用
            #newidstr=str(newid)
            #print('newid',newid)
            #exec('self.Var{} = tk.IntVar()'.format(newidstr))            
            #exec('self.check{} =tk.Checkbutton(tab1, text=persenID[newid], variable=self.Var{} , onvalue=1, offvalue=0,font=("Arial", 12))'.format(newidstr,newidstr) )  
            #exec('self.check{}.grid(column=0, row=countid, sticky=tk.W)'.format(newidstr))        
            #print(newid, exec('self.Var{}.get()'.format(newidstr) ) ) 
            #countid=countid+1
            
            #不能用
            #names=locals()
            #newidstr=str(newid)
            #names.get('self.ver'+ newidstr+ '= tk.IntVar()' )
            #names.get( 'self.check'+newidstr+'= tk.Checkbutton(tab1, text=persenID[newid], variable=self.Var'+newidstr +' , onvalue=1, offvalue=0,font=("Arial", 12))' )
            #names.get( 'self.check'+newidstr +'.grid(column=0, row=countid, sticky=tk.W)' )
            #print(newid, names.get('self.ver'+ newidstr )  )
            #countid=countid+1
            
            #用locals在self def 中不能傳遞值
            #locals()['self.Var'+str(newid)] = tk.IntVar()
            #locals()['self.check'+str(newid) ] = tk.Checkbutton(tab1, text=persenID[newid], variable=locals()['self.Var'+str(newid)], onvalue=1, offvalue=0,font=('Arial', 12))
            ##globals()['self.check'+str(newid)].select()  
            #locals()['self.check'+str(newid)].grid(column=0, row=countid, sticky=tk.W)        
            #countid=countid+1
            #print( newid,locals()['self.Var'+str(newid)].get()   )            
        
            #將locals改為globals則可以傳遞到def
            globals()['self.Var'+str(newid)] = tk.IntVar()
            globals()['self.check'+str(newid) ] = tk.Checkbutton(tab1, text='DP'+pdID[newid]+' '+ persenID[newid], variable=globals()['self.Var'+str(newid)], onvalue=1, offvalue=0,font=('Arial', 12))
            #globals()['self.check'+str(newid)].select()  
            globals()['self.check'+str(newid)].grid(column=0, row=countid, sticky=tk.W)        
            countid=countid+1
            print( newid,globals()['self.Var'+str(newid)].get()   )
            
      
        spaceLabel= tk.Label(tab1,textvariable="             " )
        spaceLabel.grid(column=0, row=countid, sticky=tk.W)         
        countid=countid+1
        
        self.Button = tk.Button(tab1, text='確定',font=('Arial', 12),justify = tk.LEFT,command=self.printcheckbutton ) 
        self.Button.grid(column=0,row=countid , sticky=tk.W ) 
        self.Button4 = tk.Button(tab1, text='全選',font=('Arial', 12),justify = tk.LEFT,command=self.selectall1 ) 
        self.Button4.grid(column=1,row=countid , sticky=tk.W )  
        self.Button5 = tk.Button(tab1, text='清除',font=('Arial', 12),justify = tk.LEFT,command=self.disselectall1 ) 
        self.Button5.grid(column=2,row=countid , sticky=tk.W )         
        
        
        #==================================================================================================
        self.vartitle2=tk.StringVar()
        self.vartitle2.set("編輯模型 步驟(1/3)" )
        self.titleLabel2= tk.Label(tab2,textvariable=self.vartitle2, font=('Arial', 14),justify = tk.RIGHT )
        self.titleLabel2.grid(column=0, row=0, sticky=tk.W)  
       
        
        self.vartitle22=tk.StringVar()
        self.vartitle22.set("本次編輯的員工名單，請勾選或者刪除人員" )
        self.titleLabel22= tk.Label(tab2,textvariable=self.vartitle22, font=('Arial', 12),justify = tk.RIGHT )
        self.titleLabel22.grid(column=0, row=1, sticky=tk.W)      
        
        
        self.vartitle22=tk.StringVar()
        self.vartitle22.set("檢視原始影像:" )
        self.titleLabel22= tk.Label(tab2,textvariable=self.vartitle22, font=('Arial', 12),justify = tk.RIGHT )
        self.titleLabel22.grid(column=0, row=2, sticky=tk.W)            
        
        self.Button = tk.Button(tab2, text='開啟原始影像資料夾', font=('Arial', 12),justify = tk.LEFT,command=partial(self.openfile,'~/facenet/models/person/')) 
        self.Button.grid(column=1,row=2, sticky=tk.W)        
        
        spaceLabel2= tk.Label(tab2,textvariable="             " )
        spaceLabel2.grid(column=0, row=3, sticky=tk.W)        
        
        
        self.vartitle22=tk.StringVar()
        self.vartitle22.set("編輯的員工:" )
        self.titleLabel22= tk.Label(tab2,textvariable=self.vartitle22, font=('Arial', 12),justify = tk.RIGHT )
        self.titleLabel22.grid(column=0, row=4, sticky=tk.W)          
    
        
        
        self.newbuitin2=[]
        fileid2=[]
        count1=0
        for fileidinfo in sourcefile:
            
            #print(count1,fileidinfo)
            fileinfo=fileidinfo.split('/')
            #print(fileinfo[-1])
            idinfo=fileinfo[-1].split('_')
            #print(idinfo[0])
            count1=count1+1
            fileid2.append(idinfo[0])
        
        #print('fileid2',fileid2)        
        
        
        for numaa in fileid2:
            try:
                if "1" in buitinID[numaa] :
                    #print ('numaa',numaa)
                    self.newbuitin2.append(numaa)
            except:
                print (numaa,'沒有此員工編號')
        
        countid2=5
        
        for newid in self.newbuitin2:
        
             
        
            #將locals改為globals則可以傳遞到def
            globals()['self.Var2_'+str(newid)] = tk.IntVar()
            globals()['self.check2_'+str(newid) ] = tk.Checkbutton(tab2, text='DP'+pdID[newid]+' '+persenID[newid], variable=globals()['self.Var2_'+str(newid)], onvalue=1, offvalue=0,font=('Arial', 12))
            #globals()['self.check'+str(newid)].select()  
            globals()['self.check2_'+str(newid)].grid(column=0, row=countid2, sticky=tk.W)        
            countid2=countid2+1
            print( newid,globals()['self.Var2_'+str(newid)].get()   )
            
        self.vartitle22=tk.StringVar()
        self.vartitle22.set("刪除的員工:" )
        self.titleLabel22= tk.Label(tab2,textvariable=self.vartitle22, font=('Arial', 12),justify = tk.RIGHT )
        self.titleLabel22.grid(column=0, row=countid2, sticky=tk.W)          
        countid2=countid2+1 
        
        values1=[]
        
        
        personout_file=glob.glob(r'../models/personout/*')
        
        
        for file in personout_file:
            pfile=file.split('/')
            perid=pfile[-1].split('_')
            if perid[0].isdigit()==True:
                values1.append('DP'+pdID[perid[0]]+'-'+ perid[0]+'-'+ persenID[perid[0]])
                
        values1.sort()
        values1.insert(0,'None')
        ##values1=['無','DP754-030704-陳緯仁','DP754-030704-陳緯仁']
        print('values1',values1)
        
        #選擇人員1名單bar
        varspace1=tk.StringVar()
        varspace1.set("人員1")
        spaceLabel1= tk.Label(tab2,textvariable=varspace1, font=('Arial', 12),justify = tk.LEFT )
        spaceLabel1.grid(column=0, row=countid2, sticky=tk.W)   

        self.comboExample1 = ttk.Combobox(tab2, width=20 ,values=values1 ,  font=('Arial', 12),state="readonly") 
        print(dict(self.comboExample1)) 
        self.comboExample1.grid(column=0, row=countid2,sticky=tk.N+tk.S)
        self.comboExample1.current(0)
        print('comboExample1',self.comboExample1.current(), self.comboExample1.get())
        countid2=countid2+1
        
        #選擇人員2名單bar
        varspace2=tk.StringVar()
        varspace2.set("人員2")
        spaceLabel2= tk.Label(tab2,textvariable=varspace2, font=('Arial', 12),justify = tk.LEFT )
        spaceLabel2.grid(column=0, row=countid2, sticky=tk.W)   
     
        self.comboExample2 = ttk.Combobox(tab2, width=20 ,values=values1 ,  font=('Arial', 12),state="readonly") 
        #print(dict(self.comboExample2)) 
        self.comboExample2.grid(column=0, row=countid2,sticky=tk.N+tk.S)
        self.comboExample2.current(0)
        print('comboExample2',self.comboExample2.current(), self.comboExample2.get())
        countid2=countid2+1
        
        #選擇人員3名單bar
        varspace3=tk.StringVar()
        varspace3.set("人員3")
        spaceLabel3= tk.Label(tab2,textvariable=varspace3, font=('Arial', 12),justify = tk.LEFT )
        spaceLabel3.grid(column=0, row=countid2, sticky=tk.W)   
        
        self.comboExample3 = ttk.Combobox(tab2, width=20 ,values=values1 ,  font=('Arial', 12),state="readonly") 
        #print(dict(self.comboExample3)) 
        self.comboExample3.grid(column=0, row=countid2,sticky=tk.N+tk.S)
        self.comboExample3.current(0)
        print('comboExample3',self.comboExample3.current(), self.comboExample3.get())
        countid2=countid2+1
        
        #選擇人員4名單bar
        varspace4=tk.StringVar()
        varspace4.set("人員4")
        spaceLabel4= tk.Label(tab2,textvariable=varspace4, font=('Arial', 12),justify = tk.LEFT )
        spaceLabel4.grid(column=0, row=countid2, sticky=tk.W)   
        
        self.comboExample4 = ttk.Combobox(tab2, width=20 ,values=values1 ,  font=('Arial', 12),state="readonly") 
        #print(dict(self.comboExample4)) 
        self.comboExample4.grid(column=0, row=countid2,sticky=tk.N+tk.S)
        self.comboExample4.current(0)
        print('comboExample4',self.comboExample4.current(), self.comboExample4.get())
        countid2=countid2+1
        
        #選擇人員5名單bar
        varspace5=tk.StringVar()
        varspace5.set("人員5")
        spaceLabel5= tk.Label(tab2,textvariable=varspace5, font=('Arial', 12),justify = tk.LEFT )
        spaceLabel5.grid(column=0, row=countid2, sticky=tk.W)   
        
        self.comboExample5 = ttk.Combobox(tab2, width=20 ,values=values1 ,  font=('Arial', 12),state="readonly") 
        #print(dict(self.comboExample5)) 
        self.comboExample5.grid(column=0, row=countid2,sticky=tk.N+tk.S)
        self.comboExample5.current(0)
        print('comboExample5',self.comboExample5.current(), self.comboExample5.get())
        countid2=countid2+1     
        
        spaceLabel= tk.Label(tab2,textvariable="             " )
        spaceLabel.grid(column=0, row=countid2, sticky=tk.W)         
        countid2=countid2+1
        
        self.Button2 = tk.Button(tab2, text='確定',font=('Arial', 12),justify = tk.LEFT,command=self.printcheckbutton2 ) 
        self.Button2.grid(column=0,row=countid2 , sticky=tk.W )
        self.Button4 = tk.Button(tab2, text='全選',font=('Arial', 12),justify = tk.LEFT,command=self.selectall2 ) 
        self.Button4.grid(column=1,row=countid2 , sticky=tk.W )  
        self.Button5 = tk.Button(tab2, text='清除',font=('Arial', 12),justify = tk.LEFT,command=self.disselectall2 ) 
        self.Button5.grid(column=2,row=countid2 , sticky=tk.W )          
        
        
        #==================================================================================================

        sourcefile3=glob.glob(r'../datasets/historyImage/*')
        #print('before sourcefile3',sourcefile3)
        for file in sourcefile3:
            if len (glob.glob(file+'/*' ))==0:
                sourcefile3.remove(file)
                #print(len (glob.glob(file+'/*' )),file)
        #print('after sourcefile3',sourcefile3)       
        
        self.vartitle2=tk.StringVar()
        self.vartitle2.set("補充影像" )
        self.titleLabel2= tk.Label(tab3,textvariable=self.vartitle2, font=('Arial', 14),justify = tk.RIGHT )
        self.titleLabel2.grid(column=0, row=0, sticky=tk.W)  
        
        self.vartitle2=tk.StringVar()
        self.vartitle2.set("步驟(1/3)" )
        self.titleLabel2= tk.Label(tab3,textvariable=self.vartitle2, font=('Arial', 14),justify = tk.RIGHT )
        self.titleLabel2.grid(column=1, row=0, sticky=tk.W)         
        
        self.vartitle22=tk.StringVar()
        self.vartitle22.set("可編輯的員工名單" )
        self.titleLabel22= tk.Label(tab3,textvariable=self.vartitle22, font=('Arial', 12),justify = tk.RIGHT )
        self.titleLabel22.grid(column=0, row=1, sticky=tk.W)          
        
        self.vartitle22=tk.StringVar()
        self.vartitle22.set("檢視原始影像:" )
        self.titleLabel22= tk.Label(tab3,textvariable=self.vartitle22, font=('Arial', 12),justify = tk.RIGHT )
        self.titleLabel22.grid(column=0, row=2, sticky=tk.W)            
        
        self.Button = tk.Button(tab3, text='開啟資料夾', font=('Arial', 12),justify = tk.LEFT,command=partial(self.openfile,'~/facenet/datasets/historyImage/')) 
        self.Button.grid(column=1,row=2, sticky=tk.W)               
        
        
        
        spaceLabel2= tk.Label(tab3,textvariable="             " )
        spaceLabel2.grid(column=0, row=3, sticky=tk.W)        
        
        
        self.vartitle22=tk.StringVar()
        self.vartitle22.set("編輯的員工:" )
        self.titleLabel22= tk.Label(tab3,textvariable=self.vartitle22, font=('Arial', 12),justify = tk.RIGHT )
        self.titleLabel22.grid(column=0, row=4, sticky=tk.W)          
    
        
        
        self.newbuitin3=[]
        fileid3=[]
        count1=0
        for fileidinfo in sourcefile3:
            
            #print(count1,fileidinfo)
            fileinfo=fileidinfo.split('/')
            #print(fileinfo[-1])
            idinfo=fileinfo[-1].split('_')
            #print(idinfo[0])
            count1=count1+1
            fileid3.append(idinfo[0])
        
        #print('fileid3',fileid3)        
        
        
        for numaa in fileid3:
            try:
                if "1" in buitinID[numaa] :
                    #print ('numaa',numaa)
                    self.newbuitin3.append(pdID[numaa]+'-'+numaa)
            except:
                print (numaa,'沒有此員工編號')
        
        self.newbuitin3=deleteDuplicatedElementFromList3(self.newbuitin3)
        self.newbuitin3.sort()
        #print('self.newbuitin3.sort',self.newbuitin3.sort)
        
        countid3=5
        
        rowline=0
        for newid in self.newbuitin3:
        
            spartnumber=newid.split('-')
            
            #將locals改為globals則可以傳遞到def
            globals()['self.Var3_'+str(spartnumber[1])] = tk.IntVar()
            globals()['self.check3_'+str(spartnumber[1]) ] = tk.Checkbutton(tab3, text='DP'+spartnumber[0]+' '+ persenID[spartnumber[1]], variable=globals()['self.Var3_'+str(spartnumber[1])], onvalue=1, offvalue=0,font=('Arial', 12))
            #globals()['self.check3_'+str(spartnumber[1])].select()   
            globals()['self.check3_'+str(spartnumber[1])].grid(column=rowline, row=countid3, sticky=tk.W)        
            
            #print( newid,globals()['self.Var3_'+str(spartnumber[1])].get()   )   
            rowline=rowline+1
            if rowline==5:
                countid3=countid3+1
            if rowline==5:
                rowline=0
      
        spaceLabel3= tk.Label(tab3,textvariable="             " )
        spaceLabel3.grid(column=0, row=countid3, sticky=tk.W)         
        countid3=countid3+1
            
        self.Button3 = tk.Button(tab3, text='確定',font=('Arial', 12),justify = tk.LEFT,command=self.printcheckbutton3 ) 
        self.Button3.grid(column=0,row=countid3 , sticky=tk.W )         
        self.Button4 = tk.Button(tab3, text='全選',font=('Arial', 12),justify = tk.LEFT,command=self.selectall3 ) 
        self.Button4.grid(column=1,row=countid3 , sticky=tk.W )  
        self.Button5 = tk.Button(tab3, text='清除',font=('Arial', 12),justify = tk.LEFT,command=self.disselectall3 ) 
        self.Button5.grid(column=2,row=countid3 , sticky=tk.W )          
        
      #=====================================================================================
        
    
        
        root.mainloop()   
        
    def disselectall3(self):
        for newid in self.newbuitin3:
        
            spartnumber=newid.split('-')
            globals()['self.check3_'+str(spartnumber[1])].deselect()                
        root.mainloop()  
        
    def selectall3(self):
        for newid in self.newbuitin3:
        
            spartnumber=newid.split('-')
            globals()['self.check3_'+str(spartnumber[1])].select()                
        root.mainloop()  
        
    def disselectall2(self):
        for newid in self.newbuitin2:
        
       
            globals()['self.check2_'+str(newid)].deselect()                
        root.mainloop()  
        
    def selectall2(self):
        for newid in self.newbuitin2:
        
   
            globals()['self.check2_'+str(newid)].select()                
        root.mainloop()  
        

    def disselectall1(self):
        for newid in self.newbuitin:
        
       
            globals()['self.check'+str(newid)].deselect()                
        root.mainloop()  
        
    def selectall1(self):
        for newid in self.newbuitin:
        
            globals()['self.check'+str(newid)].select()                
        root.mainloop()  
        







    def printcheckbutton3(self):
        personget=[]
        newpersonget=[]
        personzh=[]
        for newid in self.newbuitin3:
            splitnew=newid.split('-')
            print (splitnew[1],globals()['self.Var3_'+str(splitnew[1])].get() )
            if globals()['self.Var3_'+str(splitnew[1])].get()==1:
                personget.append(splitnew[1])
                personzh.append(persenID[splitnew[1]])
        print('personget',personget)
        print('personzh',personzh)
        answer=self.msgBox1(personzh)
        print ('answer',answer)
        if answer==True :
                
            global current
            ts=threading.Thread(target=progress)
            ts.start()          
            
            for pe in personget:
                newpersonget.append(pe+'_'+ennameID[pe])
            
            print('newpersonget',newpersonget)
            pic_resize.main(newpersonget,'historyImage')
            #if current1==100:
            current=100
            
            time.sleep(1)
            self.msgBox12(personzh)       
            mode='historyImage'
            self.To_picsize(personget,mode ) 
     
 
    def printcheckbutton2(self):
        personget=[]
        newpersonget=[]
        personzh=[]
        
        #刪除的名單
        delelist=[]
        delelistzh=[]
        if self.comboExample1.get()!='None':
            get1=self.comboExample1.get().split('-')
            delelist.append( get1[1] ) 
            delelistzh.append( get1[2] ) 
        if self.comboExample2.get()!='None':
            get2=self.comboExample2.get().split('-')
            delelist.append( get2[1] )
            delelistzh.append( get2[2] ) 
        if self.comboExample3.get()!='None':
            get3=self.comboExample3.get().split('-')
            delelist.append( get3[1] ) 
            delelistzh.append( get3[2] ) 
        if self.comboExample4.get()!='None':
            get4=self.comboExample4.get().split('-')
            delelist.append( get4[1] )
            delelistzh.append( get4[2] ) 
        if self.comboExample5.get()!='None':
            get5=self.comboExample5.get().split('-')
            delelist.append( get5[1] )   
            delelistzh.append( get5[2] ) 
        print('delelist',delelist)        
        
        
        for newid in self.newbuitin2:
            print (newid,globals()['self.Var2_'+str(newid)].get() )
            if globals()['self.Var2_'+str(newid)].get()==1:
                personget.append(newid)
                personzh.append(persenID[newid])
        print('personget',personget)
        print('personzh',personzh)
        answer=self.msgBox22(personzh,delelistzh)
        print ('answer',answer)
        
        
        
        
        if answer==True :
                
            for mvperson in delelist :
                shutil.move(os.path.expanduser('~')+'/facenet/models/personout/'+mvperson+'_'+ennameID[mvperson],os.path.expanduser('~')+'/facenet/models/personout_delete/'+mvperson+'_'+ennameID[mvperson] )            
             
            global current
            ts=threading.Thread(target=progress)
            ts.start()          
            
            for pe in personget:
                newpersonget.append(pe+'_'+ennameID[pe])
            
            print('newpersonget',newpersonget)
            pic_resize.main(newpersonget,'person')
            #if current1==100:
            current=100
            
            time.sleep(1)
            self.msgBox23(personzh,delelistzh)       
            mode='person'
            self.To_picsize(personget,mode ) 
            
 

    def printcheckbutton(self):
        personget=[]
        newpersonget=[]
        personzh=[]
        for newid in self.newbuitin:
            print (newid,globals()['self.Var'+str(newid)].get() )
            if globals()['self.Var'+str(newid)].get()==1:
                personget.append(newid)
                personzh.append(persenID[newid])
        print('personget',personget)
        print('personzh',personzh)
        answer=self.msgBox1(personzh)
        print ('answer',answer)
        if answer==True :
                
            global current
            ts=threading.Thread(target=progress)
            ts.start()          
            
            for pe in personget:
                newpersonget.append(pe+'_'+ennameID[pe])
            
            print('newpersonget',newpersonget)
            pic_resize.main(newpersonget,'person')
            #if current1==100:
            current=100
            
            time.sleep(1)
            self.msgBox12(personzh)       
            mode='person'
            self.To_picsize(personget,mode )
        
      
        #def progress(self):
            #global current
            #current=0
            #window_sign_up = tk.Tk()
            #window_sign_up.geometry('380x100')
            #window_sign_up.title('匯入晶片卡資料')
            
            #pwdLabel=tk.Label(window_sign_up, text='匯入進度 ' ,font=('Arial', 12))
            #pwdLabel.pack(side=tk.LEFT    )       
            
            #progressbar=ttk.Progressbar(window_sign_up,orient="horizontal",length=280,mode="determinate")
            #progressbar.pack(side=tk.LEFT    )   
            #maxValue=100
            #progressbar["maximum"]=maxValue
            #for i in range(95):
         
                #progressbar['value']=i ##
        
                #progressbar.update()
                #time.sleep(0.05)    
                #if current==100:
                    #progressbar['value']=100
                    #break
            #if current==100:
                #progressbar['value']=100
            #window_sign_up.mainloop()    

    
    def no_file_worning11(self):
        tk.messagebox.showwarning( title='錯誤', message='請正確輸入六位數字員工編號')
 
        
    def msgBox1(self,personzh):
        ding=" ".join(personzh)
        answer=tk.messagebox.askyesno( title='訊息', message='本次新增 %s %d位人員?'%(ding,len(personzh) ) )    
        if answer==True:
            return answer
        else:
            return answer
        
    def msgBox22(self,personzh,delelistzh):
        ding=" ".join(personzh)
        ding2=" ".join(delelistzh)
        answer=tk.messagebox.askyesno( title='訊息', message='本次編輯 %s %d位人員，刪除 %s %d位人員?'%(ding,len(personzh),ding2,len(delelistzh) ) )    
        if answer==True:
            return answer
        else:
            return answer      
        
    def msgBox23(self,personzh,delelistzh):
        ding=" ".join(personzh)
        ding2=" ".join(delelistzh)
        answer=tk.messagebox.askyesno( title='訊息', message='完成 %s %d位人員影像裁切，刪除 %s %d位人員'%(ding,len(personzh),ding2,len(delelistzh) ) )    
        if answer==True:
            return answer
        else:
            return answer     
        
        
    def msgBox12(self,personzh):
        ding=" ".join(personzh)
        tk.messagebox.showinfo( title='訊息', message='完成 %s %d位人員影像裁切'%(ding,len(personzh) ) )    

    def To_picsize(self,personq,mode ):
        
        print('personq, mode',personq,mode)
        self.page.destroy()
        picsize_page(self.root,personq,mode)    
    def openfile(self,filepath):
        os.system("nautilus %s"%(filepath))         


class picsize_page(object):
    def __init__(self, master=None,personq=0,mode=0):
        self.root = master
        self.page = tk.Frame(self.root)
        self.page.grid()
        self.personq=personq
        self.mode=mode
        
        
       
                
        self.vartitle=tk.StringVar()
        self.vartitle.set("影像訓練前檢視Image labeling  步驟(2/3)" )
        self.titleLabel= tk.Label(self.page,textvariable=self.vartitle, font=('Arial', 14),justify = tk.RIGHT )
        self.titleLabel.grid(column=0, row=0, sticky=tk.W)  
        
        self.vartitle=tk.StringVar()
        self.vartitle.set("請點擊下面按鈕，並確認影像裁切的內容是否正確" )
        self.titleLabel= tk.Label(self.page,textvariable=self.vartitle, font=('Arial', 12),justify = tk.RIGHT )
        self.titleLabel.grid(column=0, row=1, sticky=tk.W)          
        
        
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=2, sticky=tk.W)        
        
        countid=3
        
     
        
        for personget in self.personq :
            self.Button = tk.Button(self.page, text='DP'+pdID[personget]+' '+persenID[personget], font=('Arial', 12),justify = tk.LEFT,command=partial(self.openfile,'~/facenet/models/personout/'+ personget+'_'+ennameID[personget])) 
            self.Button.grid(column=0,row=countid, sticky=tk.W)
            countid=countid+1
        
        countid=countid+1
        
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=countid, sticky=tk.W)         
        countid=countid+1
        
        self.vartitle=tk.StringVar()
        self.vartitle.set("每個人影像數量上限為500，影像檢查無誤，按確認鍵" )
        self.titleLabel= tk.Label(self.page,textvariable=self.vartitle, font=('Arial', 12),justify = tk.RIGHT )
        self.titleLabel.grid(column=0, row=countid, sticky=tk.W)  
        countid=countid+1
        self.Button = tk.Button(self.page, text='確定',font=('Arial', 12),justify = tk.LEFT,command=partial(self.To_train,self.personq,self.mode ) ) 
        self.Button.grid(column=0,row=countid , sticky=tk.W )      
        self.Button = tk.Button(self.page, text='不訓練並回前頁繼續編輯',font=('Arial', 12),justify = tk.LEFT,command=partial(self.To_home,self.personq )  ) 
        self.Button.grid(column=1,row=countid , sticky=tk.W )         
        
    def openfile(self,filepath):
        os.system("nautilus %s"%(filepath)) 
        
    def To_train(self,personq,mode ):
        

            
        print('personq,mode',personq,mode)
        self.page.destroy()
        training_page(self.root,personq,mode)      
        
    def To_home(self,personq ):
        personzh=[]
        for newid in self.personq:
            personzh.append(persenID[newid])   
            
        if self.mode=='historyImage' :
            for mvperson in self.personq :
                shutil.move(os.path.expanduser('~')+'/facenet/datasets/historyImage/'+mvperson+'_'+ennameID[mvperson],os.path.expanduser('~')+'/facenet/models/historyImageout/'+mvperson+'_'+ennameID[mvperson] )
        else:
            for mvperson in self.personq :
                shutil.move(os.path.expanduser('~')+'/facenet/models/person/'+mvperson+'_'+ennameID[mvperson],os.path.expanduser('~')+'/facenet/models/trainout/'+mvperson+'_'+ennameID[mvperson] )              
        
        self.msgBox12(personzh)
        self.page.destroy()
        secondpage(self.root)       
        
    def msgBox12(self,personzh):
        ding=" ".join(personzh)
        tk.messagebox.showinfo( title='訊息', message='已新增/編輯 %s %d位人員，於下次訓練模型時自動帶入'%(ding,len(personzh) ) )      
        
   

class training_page(object):
    def __init__(self, master=None,personq=0,mode=0):
        self.root = master
        self.page = tk.Frame(self.root)
        self.page.grid()
        self.personq=personq
        self.mode=mode
        
        personzh=[]
        for newid in self.personq:
                personzh.append(persenID[newid])        
        
        
        self.vartitle=tk.StringVar()
        self.vartitle.set("影像訓練Image training  步驟(3/3)" )
        self.titleLabel= tk.Label(self.page,textvariable=self.vartitle, font=('Arial', 14),justify = tk.RIGHT )
        self.titleLabel.grid(column=0, row=0, sticky=tk.W)  
        
        self.vartitle=tk.StringVar()
        self.vartitle.set("本次編輯圖像訓練資料人員如下：" )
        self.titleLabel= tk.Label(self.page,textvariable=self.vartitle, font=('Arial', 12),justify = tk.RIGHT )
        self.titleLabel.grid(column=0, row=1, sticky=tk.W)          
        
        
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=2, sticky=tk.W)        
        
        countid=3
        COUNTPER=1
        for personfind in self.personq:
            
            self.vartitle=tk.StringVar()
            self.vartitle.set('NO.'+str(COUNTPER)+' ' +str(personfind)+' / '+persenID[personfind] )
            self.titleLabel= tk.Label(self.page,textvariable=self.vartitle, font=('Arial', 12),justify = tk.RIGHT )
            self.titleLabel.grid(column=0, row=countid, sticky=tk.W)            
            COUNTPER=COUNTPER+1
            countid=countid+1
        
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=countid, sticky=tk.W)   
        countid=countid+1
        
        
        self.Varlater= tk.IntVar()
        self.checklater = tk.Checkbutton(self.page, text='設定為稍後訓練，訓練時間改為離峰時段', variable=self.Varlater, onvalue=1, offvalue=1,font=('Arial', 12))
        self.checklater.grid(column=0, row=countid, sticky=tk.W)        
        countid=countid+1
        print( 'Varlater.get()',self.Varlater.get() )  
        
        
        self.vartitle=tk.StringVar()
        self.vartitle.set("點擊確認開始進行訓練資料" )
        self.titleLabel= tk.Label(self.page,textvariable=self.vartitle, font=('Arial', 12),justify = tk.RIGHT )
        self.titleLabel.grid(column=0, row=countid, sticky=tk.W)  
        countid=countid+1
        self.Button = tk.Button(self.page, text='確定',font=('Arial', 12),justify = tk.LEFT,command=partial(self.trainingbutton, personzh)  ) 
        self.Button.grid(column=0,row=countid , sticky=tk.W )  
        self.Button = tk.Button(self.page, text='回首頁',font=('Arial', 12),justify = tk.LEFT,command=self.To_home  ) 
        self.Button.grid(column=1,row=countid , sticky=tk.W )              
        
        
        
    def msgBox1(self,personzh):
        ding=" ".join(personzh)
        answer=tk.messagebox.askyesno( title='訊息', message='訓練模型將新增 %s %d位人員，並於離峰時間訓練模型資料'%(ding,len(personzh) ) )    
        if answer==True:
            return answer
        else:
            return answer    
        
    def msgBox2(self,personzh):
        ding=" ".join(personzh)
        answer=tk.messagebox.askyesno( title='訊息', message='訓練模型將新增 %s %d位人員，即將開始訓練模型資料'%(ding,len(personzh) ) )    
        if answer==True:
            return answer
        else:
            return answer           
        
    def msgBox12(self,personzh):
        ding=" ".join(personzh)
        tk.messagebox.showinfo( title='訊息', message='已經完成訓練模型，請重新啟動門禁系統，即可更新資料'  ) 
    def msgBox13(self):
        tk.messagebox.showinfo( title='訊息', message='設定完成，將於離峰時間20時training影像辨識模型'  ) 
        
        
    def trainingbutton(self,personzh):
   
        print('Varlater.get()',self.Varlater.get()  )
        if self.Varlater.get()==1:
            answer=self.msgBox1(personzh)
            print ('answer',answer)
            if answer==True:
                
                if self.mode=='historyImage' :
                    for mvperson in self.personq :
                        shutil.move(os.path.expanduser('~')+'/facenet/datasets/historyImage/'+mvperson+'_'+ennameID[mvperson],os.path.expanduser('~')+'/facenet/models/historyImageout/'+mvperson+'_'+ennameID[mvperson] )
                else:
                    for mvperson in self.personq :
                        shutil.move(os.path.expanduser('~')+'/facenet/models/person/'+mvperson+'_'+ennameID[mvperson],os.path.expanduser('~')+'/facenet/models/trainout/'+mvperson+'_'+ennameID[mvperson] )              
     
                #修改database的新建立者為已建立者
                onlyuse = np.loadtxt(open(os.path.expanduser('~')+'/facenet/models/database_Employee.csv',encoding='utf-8'),dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5,6,7))
                
                for perlist in self.personq:
                    onlyuseindex=np.argwhere(onlyuse==perlist)
                    print('onlyuseindex',onlyuseindex)
                    print(onlyuseindex[:,0])
                    #print('person_only',person_only)
                    onlyuse[onlyuseindex[:,0],0]=1
                print('after onlyuse',onlyuse)
                
                if len (glob.glob(os.path.expanduser('~')+'/facenet/models/database_Employee.csv'))==1:
                    os.remove(os.path.expanduser('~')+'/facenet/models/database_Employee.csv')
                              
                with open(os.path.expanduser('~')+'/facenet/models/database_Employee.csv','a',encoding = 'utf-8') as f: 
                    np.savetxt(f, onlyuse,fmt='%s', delimiter=",") 
                            
                self.msgBox13()       
                
                
            
        if self.Varlater.get()==0:
            answer=self.msgBox2(personzh)
            print ('answer',answer)
            if answer==True:
       
                global current
                ts=threading.Thread(target=progress2)
                ts.start()
                classifierAll.main()      
                namelist.main()
                current=100
                time.sleep(1)
                
                if self.mode=='historyImage' :
                    for mvperson in self.personq :
                        shutil.move(os.path.expanduser('~')+'/facenet/datasets/historyImage/'+mvperson+'_'+ennameID[mvperson],os.path.expanduser('~')+'/facenet/models/historyImageout/'+mvperson+'_'+ennameID[mvperson] )
                else:
                    for mvperson in self.personq :
                        shutil.move(os.path.expanduser('~')+'/facenet/models/person/'+mvperson+'_'+ennameID[mvperson],os.path.expanduser('~')+'/facenet/models/trainout/'+mvperson+'_'+ennameID[mvperson] )              
                
           
                #修改database的新建立者為已建立者
                onlyuse = np.loadtxt(open(os.path.expanduser('~')+'/facenet/models/database_Employee.csv',encoding='utf-8'),dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5,6,7))
                
                for perlist in self.personq:
                    onlyuseindex=np.argwhere(onlyuse==perlist)
                    print('onlyuseindex',onlyuseindex)
                    print(onlyuseindex[:,0])
                    #print('person_only',person_only)
                    onlyuse[onlyuseindex[:,0],0]=1
                print('after onlyuse',onlyuse)
                
                if len (glob.glob(os.path.expanduser('~')+'/facenet/models/database_Employee.csv'))==1:
                    os.remove(os.path.expanduser('~')+'/facenet/models/database_Employee.csv')
                              
                with open(os.path.expanduser('~')+'/facenet/models/database_Employee.csv','a',encoding = 'utf-8') as f: 
                    np.savetxt(f, onlyuse,fmt='%s', delimiter=",")                 
                     
                     
                     
                self.msgBox12(personzh)    
                
        
    def To_home(self):
        self.page.destroy()
        secondpage(self.root)  



#建立資料夾
if not os.path.isdir('datas/'):
    os.mkdir('datas/')    
else :
    print ('data  file exist') 
    

newyear,newmonth,newday=month_and_day()






#downftp.quit()                  # 退出FTP伺服器   






root = tk.Tk()
# root = tk.Toplevel()
# https://blog.csdn.net/FunkyPants/article/details/78163021

root.title('撼訊科技 影像模型編輯系統')
root.geometry('500x800')

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)

root.config(menu=menubar)
number123,persenID,pdID,fullID,pwdID,nameID,buitinID,ennameID=person_pd_ID()
secondpage(root)


root.mainloop() 