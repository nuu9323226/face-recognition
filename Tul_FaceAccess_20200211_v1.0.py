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

from tkinter import filedialog
#20190203 v1.0版 篩選資料，呈現12個月的資料至表格中
#update release 2020/02/10 v1.1修改資料夾位置models/day ==>放每天檔案 ./data==>放整理後每月的資料  ftp:  /home/AccessFace/day==>放每天  /home/AccessFace/month==>放每個月
                            #新增從到ftp下載每個月份的檔案的設定
import xlrd
#需要安裝sudo pip3 install xlrd
import csv

dpartment=[100,120,121,150,210,220,230,310,325,350,750,756,754,570,160,510,530]


def setectfile():
    file_path = filedialog.askopenfilename()
    #print(file_path)
    pathtofile='data/'
    
    xlsx_to_csv(file_path,pathtofile)
    sp1=file_path.split('/')
    sp2=os.path.splitext(sp1[-1])[0]
    chinesenumber,chinesepersenID=chineseperson_pd_ID()
    onlyuse = np.loadtxt(open(pathtofile+sp2+'.csv',encoding='utf-8'),dtype=np.str,delimiter=',',usecols=(0,3,4,5))
    onlyuse = np.delete(onlyuse, 0, axis=0)
    #print('onlyuse',onlyuse)
    ID,persenID,pdID,fullID=person_pd_ID()
    chinese_number,chinese_persenID=chineseperson_pd_ID()
    #將日期從202002 ==> 2020/02
    sp3=sp2[:6]
    
    try:
        a=int(sp3)
        try:
            os.remove(pathtofile+sp3+'-idcard.csv')
            print(pathtofile+sp3+'-idcard.csv 刪除成功' )
        except:
            print('data'+sp3+'-idcard.csv 檔案不存在')
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
                #print('ddd yes',ddd)
                use_dayindex=np.argwhere(onlyuse==ddd)
                #print('use_dayindex',use_dayindex)
                d2d=ddd[:4]+'-'+ddd[5:7]+'-'+ddd[8:]
                dayonlyuse=onlyuse[use_dayindex[:,0]]
                #print('dayonlyuse',dayonlyuse)
                #在該日期2020/02/01下針對name.txt有註冊的每個人取行
                for idfile in ID:
                    chinese_persenID[idfile]
                    dayonlyuseindex=np.argwhere(dayonlyuse==chinese_persenID[idfile])
                    dayperson_only=dayonlyuse[dayonlyuseindex[:,0]]
                    #print('dayperson_only',dayperson_only)
                    if  dayperson_only[:,2] != ''  :
                        #print(dayperson_only[0,2])
                        dn2=dayperson_only[0,2]
                        final = 'idcard,'+ idfile +','+persenID[idfile] +','+ pdID[idfile] +','+d2d+','+dn2+':00'
                        finalid.append(final)
                            
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
        ftp.connect('192.168.99.158',port,timeout) # 連線FTP伺服器
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
    os.system("echo sat | sudo -S gnome-terminal -x bash -c 'sudo python3 ./conbine2-0207-v2.2.py'")

def quit():
    root.quit()

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
    train_name = open('data/name.txt','r') 
    
    lines = train_name.readlines()
    count=0
    for a in lines:
        b=a.split('\n')
        lines[count]=b[0]
        count += 1
    train_name.close
    return lines

def read_chinesename_object():
    train_name = open('data/chinesename.txt','r') 
    
    lines = train_name.readlines()
    count=0
    for a in lines:
        b=a.split('\n')
        lines[count]=b[0]
        count += 1
    train_name.close
    return lines


def chineseperson_pd_ID():
    allname=read_chinesename_object()
    #print('allname',allname)
    name123=[]
    number123=[]
    for a in allname:
        #print(a)
        all_23=a.split(",")
        #print(all_23)
        number15=all_23[0]
        name15=all_23[1]
        number123.append(number15)
        name123.append(name15)
    #print(name123)
    #print(number123)

    persenID = dict(zip(number123, name123))
 
    return number123,persenID



