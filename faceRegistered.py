from tkinter import *
import cv2,os
from PIL import Image,ImageTk
from tkinter import filedialog
from datetime import datetime, timedelta
import numpy as np
import glob
path_database='../models/'
Employeefile = path_database + 'database_Employee.csv'
recoding=0
neweh_name=0
newid=0
newdate=datetime.now().strftime("%Y-%m-%d")
import random
import time
import tkinter as tk
import tkinter.messagebox
countframe=0
initfile=0

def read_train_object():
    train_name = open(path_database+Employeefile,'r') 
    
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


def no_file_worning2():
    tk.messagebox.showwarning( title='錯誤', message='無攝影鏡頭')   
def no_file_worning3():
    tk.messagebox.showwarning( title='錯誤', message='無此資料夾')      
def video_loop():
    success, img = camera.read()  # 從camera輸入影像
    
    saveframe = img.copy()
    global newdate,countframe

    if success:
        cv2.waitKey(1000)
        cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)#轉換顏色從BGR到RGBA 
        current_image = Image.fromarray(cv2image)#將圖像轉換成Image類別
        imgtk = ImageTk.PhotoImage(image=current_image)
        panel.imgtk = imgtk
        panel.config(image=imgtk)
        root.after(1, video_loop)
        countframe=countframe+1
        if recoding==1  and countframe%3==0 : #迴圈控制錄製影像速度countframe越低則紀錄速度快 countframe 越高越慢
            
            #print('heklllo')
            #sourcefile=glob.glob(r'../models/person/'+newid+'_'+neweh_name+'/*')
            #print('countframe',countframe)
            #存檔
            cv2.imwrite('../models/person/'+newid+'_'+neweh_name+'/'+newid+'_'+neweh_name+'_'+ newdate+random.choice('abcdefgf')+ str(countframe)+ '.jpg',saveframe ,[int(cv2.IMWRITE_JPEG_QUALITY), 100])
            
            #讀取檔案資料夾大於50則回報一次
            ding=os.listdir('../models/person/'+newid+'_'+neweh_name+'/')
            if len(ding)%50==0:  
                #print('len',len(ding))
                getframe_resultString.set("已經紀錄 {} 張影像".format(len(ding)  ))    



