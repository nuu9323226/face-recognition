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
# windows版本打包指令 pyinstaller.exe -F -w .\user-gui-debug0427.py -i tul_logo.ico
# windows版本 更改 Arial==>微軟正黑體
"""
#20200422 1.修復檢視會跑位vbar.grid(column=10,row=5) ==>vbar.grid(column=10,row=7) 2.修復windows需要強至使用encoding = 'utf-8'  downftp.encoding='utf-8'
          3.增加使用亂碼檔名 4.增加網路錯誤時顯示網路連線錯誤提醒
"""

VERSON='20200518'

#檔案密碼
firstmonth='FSvQnEV'
secendmonth='9XuTbag'
thirdmonth='mR57Zg'
allmonthdic=[firstmonth,secendmonth,thirdmonth]

cardid='K5tuP'
faceid='Gn9r2'
personalid='55EBT'
alltypedic=[cardid,faceid,personalid]
alltypename=['idcard','face','personal']
alltypechange = dict(zip(alltypename, alltypedic))
global failconn
failconn=0
path88 =  'data/'

#from ftplib import FTP_TLS
try:
    downftp = FTP()
    timeout = 6
    port = 21
    #如果ftp有啟動ftps (ssl/tls)加密服務則需要用以下方式連線
    #https://stackoverflow.com/questions/5534830/ftpes-ftp-over-explicit-tls-ssl-in-python
    #from ftplib import FTP_TLS
    #downftp=FTP_TLS('61.220.84.60')
    downftp.connect('61.220.84.60',port,timeout) # 連線FTP伺服器
    downftp.login('Vincent','helloworld') # 登入
    downftp.encoding='utf-8'
    downftp.set_pasv(False)
    print (downftp.getwelcome())  # 獲得歡迎資訊 
    #d=ftp.cwd('home/AccessFace/month')    # 設定FTP路徑
    monthftp=downftp.nlst('home/AccessFace/month') #獲取ftp上的所以月份檔案
    print('monthftp',monthftp)
except:
    print('not connect to ftp')
    failconn=1

def weekreport(daytime):
    weekreturn=0
    qweek=datetime.strptime (daytime,'%Y-%m-%d').weekday() 
    if qweek==0:
        weekreturn='一'
    if qweek==1:
        weekreturn='二'
    if qweek==2:
        weekreturn='三'
    if qweek==3:
        weekreturn='四'  
    if qweek==4:
        weekreturn='五'  
    if qweek==5:
        weekreturn='六'  
    if qweek==6:
        weekreturn='日'         
    
    return weekreturn

def ftpconn():
    try:
        f=open(path88+'database_Employee-notchinese.csv', 'wb')
        downftp.retrbinary('RETR ' + 'home/AccessFace/config/database_Employee-notchinese.csv', f.write )
        print('download file'+path88+'database_Employee-notchinese.csv')                    
        f.close()
        
        number123,persenID,pdID,fullID,pwdID,nameID=person_pd_ID()
        os.remove(path88+'database_Employee-notchinese.csv')
        print(path88+'database_Employee-notchinese.csv 刪除成功' )
        return number123,persenID,pdID,fullID,pwdID,nameID

    except:
        print("download failed. check.......................")    
        mainpage(root)


