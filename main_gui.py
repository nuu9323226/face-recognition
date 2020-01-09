# -*- coding: utf-8 -*- 

import tkinter as tk
import glob
from PIL import Image, ImageTk


dpartment=[100,120,121,150,220,223,310,325,330,350,750,756,760,570,160,510,530]


def add_callbackFunc():
    pdset=secondpage()
    pdset1=mainpage()
    print('numberString',pdset.numberString.get())
    print('nameString',pdset.nameString.get())
    #pdset.add_resultString.set("{} {}新增成功".format(pdset.numberString.get(),pdset.nameString.get()))

    
    
def reduce_callbackFunc():
    reduce_resultString.set("{} {}成功刪除".format(numberString.get(),nameString.get()))


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
        self.Button = tk.Button(self.page, text=u'DP100總經理室', font=('Arial', 12),justify = tk.LEFT,command=self.secpage) 
        self.Button.grid(column=0,row=0, sticky=tk.W) 
        self.Button = tk.Button(self.page, text=u'DP760軟體', font=('Arial', 12),justify = tk.LEFT,command=self.th3page) 
        self.Button.grid(column=1,row=0,sticky=tk.W) 
        
        
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=1, sticky=tk.W)

        #從資料夾抓取以建檔名稱
        filename=[]
        sourcefile=glob.glob(r'../datasets/personout/*')
        print('sourcefile',sourcefile)
        for a in sourcefile:
            finalname=a.split("/")
            filename.append(finalname[-1])
        print ('finalname',filename)
        print('len(filename',len(filename))
        line1=2

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
        
        
#         root.mainloop()   

        
        
        

    def secpage(self):
        self.page.destroy()
        secondpage(self.root)
        
        
    def th3page(self):
        self.page.destroy()
        th3page(self.root)
    