def add_result():
    stop_resultString.set('           ')  
    getframe_resultString.set('            ')   
    print('idnumberString',idnumberString.get())
    print('nameString',nameString.get())   
    print('egnameString',egnameString.get())  
    print('pdString',pdString.get())  
    print('bdString',bdString.get())  
    newdate=datetime.now().strftime("%Y-%m-%d")
    global initfile
    #buildin人臉識別資料 / register人臉圖資  / 工號 / 中文名 / 英文名 / 部門 / buildin人臉識別資料日期 / register人臉圖資日期


    '''
    如果database_Employee.csv初始沒這個檔案，會造成錯誤因此需要偵測這個檔案是否存在，採取兩個方式進行
    dataperson ['2222']
    Exception in Tkinter callback
    Traceback (most recent call last):
      File "/usr/lib/python3.5/tkinter/__init__.py", line 1553, in __call__
        return self.func(*args)
      File "/home/vincent/facenet/real-time-deep-face-recognition/faceRegistered.py", line 140, in getframe_result
        getframe_resultString.set("員工 {} {} 紀錄影像中.... 請雙眼直視鏡頭".format(idnumberString.get(),dataperson[0,1]  ))
    IndexError: too many indices for array
    initfile為1則表示初始偵測沒有database_Employee.csv這個檔案會觸發這個機制，預防bug
    '''

    if initfile==1: #initfile為1則表示初始偵測沒有database_Employee.csv
        
        #建立這個檔案database_Employee.csv
        f=open(path_database+'database_Employee.csv','a') 
        f.close       
       
        
        finalid=[]
        finalid.append('0,1,'+idnumberString.get() +','+nameString.get() +','+egnameString.get() +','+pdString.get() +','+bdString.get() +','+'register-'+newdate )
        
        print('finalid',finalid)
        
        #np.savetxt(path_database+'database_Employee.csv', finalid,fmt='%s', delimiter=',')
        with open(path_database+'database_Employee.csv','a') as f: 
            np.savetxt(f, finalid,fmt='%s', delimiter=',')
        f.close    
        
        add_resultString.set("員工 {} {} {},部門{} 新增成功".format(idnumberString.get(),nameString.get(),egnameString.get(),pdString.        get()))    
        
        if not os.path.isdir('../models/person/'+idnumberString.get()+'_'+egnameString.get()+'/' ):
            os.mkdir('../models/person/'+idnumberString.get()+'_'+egnameString.get())    
        else :
            print ('data  file exist')         
            
        
    
    elif initfile==0:  #initfile為0則表示初始偵測有database_Employee.csv
        
       
        Employeefile1 = np.loadtxt(Employeefile,dtype=np.str,delimiter=',',usecols=(2,3,4))
        print('Employeefile1',Employeefile1)
        
        #onlyid=Employeefile1[:,2]
        #print()
        #print('onlyid',onlyid)
        EmployeeHaveindex=np.argwhere(Employeefile1==idnumberString.get() )  #依照工號找尋紀錄 
        print('EmployeeHaveindex',EmployeeHaveindex) 
        id1=EmployeeHaveindex[:,0] #將找到index從2維轉為1維
        print('id1',id1) 
        if len(id1)==0: #如果紀錄為0筆
            
            
            finalid=[]
            finalid.append('0,1,'+idnumberString.get() +','+nameString.get() +','+egnameString.get() +','+pdString.get() +','+bdString.get() +','+'register-'+newdate )
            
            print('finalid',finalid)
            
            #np.savetxt(path_database+'database_Employee.csv', finalid,fmt='%s', delimiter=',')
            with open(path_database+'database_Employee.csv','a') as f: 
                np.savetxt(f, finalid,fmt='%s', delimiter=',')
            f.close    
            
            add_resultString.set("員工 {} {} {},部門{} 新增成功".format(idnumberString.get(),nameString.get(),egnameString.get(),pdString.        get()))    
            
            if not os.path.isdir('../models/person/'+idnumberString.get()+'_'+egnameString.get()+'/' ):
                os.mkdir('../models/person/'+idnumberString.get()+'_'+egnameString.get())    
            else :
                print ('data  file exist')         
            
        
        if len(id1)==1: #如果紀錄為1筆
            
            print('i have one apple')
            dataperson=Employeefile1[EmployeeHaveindex[:,0]]
            print('dataperson',dataperson)
            add_resultString.set("員工 {} {} 已建立過資料，請直接開始建立人臉生物識別".format(idnumberString.get(),dataperson[0,1] ))    
                
            if not os.path.isdir('../models/person/'+idnumberString.get()+'_'+dataperson[0,2]+'/' ):
                os.mkdir('../models/person/'+idnumberString.get()+'_'+dataperson[0,2])    
            else :
                print ('/models/person/'+idnumberString.get()+'_'+dataperson[0,2]+'  file exist')        
            
        
        

