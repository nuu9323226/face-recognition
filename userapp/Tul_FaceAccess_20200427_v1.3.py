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
# pyinstaller -F -w .\Tul_FaceAccess_20200427_v1.3.py -i tul_logo.ico
#import faceRegistered
#20190203 v1.0版 篩選資料，呈現12個月的資料至表格中
#update release 2020/02/10 v1.1修改資料夾位置models/day ==>放每天檔案 ./datas==>放整理後每月的資料  ftp:  /home/AccessFace/day==>放每天  /home/AccessFace/month==>放每個月
                            #新增從到ftp下載每個月份的檔案的設定
#update release 2020/02/14 v1.2增加匯入晶片卡資料功能    
#update release 2020/04/24 v1.3 (1)整合個人板功能，可以檢視晶片卡 人臉跟外出紀錄 (2)新增查看上班時數功能
import xlrd
#需要安裝sudo pip3 install xlrd
import csv

dpartment=[100,120,121,150,210,220,230,310,325,350,'TCMC',750,756,754,'IOTU',570,160,510,530]

def helloworld():
    print('helloworld')

def TimeSubtraction(ontime,offtime):
    TOontime=datetime.strptime (ontime,'%H:%M:%S')
    TOofftime=datetime.strptime (offtime,'%H:%M:%S')
    return str(TOofftime-TOontime) 

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


def facebuind():
    os.system('python3 faceRegistered.py')



def read_name_object():
    train_name = open('datas/database_Employee.csv','r',encoding='utf-8') 
    
    lines = train_name.readlines()
    count=0
    for a in lines:
        b=a.split('\n')
        lines[count]=b[0]
        count += 1
    train_name.close
    return lines


def person_pd_ID():
    allname=read_name_object()
    #print('allname',allname)
    name123=[]
    number123=[]
    pd123=[]
    pwd123=[]
    twzhname123=[]
    for a in allname:
        #print(a)
        all_23=a.split(",")
        #print(all_23)
        number15=all_23[2]
        name15=all_23[3]
        twzhname15=all_23[3]
        pd15=all_23[5]
        number123.append(number15)
        name123.append(name15)
        pd123.append(pd15)
        twzhname123.append(twzhname15)

    persenID = dict(zip(number123, name123))
    pdID = dict(zip(number123, pd123))
    nameID=dict(zip(name123,number123) )
    twzhnameID=dict(zip(number123,twzhname123) )
    fullID=dict(zip(number123,allname) )
    
    return number123,persenID,pdID,nameID,twzhnameID,fullID




def setectfile():
    
    if len(glob.glob('datas/database_Employee.csv') ) ==0:
        try:
            f=open('datas/database_Employee.csv', 'wb')
            downftp.retrbinary('RETR ' + 'home/AccessFace/config/database_Employee.csv', f.write )
            print('download file  datas/database_Employee.csv')                    
            f.close()    
            
        except:
            print("failed  datas/database_Employee.csv' download. check.......................")    
            
    
    number123,persenID,pdID,nameID,twzhnameID,fullID=person_pd_ID()
    
    
    file_path = filedialog.askopenfilename()
    #print(file_path)
    pathtofile='datas/'
    
    xlsx_to_csv(file_path,pathtofile)
    sp1=file_path.split('/')
    sp2=os.path.splitext(sp1[-1])[0]
    onlyuse = np.loadtxt(open(pathtofile+sp2+'.csv',encoding='utf-8'),dtype=np.str,delimiter=',',usecols=(0,3,4,5))
    onlyuse = np.delete(onlyuse, 0, axis=0)
    #print('onlyuse',onlyuse)
    #將日期從202002 ==> 2020/02
    sp3=sp2[:6]
    
    try:
        a=int(sp3)
        try:
            os.remove(pathtofile+sp3+'-idcard.csv')
            print(pathtofile+sp3+'-idcard.csv 刪除成功' )
        except:
            print('datas'+sp3+'-idcard.csv 檔案不存在')
        daymonth=sp3[:4]+'/'+sp3[4:]
        #取出第一排日期，並刪除重複項目
        date=onlyuse[:,0]
        uniquedate = np.unique(date)
        #uniquedate = np.argsort(uniquedate)
        print(uniquedate)
        #符合檔名的202002的月份才取出其index 例如2020/02/01
        finalid=[]
        for ddd in uniquedate:
            if daymonth in ddd: #ddd為20200201 daymonth為202002
                print('ddd yes',ddd)
                use_dayindex=np.argwhere(onlyuse==ddd)
                print('use_dayindex',use_dayindex)
                d2d=ddd[:4]+'-'+ddd[5:7]+'-'+ddd[8:]
                dayonlyuse=onlyuse[use_dayindex[:,0]]
                print('dayonlyuse',dayonlyuse)
                #在該日期2020/02/01下針對name.txt有註冊的每個人取行
                for idfile in number123:
                    print('start to name: ' +idfile)
                    dayonlyuseindex=np.argwhere(dayonlyuse==twzhnameID[idfile])
                    print('start to twzh name: ' +twzhnameID[idfile])
                    dayperson_only=dayonlyuse[dayonlyuseindex[:,0]]
                    print('dayperson_only',dayperson_only)
                    
                    #上班
                    if  dayperson_only[:,2] != ''  :
                        print(dayperson_only[0,2])
                        dn2=dayperson_only[0,2]
                        final = 'idcard,'+ idfile +','+persenID[idfile] +','+ pdID[idfile] +','+d2d+','+dn2+':00'
                        finalid.append(final)
                    #下班
                    if  dayperson_only[:,3] != ''  :
                        print(dayperson_only[0,3])
                        dn3=dayperson_only[0,3]
                        final = 'idcard,'+ idfile +','+persenID[idfile] +','+ pdID[idfile] +','+d2d+','+dn3+':00'
                        finalid.append(final)       
                
                    
                          
                            
        with open(pathtofile+sp3+'-idcard.csv','a') as f: 
            np.savetxt(f, finalid,fmt='%s', delimiter=",")
        f.close
        
        try:
            os.remove(pathtofile+sp2+'.csv')
            print(pathtofile+sp2+'.csv 刪除成功')
        except:
            print(pathtofile+sp2+'.csv 檔案不存在')        
        
        
        ftp = FTP()
        timeout = 30
        port = 21
        ftp=FTP_TLS('192.168.91.158')
        #ftp.connect('192.168.99.158',port,timeout) # 連線FTP伺服器
        ftp.login('Vincent','helloworld') # 登入
        print (ftp.getwelcome())  # 獲得歡迎資訊 
        #d=ftp.cwd('home/AccessFace/')    # 設定FTP路徑     
        try:
            #d=ftp.cwd('home/AccessFace/')
            ftp.storbinary('STOR '+'home/AccessFace/month/'+sp3+'-idcard.csv' , open(pathtofile+sp3+'-idcard.csv', 'rb')) # 上傳FTP檔案
            print("succes upload: " +'home/AccessFace/month/'+sp3+'-idcard.csv')
        except:
            print("upload failed. check.......................")
            
        ftp.quit()                  # 退出FTP伺服器      
        
        tkinter.messagebox.showinfo(title='成功訊息', message=sp3[:4]+'年'+sp3[4:]+'月資料已匯入完成')
    
    except:
        try:
            os.remove(pathtofile+sp2+'.csv')
            print(pathtofile+sp2+'.csv 刪除成功')
        except:
            print(pathtofile+sp2+'.csv 檔案不存在')  
        tk.messagebox.showwarning( title='錯誤', message='請將檔名設置yyyymm開頭')
        
