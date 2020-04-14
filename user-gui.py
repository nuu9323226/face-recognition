import datetime,os
import tkinter as tk
import tkinter.messagebox
import glob
import numpy as np
#from PIL import Image, ImageTk
from functools import partial
#import tkinter
from  tkinter import ttk
from ftplib import FTP
from ftplib import FTP_TLS
from tkinter import filedialog
from datetime import datetime, timedelta
#import faceRegistered
#20190203 v1.0版 篩選資料，呈現12個月的資料至表格中
#update release 2020/02/10 v1.1修改資料夾位置models/day ==>放每天檔案 ./data==>放整理後每月的資料  ftp:  /home/AccessFace/day==>放每天  /home/AccessFace/month==>放每個月
                            #新增從到ftp下載每個月份的檔案的設定
#update release 2020/02/14 v1.2增加匯入晶片卡資料功能                
import xlrd
#需要安裝sudo pip3 install xlrd
import csv

#from ftplib import FTP_TLS
downftp = FTP()
timeout = 30
port = 21
#如果ftp有啟動ftps (ssl/tls)加密服務則需要用以下方式連線
#https://stackoverflow.com/questions/5534830/ftpes-ftp-over-explicit-tls-ssl-in-python
#from ftplib import FTP_TLS
#downftp=FTP_TLS('61.220.84.60')
downftp.connect('61.220.84.60',port,timeout) # 連線FTP伺服器
downftp.login('Vincent','helloworld') # 登入
downftp.set_pasv(False)
print (downftp.getwelcome())  # 獲得歡迎資訊 
#d=ftp.cwd('home/AccessFace/month')    # 設定FTP路徑
monthftp=downftp.nlst('home/AccessFace/month') #獲取ftp上的所以月份檔案
print('monthftp',monthftp)
path88 =  'data/'
pathimage='image/'

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
    train_name = open('data/database_Employee-notchinese.csv','r') 
    
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
    for a in allname:
        #print(a)
        all_23=a.split(",")
        #print(all_23)
        number15=all_23[2]
        name15=all_23[3]
        pd15=all_23[5]
        pwd15=all_23[4]
        number123.append(number15)
        name123.append(name15)
        pd123.append(pd15)
        pwd123.append(pwd15)

    #print(name123)
    #print(number123)
    #print(pd123)

    persenID = dict(zip(number123, name123))
    pdID = dict(zip(number123, pd123))
    fullID=dict(zip(number123,allname) )
    pwdID=dict(zip(number123,pwd123) )
    nameID=dict(zip(name123,number123) )
    #print(persenID)
    #print(pdID)
    return number123,persenID,pdID,fullID,pwdID,nameID


class mainpage(object):
    def __init__(self, master=None):
        self.root = master 
        root.geometry('500x300')
        self.page = tk.Frame(self.root)        
        self.page.pack()
        
        canvas = tk.Canvas(self.page, height=500, width=500)
        image_file = tk.PhotoImage(file='tul_logo1.gif')
        self.image = canvas.create_image(0,0, anchor='nw', image=image_file)
        canvas.pack(side='top')
        
        # user information
        
        self.varname=tk.StringVar()
        self.varname.set("員工編號 ")
        self.numberLabel= tk.Label(self.page,textvariable=self.varname, font=('Arial', 12),justify = tk.RIGHT )
        self.numberLabel.place(x=50, y= 150)       
                
        self.varpwd=tk.StringVar()
        self.varpwd.set("密碼 ")
        self.pwdLabel= tk.Label(self.page,textvariable=self.varpwd, font=('Arial', 12),justify = tk.RIGHT )
        self.pwdLabel.place(x=50, y= 190) 
        
        
        self.varpwdtitle=tk.StringVar()
        self.varpwdtitle.set("預設密碼為英文名")
        self.pwdtitleLabel= tk.Label(self.page,textvariable=self.varpwdtitle, font=('Arial', 10),justify = tk.RIGHT )
        self.pwdtitleLabel.place(x=160, y= 215)          
        
        
        
        self.var_usr_name = tk.StringVar()
        self.var_usr_pwd = tk.StringVar()
        #var_usr_name.set('請輸入中文姓名')
        #self.var_usr_pwd.set('預設密碼為工號')
        self.entry_usr_name = tk.Entry(self.page, textvariable=self.var_usr_name)
        self.entry_usr_name.place(x=160, y=150)
        self.entry_usr_pwd = tk.Entry(self.page, textvariable=self.var_usr_pwd, show='*')
        self.entry_usr_pwd.place(x=160, y=190)
        
   
        
        # login and sign up button
        self.btn_login = tk.Button(self.page, text='登入',font=('Arial', 12) , command=self.conform)
        self.btn_login.place(x=180, y=240)
        self.btn_sign_up = tk.Button(self.page, text='輸入工號直接登入',font=('Arial', 12), command=self.conform1 )
        self.btn_sign_up.place(x=270, y=240)

        root.mainloop() 
        
        
        
    def conform1(self):
        print('pwd',self.var_usr_name.get())
        inputpwd=self.var_usr_name.get()
        #,pwdID,nameID
        self.secpage(inputpwd)
             
    
    

    def conform(self):
        print('name',self.var_usr_name.get())
        inputnumber=self.var_usr_name.get()
        print('pwd',self.var_usr_pwd.get())
        inputpwd=self.var_usr_pwd.get()
        print('pwdID[inputnumber]',pwdID[inputnumber])
        #,pwdID,nameID
        
        try :
            print(inputnumber)
            print('pwdID[inputnumber]',pwdID[inputnumber])
            if pwdID[inputnumber] == inputpwd :
            
                self.secpage(inputnumber)
            else:
                self.no_file_worning1()
        except:
            self.no_file_worning()
            
    def no_file_worning(self):
        tk.messagebox.showwarning( title='錯誤', message='輸入資料錯誤，請重新輸入')
    def no_file_worning1(self):
        tk.messagebox.showwarning( title='錯誤', message='密碼不符，請重新輸入')
        
    def secpage(self,dp):
        print('secpage' ,dp)
        self.page.destroy()
        secondpage(self.root,dp)
        
        
    def th3page(self):
        self.page.destroy()
        th3page(self.root)