def getframe_result(): #開始紀錄
    stop_resultString.set('           ')  
    print('idnumberString',idnumberString.get())
    print('nameString',nameString.get())   
    print('egnameString',egnameString.get())  
    print('pdString',pdString.get())  
    newdate=datetime.now().strftime("%Y-%m-%d")
    #buildin人臉識別資料 / register人臉圖資  / 工號 / 中文名 / 英文名 / 部門 / buildin人臉識別資料日期 / register人臉圖資日期
    
    #f=open(path_database+'database_Employee.csv','a') 
    #f.close       
   
    Employeefile1 = np.loadtxt(Employeefile,dtype=np.str,delimiter=',',usecols=(2,3,4))
    print('Employeefile1',Employeefile1)
    
    #onlyid=Employeefile1[:,2]
    #print()
    #print('onlyid',onlyid)
    EmployeeHaveindex=np.argwhere(Employeefile1==str(idnumberString.get() )) 
    print('EmployeeHaveindex',EmployeeHaveindex)
    id1=EmployeeHaveindex[:,0]
    print('id1',id1)
    sourcefile=glob.glob(path_database+'database_Employee.csv')
    print('len sourcefile',len(sourcefile) )
    

 
    if len(id1)==0 and initfile==0 :
        
        

        getframe_resultString.set('員工資料未建立，請重新註冊 ')    
       
        
    
    elif len(id1)==1 and initfile==1:
        
        print('i have one apple')
        dataperson=Employeefile1[EmployeeHaveindex[:,0]]
        print('dataperson',dataperson)
        getframe_resultString.set("員工 {} {} 紀錄影像中.... 請雙眼直視鏡頭".format(idnumberString.get(),nameString.get()  ))    
            
        if not os.path.isdir('../models/person/'+idnumberString.get()+'_'+egnameString.get()+'/' ):
            os.mkdir('../models/person/'+idnumberString.get()+'_'+egnameString.get())    
        else :
            print ('/models/person/'+idnumberString.get()+'_'+egnameString.get()+'  file exist')        
        global recoding,neweh_name,newid
        recoding=1
        neweh_name=egnameString.get()
        newid=idnumberString.get()
        
    elif len(id1)==1 and initfile==0:
        
        print('i have one apple')
        dataperson=Employeefile1[EmployeeHaveindex[:,0]]
        print('dataperson',dataperson)
        getframe_resultString.set("員工 {} {} 紀錄影像中.... 請雙眼直視鏡頭".format(idnumberString.get(),dataperson[0,1]  ))    
            
        if not os.path.isdir('../models/person/'+idnumberString.get()+'_'+dataperson[0,2]+'/' ):
            os.mkdir('../models/person/'+idnumberString.get()+'_'+dataperson[0,2])    
        else :
            print ('/models/person/'+idnumberString.get()+'_'+dataperson[0,2]+'  file exist')        
        global recoding,neweh_name,newid
        recoding=1
        neweh_name=dataperson[0,2]
        newid=idnumberString.get()    


def openfile():
    number123,persenID,pdID,fullID,pwdID,nameID,buitinID,ennameID=person_pd_ID()
    path='~/facenet/models/person/'
    
    
    #if not os.path.isdir(path+idnumberString.get()+'_'+ennameID[idnumberString.get()]):
        #print('cant find file '+path+idnumberString.get()+'_'+ennameID[idnumberString.get()])    
        #no_file_worning3()
    #else :
    try:
        print ('datas/remote/'+path+idnumberString.get()+'_'+ennameID[idnumberString.get()]+'   => file exist')        
        os.system("nautilus %s"%(path+idnumberString.get()+'_'+ennameID[idnumberString.get()] )) 
    except:
        no_file_worning3()
    
def stop_result():
    global recoding
    recoding=0
    stop_resultString.set('結束紀錄影像')    
    getframe_resultString.set('            ')   

    

camera = cv2.VideoCapture(0)    



sourcefile=glob.glob(path_database+'database_Employee.csv')
print('len sourcefile',len(sourcefile) )
if len(sourcefile)==0:
    initfile=1
    
    
if not os.path.isdir('../models/'):
    os.mkdir('../models/')    
else :
    print ('d../models/  file exist') 
    
if not os.path.isdir('../models/person'):
    os.mkdir('../models/person')    
else :
    print ('../models/person  file exist') 



root = Tk()
root.title("TUL Face Registered")
#root.protocol('WM_DELETE_WINDOW', detector)

panel = Label(root)  # initialize image panel
panel.grid(columnspan=9, row=2, sticky='W')
root.config(cursor="arrow")

number123,persenID,pdID,fullID,pwdID,nameID,buitinID,ennameID=person_pd_ID()