def xlsx_to_csv(file_path,savepath):
    workbook = xlrd.open_workbook(file_path)
    table = workbook.sheet_by_index(0)  
    sp1=file_path.split('/')
    sp2=os.path.splitext(sp1[-1])[0]
    with open(savepath+sp2+'.csv', 'w', encoding='utf-8') as f:
        write = csv.writer(f)
        for row_num in range(table.nrows):
            row_value = table.row_values(row_num)
            write.writerow(row_value)

def deleteDuplicatedElementFromList3(listA):
#return list(set(listA))
    return sorted(set(listA), key = listA.index)

def rundetect():
    #os.system("echo sat | sudo -S gnome-terminal -x bash -c 'sudo python3 ./conbine2-0207-v2.2.py'")
    os.system("echo sat | sudo python3 ./conbine2-0207-v2.2.py &") #背景執行

def quit():
    root.quit()

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

# def read_train_object():
#     train_name = open('datas/name.txt','r') 
    
#     lines = train_name.readlines()
#     count=0
#     for a in lines:
#         b=a.split('\n')
#         lines[count]=b[0]
#         count += 1
#     train_name.close
#     return lines








class mainpage(object):
    def __init__(self, master=None):
        self.root = master 
        
        self.page = tk.Frame(self.root) 
        self.page.grid()
        #self.dport='760'
        
        #建立button
        self.Button = tk.Button(self.page, text=u'DP100總經理室', font=('微軟正黑體', 12),justify = tk.LEFT,command=partial(self.secpage,'100')) 
        self.Button.grid(column=0,row=0, sticky=tk.W) 
        self.Button = tk.Button(self.page, text=u'DP120品保', font=('微軟正黑體', 12),justify = tk.LEFT,command=partial(self.secpage,'120')) 
        self.Button.grid(column=1,row=0,sticky=tk.W) 
        self.Button = tk.Button(self.page, text=u'DP121測試', font=('微軟正黑體', 12),justify = tk.LEFT,command=partial(self.secpage,'121')) 
        self.Button.grid(column=2,row=0, sticky=tk.W)  
        self.Button = tk.Button(self.page, text=u'DP150稽核室', font=('微軟正黑體', 12),justify = tk.LEFT,command=partial(self.secpage,'150')) 
        self.Button.grid(column=3,row=0, sticky=tk.W) 
        self.Button = tk.Button(self.page, text=u'DP210人資總務', font=('微軟正黑體', 12),justify = tk.LEFT,command=partial(self.secpage,'210')) 
        self.Button.grid(column=4,row=0,sticky=tk.W)          
        self.Button = tk.Button(self.page, text=u'DP220財快', font=('微軟正黑體', 12),justify = tk.LEFT,command=partial(self.secpage,'220')) 
        self.Button.grid(column=5,row=0, sticky=tk.W) 
        self.Button = tk.Button(self.page, text=u'IOTU撼智物聯', font=('微軟正黑體', 12),justify = tk.LEFT,command=partial(self.secpage,'IOTU')) 
        self.Button.grid(column=6,row=0, sticky=tk.W)         
        
        
        self.Button = tk.Button(self.page, text=u'DP230資訊', font=('微軟正黑體', 12),justify = tk.LEFT,command=partial(self.secpage,'230')) 
        self.Button.grid(column=0,row=1,sticky=tk.W) 
        self.Button = tk.Button(self.page, text=u'DP310業務', font=('微軟正黑體', 12),justify = tk.LEFT,command=partial(self.secpage,'310')) 
        self.Button.grid(column=1,row=1, sticky=tk.W) 
        self.Button = tk.Button(self.page, text=u'DP325 IPC', font=('微軟正黑體', 12),justify = tk.LEFT,command=partial(self.secpage,'325')) 
        self.Button.grid(column=2,row=1,sticky=tk.W) 
        self.Button = tk.Button(self.page, text=u'DP350產品中心', font=('微軟正黑體', 12),justify = tk.LEFT,command=partial(self.secpage,'350')) 
        self.Button.grid(column=3,row=1, sticky=tk.W) 
        self.Button = tk.Button(self.page, text=u'DP750研一', font=('微軟正黑體', 12),justify = tk.LEFT,command=partial(self.secpage,'750')) 
        self.Button.grid(column=4,row=1,sticky=tk.W)
        self.Button = tk.Button(self.page, text=u'DP756研二', font=('微軟正黑體', 12),justify = tk.LEFT,command=partial(self.secpage,'756')) 
        self.Button.grid(column=5,row=1, sticky=tk.W) 
        
        self.Button = tk.Button(self.page, text=u'TCMC撼衛生醫', font=('微軟正黑體', 12),justify = tk.LEFT,command=partial(self.secpage,'TCMC')) 
        self.Button.grid(column=6,row=1, sticky=tk.W)         
        
        self.Button = tk.Button(self.page, text=u'DP754軟體研發', font=('微軟正黑體', 12),justify = tk.LEFT,command=partial(self.secpage,'754')) 
        self.Button.grid(column=0,row=2,sticky=tk.W) 
        self.Button = tk.Button(self.page, text=u'DP570技轉', font=('微軟正黑體', 12),justify = tk.LEFT,command=partial(self.secpage,'570')) 
        self.Button.grid(column=1,row=2, sticky=tk.W) 
        self.Button = tk.Button(self.page, text=u'DP160 RMA', font=('微軟正黑體', 12),justify = tk.LEFT,command=partial(self.secpage,'160')) 
        self.Button.grid(column=2,row=2,sticky=tk.W) 
        self.Button = tk.Button(self.page, text=u'DP510採購', font=('微軟正黑體', 12),justify = tk.LEFT,command=partial(self.secpage,'510')) 
        self.Button.grid(column=3,row=2,sticky=tk.W)    
        self.Button = tk.Button(self.page, text=u'DP530船務', font=('微軟正黑體', 12),justify = tk.LEFT,command=partial(self.secpage,'530')) 
        self.Button.grid(column=4,row=2,sticky=tk.W)         
       
      
       
        varspace=tk.StringVar()
        varspace.set("總共建制人數:"+ str(len(number123))+'位' )
        spaceLabel= tk.Label(self.page,textvariable=varspace, font=('微軟正黑體', 12),justify = tk.LEFT )
        spaceLabel.grid(column=0, row=3, sticky=tk.W)
        
        varspaceqq=tk.StringVar()
        varspaceqq.set("     *名單為隨機排序" )
        spaceLabel1= tk.Label(self.page,textvariable=varspaceqq, font=('微軟正黑體', 10),justify = tk.LEFT )
        spaceLabel1.grid(column=0, row=4, sticky=tk.W)

        #從資料夾抓取以建檔名稱
        filename=[]
        sourcefile=glob.glob(r'image/*')
        print('sourcefile',sourcefile)
        for a in sourcefile:
            finalname=a.split("/")
            filename.append(finalname[-1])
        print ('finalname',filename)
        print('len(filename',len(filename))
        line1=5



        for dpart in dpartment:

            #print('dpartment',dpart)
            #locals()['self.var'+str(dpart)]=tk.StringVar()
            #locals()['self.var'+str(dpart)].set(str(dpart)+'部門:  ')
            #locals()['self.textLabel'+str(dpart)] = tk.Label(self.page,textvariable=locals()['self.var'+str(dpart)], bg='green', font=('微軟正黑體', 12),justify = tk.LEFT)
            #locals()['self.textLabel'+str(dpart)].grid(column=0, row=line1, sticky=tk.W)
            #line1=line1+1
            print('line1',line1)
            gpart=[]
            
            for c,v in pdID.items():
                if str(v)==str(dpart):
                    gpart.append(c)
                    print('number',c)
            
            
            print('len(gpart)',len(gpart))
            column01=1
            if len(gpart)<7:
                
                
                for personq in gpart:
                    print('personq',personq)
                    print('persenID',persenID[personq])
                    locals()['self.var'+str(personq)]=tk.StringVar()
                    locals()['self.var'+str(personq)].set(persenID[personq])
                    locals()['self.textLabel'+str(personq)] = tk.Label(self.page,textvariable=locals()['self.var'+str(personq)], font=('微軟正黑體', 10),justify = tk.LEFT)
                    locals()['self.textLabel'+str(personq)].grid(column=gpart.index(personq)+1, row=line1, sticky=tk.W)
        
    
                line1=line1+1
                
                
            else:
                runrurn=len(gpart)/6
                print('len(gpart)/6',runrurn)
                rundiv=len(gpart)%6
                print('len(gpart)%6',rundiv)
         
                    
                for personq in gpart:
                        print('column',(gpart.index(personq))%7)
                        print('line1',line1)
                        print('personq',personq)
                        print('persenID',persenID[personq])
                        locals()['self.var'+str(personq)]=tk.StringVar()
                        locals()['self.var'+str(personq)].set(persenID[personq])
                        locals()['self.textLabel'+str(personq)] = tk.Label(self.page,textvariable=locals()['self.var'+str(personq)], font=('微軟正黑體', 10),justify = tk.LEFT)
                        locals()['self.textLabel'+str(personq)].grid(column=((gpart.index(personq))%7)+1 , row=line1, sticky=tk.W)
                        if (gpart.index(personq)+1)%7==0 or len(gpart)-1==gpart.index(personq):
                            line1=line1+1

                        
        line1=5                        
        for dpart in dpartment:
            print('line1',line1)
            gpart=[]
            
            for c,v in pdID.items():
                if str(v)==str(dpart):
                    gpart.append(c)
                    print('number',c)
            
            
            print('len(gpart)',len(gpart))
            column01=0
            print('dpartment',dpart)
            locals()['self.var'+str(dpart)]=tk.StringVar()
            locals()['self.var'+str(dpart)].set(str(dpart)+'部門:  ')
            locals()['self.textLabel'+str(dpart)] = tk.Label(self.page,textvariable=locals()['self.var'+str(dpart)], bg='green', font=('微軟正黑體', 10),justify = tk.LEFT)
            locals()['self.textLabel'+str(dpart)].grid(column=column01, row=line1, sticky=tk.W)
            if  len(gpart)<7:              
                line1=line1+1
            else:       
                for personq in gpart:
                    print('line1',line1)
                    if (gpart.index(personq)+1)%7==0 or len(gpart)-1==gpart.index(personq):
                        line1=line1+1                    
                

        
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
        self.Button = tk.Button(self.page, text=u'主畫面',font=('微軟正黑體', 12),justify = tk.LEFT,command=self.mainpage) 
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
        spaceLabel= tk.Label(self.page,textvariable=varspace, font=('微軟正黑體', 12),justify = tk.LEFT )
        spaceLabel.grid(column=0, row=3, sticky=tk.W)
        
        #增減人員
        
        #self.varnumber=tk.StringVar()
        #self.varnumber.set("工號")
        #self.numberLabel= tk.Label(self.page,textvariable=self.varnumber, font=('微軟正黑體', 12),justify = tk.RIGHT )
        #self.numberLabel.grid(column=1, row=0, sticky=tk.E)        
        
        #self.varname=tk.StringVar()
        #self.varname.set("姓名")
        #self.nameLabel= tk.Label(self.page,textvariable=self.varname, font=('微軟正黑體', 12),justify = tk.RIGHT )
        #self.nameLabel.grid(column=1, row=1, sticky=tk.E)   
        
        #self.varpd=tk.StringVar()
        #self.varpd.set("部門異動")
        #self.nameLabel= tk.Label(self.page,textvariable=self.varpd, font=('微軟正黑體', 12),justify = tk.RIGHT )
        #self.nameLabel.grid(column=1, row=2, sticky=tk.E)           
        
        ##填字匡
        #self.numberString = tk.StringVar()
        #self.entrynumber = tk.Entry(self.page, width=20, textvariable=self.numberString)
        #self.entrynumber.grid(column=2, row=0, padx=1)
        
        #self.nameString = tk.StringVar()
        #self.entryname = tk.Entry(self.page, width=20, textvariable=self.nameString)
        #self.entryname.grid(column=2, row=1, padx=1)
        
        #self.pdString = tk.StringVar()
        #self.entrypd = tk.Entry(self.page, width=20, textvariable=self.pdString)
        #self.entrypd.grid(column=2, row=2, padx=1)        
        
                
        ##按鈕
        #self.addButton = tk.Button(self.page, text = '新增',command=self.add_callbackFunc )
        #self.addButton.grid(column=3, row=0, pady=1, sticky=tk.W)
        
        #self.reduceButton = tk.Button(self.page, text = '刪除',command=self.reduce_callbackFunc)
        #self.reduceButton.grid(column=3, row=1, pady=1, sticky=tk.W)        
        
        #self.reduceButton = tk.Button(self.page, text = '編輯',command=self.eddit_callbackFunc)
        #self.reduceButton.grid(column=3, row=2, pady=1, sticky=tk.W)         
        
        
        ##回應的字顯示
        #self.add_resultString=tk.StringVar()
        #self.add_resultLabel = tk.Label(self.page, textvariable=self.add_resultString,fg="#DC143C" )
        #self.add_resultLabel.grid(column=0, row=1, padx=1, sticky=tk.W)        
        
        #self.reduce_resultString=tk.StringVar()
        #self.reduce_resultLabel = tk.Label(self.page, textvariable=self.reduce_resultString,fg="#DC143C" )
        #self.reduce_resultLabel.grid(column=0, row=1, padx=1, sticky=tk.W)   
        
        #self.eddit_resultString=tk.StringVar()
        #self.eddit_resultLabel = tk.Label(self.page, textvariable=self.eddit_resultString,fg="#DC143C" )
        #self.eddit_resultLabel.grid(column=0, row=1, padx=1, sticky=tk.W)         

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
            
            if len(gpart)>=7:#沒有加=會有6個人不顯示的bug
            
                print('personq',personq)
                print('persenID',persenID[personq])
                #locals()['self.var'+str(personq)]=tk.StringVar()
                #locals()['self.var'+str(personq)].set(personq+' '+persenID[personq])
                
                #locals()['self.textLabel'+str(personq)] = tk.Label(self.page,textvariable=locals()['self.var'+str(personq)], font=('微軟正黑體', 12),justify = tk.LEFT)#显示文字内容 
                #locals()['self.textLabel'+str(personq)].grid(column=column01, row=line1, sticky=tk.W) #自动对齐,side：方位
                
                locals()['self.Button'+str(personq)]= tk.Button(self.page,text =str(personq+' '+persenID[personq]),font=('微軟正黑體', 12) ,command=partial(self.personpage1,personq) )
                locals()['self.Button'+str(personq)].grid(column=column01, row=line1, pady=1, sticky=tk.W)
                
                #self.addButton = tk.Button(self.page, text = '新增',command=self.add_callbackFunc )
                #self.addButton.grid(column=3, row=0, pady=1, sticky=tk.W)                
                
                column01=column01+1
                if column01==6:
                    line1=line1+2
                    column01=0
                    
            if len(gpart)<7:
            
                print('personq',personq)
                print('persenID',persenID[personq])
                locals()['self.var'+str(personq)]=tk.StringVar()
                locals()['self.var'+str(personq)].set(personq+' '+persenID[personq])
                #locals()['self.textLabel'+str(personq)] = tk.Label(self.page,textvariable=locals()['self.var'+str(personq)], font=('微軟正黑體', 12),justify = tk.LEFT)#显示文字内容 
                #locals()['self.textLabel'+str(personq)].grid(column=column01, row=line1, sticky=tk.W) #自动对齐,side：方位
                
                
                #======learning=====
                #button需要引數傳遞在這裡需要用到partial(funtion名稱, 2)
                #https://www.delftstack.com/zh-tw/howto/python-tkinter/how-to-pass-arguments-to-tkinter-button-command/
                #======learning=====
                
                locals()['self.Button'+str(personq)]= tk.Button(self.page,text =str(personq+' '+persenID[personq]),font=('微軟正黑體', 12) ,command=partial(self.personpage1,personq) )
                locals()['self.Button'+str(personq)].grid(column=column01, row=line1, pady=1, sticky=tk.W)
                #self.addButton = tk.Button(self.page, text = '新增',command=self.add_callbackFunc )
                #self.addButton.grid(column=3, row=0, pady=1, sticky=tk.W)                 
                
                column01=column01+1

        ##建立照片欄
        #line1=5
        #column01=0
            
        #for imagep in gpart:
            
            #if len(gpart)>=6:
            
            
                #print('fullID[imagep]',fullID[imagep])
                #print('imagep',imagep)
                #try:
                    #file_resize=glob.glob(r'image/'+fullID[imagep]+'/*001.png')
                    #print('file_resize',file_resize)
                    #print("file_resize[-1]",file_resize[-1])
                #except:
                    #file_resize=glob.glob(r'image/'+fullID[imagep]+'/*.png')
                    #print('file_resize',file_resize)
                    #print("file_resize[-1]",file_resize[-1])
                    #print('error')