class secondpage(object):
    def __init__(self, master=None,dp=0):
        self.root = master
        root.geometry('600x800')

        self.page = tk.Frame(self.root)
        self.page.grid() 
        self.dp=dp
        print('selfdp',self.dp)
        self.Button = tk.Button(self.page, text=u'回登入頁',font=('Arial', 12),justify = tk.LEFT,command=self.mainpage) 
        self.Button.grid(column=0,row=0, sticky=tk.W) 
        
        self.Button = tk.Button(self.page, text=u'出缺勤查詢',font=('Arial', 12),justify = tk.LEFT,command=partial(self.personpage1,self.dp) ) 
        self.Button.grid(columnspan=2,row=0, sticky=tk.N+tk.S)         
        
        ##空白行
        #self.spaceLabel1= tk.Label(self.page,textvariable="      撼訊科技 遠端出勤打卡系統       " )
        #self.spaceLabel1.grid(column=0, row=1, sticky=tk.W)
        
        self.varpwdtitle=tk.StringVar()
        self.varpwdtitle.set("            ")
        self.pwdtitleLabel= tk.Label(self.page,textvariable=self.varpwdtitle, font=('Arial', 10),justify = tk.RIGHT )
        self.pwdtitleLabel.grid(column=0, row=1, sticky=tk.W)       
        
        self.vartitle=tk.StringVar()
        self.vartitle.set("撼訊科技 遠端出勤打卡系統")
        self.titleLabel= tk.Label(self.page,textvariable=self.vartitle, font=('Arial', 14),justify = tk.RIGHT )
        self.titleLabel.grid(column=0, row=2, sticky=tk.W)   
        
        self.vartitle2=tk.StringVar()
        self.vartitle2.set("員工： "+persenID[self.dp]+ '        部門： '+ pdID[self.dp])
        self.title2Label= tk.Label(self.page,textvariable=self.vartitle2, font=('Arial', 12),justify = tk.RIGHT )
        self.title2Label.grid(column=0,   row=3, sticky=tk.W)    
        #空白
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=4, sticky=tk.W) 
        
        self.vartitle2=tk.StringVar()
        self.vartitle2.set('  請輸入以下資訊，並按確定，系統將送出當下時間')
        self.title2Label= tk.Label(self.page,textvariable=self.vartitle2, font=('Arial', 12),justify = tk.RIGHT )
        self.title2Label.grid(column=0,   row=5, sticky=tk.W)    
        
        #self.mode='A'
        self.var1 = tk.StringVar()
        self.var1.set("A")
        #self.var1.grid(column=1, row=3,sticky=tk.W)
        
        #self.mode=""
   
        
        self.selectcircle1=tk.Radiobutton(self.page,text = '  異地上班', variable=self.var1, value='A',command=partial(self.dtest,'work')  , font=('Arial', 12) )
        self.selectcircle1.grid(column=0, row=6, pady=1, sticky=tk.W)      
        
        self.selectcircle2=tk.Radiobutton(self.page,text = '  異地下班',variable=self.var1,value='B',command=partial(self.dtest,'offwork')  , font=('Arial', 12) )
        self.selectcircle2.grid(column=0, row=6, pady=2, sticky=tk.N+tk.S)       
        
        #空白
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=7, sticky=tk.W)                  
        
        
        self.sv = ttk.Separator(self.page, orient=tk.HORIZONTAL)
        self.sv.grid(row=8,columnspan=8,sticky="ew")        
        
        
        
        self.selectcircle3=tk.Radiobutton(self.page,text = '  外出',variable=self.var1,value='C',command=partial(self.dtest,'businesstrip')  , font=('Arial', 12) )
        self.selectcircle3.grid(column=0, row=9, pady=1, sticky=tk.W  )     
        
        
        self.varBusinesstrip=tk.StringVar()
        self.varBusinesstrip.set("            事由:")
        self.BusinesstripLabel= tk.Label(self.page,textvariable=self.varBusinesstrip, font=('Arial', 12),justify = tk.RIGHT )
        self.BusinesstripLabel.grid(columnspan=9, row=10, pady=1, sticky=tk.W)  
        
        self.varBusinessWhy = tk.StringVar()
        self.entryBusinessWhy = tk.Entry(self.page, textvariable=self.varBusinessWhy)
        self.entryBusinessWhy.grid(columnspan=2,column=0, row=10, pady=1, sticky=tk.N+tk.S)    
        
        self.varthing2=tk.StringVar()
        self.varthing2.set("            地點:")
        self.varthing2Label= tk.Label(self.page,textvariable=self.varthing2, font=('Arial', 12),justify = tk.RIGHT )
        self.varthing2Label.grid(columnspan=9, row=11, pady=1, sticky=tk.W)
        
  
        self.varBusinessLocation = tk.StringVar()
        self.entryBusinessLocation = tk.Entry(self.page, textvariable=self.varBusinessLocation)
        self.entryBusinessLocation.grid(columnspan=2,column=0, row=11, pady=1, sticky=tk.N+tk.S)
        
        
        self.varthing2=tk.StringVar()
        self.varthing2.set("     同行人員:")
        self.varthing2Label= tk.Label(self.page,textvariable=self.varthing2, font=('Arial', 12),justify = tk.RIGHT )
        self.varthing2Label.grid(columnspan=9,column=0, row=12, pady=1, sticky=tk.W)
        
        
        self.varBusinessPerson1 = tk.StringVar()
        self.entryBusinessPerson1 = tk.Entry(self.page, textvariable=self.varBusinessPerson1)
        self.entryBusinessPerson1.grid(columnspan=2,column=0, row=12, pady=1, sticky=tk.N+tk.S)         
        self.varBusinessPerson1.set('同事1')
        
        self.varBusinessPerson2 = tk.StringVar()
        self.entryBusinessPerson2 = tk.Entry(self.page, textvariable=self.varBusinessPerson2)
        self.entryBusinessPerson2.grid(columnspan=2,column=1, row=12, pady=1, sticky=tk.N+tk.S) 
        self.varBusinessPerson2.set('同事2')
        
        self.varthing2=tk.StringVar()
        self.varthing2.set("     (請輸入工號)")
        self.varthing2Label= tk.Label(self.page,textvariable=self.varthing2, font=('Arial', 10),justify = tk.RIGHT )
        self.varthing2Label.grid(columnspan=9,column=0, row=13, pady=1, sticky=tk.W)        
        
        self.varBusinessPerson3 = tk.StringVar()
        self.entryBusinessPerson3 = tk.Entry(self.page, textvariable=self.varBusinessPerson3)
        self.entryBusinessPerson3.grid(columnspan=2,column=0, row=13, pady=1, sticky=tk.N+tk.S)         
        self.varBusinessPerson3.set('同事3')
        
        self.varBusinessPerson4 = tk.StringVar()
        self.entryBusinessPerson4 = tk.Entry(self.page, textvariable=self.varBusinessPerson4)
        self.entryBusinessPerson4.grid(columnspan=2,column=1, row=13, pady=1, sticky=tk.N+tk.S)          
        self.varBusinessPerson4.set('同事4')
        
        self.varthing2=tk.StringVar()
        self.varthing2.set("     外出日期:")
        self.varthing2Label= tk.Label(self.page,textvariable=self.varthing2, font=('Arial', 12),justify = tk.RIGHT )
        self.varthing2Label.grid(columnspan=9,column=0, row=14, pady=1, sticky=tk.W)  
        
        
        #選擇月份bar
        monthlist=['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月']
        self.comboMonth = ttk.Combobox(self.page, width=7 ,values=monthlist, font=('Arial', 12),state="readonly") 
        print(dict(self.comboMonth)) 
        self.comboMonth.grid(columnspan=2,column=0, row=14,sticky=tk.N+tk.S)
        self.comboMonth.current(int(newmonth)-1)
        print(self.comboMonth.current(), self.comboMonth.get())
        
        
        #選擇月份bar
        daylist=['1日','2日','3日','4日','5日','6日','7日','8日','9日','10日','11日','12日','13日','14日','15日','16日','17日','18日','19日','20日',
                 '21日','22日','23日','24日','25日','26日','27日','28日','29日','30日','31日']
        self.comboDay = ttk.Combobox(self.page, width=7 ,values=daylist, font=('Arial', 12),state="readonly") 
        print(dict(self.comboDay)) 
        self.comboDay.grid(columnspan=2,column=1, row=14,sticky=tk.N+tk.S)
        self.comboDay.current(int(newday)-1)
        print(self.comboDay.current(), self.comboDay.get())   
        
        self.varthing2=tk.StringVar()
        self.varthing2.set("     外出時間:")
        self.varthing2Label= tk.Label(self.page,textvariable=self.varthing2, font=('Arial', 12),justify = tk.RIGHT )
        self.varthing2Label.grid(columnspan=9,column=0, row=15, pady=1, sticky=tk.W)  
                
        self.varBusinessOutTime = tk.StringVar()
        self.entryBusinessOutTime = tk.Entry(self.page, textvariable=self.varBusinessOutTime)
        self.entryBusinessOutTime.grid(columnspan=2,column=0, row=15, pady=1, sticky=tk.N+tk.S)         
        self.varBusinessOutTime.set('00:00')
        

        
        #空白
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=17, sticky=tk.W)          
        
        self.sv = ttk.Separator(self.page, orient=tk.HORIZONTAL)
        self.sv.grid(row=18,columnspan=8,sticky="ew")         

        #空白
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=19, sticky=tk.W) 


        self.Button = tk.Button(self.page, text=u'確定',font=('Arial', 12),justify = tk.LEFT,command=partial(self.takerun)  ) 
        self.Button.grid(column=0,row=20, sticky=tk.N+tk.S)   
        

        root.mainloop()   
        
    def dtest(self, mode):
        self.mode=mode
        print('self.mode',self.mode)
        
        
    def takerun(self):
        #print('mode',mode)
        if not os.path.isdir('data/'):
            os.mkdir('data/')    
        else :
            print ('data  file exist')         
        
        path='home/AccessFace/home_card/'+self.dp+'/'
        personftp=downftp.nlst(path)
            
        print('personftp',personftp)     
        path88='data/'
        values12=self.dp+'-'+newyear+newmonth
        for pathperson in personftp:
            personfile=pathperson.split('/')
            personmonth=personfile[-1]
            print('personmonth',personmonth)
            personmonth1=personmonth.split('.')
            pmonth=personmonth1[0].split('-')
            if pmonth[1]==newyear+newmonth :
                print('pathperson yes',pathperson)
                
                f=open(path88+values12+'-personal.csv', 'wb')
                downftp.retrbinary('RETR ' + pathperson, f.write )
                print('download file'+path88+values12+'-personal.csv')                    
                f.close()
                
        
        newdate=datetime.now().strftime("%Y-%m-%d")
        newdtime=datetime.now().strftime("%H:%M:%S")
        
        try: 
            print('self.mode',self.mode)
            if self.mode=="offwork" :
                finalid=[]
                
                finalid.append(self.mode+','+ self.dp  +','+ persenID[self.dp] +','+ pdID[self.dp] +','+ newdate +','+newdtime+',None,None' )
                
                print('finalid',finalid)
                
                #np.savetxt(path_database+'database_Employee.csv', finalid,fmt='%s', delimiter=',')
                with open(path88+values12+'-personal.csv','a') as f: 
                    np.savetxt(f, finalid,fmt='%s', delimiter=',')
                f.close                    
                
            elif self.mode=="businesstrip" :
                finalid=[]
                
                #if self.varBusinessPerson1.get=="" or self.varBusinessPerson1.get=="同事1"  or  self.varBusinessPerson1.get==:
                
                
                finalid.append(self.mode+','+ self.dp  +','+ persenID[self.dp] +','+ pdID[self.dp] +','+ newdate +','+newdtime+',None,None' )
                
                print('finalid',finalid)
                
                #np.savetxt(path_database+'database_Employee.csv', finalid,fmt='%s', delimiter=',')
                with open(path88+values12+'-personal.csv','a') as f: 
                    np.savetxt(f, finalid,fmt='%s', delimiter=',')
                f.close        
            
            
        except:
            self.mode='work'
            print('self.mode',self.mode)
            finalid=[]
            
            finalid.append(self.mode+','+ self.dp  +','+ persenID[self.dp] +','+ pdID[self.dp] +','+ newdate +','+newdtime+',None,None' )
            
            print('finalid',finalid)
            
            #np.savetxt(path_database+'database_Employee.csv', finalid,fmt='%s', delimiter=',')
            with open(path88+values12+'-personal.csv','a') as f: 
                np.savetxt(f, finalid,fmt='%s', delimiter=',')
            f.close
            
        try:
            #d=ftp.cwd('home/AccessFace/')
            downftp.storbinary('STOR '+'home/AccessFace/home_card/'+self.dp+'/'+values12+'-personal.csv' , open(path88+values12+'-personal.csv', 'rb')) # 上傳FTP檔案
            print("succes upload: " +'home/AccessFace/home_card/'+self.dp+'/'+values12+'-personal.csv')
        except:
            print("upload failed: " +'home/AccessFace/home_card/'+self.dp+'/'+values12+'-personal.csv')
            print("upload failed. check.................        ......")
        
            
    def mainpage(self):
        self.page.destroy()
        mainpage(self.root)
        
    def personpage1(self,personq ):
        
        print('personq',personq)
        self.page.destroy()
        personpage(self.root,personq)