varnumber=StringVar()
varnumber.set("    撼訊科技 員工人臉資料庫 管理系統")
numberLabel= Label(root,textvariable=varnumber, font=('Arial', 12),justify = RIGHT )
numberLabel.grid(column=0, row=0, sticky=W) 

varnumber=StringVar()
varnumber.set("    建立人臉生物識別")
numberLabel= Label(root,textvariable=varnumber, font=('Arial', 12),justify = RIGHT )
numberLabel.grid(column=0, row=1, sticky=W) 


vartop=StringVar()
vartop.set("   請輸入員工資料：")
topLabel= Label(root,textvariable=vartop, font=('Arial', 12),justify = RIGHT )
topLabel.grid(column=0, row=3, sticky=W) 

varidnumber=StringVar()
varidnumber.set("  工號")
idnumbeLabel= Label(root,textvariable=varidnumber, font=('Arial', 12),justify = RIGHT )
idnumbeLabel.grid(column=0, row=4, sticky=W) 

varname=StringVar()
varname.set("  中文名")
nameLabel= Label(root,textvariable=varname, font=('Arial', 12),justify = RIGHT )
nameLabel.grid(column=0, row=5, sticky=W) 

varegname=StringVar()
varegname.set("  英文名")
egnameLabel= Label(root,textvariable=varegname, font=('Arial', 12),justify = RIGHT )
egnameLabel.grid(column=0, row=6, sticky=W) 


varpd=StringVar()
varpd.set("  部門")
pdLabel= Label(root,textvariable=varpd, font=('Arial', 12),justify = RIGHT )
pdLabel.grid(column=0, row=7, sticky=W) 

varpd=StringVar()
varpd.set("  西元生日")
pdLabel= Label(root,textvariable=varpd, font=('Arial', 12),justify = RIGHT )
pdLabel.grid(column=1, row=7, sticky=W) 


#填字匡
idnumberString = StringVar()
entryidnumber = Entry(root, width=20, textvariable=idnumberString)
entryidnumber.grid(column=0, row=4, padx=1,sticky=N+S)

nameString = StringVar()
entryname = Entry(root, width=20, textvariable=nameString)
entryname.grid(column=0, row=5, padx=1,sticky=N+S)

egnameString = StringVar()
entryegname = Entry(root, width=20, textvariable=egnameString)
entryegname.grid(column=0, row=6, padx=1,sticky=N+S)

pdString = StringVar()
entrypd = Entry(root, width=20, textvariable=pdString)
entrypd.grid(column=0, row=7, padx=1,sticky=N+S)

bdString = StringVar()
entrybd = Entry(root, width=20, textvariable=bdString)
entrybd.grid(column=2, row=7, padx=1,sticky=N+S)


btn = Button(root, text="註冊", font=('Arial', 12), command=add_result)
btn.grid(column=0, row=8, sticky=W)

add_resultString=StringVar()
add_resultLabel = Label(root, textvariable=add_resultString,fg="#DC143C", font=('Arial', 12))
add_resultLabel.grid(columnspan=9, row=8, padx=1, sticky=S)  


btn = Button(root, text="開始建立人臉生物識別", font=('Arial', 12), command=getframe_result )
btn.grid(column=0, row=9, sticky=W)

getframe_resultString=StringVar()
getframe_resultLabel = Label(root, textvariable=getframe_resultString,fg="#9400D3", font=('Arial', 12))
getframe_resultLabel.grid(column=1, row=9, padx=1, sticky=W)  


btn = Button(root, text="停止", font=('Arial', 12), command=stop_result )
btn.grid(column=0, row=10, sticky=W)

btn = Button(root, text="打開資料夾", font=('Arial', 12), command=openfile )
btn.grid(column=2, row=10, sticky=E)

stop_resultString=StringVar()
stop_resultLabel = Label(root, textvariable=stop_resultString,fg="#228B22", font=('Arial', 12))
stop_resultLabel.grid(column=1, row=10, padx=1, sticky=W)  

try:
    video_loop()

except:
    no_file_worning2()
root.mainloop()

camera.release()
cv2.destroyAllWindows()