##                 pil_image = Image.open(r'C:\Users\23216\Desktop\1.jpg') 

##                 realname=file_resize[0].split('/')
                #print("file_resize[-1]",file_resize[-1])
                #locals()['photo'+str(imagep)] = tk.PhotoImage(file=file_resize[-1])  #file：t图片路径
                #locals()['imgLabel'+str(imagep)]  = tk.Label(self.page,image=locals()['photo'+str(imagep)])#把图片整合到标签类中
                #locals()['imgLabel'+str(imagep)].grid(column=column01, row=line1, sticky=tk.W)
                #column01=column01+1
                #if column01==5:
                    #line1=line1+2
                    #column01=0
                    
            #if len(gpart)<6:
                
                #print('fullID[imagep]',fullID[imagep])
                #print('imagep',imagep)
                #try:
                    #file_resize=glob.glob(r'image/'+fullID[imagep]+'/*001.png')
                #except:
                    #file_resize=glob.glob(r'image/'+fullID[imagep]+'/*.png')
                #print('file_resize',file_resize)


##                 pil_image = Image.open(r'C:\Users\23216\Desktop\1.jpg') 

##                 realname=file_resize[0].split('/')
                #print("file_resize[-1]",file_resize[-1])
                #locals()['photo'+str(imagep)] = tk.PhotoImage(file=file_resize[-1])  #file：t图片路径
                #locals()['imgLabel'+str(imagep)]  = tk.Label(self.page,image=locals()['photo'+str(imagep)])#把图片整合到标签类中
                #locals()['imgLabel'+str(imagep)].grid(column=column01, row=line1, sticky=tk.W)
                #column01=column01+1
        
        
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
        self.Button = tk.Button(self.page, text=u'回登入頁',font=('微軟正黑體', 12),justify = tk.LEFT,command=self.mainpage ) 
        self.Button.grid(column=0,row=0 , sticky=tk.W ) 
        self.Button = tk.Button(self.page, text=u'返回',font=('微軟正黑體', 12),justify = tk.LEFT,command=partial(self.secpage,pdID[personq])) 
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
            for nt in range(-13,-1):
                #abs取對值
                tmonth=str(newtyear)+"/"+str(abs(nt+1))
                values1.append(tmonth )
                valuesmonth.append(str(newtyear))
                valuesmonth.append(str(abs(nt+1)) )
        else :#如果是非12月倒數到1，年減1
            for ny in range(0,12):
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
 
        
        #下載資料
        self.callbackallthing(values1)
        #print('self.onlyRemote1',self.onlyRemote1)        
        
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=1, sticky=tk.W)
        
        varspace=tk.StringVar()
        varspace.set("個人頁面查詢： "+self.personq+ ' ' +persenID[personq] )
        spaceLabel= tk.Label(self.page,textvariable=varspace, font=('微軟正黑體', 12),justify = tk.LEFT )
        spaceLabel.grid(column=0, row=2, sticky=tk.W)
        
        
        
        
        

                
        print('values1',values1)
        varspace=tk.StringVar()
        varspace.set("選擇月份：")
        spaceLabel= tk.Label(self.page,textvariable=varspace, font=('微軟正黑體', 12),justify = tk.LEFT )
        spaceLabel.grid(column=0, row=3, sticky=tk.W)
        
        
        
        #選擇月份bar
        self.comboExample = ttk.Combobox(self.page, width=7 ,values=values1, font=('微軟正黑體', 12),state="readonly") 
        
        
        print(dict(self.comboExample)) 
        self.comboExample.grid(column=0, row=3,sticky=tk.N+tk.S)
        self.comboExample.current(0)
        print(self.comboExample.current(), self.comboExample.get())
    
        #選擇月份事件按鈕
        self.addButton = tk.Button(self.page, text = '查詢',command=partial(self.month_callbackFunc,personq), font=('微軟正黑體', 12) )
        self.addButton.grid(column=0, row=3, pady=1, sticky=tk.E)        
        
        
        
        
        #選擇月份事件按鈕
        self.addButton = tk.Button(self.page, text = '重新整理',command=partial(self.callbackallthingFlesh,values1), font=('微軟正黑體', 12) )
        self.addButton.grid(column=1, row=3, pady=1, sticky=tk.E)   
        
        self.var1 = tk.StringVar()
        self.var1.set("A")
        
        #circleLabel= tk.Label(self.page,textvariable=self.var1, font=('微軟正黑體', 12),justify = tk.LEFT )
        #circleLabel.grid(column=1, row=3, sticky=tk.W)   
        #self.var1.grid(column=0, row=4,sticky=tk.N+tk.S)
        self.selectcircle=tk.Radiobutton(self.page,text = '合併檢視', variable=self.var1, value='A',command=partial(self.month_callbackFunc,personq)   , font=('微軟正黑體', 12) )
        self.selectcircle.grid(column=0, row=4, pady=0, sticky=tk.W)      
        
        self.selectcircle=tk.Radiobutton(self.page,text = '檢視晶片卡',variable=self.var1,value='B',command=partial(self.show_idcard_callbackFunc,personq)   , font=('微軟正黑體', 12) )
        self.selectcircle.grid(column=0,columnspan=2, row=4, pady=0, sticky=tk.N+tk.S)       
        
        self.selectcircle=tk.Radiobutton(self.page,text = '檢視人臉識別', variable=self.var1,value='C',command=partial(self.show_face_callbackFunc,personq)  , font=('微軟正黑體', 12) )
        self.selectcircle.grid(column=0,columnspan=2, row=4, pady=0, sticky=tk.E)   
        
        self.selectcircle=tk.Radiobutton(self.page,text = '公出及遠端', variable=self.var1,value='D',command=partial(self.show_remote_callbackFunc,personq)  , font=('微軟正黑體', 12) )
        self.selectcircle.grid(column=0,columnspan=2, row=5, pady=0, sticky=tk.E)         
        
        #空白
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=6, sticky=tk.W)          
        
        path88='datas/remote/'+self.personq+'/'
        values123=self.personq+'-'+self.stryear+self.strmonth
        #讀取csv並且取012345 colums
        onlyuse = np.loadtxt('datas/'+self.stryear+self.strmonth +'-face.csv', dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5,0,1) )
        print('onlyuse',onlyuse)        
        
        if len(glob.glob('datas/'+ self.stryear+self.strmonth  + '-idcard.csv' ))>=1 :
            print(glob.glob('datas/'+self.stryear+self.strmonth + '-idcard.csv' ))
            onlyidcard = np.loadtxt('datas/'+ self.stryear+self.strmonth  + '-idcard.csv'  ,dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5,0,1))
