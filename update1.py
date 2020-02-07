from ftplib import FTP
    
ftp = FTP()
timeout = 30
port = 21
ftp.connect('192.168.99.158',port,timeout) # 連線FTP伺服器
ftp.login('Vincent','helloworld') # 登入
print (ftp.getwelcome())  # 獲得歡迎資訊 
d=ftp.cwd('home/backup')    # 設定FTP路徑
#list = ftp.nlst()       # 獲得目錄列表
#for name in list:
 #   print(name)             # 列印檔名字
name='202002.csv'
path =  'data/'    # 檔案儲存路徑

#f = open(path,'wb')         # 開啟要儲存檔案
#ftp.retrbinary(filename,f.write) # 儲存FTP上的檔案
#ftp.delete(d+name)            # 刪除FTP檔案
ftp.storbinary('STOR '+name, open(path+name, 'rb')) # 上傳FTP檔案
ftp.quit()                  # 退出FTP伺服器
