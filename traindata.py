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
# windows版本打包指令 pyinstaller.exe -F -w .\user-gui-debug0427.py -i tul_logo.ico
# windows版本 更改 Arial==>微軟正黑體

global current

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
    train_name = open('datas/database_Employee.csv','r') 
    
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
        root.geometry('700x750')

        self.page = tk.Frame(self.root)
        self.page.grid()
        #self.dp=dp
        #print('selfdp',self.dp)
        #self.Button = tk.Button(self.page, text=u'回登入頁',font=('Arial', 12),justify = tk.LEFT,command=self.mainpage) 
        #self.Button.grid(column=0,row=0, sticky=tk.W) 
        
        #self.Button = tk.Button(self.page, text=u'出缺勤查詢',font=('Arial', 12),justify = tk.LEFT,command=partial(self.personpage1,self.dp) ) 
        #self.Button.grid(columnspan=2,row=0, sticky=tk.N+tk.S)       
        
        #self.Button = tk.Button(self.page, text=u'關於版本',font=('Arial', 12),justify = tk.LEFT,command=self.readme ) 
        #self.Button.grid(column=1,row=0, sticky=tk.W)          
        
        ##空白行
        #self.spaceLabel1= tk.Label(self.page,textvariable="      撼訊科技 遠端出勤打卡系統       " )
        #self.spaceLabel1.grid(column=0, row=1, sticky=tk.W)
        
        #self.varpwdtitle=tk.StringVar()
        #self.varpwdtitle.set("            ")
        #self.pwdtitleLabel= tk.Label(self.page,textvariable=self.varpwdtitle, font=('Arial', 10),justify = tk.RIGHT )
        #self.pwdtitleLabel.grid(column=0, row=1, sticky=tk.W)       
        
        #self.vartitle=tk.StringVar()
        #self.vartitle.set("撼訊科技 人臉識別 員工圖像訓練" )
        #self.titleLabel= tk.Label(self.page,textvariable=self.vartitle, font=('Arial', 14),justify = tk.RIGHT )
        #self.titleLabel.grid(column=0, row=2, sticky=tk.W)   
        
        #self.vartitle2=tk.StringVar()
        ##self.vartitle2.set("員工： "+persenID[self.dp]+ '        部門： '+ pdID[self.dp])
        #self.title2Label= tk.Label(self.page,textvariable=self.vartitle2, font=('Arial', 12),justify = tk.RIGHT )
        #self.title2Label.grid(column=0,   row=3, sticky=tk.W)    
        ##空白
        #spaceLabel= tk.Label(self.page,textvariable="             " )
        #spaceLabel.grid(column=0, row=4, sticky=tk.W) 
        
        #self.vartitle2=tk.StringVar()
        #self.vartitle2.set('  請輸入以下資訊，並按確定')
        #self.title2Label= tk.Label(self.page,textvariable=self.vartitle2, font=('Arial', 12),justify = tk.RIGHT )
        #self.title2Label.grid(column=0,   row=5, sticky=tk.W)    
        
        tabControl = ttk.Notebook(self.page)          # Create Tab Control
        
        tab1 = ttk.Frame(tabControl)            # Create a tab 
        tabControl.add(tab1, text='新建立' )      # Add the tab
        
        tab2 = ttk.Frame(tabControl)            # Add a second tab
        tabControl.add(tab2, text='補充影像' )      # Make second tab visible
        
        
        tab3 = ttk.Frame(tabControl)            # Add a second tab
        tabControl.add(tab3, text='補充影像(自動拍攝)' )      # Make second tab visible        
        

        #tabControl.grid(column=0,   row=6, sticky=tk.W)   
        tabControl.pack(expand=1, fill="both",side = tk.LEFT ) 
        
        
        
        #monty = ttk.LabelFrame(tab1, text='控件示范区1')
        
        ##monty.grid(column=0, row=0, padx=8, pady=4)        
        #monty.pack(side = "right", fill="both", expand = True) 
        
        self.vartitle=tk.StringVar()
        self.vartitle.set("新建立(1/3)" )
        self.titleLabel= tk.Label(tab1,textvariable=self.vartitle, font=('Arial', 14),justify = tk.RIGHT )
        self.titleLabel.grid(column=0, row=0, sticky=tk.W)  
        
        self.vartitle=tk.StringVar()
        self.vartitle.set("本次新增的員工如下，請勾選要新增的人員" )
        self.titleLabel= tk.Label(tab1,textvariable=self.vartitle, font=('Arial', 12),justify = tk.RIGHT )
        self.titleLabel.grid(column=0, row=1, sticky=tk.W)          
        
        
        spaceLabel= tk.Label(tab1,textvariable="             " )
        spaceLabel.grid(column=0, row=2, sticky=tk.W)        
        
        
        
        sourcefile=glob.glob(r'../models/person/*')
        
        self.newbuitin=[]
        fileid=[]
        count1=0
        for fileidinfo in sourcefile:
            
            print(count1,fileidinfo)
            fileinfo=fileidinfo.split('/')
            print(fileinfo[-1])
            idinfo=fileinfo[-1].split('_')
            print(idinfo[0])
            count1=count1+1
            fileid.append(idinfo[0])
        
        print('fileid',fileid)        
        
        
        for numaa in fileid:
            try:
                if "0" in buitinID[numaa] :
                    print ('numaa',numaa)
                    self.newbuitin.append(numaa)
            except:
                print (numaa,'沒有此員工編號')
        
        countid=3
        
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
            globals()['self.check'+str(newid) ] = tk.Checkbutton(tab1, text=persenID[newid], variable=globals()['self.Var'+str(newid)], onvalue=1, offvalue=0,font=('Arial', 12))
            #globals()['self.check'+str(newid)].select()  
            globals()['self.check'+str(newid)].grid(column=0, row=countid, sticky=tk.W)        
            countid=countid+1
            print( newid,globals()['self.Var'+str(newid)].get()   )
            
      
        spaceLabel= tk.Label(tab1,textvariable="             " )
        spaceLabel.grid(column=0, row=countid, sticky=tk.W)         
        countid=countid+1
        
        self.Button = tk.Button(tab1, text='確定',font=('Arial', 12),justify = tk.LEFT,command=self.printcheckbutton ) 
        self.Button.grid(column=0,row=countid , sticky=tk.W ) 
        
        root.mainloop()   
 

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
            pic_resize.main(newpersonget)
            #if current1==100:
            current=100
            
            time.sleep(1)
            self.msgBox12(personzh)       
            
            self.To_picsize(personget )
        
      
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
        
    def msgBox12(self,personzh):
        ding=" ".join(personzh)
        tk.messagebox.showinfo( title='訊息', message='完成 %s %d位人員影像裁切'%(ding,len        (personzh) ) )    

    def To_picsize(self,personq ):
        
        print('personq',personq)
        self.page.destroy()
        picsize_page(self.root,personq)      