#             print('onlyonlyidcard.shape,onlyonlyidcard.ndim',onlyonlyidcard.shape[0],onlyonlyidcard.shape[1],onlyonlyidcard.ndim)
            print('===========onlyidcard===========',onlyidcard) 
            
            onlyuse=np.concatenate((onlyidcard,onlyuse),axis=0)    #拼接陣列     
        
        if len(glob.glob(path88+values123+ '-personal.csv' ))>=1 :
             
            print(glob.glob(path88+values123+ '-personal.csv' ))
            
            
            onlyRemote = np.loadtxt(path88+values123+ '-personal.csv' ,dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5,6,7),encoding = 'utf-8')
            print('onlyRemote.shape,onlyRemote.ndim',onlyRemote.shape[0],onlyRemote.ndim)
            if onlyRemote.ndim==1:
                ##np.reshape(onlyRemote,(2,6) , order='F') 
                ##print('reshape onlyRemote',onlyRemote)
                ##onlyRemote[None,:].shape 
                ##arrayB = np.ones((1, onlyRemote.shape[0] ))
                #arrayB = np.empty([1, onlyRemote.shape[0] ], dtype='string')
                #numset=0
                #for onevole in onlyRemote:
                np.insert(onlyuse,-1,onlyRemote,axis=0)
                    
                    
                    
                #np.append(onlyuse, onlyRemote, axis=0)
            else:
                onlyuse=np.concatenate((onlyRemote,onlyuse),axis=0)        
    
        
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
        tree["columns"]=("狀態別","日期","第一筆時間","最後筆時間","時數","事由")
        tree.column("狀態別",width=80)   #表示列,不显示
        tree.column("日期",width=130)   #表示列,不显示
        tree.column("第一筆時間",width=100)
        tree.column("最後筆時間",width=100)
        tree.column("時數",width=100)
        tree.column("事由",width=100)
        tree.heading("狀態別",text="狀態別")  #显示表头
        tree.heading("日期",text="日期")  #显示表头
        tree.heading("第一筆時間",text="第一筆時間")
        tree.heading("最後筆時間",text="最後筆時間")
        tree.heading("時數",text="時數")
        tree.heading("事由",text="事由")     
        #tree.insert("", insert_mode, text='name first col')
        style = ttk.Style()
        style.configure("Treeview", font=('微軟正黑體',12))
        style.configure("Treeview.Heading", font=('微軟正黑體', 12))     
        
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
            #print('type123',type123)
            #print('name123',name123)
            #print('datetime',datetime)
            #print('ontime',ontime)
            #print('offtime',offtime)            
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
                    tree.insert("",line123,text=name123[0] ,values=(type123[0],datetime[0]+'('+weekfial+')',ontime[0],"  ",thing123[0],location123[0]))
                else:
                    tree.insert("",line123,text=name123[0] ,values=(type123[0],datetime[0]+'('+weekfial+')',ontime[0],"  "," "," "))
                    
        
            else :
                Timesubtraction=TimeSubtraction(ontime[0],offtime[1])
                print('Timesubtraction',Timesubtraction)                
                if type123[0]=='open':
                    type123[0]='Face'   
                if type123[0]=='idcard':
                    type123[0]='Card'       
                if type123[0]=='OutsideWork' or type123offtime[1]=='OutsideWork':
                    if type123[0]=='OutsideWork':
                        thing123=onlyuse_id_a[0:1,6]
                        mainthing=thing123[0]
                    else :
                        thing123=onlyuse_id_a[:,6]
                        mainthing=thing123[1]
                    
