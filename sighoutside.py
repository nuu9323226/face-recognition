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

global failconn
failconn=0
path88 =  'data/'

from ftplib import FTP_TLS
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
    
#try:
    #downftp = FTP()
    #timeout = 6
    #port = 21
    ##如果ftp有啟動ftps (ssl/tls)加密服務則需要用以下方式連線
    ##https://stackoverflow.com/questions/5534830/ftpes-ftp-over-explicit-tls-ssl-in-python
    #from ftplib import FTP_TLS
    #downftp=FTP_TLS('dsm2.tul.com.tw')
    ##downftp.connect('61.220.84.60',port,timeout) # 連線FTP伺服器
    #downftp.login('TulAccessControl','@Tul760acc') # 登入
    #downftp.encoding='utf-8'
    #downftp.set_pasv(False)
    #print (downftp.getwelcome())  # 獲得歡迎資訊 
    ##d=ftp.cwd('home/AccessFace/month')    # 設定FTP路徑
    #monthftp=downftp.nlst('home/AccessFace/month') #獲取ftp上的所以月份檔案
    #print('monthftp',monthftp)    
    
    
except:
    print('not connect to ftp')
    failconn=1



def ftpconn():
    try:
        f=open(path88+'database_Employee.csv', 'wb')
        downftp.retrbinary('RETR ' + 'home/AccessFace/config/database_Employee.csv', f.write )
        print('download file'+path88+'database_Employee.csv')                    
        f.close()
        
        number123,persenID,pdID,fullID,pwdID,nameID=person_pd_ID()
        #os.remove(path88+'database_Employee.csv')
        print(path88+'database_Employee.csv 刪除成功' )
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





class secondpage(object):
    def __init__(self, master=None):
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
        
        self.varpwdtitle=tk.StringVar()
        self.varpwdtitle.set("            ")
        self.pwdtitleLabel= tk.Label(self.page,textvariable=self.varpwdtitle, font=('Arial', 10),justify = tk.RIGHT )
        self.pwdtitleLabel.grid(column=0, row=1, sticky=tk.W)       
        
        self.vartitle=tk.StringVar()
        self.vartitle.set("撼訊科技 公出電子表單" )
        self.titleLabel= tk.Label(self.page,textvariable=self.vartitle, font=('Arial', 14),justify = tk.RIGHT )
        self.titleLabel.grid(column=0, row=2, sticky=tk.W)   
        
        self.vartitle2=tk.StringVar()
        #self.vartitle2.set("員工： "+persenID[self.dp]+ '        部門： '+ pdID[self.dp])
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
        
        #self.Button = tk.Button(self.page, text=u'清除',font=('Arial', 12),justify = tk.LEFT,command=partial(self.secpage,self.dp)  ) 
        #self.Button.grid(column=1,row=21, sticky=tk.W)          
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
          
        
  
        root.mainloop()   
        
 
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
         
        
    def takerun(self):
        #print('mode',mode)
        if not os.path.isdir('data/'):
            os.mkdir('data/')    
        else :
            print ('data  file exist')     
            
            
        self.dp=self.varBusinessPerson1.get()

        
        
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
            #addperson.append(self.dp)
            
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
root.geometry('500x300')

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)

root.config(menu=menubar)

number123,persenID,pdID,fullID,pwdID,nameID=person_pd_ID()

secondpage(root)

root.mainloop() 