class personpage(object):
    def __init__(self, master=None,personq=0):
        self.root = master
        self.page = tk.Frame(self.root)
        self.page.grid()
        
        self.personq=personq
        self.Button = tk.Button(self.page, text=u'回登入頁',font=('Arial', 12),justify = tk.LEFT,command=self.mainpage ) 
        self.Button.grid(column=0,row=0 , sticky=tk.W ) 
        self.Button = tk.Button(self.page, text=u'返回',font=('Arial', 12),justify = tk.LEFT,command=partial(self.secpage,self.personq ) ) 
        self.Button.grid(columnspan=2 , row=0 , sticky=tk.N+tk.S)         
        
        #製作一年日期的查詢表
        sourceyear,sourcemonth,sourceday=month_and_day()
        #newtyear,newmonth,newday=month_and_day()
        
        print(sourceyear)
        print(sourcemonth)
        self.stryear=sourceyear
        self.strmonth=sourcemonth
        
        newtyear=int(sourceyear)
        newmonth=int(sourcemonth)
        
        values1=[]
        valuesmonth=[]
        valuesyear=[]
        #如果是12月倒數到1 取三個月值
        if newmonth==12 :
            for nt in range(-13,-10):
                #abs取對值
                tmonth=str(newtyear)+"/"+str(abs(nt+1))
                values1.append(tmonth )
                valuesmonth.append(str(newtyear))
                valuesmonth.append(str(abs(nt+1)) )
        else :#如果是非12月倒數到1，年減1
            for ny in range(0,3):
                if int(newmonth)==0 :
                    newtyear=int(newtyear)-1
                    newmonth=12
                values1.append(str(newtyear)+'/'+str(newmonth) )
                valuesyear.append(str(newtyear) )
                valuesmonth.append(str(newmonth) )                
                newmonth=int(newmonth)-1        
        
        
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=1, sticky=tk.W)
        
        varspace=tk.StringVar()
        varspace.set("個人頁面查詢： "+self.personq+ ' ' +persenID[personq] )
        spaceLabel= tk.Label(self.page,textvariable=varspace, font=('Arial', 12),justify = tk.LEFT )
        spaceLabel.grid(column=0, row=2, sticky=tk.W)
        
        
        
        
        

                
        print('values1',values1)
        varspace=tk.StringVar()
        varspace.set("選擇月份：")
        spaceLabel= tk.Label(self.page,textvariable=varspace, font=('Arial', 12),justify = tk.LEFT )
        spaceLabel.grid(column=0, row=3, sticky=tk.W)
        
        
        
        #選擇月份bar
        self.comboExample = ttk.Combobox(self.page, width=7 ,values=values1, font=('Arial', 12),state="readonly") 
        
        
        print(dict(self.comboExample)) 
        self.comboExample.grid(column=0, row=3,sticky=tk.N+tk.S)
        self.comboExample.current(0)
        print(self.comboExample.current(), self.comboExample.get())
    
        #選擇月份事件按鈕
        self.addButton = tk.Button(self.page, text = '查詢',command=partial(self.month_callbackFunc,personq), font=('Arial', 12) )
        self.addButton.grid(column=0, row=3, pady=1, sticky=tk.E)        
        
        
        
        
        #選擇月份事件按鈕
        #self.addButton = tk.Button(self.page, text = '重新整理資料庫',command=partial(self.allmonth_flesh,valuesmonth,valuesyear,values1), font=('Arial', 12) )
        #self.addButton.grid(column=1, row=3, pady=1, sticky=tk.E)   
        
        self.var1 = tk.StringVar()
        self.var1.set("A")
        
        #circleLabel= tk.Label(self.page,textvariable=self.var1, font=('Arial', 12),justify = tk.LEFT )
        #circleLabel.grid(column=1, row=3, sticky=tk.W)   
        #self.var1.grid(column=0, row=4,sticky=tk.N+tk.S)
        self.selectcircle=tk.Radiobutton(self.page,text = '合併檢視', variable=self.var1, value='A',command=partial(self.month_callbackFunc,personq)   , font=('Arial', 12) )
        self.selectcircle.grid(column=0, row=4, pady=1, sticky=tk.W)      
        
        self.selectcircle=tk.Radiobutton(self.page,text = '檢視晶片卡',variable=self.var1,value='B',command=partial(self.show_idcard_callbackFunc,personq)   , font=('Arial', 12) )
        self.selectcircle.grid(column=0,columnspan=2, row=4, pady=1, sticky=tk.N+tk.S)       
        
        self.selectcircle=tk.Radiobutton(self.page,text = '檢視人臉識別', variable=self.var1,value='C',command=partial(self.show_face_callbackFunc,personq)  , font=('Arial', 12) )
        self.selectcircle.grid(column=1, row=4, pady=1, sticky=tk.W)   
        
        self.selectcircle=tk.Radiobutton(self.page,text = '遠端', variable=self.var1,value='D',command=partial(self.show_remote_callbackFunc,personq)  , font=('Arial', 12) )
        self.selectcircle.grid(column=1, row=5, pady=1, sticky=tk.W)         
        
        #空白
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=6, sticky=tk.W)          
        
        
        
        #讀取csv並且取012345 colums
        onlyuse = np.loadtxt('data/'+self.stryear+self.strmonth+'.csv',dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5))
        print('onlyuse',onlyuse)        
        
        if len(glob.glob('data/'+self.stryear+self.strmonth+'-idcard.csv'))>=1 :
            print(glob.glob('data/'+self.stryear+self.strmonth+'-idcard.csv'))
            onlyidcard = np.loadtxt('data/'+self.stryear+self.strmonth+'-idcard.csv',dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5))
            print('===========onlyidcard===========',onlyidcard) 
            onlyuse=np.concatenate((onlyidcard,onlyuse),axis=0)    #拼接陣列     
        
        
        
        #搜尋是"vincent"的索引值
        userid=np.argwhere(onlyuse==persenID[self.personq])     
        #print('userid',userid)

        #透過索引值取出符合"vincent"要的rows
        onlyuse_id=onlyuse[userid[:,0],: ]
        #print('onlyuse_id',onlyuse_id)
   
        #=====learning=====保留搜尋到的列(row)到新的array
        #從array取得等於'Vincent'的索引
        #b[['open' '030704' 'Vincent' '760' '2020-01-02']
         #['open' '030704' 'Vincent' '760' '2020-01-02']
         #['open' '030704' '陳緯仁' '760' '2020-01-02']  
        #g=np.argwhere(b=='Vincent') 
        #g [[ 0  2]
          #[ 1  2]  
        
        #g[:,0]表示取出搜尋到colum索引 (0,1)
        #h=b[g[:,0],: ]表示將索引值colum的取出對應的rows ==>  b[[x,x,x,x,x],: ]取rows    b[:,[x,x,x,x,x] ] 取colums
        #h[['open' '030704' 'Vincent' '760' '2020-01-02']
         #['open' '030704' 'Vincent' '760' '2020-01-02']
        #=====learning=====        
        
        
        
        #=====learning=====刪除搜尋到的列(row)
        #從array取得等於'Vincent'的索引
        #b[['open' '030704' 'Vincent' '760' '2020-01-02']
         #['open' '030704' 'Vincent' '760' '2020-01-02']
         #['open' '030704' '陳緯仁' '760' '2020-01-02']  
        #g=np.argwhere(b=='Vincent') 
        #g [[ 0  2]
          #[ 1  2]  
        #接著將取出g的第一欄(colum) (g[:,[0]])並且打它變成一維陣列(.reshape(1, -1)[0)  ex.  g[:,[0]].reshape(1, -1)[0]
        #同理使用g[:,[0]].flatten()也可以把二維轉成一維
        #h=np.delete(b,g[:,[0]].reshape(1, -1)[0], axis = 0 ) #axis = 0刪除row axis =         1刪除colum
        #or h=np.delete(b,g[:,[0]].flatten(), axis = 0 )
        #or h=np.delete(b,g[:,0], axis = 0 )
        #h [['open' '030704' '陳緯仁' '760' '2020-01-02']]
        #=====learning=====
        
        #針對日期做排序 
        #這個寫法參考https://stackoverflow.com/questions/2828059/sorting-arrays-in-numpy-by-column/30623882
        ind = np.argsort( onlyuse_id[:,4] )
        #print('ind',ind)
        onlyuse_id = onlyuse_id[ind]
        #print('onlyuse_id',onlyuse_id)
        
        #=====learning=====排序
        #numpy.sort(a, axis, kind, order) 按照組數order排序
        #https://www.runoob.com/numpy/numpy-sort-search.html
        #dtype = [('state', str), ('id', int), ('name', str), ('dp', int), ('date', int), ('time', int)   ]
        #new_onlyuse_id = np.array(onlyuse_id, dtype=dtype) 
        #new_onlyuse_id=np.sort(new_onlyuse_id, order = date)        
        
        
    #======針對日期下的時間做排序======
        #取出日期
        date=onlyuse_id[:,4]
        #print(date)
        #刪除重複的日期
        uniquedate = np.unique(date) #刪除重複的元素https://www.twblogs.net/a/5c1f8d88bd9eee16b3daa874/
        print('uniquedate',uniquedate)
        
        #找尋除了第一筆跟最後一筆的其餘資料等要刪除的資料，並將index放入到detnum裡面
        detnum=[]
        for d in uniquedate:
            #找出符合日期的rows,取得index  ex.2020-01-01
            dindex_onlyuse=np.argwhere(onlyuse_id==d)
            #取得在原來array的index
            id1=dindex_onlyuse[:,0]
            #print('id1',id1)
            #利用index取出那兩rows
            onlyuse_id_a=onlyuse_id[dindex_onlyuse[:,0]]
            #print('onlyuse_id_a',onlyuse_id_a)
            
            #針對該兩rows排序 取出index
            index1=np.argsort(onlyuse_id_a[:,5] )
            #print('index1',index1)
            dingy=len(index1)-1
            
            if len(index1)>2:
                #print('index len pass>2',len(index1))
                
                for num in range(len(index1) ) :
                    #print(num)
                    if  (num != 0  and num != dingy) :
                        #print("num must detete")
                        #print('id1[index1[num]]',id1[index1[num]])
                        #從num順序找到id的實際index，並把它加到detnum最後在一次刪除
                        detnum.append(id1[index1[num]])
                    
                    #elif num==0:
                        #print("num is 0")                        
                    
                    #elif num == dingy  :
                        #print("num is last")
       
        #刪除除了第一筆跟最後一筆的其餘資料            
        print('除了當日第一筆跟最後一筆保留，其餘要刪除的項目detnum',detnum)
        onlyuse_id = np.delete(onlyuse_id, detnum, axis = 0)        
        
        #針對第一筆及最後一筆偵測如果時間相反則調換順序
        for d in uniquedate:
            #找出符合日期的rows,取得index  ex.2020-01-01
            dindex_onlyuse1=np.argwhere(onlyuse_id==d)
            #取得在原來array的index
            id1_1=dindex_onlyuse1[:,0]
            #print('id1_1',id1_1)
            #利用index取出那兩rows
            onlyuse_id_a_1=onlyuse_id[dindex_onlyuse1[:,0]]
            #print('onlyuse_id_a_1',onlyuse_id_a_1)
            
            index1_1=np.argsort(onlyuse_id_a_1[:,5] )
            #print('index1_1',index1_1)                
            
            #實際排序
            #onlyuse_id_a=onlyuse_id_a[index1]
            #print('change',onlyuse_id_a)
            
            #如果index第一個值為1，則時間順序需要交換，則需要在實際的陣列交喚
            if index1_1[0]>=1:
                #互換，僅限於兩個rows互換
                onlyuse_id[[id1_1[-1],id1_1[0]], :] = onlyuse_id[[id1_1[0], id1_1[1]], :]

        #print('最後調整的項目（含刪除）after',onlyuse_id)
        
        tree=ttk.Treeview(self.page,height =20 ,show='headings')#表格show='headings'隱藏第一欄
        tree["columns"]=("姓名","日期","第一筆時間","最後筆時間")
        tree.column("姓名",width=100)   #表示列,不显示
        tree.column("日期",width=100)   #表示列,不显示
        tree.column("第一筆時間",width=100)
        tree.column("最後筆時間",width=100)
        tree.heading("姓名",text="姓名")  #显示表头
        tree.heading("日期",text="日期")  #显示表头
        tree.heading("第一筆時間",text="第一筆時間")
        tree.heading("最後筆時間",text="最後筆時間")
        #tree.insert("", insert_mode, text='name first col')
        style = ttk.Style()
        style.configure("Treeview", font=('Arial',12))
        style.configure("Treeview.Heading", font=('Arial', 12))     
        
        line123=0
        for d in uniquedate:
            #找出符合日期的rows,取得index  ex.2020-01-01
            dindex_onlyuse=np.argwhere(onlyuse_id==d)
            #取得在原來array的index
            id1=dindex_onlyuse[:,0]
            #利用index取出那兩rows
            onlyuse_id_a=onlyuse_id[dindex_onlyuse[:,0]]
            #print            ('onlyuse_id_a',onlyuse_id_a)
            
            #print('onlyuse_id_a',onlyuse_id_a)
            #print('vvvv', onlyuse_id_a[:,5]  )
            
            name123=onlyuse_id_a[0:1,2]
            datetime=onlyuse_id_a[0:1,4]
            ontime=onlyuse_id_a[0:1,5]
            offtime=onlyuse_id_a[:,5]
            
            
            
            if len(id1)==1:
                tree.insert("",line123,text=name123[0] ,values=(name123[0],datetime[0],ontime[0],"  ") )
        
            else :
                tree.insert("",line123,text=name123[0] ,values=(name123[0],datetime[0],ontime[0],offtime[1]  ))
                
            line123=line123+1
    
        #vertical scrollbar------------    https://www.cnblogs.com/Tommy-Yu/p/4156014.html
        vbar = ttk.Scrollbar(self.page,orient=tk.VERTICAL,command=tree.yview)
        vbar.grid(column=10,row=7,sticky=tk.NS) 
        tree.configure(yscrollcommand=vbar.set)
        #tree.tag_configure ("monospace", font =(None，12) )
        tree.grid(columnspan=9,row=7,sticky=tk.W)    
        
        root.mainloop()   
        
    def mainpage(self):
        self.page.destroy()
        mainpage(self.root)

    def secpage(self,dp):
        self.page.destroy()
        secondpage(self.root,dp)


    def no_file_worning(self):
        tk.messagebox.showwarning( title='錯誤', message='沒有此月份資料，請重新匯入資料')

      
    def allmonth_flesh(self,valuesmonth,valuesyear,values1):
 
        #將輸入的日期格式轉換ex. 2020/1 ==> 202001
        pdtrue=[]
        for avv in values1:
            pday=avv.split('/')
            # x.month=10
            if int(pday[1])<10 and int(pday[1])>=1:
                pday[1]='0'+str(pday[1])
                #print (month)
            else :
                pday[1]=str(pday[1])            
            pdtrue.append(pday[0]+pday[1])
        print('pdtrue',pdtrue)
    
        #將轉換的月份ex.202001 搜尋對應日期的檔案
        for pmonth in pdtrue :
            month_file=glob.glob(r'../models/day/'+pmonth+'*-Full')
            print('month_file',month_file)
            
            month_file.sort()
            
            
            
            #搜尋到202001＊＊-Full等檔案，進一步找尋含有open的欄位
            for  dday in month_file:
                
                print('dday',dday)
                day_used = np.loadtxt(dday,dtype=np.str,delimiter='  ',usecols=(0))
                day_used=day_used.flatten()

                
                #將日期切割成單純的日期時間2019-12-11 18:07:33
                lined=0
                for findtime in  day_used :
                    
                    timemark=findtime.split('@')
                    #print('in',np.argwhere(findtime))
                    day_used[lined]=timemark[-1]
                    lined=lined+1
                    
                    
                #找出有open及open前一列的日期時間 
                index_open=[]
                line_open=0                
                for findopen in day_used:
                    if "Open" in findopen :
                        index_open.append(line_open-1)
                        index_open.append(line_open)
                    line_open=line_open+1
                    
                #利用index再次找出只有open及時間的陣列到day_used
                day_used=day_used[index_open ]
                
                
                #np.append(day_used,[['eeeeeeeeeeeeeeeee','111']],0)
                #print ('index_open',index_open)

                a1=np.array(dday)
                np.insert(day_used,0,values=a1,axis=0)
                print ("AFTER" ,day_used)
                #https://www.twblogs.net/a/5be2440f2b717720b51d2722
                
                index_hash=[]
                line_hash=0                 
                hash1=pmonth[:4]+'-'+pmonth[4:] #將202001變成2020-01
                #搜尋在202001＊裡面有2020-01＊開頭的時間將該行跟下一行抓取出來，以避免used id重複
                for day_check in day_used:
                    if hash1 in day_check :
                        index_hash.append(line_hash)
                        index_hash.append(line_hash+1)
                    line_hash=line_hash+1
                day_used=day_used[index_hash ]
                
                #轉換為open,030704,Vincent,754,2019-07-02,09:21:07格式
                finalid=[]
                index_ting=[]
                line_ting=0                 
                for day_check1 in day_used:
                    if hash1 in day_check1 :
                        #print('ddddddddd',day_used[line_ting+1])
                        #print('line_ting',line_ting)
                        groupid=day_used[line_ting+1].split(',')
                        realid=groupid[1].split(':')
                        #print('realid',realid[1])
                        dayandtime=day_check1.split(' ')
                        try :
                            newid='open,'+realid[1]+','+persenID[realid[1]] +','+ pdID[realid[1]] +','+dayandtime[0]+','+dayandtime[1]
                            #print('newid',newid)
                            finalid.append(newid)
                        except:
                            print('worning:'+realid[1]+'已經消失了')
                    line_ting=line_ting+1
                    
                #print('finalid',finalid)
                    
                #存檔
                with open('data/'+pmonth+'.csv','a') as f: 
                    #for i in range(5): 
                        #newresult = np.random.rand(2, 3) 
                   
                    np.savetxt(f, finalid,fmt='%s', delimiter=",")   
                #如何不覆蓋savetxt寫法
                #http://cn.voidcc.com/question/p-dfrpzwva-tp.html
                
            
   
        #daynamefile=[]
        #for ass in month_file :
            #daynamefile=ass.split('/')
            #print('daynamefile',str(daynamefile))
        ##for tryyear in valuesyear:
            
        
        
      
      
        
    def month_callbackFunc(self,personq):
        print('get month',self.comboExample.get())
                         
        
        callbackmonth=self.comboExample.get().split('/')
        backmonth=int(callbackmonth[1])
        
        # x.month=10
        if backmonth<10 and backmonth>=1:
            backmonth='0'+str(backmonth)
            #print (month)
        else :
            backmonth=str(backmonth)
          
        #print('backmonth',backmonth)
        
        #讀取csv並且取012345 colums
        
        try:
            onlyuse = np.loadtxt('data/'+callbackmonth[0]+backmonth+'.csv',dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5))
            print(onlyuse)
            
            
            if len(glob.glob('data/'+callbackmonth[0]+backmonth+'-idcard.csv'))>=1 :
                print(glob.glob('data/'+callbackmonth[0]+backmonth+'-idcard.csv'))
                onlyidcard = np.loadtxt('data/'+callbackmonth[0]+backmonth+'-idcard.csv',dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5))
                print('===========onlyidcard===========',onlyidcard) 
                onlyuse=np.concatenate((onlyidcard,onlyuse),axis=0)
                
            print('===========onlyuse===========',onlyuse)
            #搜尋是"vincent"的索引值
            userid=np.argwhere(onlyuse==persenID[self.personq])     
            #print('userid',userid)
    
            #透過索引值取出符合"vincent"要的rows
            onlyuse_id=onlyuse[userid[:,0],: ]
            #print('onlyuse_id',onlyuse_id)
       
            #針對日期做排序 
            #這個寫法參考https://stackoverflow.com/questions/2828059/sorting-arrays-in-numpy-by-column/30623882
            ind = np.argsort( onlyuse_id[:,4] )
            #print('ind',ind)
            onlyuse_id = onlyuse_id[ind]
            #print('onlyuse_id',onlyuse_id)
    
            #======針對日期下的時間做排序======
            #取出日期
            date=onlyuse_id[:,4]
            #print(date)
            #刪除重複的日期
            uniquedate = np.unique(date) #刪除重複的元素https://www.twblogs.net/a/5c1f8d88bd9eee16b3daa874/
            #print('uniquedate',uniquedate)
            
            #找尋除了第一筆跟最後一筆的其餘資料等要刪除的資料，並將index放入到detnum裡面
            detnum=[]
            for d in uniquedate:
                #找出符合日期的rows,取得index  ex.2020-01-01
                dindex_onlyuse=np.argwhere(onlyuse_id==d)
                #取得在原來array的index
                id1=dindex_onlyuse[:,0]
                #print('id1',id1)
                #利用index取出那兩rows
                onlyuse_id_a=onlyuse_id[dindex_onlyuse[:,0]]
                #print('onlyuse_id_a',onlyuse_id_a)
                
                #針對該兩rows排序 取出index
                index1=np.argsort(onlyuse_id_a[:,5] )
                #print('index1',index1)
                dingy=len(index1)-1
                
                if len(index1)>2:
                    #print('index len pass>2',len(index1))
                    
                    for num in range(len(index1) ) :
                        #print(num)
                        if  (num != 0  and num != dingy) :
                            #print("num must detete")
                            #print('id1[index1[num]]',id1[index1[num]])
                            #從num順序找到id的實際index，並把它加到detnum最後在一次刪除
                            detnum.append(id1[index1[num]])
                        
                        #elif num==0:
                            #print("num is 0")                        
                        
                        #elif num == dingy  :
                            #print("num is last")
           
            #刪除除了第一筆跟最後一筆的其餘資料            
            print('除了當日第一筆跟最後一筆保留，其餘要刪除的項目detnum',detnum)
            onlyuse_id = np.delete(onlyuse_id, detnum, axis = 0)        
            
            #針對第一筆及最後一筆偵測如果時間相反則調換順序
            for d in uniquedate:
                #找出符合日期的rows,取得index  ex.2020-01-01
                dindex_onlyuse1=np.argwhere(onlyuse_id==d)
                #取得在原來array的index
                id1_1=dindex_onlyuse1[:,0]
                #print('id1_1',id1_1)
                #利用index取出那兩rows
                onlyuse_id_a_1=onlyuse_id[dindex_onlyuse1[:,0]]
                #print('onlyuse_id_a_1',onlyuse_id_a_1)
                
                index1_1=np.argsort(onlyuse_id_a_1[:,5] )
                #print('index1_1',index1_1)                
                
                #實際排序
                #onlyuse_id_a=onlyuse_id_a[index1]
                #print('change',onlyuse_id_a)
                
                #如果index第一個值為1，則時間順序需要交換，則需要在實際的陣列交喚
                if index1_1[0]>=1:
                    #互換，僅限於兩個rows互換
                    onlyuse_id[[id1_1[-1],id1_1[0]], :] = onlyuse_id[[id1_1[0], id1_1[1]], :]
    
            #print('最後調整的項目（含刪除）after',onlyuse_id)
            
            tree=ttk.Treeview(self.page,height =20 ,show='headings')#表格show='headings'隱藏第一欄
            tree["columns"]=("姓名","日期","第一筆時間","最後筆時間")
            tree.column("姓名",width=100)   #表示列,不显示
            tree.column("日期",width=100)   #表示列,不显示
            tree.column("第一筆時間",width=100)
            tree.column("最後筆時間",width=100)
            tree.heading("姓名",text="姓名")  #显示表头
            tree.heading("日期",text="日期")  #显示表头
            tree.heading("第一筆時間",text="第一筆時間")
            tree.heading("最後筆時間",text="最後筆時間")
            #tree.insert("", insert_mode, text='name first col')
            style = ttk.Style()
            style.configure("Treeview", font=('Arial',12))
            style.configure("Treeview.Heading", font=('Arial', 12)) 
            
            line123=0
            for d in uniquedate:
                #找出符合日期的rows,取得index  ex.2020-01-01
                dindex_onlyuse=np.argwhere(onlyuse_id==d)
                #取得在原來array的index
                id1=dindex_onlyuse[:,0]
                #利用index取出那兩rows
                onlyuse_id_a=onlyuse_id[dindex_onlyuse[:,0]]
                #print            ('onlyuse_id_a',onlyuse_id_a)
                
                #print('onlyuse_id_a',onlyuse_id_a)
                #print('vvvv', onlyuse_id_a[:,5]  )
                
                name123=onlyuse_id_a[0:1,2]
                datetime=onlyuse_id_a[0:1,4]
                ontime=onlyuse_id_a[0:1,5]
                offtime=onlyuse_id_a[:,5]
                
                
                        
                if len(id1)==1:
                    tree.insert("",line123,text=name123[0] ,values=(name123[0],datetime[0],ontime[0],"  "))
            
                else :
                    tree.insert("",line123,text=name123[0] ,values=(name123[0],datetime[0],ontime[0],offtime[1]  ) )
                    
                line123=line123+1
        
            #vertical scrollbar------------    https://www.cnblogs.com/Tommy-Yu/p/4156014.html
            vbar = ttk.Scrollbar(self.page,orient=tk.VERTICAL,command=tree.yview)
            vbar.grid(column=10,row=5,sticky=tk.NS) 
            tree.configure(yscrollcommand=vbar.set)
            
            tree.grid(columnspan=9,row=5,sticky=tk.W)    
    
            root.mainloop()   
            
            
            
        except:
            self.no_file_worning()
        



    def show_idcard_callbackFunc(self,personq):
        print('get month',self.comboExample.get())
                         
      
        callbackmonth=self.comboExample.get().split('/')
        backmonth=int(callbackmonth[1])
        
        # x.month=10
        if backmonth<10 and backmonth>=1:
            backmonth='0'+str(backmonth)
            #print (month)
        else :
            backmonth=str(backmonth)
          
        #print('backmonth',backmonth)
        
        #讀取csv並且取012345 colums
        
        try:
            onlyuse = np.loadtxt('data/'+callbackmonth[0]+backmonth+'-idcard.csv',dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5))
            print(onlyuse)
            
            
     
                
            print('===========onlyuse===========',onlyuse)
            #搜尋是"vincent"的索引值
            userid=np.argwhere(onlyuse==self.personq)     
            #print('userid',userid)
    
            #透過索引值取出符合"vincent"要的rows
            onlyuse_id=onlyuse[userid[:,0],: ]
            #print('onlyuse_id',onlyuse_id)
       
            #針對日期做排序 
            #這個寫法參考https://stackoverflow.com/questions/2828059/sorting-arrays-in-numpy-by-column/30623882
            ind = np.argsort( onlyuse_id[:,4] )
            #print('ind',ind)
            onlyuse_id = onlyuse_id[ind]
            #print('onlyuse_id',onlyuse_id)
    
            #======針對日期下的時間做排序======
            #取出日期
            date=onlyuse_id[:,4]
            #print(date)
            #刪除重複的日期
            uniquedate = np.unique(date) #刪除重複的元素https://www.twblogs.net/a/5c1f8d88bd9eee16b3daa874/
            #print('uniquedate',uniquedate)
            
            #找尋除了第一筆跟最後一筆的其餘資料等要刪除的資料，並將index放入到detnum裡面
            detnum=[]
            for d in uniquedate:
                #找出符合日期的rows,取得index  ex.2020-01-01
                dindex_onlyuse=np.argwhere(onlyuse_id==d)
                #取得在原來array的index
                id1=dindex_onlyuse[:,0]
                #print('id1',id1)
                #利用index取出那兩rows
                onlyuse_id_a=onlyuse_id[dindex_onlyuse[:,0]]
                #print('onlyuse_id_a',onlyuse_id_a)
                
                #針對該兩rows排序 取出index
                index1=np.argsort(onlyuse_id_a[:,5] )
                #print('index1',index1)
                dingy=len(index1)-1
                
                if len(index1)>2:
                    #print('index len pass>2',len(index1))
                    
                    for num in range(len(index1) ) :
                        #print(num)
                        if  (num != 0  and num != dingy) :
                            #print("num must detete")
                            #print('id1[index1[num]]',id1[index1[num]])
                            #從num順序找到id的實際index，並把它加到detnum最後在一次刪除
                            detnum.append(id1[index1[num]])
                        
                        #elif num==0:
                            #print("num is 0")                        
                        
                        #elif num == dingy  :
                            #print("num is last")
           
            #刪除除了第一筆跟最後一筆的其餘資料            
            print('除了當日第一筆跟最後一筆保留，其餘要刪除的項目detnum',detnum)
            onlyuse_id = np.delete(onlyuse_id, detnum, axis = 0)        
            
            #針對第一筆及最後一筆偵測如果時間相反則調換順序
            for d in uniquedate:
                #找出符合日期的rows,取得index  ex.2020-01-01
                dindex_onlyuse1=np.argwhere(onlyuse_id==d)
                #取得在原來array的index
                id1_1=dindex_onlyuse1[:,0]
                #print('id1_1',id1_1)
                #利用index取出那兩rows
                onlyuse_id_a_1=onlyuse_id[dindex_onlyuse1[:,0]]
                #print('onlyuse_id_a_1',onlyuse_id_a_1)
                
                index1_1=np.argsort(onlyuse_id_a_1[:,5] )
                #print('index1_1',index1_1)                
                
                #實際排序
                #onlyuse_id_a=onlyuse_id_a[index1]
                #print('change',onlyuse_id_a)
                
                #如果index第一個值為1，則時間順序需要交換，則需要在實際的陣列交喚
                if index1_1[0]>=1:
                    #互換，僅限於兩個rows互換
                    onlyuse_id[[id1_1[-1],id1_1[0]], :] = onlyuse_id[[id1_1[0], id1_1[1]], :]
    
            #print('最後調整的項目（含刪除）after',onlyuse_id)
            
            tree=ttk.Treeview(self.page,height =20 ,show='headings')#表格show='headings'隱藏第一欄
            tree["columns"]=("姓名","日期","第一筆時間","最後筆時間")
            tree.column("姓名",width=100)   #表示列,不显示
            tree.column("日期",width=100)   #表示列,不显示
            tree.column("第一筆時間",width=100)
            tree.column("最後筆時間",width=100)
            tree.heading("姓名",text="姓名")  #显示表头
            tree.heading("日期",text="日期")  #显示表头
            tree.heading("第一筆時間",text="第一筆時間")
            tree.heading("最後筆時間",text="最後筆時間")
            #tree.insert("", insert_mode, text='name first col')
            style = ttk.Style()
            style.configure("Treeview", font=('Arial',12))
            style.configure("Treeview.Heading", font=('Arial', 12)) 
            
            line123=0
            for d in uniquedate:
                #找出符合日期的rows,取得index  ex.2020-01-01
                dindex_onlyuse=np.argwhere(onlyuse_id==d)
                #取得在原來array的index
                id1=dindex_onlyuse[:,0]
                #利用index取出那兩rows
                onlyuse_id_a=onlyuse_id[dindex_onlyuse[:,0]]
                #print            ('onlyuse_id_a',onlyuse_id_a)
                
                #print('onlyuse_id_a',onlyuse_id_a)
                #print('vvvv', onlyuse_id_a[:,5]  )
                
                name123=onlyuse_id_a[0:1,2]
                datetime=onlyuse_id_a[0:1,4]
                ontime=onlyuse_id_a[0:1,5]
                offtime=onlyuse_id_a[:,5]
                
                
                        
                if len(id1)==1:
                    tree.insert("",line123,text=name123[0] ,values=(name123[0],datetime[0],ontime[0],"  "))
            
                else :
                    tree.insert("",line123,text=name123[0] ,values=(name123[0],datetime[0],ontime[0],offtime[1]  ) )
                    
                line123=line123+1
        
            #vertical scrollbar------------    https://www.cnblogs.com/Tommy-Yu/p/4156014.html
            vbar = ttk.Scrollbar(self.page,orient=tk.VERTICAL,command=tree.yview)
            vbar.grid(column=10,row=5,sticky=tk.NS) 
            tree.configure(yscrollcommand=vbar.set)
            
            tree.grid(columnspan=9,row=5,sticky=tk.W)    
    
            root.mainloop()   
            
            
            
        except:
            self.no_file_worning()

    def show_face_callbackFunc(self,personq):
        print('get month',self.comboExample.get())
                         
      
        callbackmonth=self.comboExample.get().split('/')
        backmonth=int(callbackmonth[1])
        
        # x.month=10
        if backmonth<10 and backmonth>=1:
            backmonth='0'+str(backmonth)
            #print (month)
        else :
            backmonth=str(backmonth)
          
        #print('backmonth',backmonth)
        
        #讀取csv並且取012345 colums
        
        try:
            onlyuse = np.loadtxt('data/'+callbackmonth[0]+backmonth+'.csv',dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5))
            print(onlyuse)
            
            
     
                
            print('===========onlyuse===========',onlyuse)
            #搜尋是"vincent"的索引值
            userid=np.argwhere(onlyuse==self.personq)     
            #print('userid',userid)
    
            #透過索引值取出符合"vincent"要的rows
            onlyuse_id=onlyuse[userid[:,0],: ]
            #print('onlyuse_id',onlyuse_id)
       
            #針對日期做排序 
            #這個寫法參考https://stackoverflow.com/questions/2828059/sorting-arrays-in-numpy-by-column/30623882
            ind = np.argsort( onlyuse_id[:,4] )
            #print('ind',ind)
            onlyuse_id = onlyuse_id[ind]
            #print('onlyuse_id',onlyuse_id)
    
            #======針對日期下的時間做排序======
            #取出日期
            date=onlyuse_id[:,4]
            #print(date)
            #刪除重複的日期
            uniquedate = np.unique(date) #刪除重複的元素https://www.twblogs.net/a/5c1f8d88bd9eee16b3daa874/
            #print('uniquedate',uniquedate)
            
            #找尋除了第一筆跟最後一筆的其餘資料等要刪除的資料，並將index放入到detnum裡面
            detnum=[]
            for d in uniquedate:
                #找出符合日期的rows,取得index  ex.2020-01-01
                dindex_onlyuse=np.argwhere(onlyuse_id==d)
                #取得在原來array的index
                id1=dindex_onlyuse[:,0]
                #print('id1',id1)
                #利用index取出那兩rows
                onlyuse_id_a=onlyuse_id[dindex_onlyuse[:,0]]
                #print('onlyuse_id_a',onlyuse_id_a)
                
                #針對該兩rows排序 取出index
                index1=np.argsort(onlyuse_id_a[:,5] )
                #print('index1',index1)
                dingy=len(index1)-1
                
                if len(index1)>2:
                    #print('index len pass>2',len(index1))
                    
                    for num in range(len(index1) ) :
                        #print(num)
                        if  (num != 0  and num != dingy) :
                            #print("num must detete")
                            #print('id1[index1[num]]',id1[index1[num]])
                            #從num順序找到id的實際index，並把它加到detnum最後在一次刪除
                            detnum.append(id1[index1[num]])
                        
                        #elif num==0:
                            #print("num is 0")                        
                        
                        #elif num == dingy  :
                            #print("num is last")
           
            #刪除除了第一筆跟最後一筆的其餘資料            
            print('除了當日第一筆跟最後一筆保留，其餘要刪除的項目detnum',detnum)
            onlyuse_id = np.delete(onlyuse_id, detnum, axis = 0)        
            
            #針對第一筆及最後一筆偵測如果時間相反則調換順序
            for d in uniquedate:
                #找出符合日期的rows,取得index  ex.2020-01-01
                dindex_onlyuse1=np.argwhere(onlyuse_id==d)
                #取得在原來array的index
                id1_1=dindex_onlyuse1[:,0]
                #print('id1_1',id1_1)
                #利用index取出那兩rows
                onlyuse_id_a_1=onlyuse_id[dindex_onlyuse1[:,0]]
                #print('onlyuse_id_a_1',onlyuse_id_a_1)
                
                index1_1=np.argsort(onlyuse_id_a_1[:,5] )
                #print('index1_1',index1_1)                
                
                #實際排序
                #onlyuse_id_a=onlyuse_id_a[index1]
                #print('change',onlyuse_id_a)
                
                #如果index第一個值為1，則時間順序需要交換，則需要在實際的陣列交喚
                if index1_1[0]>=1:
                    #互換，僅限於兩個rows互換
                    onlyuse_id[[id1_1[-1],id1_1[0]], :] = onlyuse_id[[id1_1[0], id1_1[1]], :]
    
            #print('最後調整的項目（含刪除）after',onlyuse_id)
            
            tree=ttk.Treeview(self.page,height =20 ,show='headings')#表格show='headings'隱藏第一欄
            tree["columns"]=("姓名","日期","第一筆時間","最後筆時間")
            tree.column("姓名",width=100)   #表示列,不显示
            tree.column("日期",width=100)   #表示列,不显示
            tree.column("第一筆時間",width=100)
            tree.column("最後筆時間",width=100)
            tree.heading("姓名",text="姓名")  #显示表头
            tree.heading("日期",text="日期")  #显示表头
            tree.heading("第一筆時間",text="第一筆時間")
            tree.heading("最後筆時間",text="最後筆時間")
            #tree.insert("", insert_mode, text='name first col')
            style = ttk.Style()
            style.configure("Treeview", font=('Arial',12))
            style.configure("Treeview.Heading", font=('Arial', 12)) 
            
            line123=0
            for d in uniquedate:
                #找出符合日期的rows,取得index  ex.2020-01-01
                dindex_onlyuse=np.argwhere(onlyuse_id==d)
                #取得在原來array的index
                id1=dindex_onlyuse[:,0]
                #利用index取出那兩rows
                onlyuse_id_a=onlyuse_id[dindex_onlyuse[:,0]]
                #print            ('onlyuse_id_a',onlyuse_id_a)
                
                #print('onlyuse_id_a',onlyuse_id_a)
                #print('vvvv', onlyuse_id_a[:,5]  )
                
                name123=onlyuse_id_a[0:1,2]
                datetime=onlyuse_id_a[0:1,4]
                ontime=onlyuse_id_a[0:1,5]
                offtime=onlyuse_id_a[:,5]
                
                
                        
                if len(id1)==1:
                    tree.insert("",line123,text=name123[0] ,values=(name123[0],datetime[0],ontime[0],"  "))
            
                else :
                    tree.insert("",line123,text=name123[0] ,values=(name123[0],datetime[0],ontime[0],offtime[1]  ) )
                    
                line123=line123+1
        
            #vertical scrollbar------------    https://www.cnblogs.com/Tommy-Yu/p/4156014.html
            vbar = ttk.Scrollbar(self.page,orient=tk.VERTICAL,command=tree.yview)
            vbar.grid(column=10,row=5,sticky=tk.NS) 
            tree.configure(yscrollcommand=vbar.set)
            
            tree.grid(columnspan=9,row=5,sticky=tk.W)    
    
            root.mainloop()   
            
            
            
        except:
            self.no_file_worning()
              

    def show_remote_callbackFunc(self,personq):
        print('get month',self.comboExample.get())
                         
      
        callbackmonth=self.comboExample.get().split('/')
        backmonth=int(callbackmonth[1])
        
        # x.month=10
        if backmonth<10 and backmonth>=1:
            backmonth='0'+str(backmonth)
            #print (month)
        else :
            backmonth=str(backmonth)
          
        #print('backmonth',backmonth)
        
        #讀取csv並且取012345 colums
        
        #try:
        onlyuse = np.loadtxt('data/'+self.personq+'-'+callbackmonth[0]+backmonth+'-personal.csv',dtype=np.str,delimiter=',',usecols=(0,1,4,5,6,7))
        print(onlyuse)
        
        
 
            
        print('===========onlyuse===========',onlyuse)
        #搜尋是"vincent"的索引值
        userid=np.argwhere(onlyuse==self.personq)     
        #print('userid',userid)

        #透過索引值取出符合"vincent"要的rows
        onlyuse_id=onlyuse[userid[:,0],: ]
        #print('onlyuse_id',onlyuse_id)
   
        #針對日期做排序 
        #這個寫法參考https://stackoverflow.com/questions/2828059/sorting-arrays-in-numpy-by-column/30623882
        ind = np.argsort( onlyuse_id[:,4] )
        #print('ind',ind)
        onlyuse_id = onlyuse_id[ind]
        #print('onlyuse_id',onlyuse_id)

        #======針對日期下的時間做排序======
        #取出日期
        date=onlyuse_id[:,4]
        #print(date)
        #刪除重複的日期
        uniquedate = np.unique(date) #刪除重複的元素https://www.twblogs.net/a/5c1f8d88bd9eee16b3daa874/
        #print('uniquedate',uniquedate)
        
        #找尋除了第一筆跟最後一筆的其餘資料等要刪除的資料，並將index放入到detnum裡面
        detnum=[]
        for d in uniquedate:
            #找出符合日期的rows,取得index  ex.2020-01-01
            dindex_onlyuse=np.argwhere(onlyuse_id==d)
            #取得在原來array的index
            id1=dindex_onlyuse[:,0]
            #print('id1',id1)
            #利用index取出那兩rows
            onlyuse_id_a=onlyuse_id[dindex_onlyuse[:,0]]
            #print('onlyuse_id_a',onlyuse_id_a)
            
            #針對該兩rows排序 取出index
            index1=np.argsort(onlyuse_id_a[:,5] )
            #print('index1',index1)
            dingy=len(index1)-1
            
            if len(index1)>2:
                #print('index len pass>2',len(index1))
                
                for num in range(len(index1) ) :
                    #print(num)
                    if  (num != 0  and num != dingy) :
                        #print("num must detete")
                        #print('id1[index1[num]]',id1[index1[num]])
                        #從num順序找到id的實際index，並把它加到detnum最後在一次刪除
                        detnum.append(id1[index1[num]])
                    
                    #elif num==0:
                        #print("num is 0")                        
                    
                    #elif num == dingy  :
                        #print("num is last")
       
        ##刪除除了第一筆跟最後一筆的其餘資料            
        #print('除了當日第一筆跟最後一筆保留，其餘要刪除的項目detnum',detnum)
        #onlyuse_id = np.delete(onlyuse_id, detnum, axis = 0)        
        
        ##針對第一筆及最後一筆偵測如果時間相反則調換順序
        #for d in uniquedate:
            ##找出符合日期的rows,取得index  ex.2020-01-01
            #dindex_onlyuse1=np.argwhere(onlyuse_id==d)
            ##取得在原來array的index
            #id1_1=dindex_onlyuse1[:,0]
            ##print('id1_1',id1_1)
            ##利用index取出那兩rows
            #onlyuse_id_a_1=onlyuse_id[dindex_onlyuse1[:,0]]
            ##print('onlyuse_id_a_1',onlyuse_id_a_1)
            
            #index1_1=np.argsort(onlyuse_id_a_1[:,5] )
            ##print('index1_1',index1_1)                
            
            ##實際排序
            ##onlyuse_id_a=onlyuse_id_a[index1]
            ##print('change',onlyuse_id_a)
            
            ##如果index第一個值為1，則時間順序需要交換，則需要在實際的陣列交喚
            #if index1_1[0]>=1:
                ##互換，僅限於兩個rows互換
                #onlyuse_id[[id1_1[-1],id1_1[0]], :] = onlyuse_id[[id1_1[0], id1_1[1]], :]

        #print('最後調整的項目（含刪除）after',onlyuse_id)
        
        tree=ttk.Treeview(self.page,height =20 ,show='headings')#表格show='headings'隱藏第一欄
        tree["columns"]=("狀態","日期","第一筆時間","最後筆時間")
        tree.column("狀態",width=100)   #表示列,不显示
        tree.column("日期",width=100)   #表示列,不显示
        tree.column("第一筆時間",width=100)
        tree.column("最後筆時間",width=100)
        tree.heading("狀態",text="狀態")  #显示表头
        tree.heading("日期",text="日期")  #显示表头
        tree.heading("第一筆時間",text="第一筆時間")
        tree.heading("最後筆時間",text="最後筆時間")
        #tree.insert("", insert_mode, text='name first col')
        style = ttk.Style()
        style.configure("Treeview", font=('Arial',12))
        style.configure("Treeview.Heading", font=('Arial', 12)) 
        
        line123=0
        for d in uniquedate:
            #找出符合日期的rows,取得index  ex.2020-01-01
            dindex_onlyuse=np.argwhere(onlyuse_id==d)
            #取得在原來array的index
            id1=dindex_onlyuse[:,0]
            #利用index取出那兩rows
            onlyuse_id_a=onlyuse_id[dindex_onlyuse[:,0]]
            #print            ('onlyuse_id_a',onlyuse_id_a)
            
            print('onlyuse_id_a',onlyuse_id_a)
            print('vvvv', onlyuse_id_a[:,5]  )
            
            name123=onlyuse_id_a[0:1,0]
            datetime=onlyuse_id_a[0:1,2]
            ontime=onlyuse_id_a[0:1,3]
            offtime=onlyuse_id_a[:,3]
            
            
                    
            if len(id1)==1:
                tree.insert("",line123,text=name123[0] ,values=(name123[0],datetime[0],ontime[0],"  "))
        
            else :
                tree.insert("",line123,text=name123[0] ,values=(name123[0],datetime[0],ontime[0],offtime[1]  ) )
                
            line123=line123+1
    
        #vertical scrollbar------------    https://www.cnblogs.com/Tommy-Yu/p/4156014.html
        vbar = ttk.Scrollbar(self.page,orient=tk.VERTICAL,command=tree.yview)
        vbar.grid(column=10,row=5,sticky=tk.NS) 
        tree.configure(yscrollcommand=vbar.set)
        
        tree.grid(columnspan=9,row=5,sticky=tk.W)    

        root.mainloop()   
        
            
            
        #except:
            #self.no_file_worning()