class secondpage(object):
    def __init__(self, master=None):
        self.root = master
        self.page = tk.Frame(self.root)
        self.page.grid()
 
        self.Button = tk.Button(self.page, text=u'主頁',font=('Arial', 12),justify = tk.LEFT,command=self.mainpage) 
        self.Button.grid(column=0,row=0, sticky=tk.W) 
        
        #空白行
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=1, sticky=tk.W)
        
        #題字
        varspace=tk.StringVar()
        varspace.set("部門人員建制名單")
        spaceLabel= tk.Label(self.page,textvariable=varspace, font=('Arial', 12),justify = tk.LEFT )
        spaceLabel.grid(column=0, row=2, sticky=tk.W)
        
        #增減人員
        
        self.varnumber=tk.StringVar()
        self.varnumber.set("工號")
        self.numberLabel= tk.Label(self.page,textvariable=self.varnumber, font=('Arial', 12),justify = tk.RIGHT )
        self.numberLabel.grid(column=1, row=0)        
        
        self.varname=tk.StringVar()
        self.varname.set("姓名")
        self.nameLabel= tk.Label(self.page,textvariable=self.varname, font=('Arial', 12),justify = tk.RIGHT )
        self.nameLabel.grid(column=1, row=1)        
        
        self.numberString = tk.StringVar()
        self.nameString = tk.StringVar()
        self.entrynumber = tk.Entry(self.page, width=20, textvariable=self.numberString)
        self.entryname = tk.Entry(self.page, width=20, textvariable=self.nameString)
        
        self.entrynumber.grid(column=2, row=0, padx=10)
        self.entryname.grid(column=2, row=1, padx=10)        

        self.addButton = tk.Button(self.page, text = '新增',command=self.add_callbackFunc )
        self.addButton.grid(column=3, row=0, pady=10, sticky=tk.W)
        
        self.reduceButton = tk.Button(self.page, text = '刪除',command=self.reduce_callbackFunc)
        self.reduceButton.grid(column=3, row=1, pady=10, sticky=tk.W)        
        
        self.add_resultString=tk.StringVar()
        self.add_resultLabel = tk.Label(self.page, textvariable=self.add_resultString,fg="#DC143C" )
        self.add_resultLabel.grid(column=0, row=1, padx=10, sticky=tk.W)        
        
        self.reduce_resultString=tk.StringVar()
        self.reduce_resultLabel = tk.Label(self.page, textvariable=self.reduce_resultString,fg="#DC143C" )
        self.reduce_resultLabel.grid(column=0, row=1, padx=10, sticky=tk.W)   

        
        line1=3
        gpart=[]
        for c,v in pdID.items():
            if str(v)==str(100):
                gpart.append(c)
                print('number',c)
        column01=0
        for personq in gpart:
            
            if len(gpart)>5:
            
                print('personq',personq)
                print('persenID',persenID[personq])
                locals()['self.var'+str(personq)]=tk.StringVar()
                locals()['self.var'+str(personq)].set(personq+' '+persenID[personq])
                locals()['self.textLabel'+str(personq)] = tk.Label(self.page,textvariable=locals()['self.var'+str(personq)], font=('Arial', 12),justify = tk.LEFT)#显示文字内容 
                locals()['self.textLabel'+str(personq)].grid(column=column01, row=line1, sticky=tk.W) #自动对齐,side：方位
                column01=column01+1
                if column01==4:
                    line1=line1+2
                    column01=0
                    
            if len(gpart)<5:
            
                print('personq',personq)
                print('persenID',persenID[personq])
                locals()['self.var'+str(personq)]=tk.StringVar()
                locals()['self.var'+str(personq)].set(personq+' '+persenID[personq])
                locals()['self.textLabel'+str(personq)] = tk.Label(self.page,textvariable=locals()['self.var'+str(personq)], font=('Arial', 12),justify = tk.LEFT)#显示文字内容 
                locals()['self.textLabel'+str(personq)].grid(column=column01, row=line1, sticky=tk.W) #自动对齐,side：方位
                column01=column01+1

        line1=4
        column01=0
            
        for imagep in gpart:
            
            if len(gpart)>5:
            
            
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
                if column01==4:
                    line1=line1+2
                    column01=0
                    
            if len(gpart)<5:
                
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
        

    def add_callbackFunc(self):
        print('numberString',self.numberString.get())
        print('nameString',self.nameString.get())
        self.add_resultString.set("{} {}新增成功".format(self.numberString.get(),self.nameString.get()))    

    def reduce_callbackFunc(self):
        print('numberString',self.numberString.get())
        print('nameString',self.nameString.get())
        #self.add_resultLabel.delete(0, 'end')
        self.reduce_resultString.set("{} {}刪除成功".format(self.numberString.get(),self.nameString.get()))    
        
        