class picsize_page(object):
    def __init__(self, master=None,personq=0):
        self.root = master
        self.page = tk.Frame(self.root)
        self.page.grid()
        self.personq=personq
        
        
        
       
                
        self.vartitle=tk.StringVar()
        self.vartitle.set("影像訓練前檢視(Image labeling)(2/3)" )
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
            self.Button = tk.Button(self.page, text=persenID[personget], font=('Arial', 12),justify = tk.LEFT,command=partial(self.openfile,'~/facenet/models/personout/'+ personget+'_'+ennameID[personget])) 
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
        self.Button = tk.Button(self.page, text='確定',font=('Arial', 12),justify = tk.LEFT,command=partial(self.To_train,self.personq ) ) 
        self.Button.grid(column=0,row=countid , sticky=tk.W )         
        
    def openfile(self,filepath):
        os.system("nautilus %s"%(filepath)) 
        
    def To_train(self,personq ):
        
        print('personq',personq)
        self.page.destroy()
        training_page(self.root,personq)          


class training_page(object):
    def __init__(self, master=None,personq=0):
        self.root = master
        self.page = tk.Frame(self.root)
        self.page.grid()
        self.personq=personq
        
        personzh=[]
        for newid in self.personq:
                personzh.append(persenID[newid])        
        
        
        self.vartitle=tk.StringVar()
        self.vartitle.set("影像訓練(Image training)(3/3)" )
        self.titleLabel= tk.Label(self.page,textvariable=self.vartitle, font=('Arial', 14),justify = tk.RIGHT )
        self.titleLabel.grid(column=0, row=0, sticky=tk.W)  
        
        self.vartitle=tk.StringVar()
        self.vartitle.set("本次圖像訓練資料人員如下：" )
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
        self.checklater = tk.Checkbutton(self.page, text='設定為稍後訓練，訓練時間改為離峰時段', variable=self.Varlater, onvalue=1, offvalue=0,font=('Arial', 12))
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
        tk.messagebox.showinfo( title='訊息', message='完成training影像辨識模型'  ) 
    def msgBox13(self):
        tk.messagebox.showinfo( title='訊息', message='設定完成，將於離峰時間20時training影像辨識模型'  ) 
        
        
    def trainingbutton(self,personzh):
   
        print('Varlater.get()',self.Varlater.get()  )
        if self.Varlater.get()==1:
            answer=self.msgBox1(personzh)
            print ('answer',answer)
            if answer==True:

                self.msgBox13()       
                
                
            
        if self.Varlater.get()==0:
            answer=self.msgBox2(personzh)
            print ('answer',answer)
            if answer==True:
       
                global current
                ts=threading.Thread(target=progress2)
                ts.start()
                classifierAll.main()                    
                current=100
                time.sleep(1)
                namelist.main()
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

root.title('撼訊科技 人資查詢系統')
root.geometry('500x800')

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)

root.config(menu=menubar)
number123,persenID,pdID,fullID,pwdID,nameID,buitinID,ennameID=person_pd_ID()
secondpage(root)

root.mainloop() 