def person_pd_ID():
    allname=read_train_object()
    #print('allname',allname)
    name123=[]
    number123=[]
    pd123=[]
    for a in allname:
        #print(a)
        all_23=a.split("_")
        #print(all_23)
        number15=all_23[0]
        name15=all_23[1]
        pd15=all_23[2]
        number123.append(number15)
        name123.append(name15)
        pd123.append(pd15)

    #print(name123)
    #print(number123)
    #print(pd123)

    persenID = dict(zip(number123, name123))
    pdID = dict(zip(number123, pd123))
    fullID=dict(zip(number123,allname) )
    #print(persenID)
    #print(pdID)
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
       
        #self.Button = tk.Button(self.page, text=u'DP750', font=('Arial', 12),justify = tk.LEFT,command=partial(self.secpage,'750')) 
        #self.Button.grid(column=5,row=2,sticky=tk.W)         
       
        varspace=tk.StringVar()
        varspace.set("總共建制人數:"+ str(len(number123))+'位' )
        spaceLabel= tk.Label(self.page,textvariable=varspace, font=('Arial', 12),justify = tk.LEFT )
        spaceLabel.grid(column=0, row=3, sticky=tk.W)
        
        
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=4, sticky=tk.W)

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
            
            if len(gpart)>=6:#沒有加=會有6個人不顯示的bug
            
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
                    file_resize=glob.glob(r'image/'+fullID[imagep]+'/*001.png')
                    print('file_resize',file_resize)
                    print("file_resize[-1]",file_resize[-1])
                except:
                    file_resize=glob.glob(r'image/'+fullID[imagep]+'/*.png')
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
                    file_resize=glob.glob(r'image/'+fullID[imagep]+'/*001.png')
                except:
                    file_resize=glob.glob(r'image/'+fullID[imagep]+'/*.png')
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
        #如果是12月倒數到1
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
        
    
        #空白
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=4, sticky=tk.W)          
        
        
        
        #讀取csv並且取012345 colums
        onlyuse = np.loadtxt('data/'+self.stryear+self.strmonth+'.csv',dtype=np.str,delimiter=',',usecols=(0,1,2,3,4,5))
        print('onlyuse',onlyuse)        
        
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
        style.configure("Treeview.Heading", font=(None, 12))     
        
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
        vbar.grid(column=10,row=5,sticky=tk.NS) 
        tree.configure(yscrollcommand=vbar.set)
        #tree.tag_configure ("monospace", font =(None，12) )
        tree.grid(columnspan=9,row=5,sticky=tk.W)    
        
        root.mainloop()   
        
    def mainpage(self):
        self.page.destroy()
        mainpage(self.root)

    def secpage(self,dp):
        self.page.destroy()
        secondpage(self.root,dp)


    def no_file_worning(self):
        tk.messagebox.showwarning( title='錯誤', message='沒有此月份資料，請按重新整理資料庫')

      
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
        



downftp = FTP()
timeout = 30
port = 21
downftp.connect('192.168.99.158',port,timeout) # 連線FTP伺服器
downftp.login('Vincent','helloworld') # 登入
print (downftp.getwelcome())  # 獲得歡迎資訊 
#d=ftp.cwd('home/AccessFace/month')    # 設定FTP路徑
monthftp=downftp.nlst('home/AccessFace/month') #獲取ftp上的所以月份檔案
print('monthftp',monthftp)
path88 =  'data/'
pathimage='image/'

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
    f=open(path88+'name.txt', 'wb')
    downftp.retrbinary('RETR ' + 'home/AccessFace/config/name.txt', f.write )
    print('download file'+path88+'name.txt')                    
    f.close()
    f=open(path88+'chinesename.txt', 'wb')
    downftp.retrbinary('RETR ' + 'home/AccessFace/config/chinesename.txt', f.write )
    print('download file'+path88+'chinesename.txt')                    
    f.close()    
    

except:
    print("download failed. check.......................")

number123,persenID,pdID,fullID =person_pd_ID()    


newyear,newmonth,newday=month_and_day()
allname=read_train_object()
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
        if values12+'.csv' in monthftp12:
            print('glob=====',glob.glob(path88+values12+'.csv'))
            try:
                #如果同時滿足"已經下載過"得跟"不為當月份的"可以不下載
                if len(glob.glob(path88+values12+'.csv'))>=1 and newyear+newmonth+'.csv' != values12+'.csv':
                    print(values12+'.csv yes exist')
                #其餘都會重新下載資料
                else:
                    
                    print(values12+'.csv yes')
                    f=open(path88+values12+'.csv', 'wb')
                    downftp.retrbinary('RETR ' + monthftp12, f.write )
                    print('download file'+path88+values12+'.csv')                    
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



#建立每個人照片資料夾
for imageid in allname:
    if not os.path.isdir(pathimage+imageid):
        os.mkdir(pathimage+imageid)    
    else :
        print (pathimage+imageid+'  file exist')    


#下載每個人照片到資料夾
for imageid in allname:
    
    if len(glob.glob(pathimage+imageid+'/*001.png'))>=1:
        print(pathimage+imageid+'/*001.png exist')
  
    else:
        personftp=downftp.nlst('home/AccessFace/image/'+imageid+'/')
        print('personftp',personftp)
        f=open(pathimage+imageid+'/'+imageid+'_001.png', 'wb')
        try:
            downftp.retrbinary('RETR ' + personftp[0], f.write )
            print('download file '+pathimage+imageid+'/'+imageid+'_001.png')  
            f.close()
        except:
            print("download failed. check.......................")
    



downftp.quit()                  # 退出FTP伺服器   



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
filemenu.add_command(label='系統設定', command=read_train_object)
filemenu.add_command(label='後台管理', command=read_train_object)
filemenu.add_separator()    # 添加一条分隔线


# 第7步，创建一个Edit菜单项（默认不下拉，下拉内容包括Cut，Copy，Paste功能项）
editmenu = tk.Menu(menubar, tearoff=0)
# 将上面定义的空菜单命名为 Edit，放在菜单栏中，就是装入那个容器中
menubar.add_cascade(label='執行', menu=editmenu)

# 同样的在 Edit 中加入Cut、Copy、Paste等小命令功能单元，如果点击这些单元, 就会触发do_job的功能
#b=secondpage()
editmenu.add_command(label='門禁系統啟動', command=rundetect )
editmenu.add_command(label='出缺勤日報表', command=read_train_object)
editmenu.add_command(label='陌生人管理', command=read_train_object)

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