class th3page(object):
    def __init__(self, master=None):
        self.root = master
        self.page = tk.Frame(self.root)
        self.page.grid()
 
        self.Button = tk.Button(self.page, text=u'主頁',font=('Arial', 12),justify = tk.LEFT,command=self.mainpage) 
        self.Button.grid(column=0,row=0) 
        
        
        spaceLabel= tk.Label(self.page,textvariable="             " )
        spaceLabel.grid(column=0, row=1, sticky=tk.W)
        
        varspace=tk.StringVar()
        varspace.set("部門人員建制名單")
        spaceLabel= tk.Label(self.page,textvariable=varspace, font=('Arial', 12),justify = tk.LEFT )
        spaceLabel.grid(column=0, row=2, sticky=tk.W)
        
        
        line1=3
        gpart=[]
        for c,v in pdID.items():
            if str(v)==str(760):
                gpart.append(c)
                print('number',c)
        column01=0
        for personq in gpart:
            
            if len(gpart)>5:
            
                print('personq',personq)
                print('persenID',persenID[personq])
                locals()['self.var'+str(personq)]=tk.StringVar()
                locals()['self.var'+str(personq)].set(personq+' '+persenID[personq])
                locals()['self.textLabel'+str(personq)] = tk.Label(self.page,textvariable=locals()['self.var'+str(personq)], font=('Arial', 12),justify = tk.LEFT)#显示文字内容 
                locals()['self.textLabel'+str(personq)].grid(column=column01, row=line1, sticky=tk.W) #自动对齐,side：方位
                column01=column01+1
                if column01==4:
                    line1=line1+2
                    column01=0
                    
            if len(gpart)<5:
            
                print('personq',personq)
                print('persenID',persenID[personq])
                locals()['self.var'+str(personq)]=tk.StringVar()
                locals()['self.var'+str(personq)].set(personq+' '+persenID[personq])
                locals()['self.textLabel'+str(personq)] = tk.Label(self.page,textvariable=locals()['self.var'+str(personq)], font=('Arial', 12),justify = tk.LEFT)#显示文字内容 
                locals()['self.textLabel'+str(personq)].grid(column=column01, row=line1, sticky=tk.W) #自动对齐,side：方位
                column01=column01+1

        line1=4
        column01=0
            
        for imagep in gpart:
            
            if len(gpart)>5:
            
            
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
                locals()['photo'+str(imagep)] = tk.PhotoImage(file=file_resize[0])  #file：t图片路径
                locals()['imgLabel'+str(imagep)]  = tk.Label(self.page,image=locals()['photo'+str(imagep)])#把图片整合到标签类中
                locals()['imgLabel'+str(imagep)].grid(column=column01, row=line1, sticky=tk.W)
                column01=column01+1
                if column01==4:
                    line1=line1+2
                    column01=0
                    
            if len(gpart)<5:
                
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
                locals()['photo'+str(imagep)] = tk.PhotoImage(file=file_resize[0])  #file：t图片路径
                locals()['imgLabel'+str(imagep)]  = tk.Label(self.page,image=locals()['photo'+str(imagep)])#把图片整合到标签类中
                locals()['imgLabel'+str(imagep)].grid(column=column01, row=line1, sticky=tk.W)
                column01=column01+1
        
        
        root.mainloop()   
        
    def mainpage(self):
        self.page.destroy()
        mainpage(self.root)

        
def fff():
    o=th3page()
    o.page.destroy(root)


    
number123,persenID,pdID,fullID =person_pd_ID()    



root = tk.Tk()
# root = tk.Toplevel()
# https://blog.csdn.net/FunkyPants/article/details/78163021


root.title('撼訊科技 門禁管理系統')
root.geometry('800x600')

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)

menubar.add_cascade(label='開始', menu=filemenu)

# 在File中加入New、Open、Save等小菜单，即我们平时看到的下拉菜单，每一个小菜单对应命令操作。
filemenu.add_command(label='員工資料建立', command=fff  )
filemenu.add_command(label='出缺勤管理', command=fff)
filemenu.add_command(label='後台管理', command=fff)
filemenu.add_separator()    # 添加一条分隔线
filemenu.add_command(label='Exit', command=root.quit) # 用tkinter里面自带的quit()函数

# 第7步，创建一个Edit菜单项（默认不下拉，下拉内容包括Cut，Copy，Paste功能项）
editmenu = tk.Menu(menubar, tearoff=0)
# 将上面定义的空菜单命名为 Edit，放在菜单栏中，就是装入那个容器中
menubar.add_cascade(label='執行', menu=editmenu)

# 同样的在 Edit 中加入Cut、Copy、Paste等小命令功能单元，如果点击这些单元, 就会触发do_job的功能
editmenu.add_command(label='門禁系統啟動', command=fff)
editmenu.add_command(label='出缺勤紀錄日報表', command=fff)
editmenu.add_command(label='陌生人管理', command=fff)

# 第8步，创建第二级菜单，即菜单项里面的菜单
submenu = tk.Menu(filemenu) # 和上面定义菜单一样，不过此处实在File上创建一个空的菜单
filemenu.add_cascade(label='Import', menu=submenu, underline=0) # 给放入的菜单submenu命名为Import

# 第9步，创建第三级菜单命令，即菜单项里面的菜单项里面的菜单命令（有点拗口，笑~~~）
submenu.add_command(label='Submenu_1', command=fff)   # 这里和上面创建原理也一样，在Import菜单项中加入一个小菜单命令Submenu_1

# 第11步，创建菜单栏完成后，配置让菜单栏menubar显示出来
root.config(menu=menubar)

mainpage(root)

root.mainloop()     