#建立資料夾
if not os.path.isdir('data/'):
    os.mkdir('data/')    
else :
    print ('data  file exist') 
    
if not os.path.isdir('image/'):
    os.mkdir('image/')    
else :
    print ('image  file exist') 
    

try:
    f=open(path88+'database_Employee-notchinese.csv', 'wb')
    downftp.retrbinary('RETR ' + 'home/AccessFace/config/database_Employee-notchinese.csv', f.write )
    print('download file'+path88+'database_Employee-notchinese.csv')                    
    f.close()

    

except:
    print("download failed. check.......................")

number123,persenID,pdID,fullID,pwdID,nameID=person_pd_ID()    



newyear,newmonth,newday=month_and_day()

print(nameID)
print(pwdID)



#downftp.quit()                  # 退出FTP伺服器   



try:
    os.remove(path88+'database_Employee-notchinese.csv')
    print(path88+'database_Employee-notchinese.csv 刪除成功' )
except:
    print(path88+'database_Employee-notchinese.csv 檔案不存在')


root = tk.Tk()
# root = tk.Toplevel()
# https://blog.csdn.net/FunkyPants/article/details/78163021

root.title('撼訊科技 人資查詢系統')
root.geometry('500x300')

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)

root.config(menu=menubar)

mainpage(root)