def secretname(vaild):
    
    allmonthchange = dict(zip(vaild, allmonthdic))
    return allmonthchange
    


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
        pwd15=all_23[6]
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
        
        global failconn
        
        try:
            image_file = tk.PhotoImage(file='data/tul_logo1.gif')
            canvas = tk.Canvas(self.page, height=500, width=500)
            self.image = canvas.create_image(0,0, anchor='nw', image=image_file)
            canvas.pack(side='top')
        except:
            print('fial to download tul_logo1.gif')
        
        # user information
        if failconn==1:
            self.varname=tk.StringVar()
            self.varname.set("網路連線錯誤，請確認網路環境")
            self.numberLabel= tk.Label(self.page,textvariable=self.varname, font=('Arial', 16),fg="#DC143C" ,justify = tk.RIGHT )
            self.numberLabel.place(x=50, y= 100) 
            
       
        
        self.varname=tk.StringVar()
        self.varname.set("員工編號 ")
        self.numberLabel= tk.Label(self.page,textvariable=self.varname, font=('Arial', 12),justify = tk.RIGHT )
        self.numberLabel.place(x=50, y= 150)       
                
        self.varpwd=tk.StringVar()
        self.varpwd.set("密碼 ")
        self.pwdLabel= tk.Label(self.page,textvariable=self.varpwd, font=('Arial', 12),justify = tk.RIGHT )
        self.pwdLabel.place(x=50, y= 190) 
        
        
        self.varpwdtitle=tk.StringVar()
        self.varpwdtitle.set("預設密碼為員工西元出生年月日，ex.19800101")
        self.pwdtitleLabel= tk.Label(self.page,textvariable=self.varpwdtitle, font=('Arial', 10),justify = tk.RIGHT )
        self.pwdtitleLabel.place(x=160, y= 215)          
        
        
        
        
        
        
        self.var_usr_name = tk.StringVar()
        self.var_usr_pwd = tk.StringVar()
        #var_usr_name.set('請輸入中文姓名')
        #self.var_usr_pwd.set('預設密碼為身份證字號，英文字大寫')
        self.entry_usr_name = tk.Entry(self.page, textvariable=self.var_usr_name)
        self.entry_usr_name.place(x=160, y=150)
        self.entry_usr_pwd = tk.Entry(self.page, textvariable=self.var_usr_pwd, show='*')
        self.entry_usr_pwd.place(x=160, y=190)
        
   
        
        # login and sign up button
        self.btn_login = tk.Button(self.page, text='登入',font=('Arial', 12) , command=self.conform)
        self.btn_login.place(x=180, y=240)
        #self.btn_sign_up = tk.Button(self.page, text='輸入工號直接登入',font=('Arial', 12), command=self.conform1 )
        #self.btn_sign_up.place(x=270, y=240)




        root.mainloop() 
        
    def resetpwd(self):
        #np = new_pwd.get()
        #npf = new_pwd_confirm.get()
        #nn = new_name.get()
        #with open('usrs_info.pickle', 'rb') as usr_file:
            #exist_usr_info = pickle.load(usr_file)
        #if np != npf:
            #tk.messagebox.showerror('Error', 'Password and confirm password must be the same!')
        #elif nn in exist_usr_info:
            #tk.messagebox.showerror('Error', 'The user has already signed up!')
        #else:
            #exist_usr_info[nn] = np
            #with open('usrs_info.pickle', 'wb') as usr_file:
                #pickle.dump(exist_usr_info, usr_file)
            #tk.messagebox.showinfo('Welcome', 'You have successfully signed up!')
            #window_sign_up.destroy()
            
        window_sign_up = tk.Toplevel(self.root)
        window_sign_up.geometry('350x200')
        window_sign_up.title('重新設定密碼')
    
        new_name = tk.StringVar()
        new_name.set('請輸入六位數字工號')
        newLABEL=tk.Label(window_sign_up, text='工號: ',font=('Arial', 12) )
        newLABEL.place(x=10, y= 10)
        
        entry_new_name = tk.Entry(window_sign_up, textvariable=new_name,font=('Arial', 12))
        entry_new_name.place(x=150, y=10)
    
        old_pwd = tk.StringVar()
        pwdLabel=tk.Label(window_sign_up, text='舊密碼: ',font=('Arial', 12))
        pwdLabel.place(x=10, y=50)
        entry_old_pwd = tk.Entry(window_sign_up, textvariable=old_pwd, show='*',font=('Arial', 12))
        entry_old_pwd.place(x=150, y=50)    
    
    
    
        new_pwd = tk.StringVar()
        pwdLabel=tk.Label(window_sign_up, text='新密碼: ',font=('Arial', 12))
        pwdLabel.place(x=10, y=90)
        entry_usr_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*',font=('Arial', 12))
        entry_usr_pwd.place(x=150, y=90)
        
    
        new_pwd_confirm = tk.StringVar()
        confirmLabel=tk.Label(window_sign_up, text='新密碼確認: ',font=('Arial', 12))
        confirmLabel.place(x=10, y= 130)
        entry_usr_pwd_confirm = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*',font=('Arial', 12))
        entry_usr_pwd_confirm.place(x=150, y=130)
    
    
        btn_comfirm_sign_up = tk.Button(window_sign_up, text='確定', command=hello)
        btn_comfirm_sign_up.place(x=150, y=160)        
        
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
        #print('pwdID[inputnumber]',pwdID[inputnumber])
        #,pwdID,nameID
        
        try: 
            if inputnumber.isdigit() and len(inputnumber)==6 :
                print(inputnumber)
                print('pwdID[inputnumber]',pwdID[inputnumber])
                if pwdID[inputnumber] == inputpwd :
                
                    self.secpage(inputnumber)
                else:
                    self.no_file_worning1()
            else:
                self.no_file_worning()
        except:
            self.no_file_worning2()
            
    def no_file_worning(self):
        tk.messagebox.showwarning( title='錯誤', message='請正確輸入六位數字員工編號')
    def no_file_worning1(self):
        tk.messagebox.showwarning( title='錯誤', message='密碼不符，請重新輸入')
    def no_file_worning2(self):
        tk.messagebox.showwarning( title='錯誤', message='資料庫無此工號')        
        
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
        root.geometry('700x750')

        self.page = tk.Frame(self.root)
        self.page.grid() 
        self.dp=dp
        print('selfdp',self.dp)
        self.Button = tk.Button(self.page, text=u'回登入頁',font=('Arial', 12),justify = tk.LEFT,command=self.mainpage) 
        self.Button.grid(column=0,row=0, sticky=tk.W) 
        
        self.Button = tk.Button(self.page, text=u'出缺勤查詢',font=('Arial', 12),justify = tk.LEFT,command=partial(self.personpage1,self.dp) ) 
        self.Button.grid(columnspan=2,row=0, sticky=tk.N+tk.S)       
        
        self.Button = tk.Button(self.page, text=u'關於版本',font=('Arial', 12),justify = tk.LEFT,command=self.readme ) 
        self.Button.grid(column=1,row=0, sticky=tk.W)          
        
        ##空白行
        #self.spaceLabel1= tk.Label(self.page,textvariable="      撼訊科技 遠端出勤打卡系統       " )
        #self.spaceLabel1.grid(column=0, row=1, sticky=tk.W)
        
        self.varpwdtitle=tk.StringVar()
        self.varpwdtitle.set("            ")
        self.pwdtitleLabel= tk.Label(self.page,textvariable=self.varpwdtitle, font=('Arial', 10),justify = tk.RIGHT )
        self.pwdtitleLabel.grid(column=0, row=1, sticky=tk.W)       
        
        self.vartitle=tk.StringVar()
        self.vartitle.set("撼訊科技 公出電子表單" )
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
        self.vartitle2.set('  請輸入以下資訊，並按確定')
        self.title2Label= tk.Label(self.page,textvariable=self.vartitle2, font=('Arial', 12),justify = tk.RIGHT )
        self.title2Label.grid(column=0,   row=5, sticky=tk.W)    
        
        #self.mode='A'
        self.var1 = tk.StringVar()
        self.var1.set("C")
        #self.var1.grid(column=1, row=3,sticky=tk.W)
        
        #self.mode=""
   
        
        #self.selectcircle1=tk.Radiobutton(self.page,text = '  上班', variable=self.var1, value='A',command=partial(self.dtest,'Work')  , font=('Arial', 12) )
        #self.selectcircle1.grid(column=0, row=6, pady=1, sticky=tk.W)      
        
        #self.selectcircle2=tk.Radiobutton(self.page,text = '  下班',variable=self.var1,value='B',command=partial(self.dtest,'OffWork')  , font=('Arial', 12) )
        #self.selectcircle2.grid(column=0, row=6, pady=2, sticky=tk.N+tk.S)       
        
        #空白
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=7, sticky=tk.W)                  
        
        
        self.sv = ttk.Separator(self.page, orient=tk.HORIZONTAL)
        self.sv.grid(row=8,columnspan=8,sticky="ew")        
        
        
        
        self.selectcircle3=tk.Radiobutton(self.page,text = '  公出',variable=self.var1,value='C',command=partial(self.dtest,'OutsideWork')  , font=('Arial', 12) )
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
        #monthlist=['01月','02月','03月','04月','05月','06月','07月','08月','09月','10月','11月','12月']
        #設定只鎖定當月
        monthlist=[newmonth+'月']
        self.comboMonth = ttk.Combobox(self.page, width=7 ,values=monthlist, font=('Arial', 12),state="readonly") 
        print(dict(self.comboMonth)) 
        self.comboMonth.grid(columnspan=2,column=0, row=14,sticky=tk.N+tk.S)
        self.comboMonth.current(0)
        print(self.comboMonth.current(), self.comboMonth.get())
        
        
        #選擇月份bar
        daylistdefault=['01日','02日','03日','04日','05日','06日','07日','08日','09日','10日','11日','12日','13日','14日','15日','16日','17日','18日','19日','20日',
                 '21日','22日','23日','24日','25日','26日','27日','28日','29日','30日','31日']
        daylist=[]
        numserial=0
        #newday='31'
        #設定鎖定只能往回推10天
        if int(newday)>13 and int(newday)!=31 : #為方便使用者可以填寫明日的日期多增加可以預填明日的日期
            for numnum in range(14): 
                print('numnum',numnum)
                print('daylistdefault[int(newday)-1]',daylistdefault[int(newday)-numserial])
                daylist.append(daylistdefault[int(newday)-numserial])
                print('daylist',daylist)
                numserial=numserial+1
        elif int(newday)==31 : #為日期為31號則需要減一
            for numnum in range(14): 
                print('numnum',numnum)
                print('daylistdefault[int(newday)]',daylistdefault[int(newday)-1-numserial])
                daylist.append(daylistdefault[int(newday)-1-numserial])
                print('daylist',daylist)
                numserial=numserial+1   
                
        elif int(newday)==1 : #為日期為31號則需要減一
            print('daylistdefault[int(newday)]',daylistdefault[int(newday)])
            daylist.append(daylistdefault[int(newday)-1])
            print('daylist',daylist)
    
        else:
            for numnum in range(int(newday)+1): 
                print('numnum',numnum)
                print('daylistdefault[int(newday)-1]',daylistdefault[int(newday)-numserial])
                daylist.append(daylistdefault[int(newday)-numserial])
                print('daylist',daylist)
                numserial=numserial+1            
            
                
        self.comboDay = ttk.Combobox(self.page, width=7 ,values=daylist, font=('Arial', 12),state="readonly") 
        print(dict(self.comboDay)) 
        self.comboDay.grid(columnspan=2,column=1, row=14,sticky=tk.N+tk.S)
        if int(newday)==31: #31必須調整回來
            self.comboDay.current(0)
        elif int(newday)==1: 
            self.comboDay.current(0)
        else:#為方便使用者可以填寫明日的日期多增加可以預填明日的日期 但預設虛調整回當日日期
            self.comboDay.current(1)
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
        
        #分隔線
        self.sv = ttk.Separator(self.page, orient=tk.HORIZONTAL)
        self.sv.grid(row=18,columnspan=8,sticky="ew")         

        #反應
        self.varreback=tk.StringVar()
        self.varrebackLabel= tk.Label(self.page,textvariable=self.varreback, font=('Arial', 12),fg="#DC143C" ,justify = tk.RIGHT )
        self.varrebackLabel.grid(columnspan=9,column=0, row=19, pady=1, sticky=tk.W)  



        #反應
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=20, sticky=tk.W) 
        
        
        
        
        self.Button = tk.Button(self.page, text=u'確定',font=('Arial', 12),justify = tk.LEFT,command=partial(self.takerun)  ) 
        self.Button.grid(column=0,row=21, sticky=tk.N+tk.S)   
        
        self.Button = tk.Button(self.page, text=u'清除',font=('Arial', 12),justify = tk.LEFT,command=partial(self.secpage,self.dp)  ) 
        self.Button.grid(column=1,row=21, sticky=tk.W)          
        #反應
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=22, sticky=tk.W)         
        self.vartitle3=tk.StringVar()
        self.vartitle3.set('(1)公出日期填寫僅當月補填完畢，不得補登前一個月')
        self.title3Label= tk.Label(self.page,textvariable=self.vartitle3, font=('Arial', 12),fg='#228B22',justify = tk.RIGHT )
        self.title3Label.grid(column=0,   row=23, sticky=tk.W) 
        self.vartitle3=tk.StringVar()
        self.vartitle3.set('(2)補登期限為兩週時間')
        self.title3Label= tk.Label(self.page,textvariable=self.vartitle3, font=('Arial', 12),fg='#228B22',justify = tk.RIGHT )
        self.title3Label.grid(column=0,   row=24, sticky=tk.W)   
        
        
        self.vartitle5=tk.StringVar()
        self.vartitle5.set('(3)請確實填寫外出紀錄，以免影響薪資核發之權益')
        self.title5Label= tk.Label(self.page,textvariable=self.vartitle5, font=('Arial', 12),fg='#228B22',justify = tk.RIGHT )
        self.title5Label.grid(column=0,   row=25, sticky=tk.W)              
          
        
        
        self.upgrade()
        root.mainloop()   
        
    def readme(self):
        window_sign_up = tk.Toplevel(root)
        window_sign_up.geometry('350x200')
        window_sign_up.title('關於')
        
        pwdLabel=tk.Label(window_sign_up, text='撼訊科技 出缺勤管理系統 個人版本' ,font=('Arial', 12))
        pwdLabel.place(x=10, y=20)  
        
        pwdLabel=tk.Label(window_sign_up, text='軟體版本： %s'%(VERSON) ,font=('Arial', 12))
        pwdLabel.place(x=10, y=50)
        
        pwdLabel=tk.Label(window_sign_up, text='開發單位： 軟體研發中心' ,font=('Arial', 12))
        pwdLabel.place(x=10, y=80)        
        
        btn_comfirm_sign_up = tk.Button(window_sign_up, text='檢查更新', command=self.upgrade1)
        btn_comfirm_sign_up.place(x=50, y=120)            
        
    def upgrade1(self):
        #去確認remote所有目錄
        pathqq='home/AccessFace/user_version/'
        timedelta
        idperson=[]
        #time.sleep(2)
        personftpqq=downftp.nlst(pathqq)
        print('personftpqq',personftpqq)   
        for personfty in personftpqq:
            personww=personfty.split('/')
            person11=personww[-1].split('.')
            person13=person11[0].split('_')
            idperson.append(person13[-1])
        print('before verson: ',idperson)   
        verson123 = sorted(idperson,reverse = True)
        print('after verson: ',verson123) 
        try:
            if int(verson123[0])> int(VERSON):
            
                #if len(glob.glob('TUL-AttendanceMangement_user_'+VERSON+'.exe') )==1:
                    #os.remove('TUL-AttendanceMangement_user_'+VERSON+'.exe')
                for personfty in personftpqq:
                    personww=personfty.split('/')
                    person11=personww[-1].split('.')
                    person13=person11[0].split('_')
                    if person13[-1]==   verson123[0]:
                        #try:
                        f=open(personww[-1], 'wb')
                        downftp.retrbinary('RETR ' + personfty , f.write )
                        print('download file   '+personww[-1])                    
                        f.close()
                        self.no_file_worning17(str(verson123[0]))
                        #except:
                            #print('download faile '+personww[-1])
    
            else:
                self.no_file_worning18()                       
        except:
            print('error: ftp沒有任何更新檔案的版本 造成系統錯誤')    
            self.no_file_worning18()  
        
    def upgrade(self):
        #去確認remote所有目錄
        pathqq='home/AccessFace/user_version/'
        timedelta
        idperson=[]
        #time.sleep(2)
        personftpqq=downftp.nlst(pathqq)
        print('personftpqq',personftpqq)   
        for personfty in personftpqq:
            personww=personfty.split('/')
            person11=personww[-1].split('.')
            person13=person11[0].split('_')
            idperson.append(person13[-1])
        print('before verson: ',idperson)   
        verson123 = sorted(idperson,reverse = True)
        print('after verson: ',verson123) 
        try:
            if int(verson123[0])> int(VERSON):
            
                #if len(glob.glob('TUL-AttendanceMangement_user_'+VERSON+'.exe') )==1:
                    #os.remove('TUL-AttendanceMangement_user_'+VERSON+'.exe')
                for personfty in personftpqq:
                    personww=personfty.split('/')
                    person11=personww[-1].split('.')
                    person13=person11[0].split('_')
                    if person13[-1]==   verson123[0]:
                        #try:
                        f=open(personww[-1], 'wb')
                        downftp.retrbinary('RETR ' + personfty , f.write )
                        print('download file   '+personww[-1])                    
                        f.close()
                        self.no_file_worning17(str(verson123[0]))
                        #except:
                            #print('download faile '+personww[-1])
                 
    

        except:
            print('error: ftp沒有任何更新檔案的版本 造成系統錯誤')
        
        
    def dtest(self, mode):
        self.mode=mode
        print('self.mode',self.mode)
        
    def no_file_worning11(self):
        tk.messagebox.showwarning( title='錯誤', message='請正確輸入六位數字員工編號')
    def no_file_worning12(self):
        tk.messagebox.showwarning( title='錯誤', message='該員工尚未建檔，請重新確認')
    def no_file_worning13(self):
        tk.messagebox.showwarning( title='錯誤', message='事由及地點請勿空白，時間請正確填寫')

    def no_file_worning14(self):
        tk.messagebox.showwarning( title='錯誤', message='時間請按照範例hh:mm填寫正確')
    def no_file_worning15(self):
        tk.messagebox.showwarning( title='錯誤', message='小時不可以超過06-23')  
    def no_file_worning16(self):
        tk.messagebox.showwarning( title='錯誤', message='分鐘不可以超過00-59')    
    def no_file_worning17(self,verson):
        tk.messagebox.showwarning( title='程式更新', message='有新版本VER_%s已下載至本機，下次開啟請選擇新版本，並刪除舊版本'%(verson))     
    def no_file_worning18(self):
        tk.messagebox.showwarning( title='說明', message='目前已是最新版本')            
        
    def takerun(self):
        #print('mode',mode)
        if not os.path.isdir('data/'):
            os.mkdir('data/')    
        else :
            print ('data  file exist')     
            
            
        

        
        
        #去確認remote所有目錄
        pathqq='home/AccessFace/remote/'
        idperson=[]
        personftpqq=downftp.nlst(pathqq)   
        for personfty in personftpqq:
            personww=personfty.split('/')
            idperson.append(personww[-1])
        print('idperson',idperson)
        
        #沒有則建資料夾
        if self.dp not in idperson:
            print(self.dp+'沒有在ftp建立資料夾')
            downftp.mkd(pathqq+self.dp)
            print('home/AccessFace/remote/'+self.dp+': 成功建立資料夾')        
        
        
        else:
            path88='data/'
            values12=self.dp+'-'+newyear+newmonth
            personfileget=downftp.nlst(pathqq+self.dp+'/')
            print('len(personfileget)',len(personfileget))
            if len(personfileget) > 0:
                for pathperson in personfileget:
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
        
        """修改為遠端上下班不使用
        #try: 
            #print('self.mode',self.mode)
            #if self.mode=="OffWork" :
           
                #path88='data/'
                #values12=self.dp+'-'+newyear+newmonth
                #finalid=[]
                
                #finalid.append(self.mode+','+ self.dp  +','+ persenID[self.dp] +','+ pdID[self.dp] +','+ newdate +','+newdtime+',None,None' )
                
                #print('finalid',finalid)
                
                ##np.savetxt(path_database+'database_Employee.csv', finalid,fmt='%s', delimiter=',')
                #with open(path88+values12+'-personal.csv','a') as f: 
                    #np.savetxt(f, finalid,fmt='%s', delimiter=',')
                #f.close      
                
                
                #try:
                    ##d=ftp.cwd('home/AccessFace/')
                    #downftp.storbinary('STOR '+'home/AccessFace/remote/'+self.dp+'/'+values12+'-personal.csv' , open(path88+values12+'-personal.csv', 'rb')) # 上傳FTP檔案
                    #print("succes upload: " +'home/AccessFace/remote/'+self.dp+'/'+values12+'-personal.csv')
                #except:
                    #print("upload failed: " +'home/AccessFace/remote/'+self.dp+'/'+values12+'-personal.csv')
                    #print("upload failed. check.................        ......")                
                
                
                #self.varreback.set("                            ")        
                #self.varreback.set("Update: " +  persenID[self.dp] + ' 新增下班紀錄 '+ newdate+ ' '+ newdtime)
                #os.remove(path88+values12+'-personal.csv')
                
            elif self.mode=="OutsideWork" :
          """      
        self.mode="OutsideWork"
        #如果事由及地點沒填則不會繼續接下來動作
        person1=self.varBusinessPerson1.get()
        person2=self.varBusinessPerson2.get()
        person3=self.varBusinessPerson3.get()
        person4=self.varBusinessPerson4.get()   
        failBusinessWhy=0
        failBusinessPerson=0
        failBusinesstTime=0
        fail=0
        if self.varBusinessWhy.get()=="" or self.varBusinessLocation.get()==""  :
            self.no_file_worning13()
            failBusinessWhy=1
            
            
        if self.varBusinessOutTime.get()[0:2]=="00"   or  self.varBusinessOutTime.get()[:2].isdigit()!=True  or  self.varBusinessOutTime.get()[3:].isdigit()!=True or  len(self.varBusinessOutTime.get()[3:])!=2 or  len(self.varBusinessOutTime.get()[:2])!=2  :
            print('self.varBusinessOutTime.get()[0:2]',self.varBusinessOutTime.get()[:2])
            print('self.varBusinessOutTime.get()[0:2].isdigit()',self.varBusinessOutTime.get()[3:].isdigit() )
            print('self.varBusinessOutTime.get()[0:2]',self.varBusinessOutTime.get()[:2])
            print('self.varBusinessOutTime.get()[0:2].isdigit()',self.varBusinessOutTime.get()[3:].isdigit() )            
            failBusinesstTime=1
            self.no_file_worning14()
            
            
        if int(self.varBusinessOutTime.get()[:2]) not in range(6,24) :
            print('self.varBusinessOutTime.get()[:2]',self.varBusinessOutTime.get()[:2],'is not range in 06~23 hours')
            failBusinesstTime=1
            self.no_file_worning15()     
            
        if int(self.varBusinessOutTime.get()[3:]) not in range(0,60) :
            print('self.varBusinessOutTime.get()[3:]',self.varBusinessOutTime.get()[3:],'is not range in 01~59 hours')
            failBusinesstTime=1
            self.no_file_worning16()                   
            
            
        if person1!="同事1"  or person2!="同事2"  or person3!="同事3"  or person4!="同事4" :
            print('有除了同事1-4以外的資訊')
            if person1.isdigit() and len(person1)==6 or person1=="同事1" :
                print ('person1 is ok')
            else:
                fail=fail+1
                failBusinessPerson=1
            if person2.isdigit() and len(person2)==6 or person2=="同事2" :
                print ('person2 is ok')
            else:
                fail=fail+1           
                failBusinessPerson=1
            if person3.isdigit() and len(person3)==6 or person3=="同事3" :
                print ('person3 is ok') 
            else:
                fail=fail+1   
                failBusinessPerson=1
            if person4.isdigit() and len(person4)==6 or person4=="同事4":
                print ('person4 is ok')  
            else:
                fail=fail+1
                failBusinessPerson=1
            if fail!=0:
                self.no_file_worning11()    
        
        
        #事由及地點非空白 繼續動作
        if failBusinessPerson==0 and failBusinessWhy==0 and failBusinesstTime==0:
            
            addperson=[]
            addperson.append(self.dp)
            
            if len(person1)==6 and person1.isdigit() :
                
                print ('person1 add ok')
                addperson.append(person1)

            if len(person2)==6 and person2.isdigit() :
                
                print ('person2 add ok')
                addperson.append(person2)   
                
            if len(person3)==6 and person3.isdigit() :
                
                print ('person3 add ok')
                addperson.append(person3)

            if len(person4)==6 and person4.isdigit() :
                
                print ('person4 add ok')
                addperson.append(person4)   
                
            ##判斷輸入的隨行同事是否為無效值    
            #fail=0
            #if person1!="同事1"  or person2!="同事2"  or person3!="同事3"  or person4!="同事4" :
                #print('有除了同事1-4以外的資訊')
                #if person1.isdigit() and len(person1)==6 or person1=="同事1" :
                    #print ('person1 is ok')
                #else:
                    #fail=fail+1
                #if person2.isdigit() and len(person2)==6 or person2=="同事2" :
                    #print ('person2 is ok')
                #else:
                    #fail=fail+1                    
                #if person3.isdigit() and len(person3)==6 or person3=="同事3" :
                    #print ('person3 is ok') 
                #else:
                    #fail=fail+1                    
                #if person4.isdigit() and len(person4)==6 or person4=="同事4":
                    #print ('person4 is ok')  
                #else:
                    #fail=fail+1
                    
                    
            #if fail!=0:
                #self.no_file_worning11()
                    
               
            #去確認remote所有目錄
            pathqq='home/AccessFace/remote/'
            idperson=[]
            personftpqq=downftp.nlst(pathqq)   
            for personfty in personftpqq:
                personww=personfty.split('/')
                idperson.append(personww[-1])
            print('idperson',idperson)
            
            print('addperson',addperson)
            ghostpersonefail=0
            
            for oneperson in addperson: 
                if oneperson not in persenID:
                    print(oneperson+'該同仁沒建檔')
                    ghostpersonefail=1
                    self.no_file_worning12()
                    
            if ghostpersonefail==0:
                for oneperson in addperson:
                    DOWNLOAD_bug_flag=0
                    finalid=[]
                    finalid.append(self.mode+','+ oneperson  +','+ persenID[oneperson] +','+ pdID[oneperson] +','+newyear+'-'+ self.comboMonth.get()[0:2] +'-'+ 
                                   self.comboDay.get()[0:2]+','+ self.varBusinessOutTime.get()+':00'+','+ self.varBusinessWhy.get()+','+ self.varBusinessLocation.get() )
                             #comboDay +','+ self.varBusinessOutTime.get+','+ self.varBusinessWhy.get+','+ self.varBusinessLocation.get)
                    
                    print('finalid',finalid)
                    
                    
                    pathqq='home/AccessFace/remote/'
                    personftpqq=downftp.nlst(pathqq)
                        
                    print('personftpqq',personftpqq)     
                    path88='data/'
                    values123=oneperson+'-'+newyear+ self.comboMonth.get()[0:2]
                    
                    #判斷有沒有該工號資料夾 沒有的話就新建一個
                    if oneperson  not in   idperson :
                        print(oneperson+'沒有在ftp建立資料夾')
                        downftp.mkd(pathqq+oneperson)
                        print('home/AccessFace/remote/'+oneperson+': 成功建立資料夾')
                        
                        
                
                        #上傳檔案
                        finalid.append(self.mode+','+ oneperson  +','+ persenID[oneperson] +','+ pdID[oneperson] +','+newyear+'-'+ self.comboMonth.get()[0:2] +'-'+ 
                               self.comboDay.get()[0:2]+','+ self.varBusinessOutTime.get()+':00'+','+ self.varBusinessWhy.get()+','+ self.varBusinessLocation.get() )
                        with open(path88+values123 +'-personal.csv','a',encoding = 'utf-8') as f: 
                            np.savetxt(f, finalid,fmt='%s', delimiter=',',encoding = 'utf-8')
                        f.close
                            
                        
                        try:
                            #d=ftp.cwd('home/AccessFace/')
                            downftp.storbinary('STOR '+'home/AccessFace/remote/'+oneperson+'/'+values123+'-personal.csv' , open(path88+values123+'-personal.csv', 'rb')) # 上傳FTP檔案
                            print("succes upload: " +'home/AccessFace/remote/'+oneperson+'/'+values123+'-personal.csv')
                        except:
                            print("upload failed: " +'home/AccessFace/remote/'+oneperson+'/'+values123+'-personal.csv')
                            print("upload failed. check...................")    
                    
                    #其餘如果該員工在ftp有見過資料夾則上去確認是否有已存的檔案，下載修改後在上傳
                    else:
                        
                        #ftp找尋目錄是否有該資料夾的檔案
                        path='home/AccessFace/remote/'+oneperson+'/'
                        personftp=downftp.nlst(path)
                            
                        print('personftp',personftp)     
                        path88='data/'
                        values123=oneperson+'-'+newyear+ self.comboMonth.get()[0:2]
                        for pathperson in personftp:
                            personfile=pathperson.split('/')
                            personmonth=personfile[-1]
                            print('personmonth',personmonth)
                            personmonth1=personmonth.split('.')
                            pmonth=personmonth1[0].split('-')
                            if pmonth[1]==newyear+self.comboMonth.get()[0:2] :
                                print('pathperson yes',pathperson)
                                
                                f=open(path88+values123+'-personal.csv', 'wb')
                                downftp.retrbinary('RETR ' + pathperson, f.write )
                                print('download file'+path88+values123+'-personal.csv')                    
                                f.close()
                                DOWNLOAD_bug_flag=1 #因為如果有檔案表示有紀錄 可以不用啟動bug修復
                        
                        #上傳檔案
                        if DOWNLOAD_bug_flag==0: #啟動bug修復 自動新增一行以符合2維陣列
                            finalid.append(self.mode+','+ oneperson  +','+ persenID[oneperson] +','+ pdID[oneperson] +','+newyear+'-'+ self.comboMonth.get()[0:2] +'-'+ 
                                   self.comboDay.get()[0:2]+','+ self.varBusinessOutTime.get()+':00'+','+ self.varBusinessWhy.get()+','+ self.varBusinessLocation.get() )                            
                            with open(path88+values123+'-personal.csv','a',encoding = 'utf-8') as f: 
                                np.savetxt(f, finalid,fmt='%s', delimiter=',',encoding = 'utf-8')
                            f.close
                            
                        else:
                            with open(path88+values123+'-personal.csv','a',encoding = 'utf-8') as f: 
                                np.savetxt(f, finalid,fmt='%s', delimiter=',',encoding = 'utf-8')
                            f.close                            
                        
                        try:
                            #d=ftp.cwd('home/AccessFace/')
                            downftp.storbinary('STOR '+'home/AccessFace/remote/'+oneperson+'/'+values123+'-personal.csv' , open(path88+values123+'-personal.csv', 'rb')) # 上傳FTP檔案
                            print("succes upload: " +'home/AccessFace/remote/'+oneperson+'/'+values123+'-personal.csv')
                        except:
                            print("upload failed: " +'home/AccessFace/remote/'+oneperson+'/'+values123+'-personal.csv')
                            print("upload failed. check...............")
                            
                    os.remove(path88+values123+'-personal.csv')    
                #list = ['a', 'b', 'c', 'd']
                
                #print(str)     
                #https://blog.csdn.net/FrankieHello/article/details/80766439
                
            arraddperson = np.array(addperson)
            strarraddperson = ' '.join(arraddperson)    
            self.varreback.set("                            ")        
            self.varreback.set("Update: 工號 " +  strarraddperson + ' 新增公出紀錄 '+ newyear+'-'+ self.comboMonth.get()[0:2] +'-'+ 
                       self.comboDay.get()[0:2]+' '+ self.varBusinessOutTime.get()+':00'  )                                
     
                
                        
            """修改遠端上下班不使用  
            elif self.mode=="Work" :
           
                path88='data/'
                values12=self.dp+'-'+newyear+newmonth
                finalid=[]
                
                finalid.append(self.mode+','+ self.dp  +','+ persenID[self.dp] +','+ pdID[self.dp] +','+ newdate +','+newdtime+',None,None' )
                
                print('finalid',finalid)
                
                #np.savetxt(path_database+'database_Employee.csv', finalid,fmt='%s', delimiter=',')
                with open(path88+values12+'-personal.csv','a') as f: 
                    np.savetxt(f, finalid,fmt='%s', delimiter=',')
                f.close      
                
                
                try:
                    #d=ftp.cwd('home/AccessFace/')
                    downftp.storbinary('STOR '+'home/AccessFace/remote/'+self.dp+'/'+values12+'-personal.csv' , open(path88+values12+'-personal.csv', 'rb')) # 上傳FTP檔案
                    print("succes upload: " +'home/AccessFace/remote/'+self.dp+'/'+values12+'-personal.csv')
                except:
                    print("upload failed: " +'home/AccessFace/remote/'+self.dp+'/'+values12+'-personal.csv')
                    print("upload failed. check.................        ......")                  
                    
                self.varreback.set("                            ")        
                self.varreback.set("Update: " +  persenID[self.dp] + ' 新增上班紀錄 '+ newdate+ ' '+ newdtime)
                os.remove(path88+values12+'-personal.csv')
            
        except:
            self.mode='Work'
            print('self.mode',self.mode)
            path88='data/'
            values12=self.dp+'-'+newyear+newmonth            
            finalid=[]
            
            finalid.append(self.mode+','+ self.dp  +','+ persenID[self.dp] +','+ pdID[self.dp] +','+ newdate +','+newdtime+',None,None' )
            
            print('finalid',finalid)
            
            #np.savetxt(path_database+'database_Employee.csv', finalid,fmt='%s', delimiter=',')
            with open(path88+values12+'-personal.csv','a') as f: 
                np.savetxt(f, finalid,fmt='%s', delimiter=',')
            f.close
            
            try:
                #d=ftp.cwd('home/AccessFace/')
                downftp.storbinary('STOR '+'home/AccessFace/remote/'+self.dp+'/'+values12+'-personal.csv' , open(path88+values12+'-personal.csv', 'rb')) # 上傳FTP檔案
                print("succes upload: " +'home/AccessFace/remote/'+self.dp+'/'+values12+'-personal.csv')
            except:
                print("upload failed: " +'home/AccessFace/remote/'+self.dp+'/'+values12+'-personal.csv')
                print("upload failed. check.......................")
                
                
            self.varreback.set("                            ")        
            self.varreback.set("Update: " +  persenID[self.dp] + ' 新增上班紀錄 '+ newdate+ ' '+ newdtime)            
            os.remove(path88+values12+'-personal.csv')
            """
    def mainpage(self):
        self.page.destroy()
        mainpage(self.root)
        
    def personpage1(self,personq ):
        
        print('personq',personq)
        self.page.destroy()
        personpage(self.root,personq)
        
        
    def secpage(self,personq ):
        
        print('personq',personq)
        self.page.destroy()
        secondpage(self.root,personq)        

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
        
  
        
        #====
        value_mmdd=[]
        for valuesset in values1:
            
            valuesset123=valuesset.split("/")
            
            if int(valuesset123[1])<10 and int(valuesset123[1])>=1:
                month='0'+str(valuesset123[1])
                print (month)
            else :
                month=str(valuesset123[1])
                print (month)     
            value_mmdd.append(valuesset123[0]+month)
                
        print('value_mmdd',value_mmdd)
        allyesrmonthID=secretname(value_mmdd)
        
        #下載資料
        self.callbackallthing(values1)
        #print('self.onlyRemote1',self.onlyRemote1)        
        
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
        self.addButton = tk.Button(self.page, text = '查詢',command=partial(self.month_callbackFunc,personq,allyesrmonthID), font=('Arial', 12) )
        self.addButton.grid(column=0, row=3, pady=1, sticky=tk.E)        
        
        
        
        
        #選擇月份事件按鈕
        self.addButton = tk.Button(self.page, text = '重新整理',command=partial(self.callbackallthingFlesh,values1), font=('Arial', 12) )
        self.addButton.grid(column=1, row=3, pady=1, sticky=tk.E)   
        
        self.var1 = tk.StringVar()
        self.var1.set("A")
        
        #circleLabel= tk.Label(self.page,textvariable=self.var1, font=('Arial', 12),justify = tk.LEFT )
        #circleLabel.grid(column=1, row=3, sticky=tk.W)   
        #self.var1.grid(column=0, row=4,sticky=tk.N+tk.S)
        self.selectcircle=tk.Radiobutton(self.page,text = '合併檢視', variable=self.var1, value='A',command=partial(self.month_callbackFunc,personq,allyesrmonthID)   , font=('Arial', 12) )
        self.selectcircle.grid(column=0, row=4, pady=0, sticky=tk.W)      
        
        self.selectcircle=tk.Radiobutton(self.page,text = '檢視晶片卡',variable=self.var1,value='B',command=partial(self.show_idcard_callbackFunc,personq,allyesrmonthID)   , font=('Arial', 12) )
        self.selectcircle.grid(column=0,columnspan=2, row=4, pady=0, sticky=tk.N+tk.S)       
        
        self.selectcircle=tk.Radiobutton(self.page,text = '檢視人臉識別', variable=self.var1,value='C',command=partial(self.show_face_callbackFunc,personq,allyesrmonthID)  , font=('Arial', 12) )
        self.selectcircle.grid(column=1, row=4, pady=0, sticky=tk.W)   
        
        self.selectcircle=tk.Radiobutton(self.page,text = '公出', variable=self.var1,value='D',command=partial(self.show_remote_callbackFunc,personq,allyesrmonthID)  , font=('Arial', 12) )
        self.selectcircle.grid(column=1, row=5, pady=0, sticky=tk.W)         
        
        #空白
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=6, sticky=tk.W)          
        
        
        
        #讀取csv並且取012345 colums
        try: 
            onlyuse = np.loadtxt('data/'+allyesrmonthID[self.stryear+self.strmonth]+alltypechange['face'], dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5,0,1) )
            print('onlyuse',onlyuse)        

            
            
            #onlyuse=[]
            #onlyuse = np.array([['fail', self.personq  ,'None','None' ,self.stryear+'-'+self.strmonth+'-01',00:00:00,'無本月資料','None'],['fail', self.personq  ,'None','None' ,self.stryear+'-'+self.strmonth+'-01',00:00:00,'無本月資料','None']], dtype=np.str)
            #np.insert(onlyuse,0,'fail,'+ self.personq  +',None,None' +','+self.stryear+'-'+self.strmonth+'-01,00:00:00,無本月資料,None',axis=0)
            #np.append(onlyuse, 'fail,'+ self.personq  +',None,None' +','+self.stryear+'-'+self.strmonth+'-01,00:00:00,無本月資料,None', axis=0)
            #np.append(onlyuse, ['fail,'+ self.personq  +',None,None' +','+self.stryear+'-'+self.strmonth+'-01,00:00:00,無本月資料,None'], axis=0)
         
            print('onlyuse',onlyuse)  
        
            if len(glob.glob('data/'+allyesrmonthID[self.stryear+self.strmonth] + alltypechange['idcard'] ))>=1 :
                print(glob.glob('data/'+allyesrmonthID[self.stryear+self.strmonth] + alltypechange['idcard'] ))
                onlyidcard = np.loadtxt('data/'+allyesrmonthID[self.stryear+self.strmonth] + alltypechange['idcard'] ,dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5,0,1))
                print('onlyonlyidcard.shape,onlyonlyidcard.ndim',onlyidcard.shape[0],onlyidcard.shape[1],onlyidcard.ndim)
                print('===========onlyidcard===========',onlyidcard) 
                
                onlyuse=np.concatenate((onlyidcard,onlyuse),axis=0)    #拼接陣列     
            
            if len(glob.glob('data/'+allyesrmonthID[ self.stryear+self.strmonth]+ alltypechange['personal'] ))>=1 :
                 
                print(glob.glob('data/'+allyesrmonthID[ self.stryear+self.strmonth]+ alltypechange['personal']))
                
                
                onlyRemote = np.loadtxt('data/'+allyesrmonthID[ self.stryear+self.strmonth]+ alltypechange['personal'] ,dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5,6,7),encoding = 'utf-8')
                print('onlyRemote.shape,onlyRemote.ndim',onlyRemote.shape[0],onlyRemote.ndim)
                if onlyRemote.ndim==1:
                    ##np.reshape(onlyRemote,(2,6) , order='F') 
                    print('reshape onlyRemote',onlyRemote)
                    ##onlyRemote[None,:].shape 
                    ##arrayB = np.ones((1, onlyRemote.shape[0] ))
                    #arrayB = np.empty([1, onlyRemote.shape[0] ], dtype='string')
                    #numset=0
                    #for onevole in onlyRemote:
                    np.insert(onlyuse,-1,[onlyRemote],axis=0)
                    #np.append(onlyuse, [onlyRemote], axis=0)
                    #onlyuse=np.concatenate((onlyRemote,[[onlyuse]]),axis=0) 
                else:
                    onlyuse=np.concatenate((onlyRemote,onlyuse),axis=0)        
        
            print('FINAL onlyuse',onlyuse)
            #搜尋是"vincent"的索引值
            userid=np.argwhere(onlyuse==self.personq)     
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
            tree["columns"]=("狀態別","日期","第一筆時間","最後筆時間","事由","地點")
            tree.column("狀態別",width=80)   #表示列,不显示
            tree.column("日期",width=130)   #表示列,不显示
            tree.column("第一筆時間",width=100)
            tree.column("最後筆時間",width=100)
            tree.column("事由",width=100)
            tree.column("地點",width=100)
            tree.heading("狀態別",text="狀態別")  #显示表头
            tree.heading("日期",text="日期")  #显示表头
            tree.heading("第一筆時間",text="第一筆時間")
            tree.heading("最後筆時間",text="最後筆時間")
            tree.heading("事由",text="事由")
            tree.heading("地點",text="地點")     
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
                
                type123=onlyuse_id_a[0:1,0]
                type123offtime=onlyuse_id_a[:,0]
                name123=onlyuse_id_a[0:1,2]
                datetime=onlyuse_id_a[0:1,4]
                ontime=onlyuse_id_a[0:1,5]
                offtime=onlyuse_id_a[:,5]
                weekfial=weekreport(datetime[0])
    
                
                        
                if len(id1)==1:
                    if type123[0]=='open':
                        type123[0]='Face'
                    if type123[0]=='idcard':
                        type123[0]='Card'    
                    if type123[0]=='OutsideWork':
                        type123[0]='公出'  
                        thing123=onlyuse_id_a[0:1,6]
                        location123=onlyuse_id_a[0:1,7]                    
                        tree.insert("",line123,text=name123[0] ,values=(type123[0],datetime[0]+'('+weekfial+')' ,ontime[0],"  ",thing123[0],location123[0]))
                    else:
                        tree.insert("",line123,text=name123[0] ,values=(type123[0],datetime[0]+'('+weekfial+')' ,ontime[0],"  "," "," "))
                        
            
                else :
                    if type123[0]=='open':
                        type123[0]='Face'   
                    if type123[0]=='idcard':
                        type123[0]='Card'    
                        
                    if type123[0]=='idcard':
                        type123[0]='Card'   
                        
                    
                    if type123[0]=='OutsideWork' or type123offtime[1]=='OutsideWork':
                        if type123[0]=='OutsideWork':
                            thing123=onlyuse_id_a[0:1,6]
                            mainthing=thing123[0]
                            location123=onlyuse_id_a[0:1,7]
                            mainlocation=location123[0]
                        else :
                            thing123=onlyuse_id_a[:,6]
                            mainthing=thing123[1]
                            location123=onlyuse_id_a[:,7]
                            mainlocation=location123[1]
                        
    #                     type123offtime[1]=='OutsideWork'
                        type123[0]='公出'  
    #                     thing123=onlyuse_id_a[0:1,6]
    #                     location123=onlyuse_id_a[0:1,7]  
                        tree.insert("",line123,text=name123[0] ,values=(type123[0],datetime[0]+'('+weekfial+')' ,ontime[0],offtime[1],mainthing,mainlocation  ) )
    
                    else:    
                        if type123[0]=='Work' or type123offtime[1]=='Work':
                            type123[0]='遠端上班'
                        if type123[0]=='OffWork' or type123offtime[1]=='OffWork':
                            type123[0]='遠端下班'
                        tree.insert("",line123,text=name123[0] ,values=(type123[0],datetime[0]+'('+weekfial+')' ,ontime[0],offtime[1]," "," "  ) )
                    
                line123=line123+1
                
    
            #vertical scrollbar------------    https://www.cnblogs.com/Tommy-Yu/p/4156014.html
            vbar = ttk.Scrollbar(self.page,orient=tk.VERTICAL,command=tree.yview)
            vbar.grid(column=10,row=7,sticky=tk.NS) 
            tree.configure(yscrollcommand=vbar.set)
            #tree.tag_configure ("monospace", font =(None，12) )
            tree.grid(columnspan=9,row=7,sticky=tk.W)    
            
            
            #空白
            spaceLabel= tk.Label(self.page,textvariable="             " )
            spaceLabel.grid(columnspan=9, row=8, sticky=tk.W)  
            
            self.vartitle3=tk.StringVar()
            self.vartitle3.set('(1)晶片卡更新時間為次月第1天上班日，每個月更新1次')
            self.title3Label= tk.Label(self.page,textvariable=self.vartitle3, font=('Arial', 12),fg='#228B22',justify = tk.RIGHT )
            self.title3Label.grid(columnspan=9,   row=9, sticky=tk.W) 
            self.vartitle3=tk.StringVar()
            self.vartitle3.set('(2)人臉識別更新時間為隔日，每天更新1次')
            self.title3Label= tk.Label(self.page,textvariable=self.vartitle3, font=('Arial', 12),fg='#228B22',justify = tk.RIGHT )
            self.title3Label.grid(columnspan=9,   row=10, sticky=tk.W)  
            self.vartitle4=tk.StringVar()
            self.vartitle4.set('(3)資料若未更新，請按重新整理更新資料')
            self.title4Label= tk.Label(self.page,textvariable=self.vartitle4, font=('Arial', 12),fg='#228B22',justify = tk.RIGHT )
            self.title4Label.grid(columnspan=9,   row=11, sticky=tk.W)  
            
            
            root.mainloop()   
    
        except:
            self.no_file_worning_fail1()
    
    def callbackallthing(self,values):
        
        values1=[]
        for valuesset in values:
            
            valuesset123=valuesset.split("/")
            
            if int(valuesset123[1])<10 and int(valuesset123[1])>=1:
                month='0'+str(valuesset123[1])
                print (month)
            else :
                month=str(valuesset123[1])
                print (month)     
            values1.append(valuesset123[0]+month)
        
        
        idperson=[]
        #去確認remote所有目錄
        pathqq='home/AccessFace/remote/'
        personftpqq=downftp.nlst(pathqq)   
        for personfty in personftpqq:
            personww=personfty.split('/')
            idperson.append(personww[-1])
        print('idperson',idperson)
        
        #該同仁沒建檔，則建檔案資料夾
        if self.personq not in idperson:
            print(self.personq+'該同仁沒建檔')
            downftp.mkd(pathqq+self.personq)
            print('home/AccessFace/remote/'+self.personq+': 成功建立資料夾')
            
            
        else:#ftp找尋目錄是否有該資料夾的檔案
            #下載remote個人的檔案
            path='home/AccessFace/remote/'+self.personq+'/'
            personftp=downftp.nlst(path)
                

            allmonthID=secretname(values1)
            
            
            
            if len(personftp)>=1: 
                print('personftp',personftp)     
                path88='data/'
                
                for yearmonthlist in values1 : 
                    print('newyear+newmonth',newyear+newmonth)
                    
                    if newyear+newmonth==yearmonthlist: #本月必下載
                        print('yearmonthlist',yearmonthlist) 
                        values123=self.personq+'-'+yearmonthlist
                        for    personftp1 in   personftp:
                            personfile=personftp1.split('/')
                            personmonth=personfile[-1]
                            print('personmonth',personmonth)
                            personmonth1=personmonth.split('.')
                            pmonth=personmonth1[0].split('-')
                            if str(pmonth[1])==yearmonthlist :
                                print('remote file 找到了',personftp1)
                                
                                f=open(path88+allmonthID[yearmonthlist]+alltypechange['personal'], 'wb')
                                downftp.retrbinary('RETR ' + personftp1, f.write )
                                print('download file: '+path88+allmonthID[yearmonthlist]+alltypechange['personal'])                    
                                f.close()   
                                #data = pd.read_csv(path88+values123+'-personal.csv')
                                #np.save(path88+values123+'-personal.csv', data)
                                #os.remove(path88+values123+'-personal.csv')                                
                                
                    elif len(glob.glob('data/'+allmonthID[yearmonthlist]+alltypechange['personal']) )>=1 and newyear+newmonth!=yearmonthlist :#非月則是本地端有沒有檔案下載
                        print('data/'+allmonthID[yearmonthlist]+alltypechange['personal'] +'已經有檔案不下載了，非本月')
                    else :
                        print('yearmonthlist',yearmonthlist) 
                        values123=self.personq+'-'+yearmonthlist
                        for    personftp1 in   personftp:
                            personfile=personftp1.split('/')
                            personmonth=personfile[-1]
                            print('personmonth',personmonth)
                            personmonth1=personmonth.split('.')
                            pmonth=personmonth1[0].split('-')
                            if str(pmonth[1])==yearmonthlist :
                                print('remote file 找到了',personftp1)
                                
                                f=open('data/'+allmonthID[yearmonthlist]+alltypechange['personal'], 'wb')
                                downftp.retrbinary('RETR ' + personftp1, f.write )
                                print('download file: '+'data/'+allmonthID[yearmonthlist]+alltypechange['personal'])                    
                                f.close()   
                                
                    
                                
                                #os.rename
                                
                                #os.remove(path88+fullfilename[-1])                                   
                        
               
            #下載month個人的檔案 
            path1='home/AccessFace/month/'
            personftp1=downftp.nlst(path1)  
            if len(personftp1)>=1: 
                print('personftp1',personftp1)     
                path88='data/'   
                
                
                for yearmonthlist in values1 : 
                    print('yearmonthlist',yearmonthlist) 
                    
        
                    for personftphot in  personftp1 :
                        fullfilename=personftphot.split('/')
                        typeset_exe=fullfilename[-1].split('.')
                        typeset=typeset_exe[0].split('-')
                        if typeset[0]==yearmonthlist:
                            print('idcard or face file找到了',personftphot)
                                
                            if len(glob.glob('data/'+allmonthID[yearmonthlist]+alltypechange[ typeset[1] ] )) >= 1 :
                                print('data/'+allmonthID[yearmonthlist]+alltypechange[ typeset[1] ]+' 已經有檔案不下載了')
                    
                            else :
                                f=open(path88+fullfilename[-1], 'wb')
                                downftp.retrbinary('RETR ' + personftphot, f.write )
                                print('download file'+path88+fullfilename[-1])                    
                                f.close() 
                                
                                #data = pd.read_csv(path88+fullfilename[-1])
                                #np.save(path88+typeset_exe[0]+'.csv', data)
                                
                                
                                #將該員資料擷取出只有該員的資料來處理，不要儲存非該員以外的資料
                                onlyuse = np.loadtxt(path88+fullfilename[-1],dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5))
                                #print(onlyuse)
                                
                                os.remove(path88+fullfilename[-1])   
                                    
                        
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
                                #第一個月
                                if typeset[1]=='face' and values1[0]==yearmonthlist:
                                    np.savetxt(path88+firstmonth+faceid, onlyuse_id,fmt='%s', delimiter=',')
                                    print('typeset[1],yearmonthlist',typeset[1],yearmonthlist)
                                    print('file name: ',path88+firstmonth+faceid)
                                    
                                elif typeset[1]=='idcard' and values1[0]==yearmonthlist:
                                    np.savetxt(path88+firstmonth+cardid, onlyuse_id,fmt='%s', delimiter=',') 
                                    print('typeset[1],yearmonthlist',typeset[1],yearmonthlist)
                                    print('file name: ',path88+firstmonth+cardid)     
                                #第二個月   
                                elif typeset[1]=='face' and values1[1]==yearmonthlist:
                                    np.savetxt(path88+secendmonth+faceid, onlyuse_id,fmt='%s', delimiter=',')
                                    print('typeset[1],yearmonthlist',typeset[1],yearmonthlist)
                                    print('file name: ',path88+secendmonth+faceid)    
                                    
                                elif typeset[1]=='idcard' and values1[1]==yearmonthlist:
                                    np.savetxt(path88+secendmonth+cardid, onlyuse_id,fmt='%s', delimiter=',')   
                                    print('typeset[1],yearmonthlist',typeset[1],yearmonthlist)
                                    print('file name: ',path88+secendmonth+cardid)       
                                #第三個月       
                                elif typeset[1]=='face' and values1[2]==yearmonthlist:
                                    np.savetxt(path88+thirdmonth+faceid, onlyuse_id,fmt='%s', delimiter=',')
                                    print('typeset[1],yearmonthlist',typeset[1],yearmonthlist)
                                    print('file name: ',path88+thirdmonth+faceid)    
                                    
                                elif typeset[1]=='idcard' and values1[2]==yearmonthlist:
                                    np.savetxt(path88+thirdmonth+cardid, onlyuse_id,fmt='%s', delimiter=',')                                   
                                    print('typeset[1],yearmonthlist',typeset[1],yearmonthlist)
                                    print('file name: ',path88+thirdmonth+cardid)                                
                                    
                                
                                
                                
    def callbackallthingFlesh(self,values):
        
        values1=[]
        for valuesset in values:
            
            valuesset123=valuesset.split("/")
            
            if int(valuesset123[1])<10 and int(valuesset123[1])>=1:
                month='0'+str(valuesset123[1])
                print (month)
            else :
                month=str(x.month)
                print (month)     
            values1.append(valuesset123[0]+month)
        
        
        idperson=[]
        #去確認remote所有目錄
        pathqq='home/AccessFace/remote/'
        personftpqq=downftp.nlst(pathqq)   
        for personfty in personftpqq:
            personww=personfty.split('/')
            idperson.append(personww[-1])
        print('idperson',idperson)
        
        #該同仁沒建檔，則建檔案資料夾
        if self.personq not in idperson:
            print(self.personq+'該同仁沒建檔')
            downftp.mkd(pathqq+self.personq)
            print('home/AccessFace/remote/'+self.personq+': 成功建立資料夾')
            
            
        else:#ftp找尋目錄是否有該資料夾的檔案
            #下載remote個人的檔案
            path='home/AccessFace/remote/'+self.personq+'/'
            personftp=downftp.nlst(path)
                

            allmonthID=secretname(values1)
            
            
            
            if len(personftp)>=1: 
                print('personftp',personftp)     
                path88='data/'
                
                for yearmonthlist in values1 : 
                    print('newyear+newmonth',newyear+newmonth)
                    print('yearmonthlist',yearmonthlist) 
                    values123=self.personq+'-'+yearmonthlist
                    for    personftp1 in   personftp:
                        personfile=personftp1.split('/')
                        personmonth=personfile[-1]
                        print('personmonth',personmonth)
                        personmonth1=personmonth.split('.')
                        pmonth=personmonth1[0].split('-')
                        if str(pmonth[1])==yearmonthlist :
                            print('remote file 找到了',personftp1)
                            
                            f=open(path88+allmonthID[yearmonthlist]+alltypechange['personal'], 'wb')
                            downftp.retrbinary('RETR ' + personftp1, f.write )
                            print('download file: '+path88+allmonthID[yearmonthlist]+alltypechange['personal'])                    
                            f.close()   
                                               
                        
               
            #下載month個人的檔案 
            path1='home/AccessFace/month/'
            personftp1=downftp.nlst(path1)  
            if len(personftp1)>=1: 
                print('personftp1',personftp1)     
                path88='data/'   
                
                
                for yearmonthlist in values1 : 
                    print('yearmonthlist',yearmonthlist) 
                    
        
                    for personftphot in  personftp1 :
                        fullfilename=personftphot.split('/')
                        typeset_exe=fullfilename[-1].split('.')
                        typeset=typeset_exe[0].split('-')
                        if typeset[0]==yearmonthlist:
                            print('idcard or face file找到了',personftphot)
                                
                            #if len(glob.glob('data/'+allmonthID[yearmonthlist]+alltypechange[ typeset[1] ] )) >= 1 :
                                #print('data/'+allmonthID[yearmonthlist]+alltypechange[ typeset[1] ]+' 已經有檔案不下載了')
                    
                            #else :
                            f=open(path88+fullfilename[-1], 'wb')
                            downftp.retrbinary('RETR ' + personftphot, f.write )
                            print('download file'+path88+fullfilename[-1])                    
                            f.close() 
                            
                            #data = pd.read_csv(path88+fullfilename[-1])
                            #np.save(path88+typeset_exe[0]+'.csv', data)
                            
                            
                            #將該員資料擷取出只有該員的資料來處理，不要儲存非該員以外的資料
                            onlyuse = np.loadtxt(path88+fullfilename[-1],dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5))
                            #print(onlyuse)
                            
                            os.remove(path88+fullfilename[-1])   
                                
                    
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
                            #第一個月
                            if typeset[1]=='face' and values1[0]==yearmonthlist:
                                np.savetxt(path88+firstmonth+faceid, onlyuse_id,fmt='%s', delimiter=',')
                                print('typeset[1],yearmonthlist',typeset[1],yearmonthlist)
                                print('file name: ',path88+firstmonth+faceid)
                                
                            elif typeset[1]=='idcard' and values1[0]==yearmonthlist:
                                np.savetxt(path88+firstmonth+cardid, onlyuse_id,fmt='%s', delimiter=',') 
                                print('typeset[1],yearmonthlist',typeset[1],yearmonthlist)
                                print('file name: ',path88+firstmonth+cardid)     
                            #第二個月   
                            elif typeset[1]=='face' and values1[1]==yearmonthlist:
                                np.savetxt(path88+secendmonth+faceid, onlyuse_id,fmt='%s', delimiter=',')
                                print('typeset[1],yearmonthlist',typeset[1],yearmonthlist)
                                print('file name: ',path88+secendmonth+faceid)    
                                
                            elif typeset[1]=='idcard' and values1[1]==yearmonthlist:
                                np.savetxt(path88+secendmonth+cardid, onlyuse_id,fmt='%s', delimiter=',')   
                                print('typeset[1],yearmonthlist',typeset[1],yearmonthlist)
                                print('file name: ',path88+secendmonth+cardid)       
                            #第三個月       
                            elif typeset[1]=='face' and values1[2]==yearmonthlist:
                                np.savetxt(path88+thirdmonth+faceid, onlyuse_id,fmt='%s', delimiter=',')
                                print('typeset[1],yearmonthlist',typeset[1],yearmonthlist)
                                print('file name: ',path88+thirdmonth+faceid)    
                                
                            elif typeset[1]=='idcard' and values1[2]==yearmonthlist:
                                np.savetxt(path88+thirdmonth+cardid, onlyuse_id,fmt='%s', delimiter=',')                                   
                                print('typeset[1],yearmonthlist',typeset[1],yearmonthlist)
                                print('file name: ',path88+thirdmonth+cardid)                                
                                    
                                
                                
    
    def mainpage(self):
        self.page.destroy()
        mainpage(self.root)

    def secpage(self,dp):
        self.page.destroy()
        secondpage(self.root,dp)


    def no_file_worning(self):
        tk.messagebox.showwarning( title='錯誤', message='沒有此月份資料')

      
    def no_file_worning_fail1(self):
        tk.messagebox.showwarning( title='錯誤', message='尚無本月資料，請明日再來查詢') 
      
      
        
    def month_callbackFunc(self,personq,allyesrmonthID):
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
            onlyuse = np.loadtxt('data/'+allyesrmonthID[callbackmonth[0]+backmonth]+alltypechange['face'],dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5,0,1))
            print(onlyuse)
            
            
            if len(glob.glob('data/'+allyesrmonthID[callbackmonth[0]+backmonth]+alltypechange['idcard']))>=1 :
                print(glob.glob('data/'+allyesrmonthID[callbackmonth[0]+backmonth]+alltypechange['idcard']))
                onlyidcard = np.loadtxt('data/'+allyesrmonthID[callbackmonth[0]+backmonth]+alltypechange['idcard'],dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5,0,1))
                print('===========onlyidcard===========',onlyidcard) 
                if onlyidcard.ndim==1:
                    np.insert(onlyuse,1,onlyidcard,axis=0)
                else:          
                    onlyuse=np.concatenate((onlyidcard,onlyuse),axis=0)
                
    
            if len(glob.glob('data/'+allyesrmonthID[callbackmonth[0]+backmonth]+alltypechange['personal']))>=1 :
                print(glob.glob('data/'+allyesrmonthID[callbackmonth[0]+backmonth]+alltypechange['personal']))
                onlyRemote = np.loadtxt('data/'+allyesrmonthID[callbackmonth[0]+backmonth]+alltypechange['personal'],dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5,6,7),encoding = 'utf-8')
                print('===========onlyRemote===========',onlyRemote) 
                if onlyRemote.ndim==1:
                    np.insert(onlyuse,1,onlyRemote,axis=0)
                    #print('--------------------------------------------------------')
                    #print('onlyuse',onlyuse)
                else:
                    onlyuse=np.concatenate((onlyRemote,onlyuse),axis=0)             
                
                
    
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
            tree["columns"]=("狀態別","日期","第一筆時間","最後筆時間","事由","地點")
            tree.column("狀態別",width=80)   #表示列,不显示
            tree.column("日期",width=130)   #表示列,不显示
            tree.column("第一筆時間",width=100)
            tree.column("最後筆時間",width=100)
            tree.column("事由",width=100)
            tree.column("地點",width=100)
            tree.heading("狀態別",text="狀態別")  #显示表头
            tree.heading("日期",text="日期")  #显示表头
            tree.heading("第一筆時間",text="第一筆時間")
            tree.heading("最後筆時間",text="最後筆時間")
            tree.heading("事由",text="事由")
            tree.heading("地點",text="地點")  
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
                
                
                type123=onlyuse_id_a[0:1,0]
                type123offtime=onlyuse_id_a[:,0]
                name123=onlyuse_id_a[0:1,2]
                datetime=onlyuse_id_a[0:1,4]
                ontime=onlyuse_id_a[0:1,5]
                offtime=onlyuse_id_a[:,5]
                weekfial=weekreport(datetime[0])
    
                
                        
                if len(id1)==1:
                    if type123[0]=='open':
                        type123[0]='Face'
                    if type123[0]=='idcard':
                        type123[0]='Card'    
                    if type123[0]=='OutsideWork':
                        type123[0]='公出'  
                        thing123=onlyuse_id_a[0:1,6]
                        location123=onlyuse_id_a[0:1,7]                    
                        tree.insert("",line123,text=name123[0] ,values=(type123[0],datetime[0]+'('+weekfial+')' ,ontime[0],"  ",thing123[0],location123[0]))
                    else:
                        tree.insert("",line123,text=name123[0] ,values=(type123[0],datetime[0]+'('+weekfial+')' ,ontime[0],"  "," "," "))
                        
            
                else :
                    if type123[0]=='open':
                        type123[0]='Face'   
                    if type123[0]=='idcard':
                        type123[0]='Card'    
                        
                    if type123[0]=='idcard':
                        type123[0]='Card'   
                    if type123[0]=='OutsideWork' or type123offtime[1]=='OutsideWork':
                        if type123[0]=='OutsideWork':
                            thing123=onlyuse_id_a[0:1,6]
                            mainthing=thing123[0]
                            location123=onlyuse_id_a[0:1,7]
                            mainlocation=location123[0]
                        else :
                            thing123=onlyuse_id_a[:,6]
                            mainthing=thing123[1]
                            location123=onlyuse_id_a[:,7]
                            mainlocation=location123[1]
                        
    #                     type123offtime[1]=='OutsideWork'
                        type123[0]='公出'  
    #                     thing123=onlyuse_id_a[0:1,6]
    #                     location123=onlyuse_id_a[0:1,7]  
                        tree.insert("",line123,text=name123[0] ,values=(type123[0],datetime[0]+'('+weekfial+')' ,ontime[0],offtime[1],mainthing,mainlocation  ) )
    
                    else:    
                        if type123[0]=='Work' or type123offtime[1]=='Work':
                            type123[0]='遠端上班'
                        if type123[0]=='OffWork' or type123offtime[1]=='OffWork':
                            type123[0]='遠端下班'
                        tree.insert("",line123,text=name123[0] ,values=(type123[0],datetime[0]+'('+weekfial+')' ,ontime[0],offtime[1]," "," "  ) )
                    
                line123=line123+1
        
            #vertical scrollbar------------    https://www.cnblogs.com/Tommy-Yu/p/4156014.html
            vbar = ttk.Scrollbar(self.page,orient=tk.VERTICAL,command=tree.yview)
            vbar.grid(column=10,row=7,sticky=tk.NS) 
            tree.configure(yscrollcommand=vbar.set)
            
            tree.grid(columnspan=9,row=7,sticky=tk.W)   
            
            #空白
            spaceLabel= tk.Label(self.page,textvariable="             " )
            spaceLabel.grid(columnspan=9, row=8, sticky=tk.W)  
            
            self.vartitle3=tk.StringVar()
            self.vartitle3.set('(1)晶片卡更新時間為次月第1天上班日，每個月更新1次')
            self.title3Label= tk.Label(self.page,textvariable=self.vartitle3, font=('Arial', 12),fg='#228B22',justify = tk.RIGHT )
            self.title3Label.grid(columnspan=9,   row=9, sticky=tk.W) 
            self.vartitle3=tk.StringVar()
            self.vartitle3.set('(2)人臉識別更新時間為隔日，每天更新1次')
            self.title3Label= tk.Label(self.page,textvariable=self.vartitle3, font=('Arial', 12),fg='#228B22',justify = tk.RIGHT )
            self.title3Label.grid(columnspan=9,   row=10, sticky=tk.W)               
            self.vartitle4=tk.StringVar()
            self.vartitle4.set('(3)資料若未更新，請按重新整理更新資料')
            self.title4Label= tk.Label(self.page,textvariable=self.vartitle4, font=('Arial', 12),fg='#228B22',justify = tk.RIGHT )
            self.title4Label.grid(columnspan=9,   row=11, sticky=tk.W)   
    
            root.mainloop()   
        
            
            
        except:
            self.no_file_worning_fail1()
        



    def show_idcard_callbackFunc(self,personq,allyesrmonthID):
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
            onlyuse = np.loadtxt('data/'+allyesrmonthID[callbackmonth[0]+backmonth]+alltypechange['idcard'],dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5))
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
            tree["columns"]=("狀態別","日期","第一筆時間","最後筆時間","事由","地點")
            tree.column("狀態別",width=80)   #表示列,不显示
            tree.column("日期",width=130)   #表示列,不显示
            tree.column("第一筆時間",width=100)
            tree.column("最後筆時間",width=100)
            tree.column("事由",width=100)
            tree.column("地點",width=100)
            tree.heading("狀態別",text="狀態別")  #显示表头
            tree.heading("日期",text="日期")  #显示表头
            tree.heading("第一筆時間",text="第一筆時間")
            tree.heading("最後筆時間",text="最後筆時間")
            tree.heading("事由",text="事由")
            tree.heading("地點",text="地點")  
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
                weekfial=weekreport(datetime[0])
                
                        
                if len(id1)==1:
                    tree.insert("",line123,text=name123[0] ,values=("Card",datetime[0]+'('+weekfial+')',ontime[0],"  "," ", " "))
            
                else :
                    tree.insert("",line123,text=name123[0] ,values=("Card",datetime[0]+'('+weekfial+')',ontime[0],offtime[1], " "," "  ) )
                    
                line123=line123+1
        
            #vertical scrollbar------------    https://www.cnblogs.com/Tommy-Yu/p/4156014.html
            vbar = ttk.Scrollbar(self.page,orient=tk.VERTICAL,command=tree.yview)
            vbar.grid(column=10,row=7,sticky=tk.NS) 
            tree.configure(yscrollcommand=vbar.set)
            
            tree.grid(columnspan=9,row=7,sticky=tk.W)    
    
            #空白
            spaceLabel= tk.Label(self.page,textvariable="             " )
            spaceLabel.grid(columnspan=9, row=8, sticky=tk.W)  
            
            self.vartitle3=tk.StringVar()
            self.vartitle3.set('(1)晶片卡更新時間為次月第1天上班日，每個月更新1次')
            self.title3Label= tk.Label(self.page,textvariable=self.vartitle3, font=('Arial', 12),fg='#228B22',justify = tk.RIGHT )
            self.title3Label.grid(columnspan=9,   row=9, sticky=tk.W) 
            self.vartitle3=tk.StringVar()
            self.vartitle3.set('(2)人臉識別更新時間為隔日，每天更新1次')
            self.title3Label= tk.Label(self.page,textvariable=self.vartitle3, font=('Arial', 12),fg='#228B22',justify = tk.RIGHT )
            self.title3Label.grid(columnspan=9,   row=10, sticky=tk.W)               
            self.vartitle4=tk.StringVar()
            self.vartitle4.set('(3)資料若未更新，請按重新整理更新資料')
            self.title4Label= tk.Label(self.page,textvariable=self.vartitle4, font=('Arial', 12),fg='#228B22',justify = tk.RIGHT )
            self.title4Label.grid(columnspan=9,   row=11, sticky=tk.W)   
            root.mainloop()   
            
            
            
        except:
            self.no_file_worning()

    def show_face_callbackFunc(self,personq,allyesrmonthID):
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
            onlyuse = np.loadtxt('data/'+allyesrmonthID[callbackmonth[0]+backmonth]+alltypechange['face'],dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5))
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
            tree["columns"]=("狀態別","日期","第一筆時間","最後筆時間","事由","地點")
            tree.column("狀態別",width=80)   #表示列,不显示
            tree.column("日期",width=130)   #表示列,不显示
            tree.column("第一筆時間",width=100)
            tree.column("最後筆時間",width=100)
            tree.column("事由",width=100)
            tree.column("地點",width=100)
            tree.heading("狀態別",text="狀態別")  #显示表头
            tree.heading("日期",text="日期")  #显示表头
            tree.heading("第一筆時間",text="第一筆時間")
            tree.heading("最後筆時間",text="最後筆時間")
            tree.heading("事由",text="事由")
            tree.heading("地點",text="地點")  
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
                weekfial=weekreport(datetime[0])
                
                        
                if len(id1)==1:
                    tree.insert("",line123,text=name123[0] ,values=("Face",datetime[0]+'('+weekfial+')',ontime[0],"  "," "," "))
            
                else :
                    tree.insert("",line123,text=name123[0] ,values=("Face",datetime[0]+'('+weekfial+')',ontime[0],offtime[1] ," "," " ) )
                    
                line123=line123+1
        
            #vertical scrollbar------------    https://www.cnblogs.com/Tommy-Yu/p/4156014.html
            vbar = ttk.Scrollbar(self.page,orient=tk.VERTICAL,command=tree.yview)
            vbar.grid(column=10,row=7,sticky=tk.NS) 
            tree.configure(yscrollcommand=vbar.set)
            
            tree.grid(columnspan=9,row=7,sticky=tk.W)    
            #空白
            spaceLabel= tk.Label(self.page,textvariable="             " )
            spaceLabel.grid(columnspan=9, row=8, sticky=tk.W)  
            
            self.vartitle3=tk.StringVar()
            self.vartitle3.set('(1)晶片卡更新時間為次月第1天上班日，每個月更新1次')
            self.title3Label= tk.Label(self.page,textvariable=self.vartitle3, font=('Arial', 12),fg='#228B22',justify = tk.RIGHT )
            self.title3Label.grid(columnspan=9,   row=9, sticky=tk.W) 
            self.vartitle3=tk.StringVar()
            self.vartitle3.set('(2)人臉識別更新時間為隔日，每天更新1次')
            self.title3Label= tk.Label(self.page,textvariable=self.vartitle3, font=('Arial', 12),fg='#228B22',justify = tk.RIGHT )
            self.title3Label.grid(columnspan=9,   row=10, sticky=tk.W)               
            self.vartitle4=tk.StringVar()
            self.vartitle4.set('(3)資料若未更新，請按重新整理更新資料')
            self.title4Label= tk.Label(self.page,textvariable=self.vartitle4, font=('Arial', 12),fg='#228B22',justify = tk.RIGHT )
            self.title4Label.grid(columnspan=9,   row=11, sticky=tk.W)   
            root.mainloop()   
            
            
            
        except:
            self.no_file_worning_fail1()
              

    def show_remote_callbackFunc(self,personq,allyesrmonthID):
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
        print('callbackmonth[0]',callbackmonth[0])
        print('backmonth',backmonth)
        try:
            onlyuse = np.loadtxt('data/'+allyesrmonthID[callbackmonth[0]+backmonth]+alltypechange['personal'],dtype=np.str,delimiter=',',usecols=(0,1,4,5,6,7),encoding = 'utf-8')
            print(onlyuse)
            
            
     
    
            tree=ttk.Treeview(self.page,height =20 ,show='headings')#表格show='headings'隱藏第一欄
            tree["columns"]=("狀態別","日期","第一筆時間","最後筆時間","事由","地點")
            tree.column("狀態別",width=80)   #表示列,不显示
            tree.column("日期",width=130)   #表示列,不显示
            tree.column("第一筆時間",width=100)
            tree.column("最後筆時間",width=100)
            tree.column("事由",width=100)
            tree.column("地點",width=100)
            tree.heading("狀態別",text="狀態別")  #显示表头
            tree.heading("日期",text="日期")  #显示表头
            tree.heading("第一筆時間",text="第一筆時間")
            tree.heading("最後筆時間",text="最後筆時間")
            tree.heading("事由",text="事由")
            tree.heading("地點",text="地點")        
            #tree.insert("", insert_mode, text='name first col')
            style = ttk.Style()
            style.configure("Treeview", font=('Arial',12))
            style.configure("Treeview.Heading", font=('Arial', 12)) 
            
            line123=0
            
            if onlyuse.ndim>1:
            #try:#如果只有一個row的話就不會有onlyuse.shape[1]，只有onlyuse.shape[0]會造成錯誤，因此用except去接
                print('onlyuse.shape[0],onlyuse.shape[1]',onlyuse.shape[0],onlyuse.shape[1])
                for line in range(onlyuse.shape[0]) :
                    name123=onlyuse[line,0]
                    datetime=onlyuse[line,2]
                    ontime=onlyuse[line,3]
                    why=onlyuse[line,4]
                    location=onlyuse[line,5]   
                    print('name123',name123)
                    print('datetime',datetime)
                    print('ontime',ontime)
                    print('why',why)  
                    weekfial=weekreport(datetime)
                    if why=='None':
                        why=''
                    if location=='None':
                        location=''            
                    print('location',location)  
                    if name123=='OutsideWork':
                        name123='公出'
                    tree.insert("",line123,text=name123 ,values=(name123,datetime+'('+weekfial+')',ontime,"  ",why,location ) )   
                 
                    line123=line123+1
            
                #vertical scrollbar------------    https://www.cnblogs.com/Tommy-Yu/p/4156014.html
                vbar = ttk.Scrollbar(self.page,orient=tk.VERTICAL,command=tree.yview)
                vbar.grid(column=10,row=7,sticky=tk.NS) 
                tree.configure(yscrollcommand=vbar.set)
                
                tree.grid(columnspan=9,row=7,sticky=tk.W)    
        
                root.mainloop()   
            else:
            #except:
                print('onlyuse.shape[0]',onlyuse.shape[0])
               
                name123=onlyuse[0]
                datetime=onlyuse[2]
                ontime=onlyuse[3]
                why=onlyuse[4]
                location=onlyuse[5]   
                weekfial=weekreport(datetime)
                #print('name123',name123)
                #print('datetime',datetime)
                #print('ontime',ontime)
                #print('why',why)  
                if why=='None':
                    why=''
                if location=='None':
                    location=''            
                print('location',location)  
                if name123=='OutsideWork':
                    name123='公出'
                tree.insert("",0,text=name123 ,values=(name123,datetime+'('+weekfial+')',ontime,"  ",why,location ) )   
             
            
            
                #vertical scrollbar------------    https://www.cnblogs.com/Tommy-Yu/p/4156014.html
                vbar = ttk.Scrollbar(self.page,orient=tk.VERTICAL,command=tree.yview)
                vbar.grid(column=10,row=7,sticky=tk.NS) 
                tree.configure(yscrollcommand=vbar.set)
                
                tree.grid(columnspan=9,row=7,sticky=tk.W)    
                #空白
                spaceLabel= tk.Label(self.page,textvariable="             " )
                spaceLabel.grid(columnspan=9, row=8, sticky=tk.W)  
                
                self.vartitle3=tk.StringVar()
                self.vartitle3.set('(1)晶片卡更新時間為次月第1天上班日，每個月更新1次')
                self.title3Label= tk.Label(self.page,textvariable=self.vartitle3, font=('Arial', 12),fg='#228B22',justify = tk.RIGHT )
                self.title3Label.grid(columnspan=9,   row=9, sticky=tk.W) 
                self.vartitle3=tk.StringVar()
                self.vartitle3.set('(2)人臉識別更新時間為隔日，每天更新1次')
                self.title3Label= tk.Label(self.page,textvariable=self.vartitle3, font=('Arial', 12),fg='#228B22',justify = tk.RIGHT )
                self.title3Label.grid(columnspan=9,   row=10, sticky=tk.W) 
                self.vartitle4=tk.StringVar()
                self.vartitle4.set('(3)資料若未更新，請按重新整理更新資料')
                self.title4Label= tk.Label(self.page,textvariable=self.vartitle4, font=('Arial', 12),fg='#228B22',justify = tk.RIGHT )
                self.title4Label.grid(columnspan=9,   row=11, sticky=tk.W)   
                root.mainloop()               
            
            
        except:
            self.no_file_worning()



#建立資料夾
if not os.path.isdir('data/'):
    os.mkdir('data/')    
else :
    print ('data  file exist') 
    

   
if len(glob.glob(path88+'tul_logo1.gif') )==1 and os.path.getsize(path88+'tul_logo1.gif')!=0:#修正圖片0KB問題
    print('tul_logo1.gif have file')
else:
    try:
        f=open(path88+'tul_logo1.gif', 'wb')
        downftp.retrbinary('RETR ' + 'home/AccessFace/config/tul_logo1.gif', f.write )
        print('download file'+path88+'tul_logo1.gif')                    
        f.close()
    
        
    
    except:
        print("download failed. check.......................")




newyear,newmonth,newday=month_and_day()






#downftp.quit()                  # 退出FTP伺服器   






root = tk.Tk()
# root = tk.Toplevel()
# https://blog.csdn.net/FunkyPants/article/details/78163021

root.title('撼訊科技 人資查詢系統')
root.geometry('500x300')

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)

root.config(menu=menubar)
try :
    number123,persenID,pdID,fullID,pwdID,nameID=ftpconn()
except :
    print('not to connet ftp, so personID not download ')
    failconn=1
mainpage(root)

root.mainloop() 