#                     type123offtime[1]=='OutsideWork'
                    type123[0]='公出'  
                    thing123=onlyuse_id_a[0:1,6]
                    #location123=onlyuse_id_a[0:1,7]  

                    tree.insert("",line123,text=name123[0] ,values=(type123[0],datetime[0]+'('+weekfial+')',ontime[0],offtime[1],Timesubtraction,mainthing )  )
                else:    
                    if type123[0]=='Work' or type123offtime[1]=='Work':
                        type123[0]='遠端上班'
                    if type123[0]=='OffWork' or type123offtime[1]=='OffWork':
                        type123[0]='遠端下班'
                    tree.insert("",line123,text=name123[0] ,values=(type123[0],datetime[0]+'('+weekfial+')',ontime[0],offtime[1],Timesubtraction," ") )
                
            line123=line123+1
    
        #vertical scrollbar------------    https://www.cnblogs.com/Tommy-Yu/p/4156014.html
        vbar = ttk.Scrollbar(self.page,orient=tk.VERTICAL,command=tree.yview)
        vbar.grid(column=10,row=7,sticky=tk.NS) 
        tree.configure(yscrollcommand=vbar.set)
        #tree.tag_configure ("monospace", font =(None，12) )
        tree.grid(columnspan=9,row=7,sticky=tk.W)    
        
        root.mainloop()   
    
    
    def callbackallthing(self,values):
        
        if not os.path.isdir('datas/remote/'+self.personq):
            os.mkdir('datas/remote/'+self.personq)    
        else :
            print ('datas/remote/'+self.personq + ' => file exist')         
        
        
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
                

            
            
            
            
            if len(personftp)>=1: 
                print('personftp',personftp)     
                path88='datas/remote/'+self.personq+'/'
                
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
                                
                                f=open(path88+values123+'-personal.csv', 'wb')
                                downftp.retrbinary('RETR ' + personftp1, f.write )
                                print('download file: '+path88+values123+'-personal.csv')                    
                                f.close()   
              
                    elif len(glob.glob(path88+values123+'-personal.csv' ) )>=1 and newyear+newmonth!=yearmonthlist :#非月則是本地端有沒有檔案下載
                        print(path88+values123+'-personal.csv' +'已經有檔案不下載了，非本月')
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
                                
                                f=open( path88+values123+'-personal.csv' , 'wb')
                                downftp.retrbinary('RETR ' + personftp1, f.write )
                                print('download file:  '+path88+values123+'-personal.csv' )                    
                                f.close()   
                                
                    

                                
    def callbackallthingFlesh(self,values):
        
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
        print('values1',values1)
        
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
                

            #allmonthID=secretname(values1)
            
            
            
            if len(personftp)>=1: 
                print('personftp',personftp)     
                path88='datas/remote/'
                
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
                            
                            f=open(path88+self.personq+'/'+self.personq+'-'+yearmonthlist+'-personal.csv', 'wb')
                            downftp.retrbinary('RETR ' + personftp1, f.write )
                            print('download file: '+path88+self.personq+'/'+self.personq+'-'+yearmonthlist+'-personal.csv')                    
                            f.close()   
                                               
                        
               
            #下載month個人的檔案 
            path1='home/AccessFace/month/'
            personftp1=downftp.nlst(path1)  
            if len(personftp1)>=1: 
                print('personftp1',personftp1)     
                path88='datas/'   
                
                
                for yearmonthlist in values1 : 
                    print('yearmonthlist',yearmonthlist) 
                    
        
                    for personftphot in  personftp1 :
                        fullfilename=personftphot.split('/')
                        typeset_exe=fullfilename[-1].split('.')
                        typeset=typeset_exe[0].split('-')
                        if typeset[0]==yearmonthlist:
                            print('idcard or face file找到了',personftphot)
                                
                            #if len(glob.glob('datas/'+allmonthID[yearmonthlist]+alltypechange[ typeset[1] ] )) >= 1 :
                                #print('datas/'+allmonthID[yearmonthlist]+alltypechange[ typeset[1] ]+' 已經有檔案不下載了')
                    
                            #else :
                            f=open(path88+fullfilename[-1], 'wb')
                            downftp.retrbinary('RETR ' + personftphot, f.write )
                            print('download file'+path88+fullfilename[-1])                    
                            f.close() 
                            
                            
                                
                                
    
    def mainpage(self):
        self.page.destroy()
        mainpage(self.root)

    def secpage(self,dp):
        self.page.destroy()
        secondpage(self.root,dp)


    def no_file_worning(self):
        tk.messagebox.showwarning( title='錯誤', message='沒有此月份資料，請重新匯入資料')

      
 
      
      
        
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
        
        #try:
        onlyuse = np.loadtxt('datas/'+callbackmonth[0]+backmonth +'-face.csv',dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5,0,1))
        print(onlyuse)
        
        
        if len(glob.glob('datas/'+callbackmonth[0]+backmonth+'-idcard.csv' ))>=1 :
            print(glob.glob('datas/'+callbackmonth[0]+backmonth+'-idcard.csv'))
            onlyidcard = np.loadtxt('datas/'+callbackmonth[0]+backmonth+'-idcard.csv' ,dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5,0,1))
            print('===========onlyidcard===========',onlyidcard) 
            if onlyidcard.ndim==1:
                np.insert(onlyuse,1,onlyidcard,axis=0)
            else:          
                onlyuse=np.concatenate((onlyidcard,onlyuse),axis=0)
            

        if len(glob.glob('datas/remote/'+personq+'/' + personq+'-'+callbackmonth[0]+backmonth +'-personal.csv' ))>=1 :
            print(glob.glob('datas/remote/'+personq+'/' + personq+'-'+callbackmonth[0]+backmonth +'-personal.csv'))
            onlyRemote = np.loadtxt('datas/remote/'+personq+'/' + personq+'-'+callbackmonth[0]+backmonth +'-personal.csv' ,dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5,6,7),encoding = 'utf-8')
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
        tree["columns"]=("狀態別","日期","第一筆時間","最後筆時間","時數","事由")
        tree.column("狀態別",width=80)   #表示列,不显示
        tree.column("日期",width=130)   #表示列,不显示
        tree.column("第一筆時間",width=100)
        tree.column("最後筆時間",width=100)
        tree.column("時數",width=100)
        tree.column("事由",width=100)
        tree.heading("狀態別",text="狀態別")  #显示表头
        tree.heading("日期",text="日期")  #显示表头
        tree.heading("第一筆時間",text="第一筆時間")
        tree.heading("最後筆時間",text="最後筆時間")
        tree.heading("時數",text="時數")
        tree.heading("事由",text="事由")  
        #tree.insert("", insert_mode, text='name first col')
        style = ttk.Style()
        style.configure("Treeview", font=('微軟正黑體',12))
        style.configure("Treeview.Heading", font=('微軟正黑體', 12)) 
        
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
            #print('type123',type123)
            #print('name123',name123)
            #print('datetime',datetime)
            #print('ontime',ontime)
            #print('offtime',offtime)            
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
                    tree.insert("",line123,text=name123[0] ,values=(type123[0],datetime[0]+'('+weekfial+')',ontime[0],"  ",thing123[0],location123[0]))
                else:
                    tree.insert("",line123,text=name123[0] ,values=(type123[0],datetime[0]+'('+weekfial+')',ontime[0],"  "," "," "))
                    
        
            else :
                Timesubtraction=TimeSubtraction(ontime[0],offtime[1])
                print('Timesubtraction',Timesubtraction)                
                if type123[0]=='open':
                    type123[0]='Face'   
                if type123[0]=='idcard':
                    type123[0]='Card'    
                if type123[0]=='OutsideWork' or type123offtime[1]=='OutsideWork':
                    if type123[0]=='OutsideWork':
                        thing123=onlyuse_id_a[0:1,6]
                        mainthing=thing123[0]
                    else :
                        thing123=onlyuse_id_a[:,6]
                        mainthing=thing123[1]
                    