root.mainloop() 































"""
import tkinter as tk

window = tk.Tk()
window.title('撼訊科技 人資查詢系統')
window.geometry('500x300')

# welcome image
canvas = tk.Canvas(window, height=200, width=500)
image_file = tk.PhotoImage(file='tul_logo1.gif')
image = canvas.create_image(0,0, anchor='nw', image=image_file)
canvas.pack(side='top')

# user information
tk.Label(window, text='中文姓名: ').place(x=50, y= 150)
tk.Label(window, text='密碼: ').place(x=50, y= 190)
tk.Label(window, text='預設密碼為工號').place(x=160, y= 210)
var_usr_name = tk.StringVar()
var_usr_pwd = tk.StringVar()
#var_usr_name.set('請輸入中文姓名')
var_usr_pwd.set('預設密碼為工號')
entry_usr_name = tk.Entry(window, textvariable=var_usr_name)
entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd)
entry_usr_name.place(x=160, y=150)
var_usr_pwd = tk.StringVar()
entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
entry_usr_pwd.place(x=160, y=190)

def usr_login():
    pass
def usr_sign_up():
    pass

# login and sign up button
btn_login = tk.Button(window, text='登入', command=usr_login)
btn_login.place(x=170, y=230)
#btn_sign_up = tk.Button(window, text='註冊', command=usr_sign_up)
#btn_sign_up.place(x=270, y=230)

window.mainloop()

"""