#                     type123offtime[1]=='OutsideWork'
                    type123[0]='公出'  
#                     thing123=onlyuse_id_a[0:1,6]
                    #location123=onlyuse_id_a[0:1,7]  

                    tree.insert("",line123,text=name123[0] ,values=(type123[0],datetime[0]+'('+weekfial+')',ontime[0],offtime[1],Timesubtraction,mainthing )  )
                else:    
                    if type123[0]=='Work' or type123offtime[1]=='Work':
                        type123[0]='遠端上班'
                    if type123[0]=='OffWork' or type123offtime[1]=='OffWork':
                        type123[0]='遠端下班'
                    tree.insert("",line123,text=name123[0] ,values=(type123[0],datetime[0]+'('+weekfial+')',ontime[0],offtime[1],Timesubtraction," ") )
                
            line123=line123+1
    
        #vertical scrollbar------------    https://www.cnblogs.com/Tommy-Yu/p/4156014.html
        vbar = ttk.Scrollbar(self.page,orient=tk.VERTICAL,command=tree.yview)
        vbar.grid(column=10,row=7,sticky=tk.NS) 
        tree.configure(yscrollcommand=vbar.set)
        
        tree.grid(columnspan=9,row=7,sticky=tk.W)    

        root.mainloop()   
        
            
            
        #except:
            #self.no_file_worning()
        



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
            onlyuse = np.loadtxt('datas/'+callbackmonth[0]+backmonth+'-idcard.csv',dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5))
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
            style.configure("Treeview", font=('微軟正黑體',12))
            style.configure("Treeview.Heading", font=('微軟正黑體', 12)) 
            
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
            onlyuse = np.loadtxt('datas/'+callbackmonth[0]+backmonth+'-face.csv',dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5))
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
            style.configure("Treeview", font=('微軟正黑體',12))
            style.configure("Treeview.Heading", font=('微軟正黑體', 12)) 
            
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
        print('callbackmonth[0]',callbackmonth[0])
        print('backmonth',backmonth)
        try:
            onlyuse = np.loadtxt('datas/remote/'+personq+'/'+personq+'-'+callbackmonth[0]+backmonth+'-personal.csv',dtype=np.str,delimiter=',',usecols=(0,1,4,5,6,7),encoding = 'utf-8')
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
            style.configure("Treeview", font=('微軟正黑體',12))
            style.configure("Treeview.Heading", font=('微軟正黑體', 12)) 
            
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
        
                root.mainloop()               
            
            
        except:
            self.no_file_worning()



#from ftplib import FTP_TLS
downftp = FTP()
timeout = 6
port = 21
#如果ftp有啟動ftps (ssl/tls)加密服務則需要用以下方式連線
#https://stackoverflow.com/questions/5534830/ftpes-ftp-over-explicit-tls-ssl-in-python
#from ftplib import FTP_TLS
# downftp=FTP_TLS('61.220.84.60')
downftp.connect('61.220.84.60',port,timeout) # 連線FTP伺服器
downftp.login('Vincent','helloworld') # 登入
downftp.encoding='utf-8'
downftp.set_pasv(False)
print (downftp.getwelcome())  # 獲得歡迎資訊 
#d=ftp.cwd('home/AccessFace/month')    # 設定FTP路徑
monthftp=downftp.nlst('home/AccessFace/month') #獲取ftp上的所以月份檔案
print('monthftp',monthftp)
path88 =  'datas/'
pathimage='image/'

#建立資料夾
if not os.path.isdir('datas/'):
    os.mkdir('datas/')    
else :
    print ('datas  file exist') 
    
if not os.path.isdir('datas/remote/'):
    os.mkdir('datas/remote/')    
else :
    print ('datas/remote/  file exist')     
    
# if not os.path.isdir('image/'):
#     os.mkdir('image/')    
# else :
#     print ('image  file exist') 


try:
    f=open(path88+'database_Employee.csv', 'wb')
    downftp.retrbinary('RETR ' + 'home/AccessFace/config/database_Employee.csv', f.write )
    print('download file'+path88+'database_Employee.csv')                    
    f.close()
#     f=open(path88+'chinesename.txt', 'wb')
#     downftp.retrbinary('RETR ' + 'home/AccessFace/config/chinesename.txt', f.write )
#     print('download file'+path88+'chinesename.txt')                    
#     f.close()    
    

except:
    print("home/AccessFace/config/database_Employee.csv  download failed. check.......................")

number123,persenID,pdID,nameID,twzhnameID,fullID =person_pd_ID()    


newyear,newmonth,newday=month_and_day()
# allname=read_train_object()
print('newyear','newmonth',newyear,newmonth)

yearddd=int(newyear)
monthddd=int(newmonth)

values888=[]
valuesmonth888=[]
valuesyear888=[]
#如果是12月倒數到1


   

if monthddd==12 :
    for nt in range(-13,-1):
        #abs取對值
        tmonth=str(yearddd)+'/'+str(abs(nt+1))
        values888.append(tmonth )
        valuesmonth888.append(str(yearddd))
        valuesmonth888.append(str(abs(nt+1)) )
else :#如果是非12月倒數到1，年減1
    for ny in range(0,12):
        if int(monthddd)==0 :
            yearddd=int(yearddd)-1
            monthddd=12
        values888.append(str(yearddd)+'/'+str(monthddd) )
        valuesyear888.append(str(yearddd) )
        valuesmonth888.append(str(monthddd) )                
        monthddd=int(monthddd)-1  

print('values888=============',values888)



pdtrue888=[]
for avv in values888:
    pday=avv.split('/')
    # x.month=10
    if int(pday[1])<10 and int(pday[1])>=1:
        pday[1]='0'+str(pday[1])
        #print (month)
    else :
        pday[1]=str(pday[1])            
    pdtrue888.append(pday[0]+pday[1])
print('pdtrue888',pdtrue888)








#下載12個月份內的入出資料，比對ftp上所有的月份的檔案中，如果滿足當月回推12的月內的資料則進行下載的動作
for monthftp12 in monthftp:
    for values12 in pdtrue888 :
        if values12+'-face.csv' in monthftp12:
            print('glob=====',glob.glob(path88+values12+'-face.csv'))
            try:
                #如果同時滿足"已經下載過"得跟"不為當月份的"可以不下載
                if len(glob.glob(path88+values12+'-face.csv'))>=1 and newyear+newmonth+'-face.csv' != values12+'-face.csv':
                    print(values12+'-face.csv yes exist')
                #其餘都會重新下載資料
                else:
                    
                    print(values12+'-face.csv yes')
                    f=open(path88+values12+'-face.csv', 'wb')
                    downftp.retrbinary('RETR ' + monthftp12, f.write )
                    print('download file'+path88+values12+'-face.csv')                    
                    f.close()
            except:
                print("download failed. check.......................")


#下載12個月份內的入出資料，比對ftp上所有的月份的檔案中，如果滿足當月回推12的月內的資料則進行下載的動作
for monthftp12 in monthftp:
    for values12 in pdtrue888 :
        if values12+'-idcard.csv' in monthftp12:
            print('glob=====',glob.glob(path88+values12+'-idcard.csv'))
            try:
                #如果同時滿足"已經下載過"得跟"不為當月份的"可以不下載
                if len(glob.glob(path88+values12+'-idcard.csv'))>=1 and newyear+newmonth+'-idcard.csv' != values12+'-idcard.csv':
                    print(values12+'-idcard.csv yes exist')
                #其餘都會重新下載資料
                else:
                    
                    print(values12+'-idcard.csv yes')
                    f=open(path88+values12+'-idcard.csv', 'wb')
                    downftp.retrbinary('RETR ' + monthftp12, f.write )
                    print('download file'+path88+values12+'-idcard.csv')                    
                    f.close()
            except:
                print("download failed. check.......................")



# #建立每個人照片資料夾
# for imageid in allname:
#     if not os.path.isdir(pathimage+imageid):
#         os.mkdir(pathimage+imageid)    
#     else :
#         print (pathimage+imageid+'  file exist')    


# #下載每個人照片到資料夾
# for imageid in allname:
    
#     if len(glob.glob(pathimage+imageid+'/*001.png'))>=1:
#         print(pathimage+imageid+'/*001.png exist')
  
#     else:
#         personftp=downftp.nlst('home/AccessFace/image/'+imageid+'/')
#         print('personftp',personftp)
#         f=open(pathimage+imageid+'/'+imageid+'_001.png', 'wb')
#         try:
#             downftp.retrbinary('RETR ' + personftp[0], f.write )
#             print('download file '+pathimage+imageid+'/'+imageid+'_001.png')  
#             f.close()
#         except:
#             print("download failed. check.......................")
    



#downftp.quit()                  # 退出FTP伺服器   



root = tk.Tk()
# root = tk.Toplevel()
# https://blog.csdn.net/FunkyPants/article/details/78163021

root.title('撼訊科技 門禁管理系統')
root.geometry('1000x850')

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)

menubar.add_cascade(label='開始', menu=filemenu)

# 在File中加入New、Open、Save等小菜单，即我们平时看到的下拉菜单，每一个小菜单对应命令操作。

filemenu.add_command(label='員工資料建立', command=facebuind )
filemenu.add_command(label='偏好設定', command=helloworld)
filemenu.add_command(label='後台管理', command=helloworld)
filemenu.add_separator()    # 添加一条分隔线


# 第7步，创建一个Edit菜单项（默认不下拉，下拉内容包括Cut，Copy，Paste功能项）
editmenu = tk.Menu(menubar, tearoff=0)
# 将上面定义的空菜单命名为 Edit，放在菜单栏中，就是装入那个容器中
menubar.add_cascade(label='執行', menu=editmenu)

# 同样的在 Edit 中加入Cut、Copy、Paste等小命令功能单元，如果点击这些单元, 就会触发do_job的功能
#b=secondpage()
editmenu.add_command(label='門禁系統啟動', command=rundetect )
editmenu.add_command(label='出缺勤日報表', command=helloworld)
editmenu.add_command(label='陌生人管理', command=helloworld)

# 第8步，创建第二级菜单，即菜单项里面的菜单
submenu = tk.Menu(filemenu) # 和上面定义菜单一样，不过此处实在File上创建一个空的菜单
filemenu.add_cascade(label='匯入ID card資料', menu=submenu, underline=0) # 给放入的菜单submenu命名为Import

# 第9步，创建第三级菜单命令，即菜单项里面的菜单项里面的菜单命令（有点拗口，笑~~~）
submenu.add_command(label='從本機匯入', command=setectfile)   # 这里和上面创建原理也一样，在Import菜单项中加入一个小菜单命令Submenu_1

filemenu.add_command(label='離開', command=root.destroy) # 用tkinter里面自带的quit()函数
# 第11步，创建菜单栏完成后，配置让菜单栏menubar显示出来
root.config(menu=menubar)

mainpage(root)

root.mainloop()     
